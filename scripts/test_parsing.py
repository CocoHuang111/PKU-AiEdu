"""校验 Judge 的 JSON 容错解析能覆盖小模型常见的几种跑偏输出。

    python -m scripts.test_parsing
"""

from __future__ import annotations

import sys

from ai_engine.evaluation.judge import (
    _accept_llm_dimension_score,
    _as_indicator_list,
    _parse_json,
    _weighted_dimension_score,
)

CASES = {
    "标准包装": '{"indicators":[{"key":"preparation","score":85}]}',
    "裸数组": '[{"key":"preparation","score":85}]',
    "代码块包裹": '```json\n{"indicators":[{"key":"a","score":70}]}\n```',
    "换了键名": '{"results":[{"key":"b","score":60}]}',
    "扁平映射": '{"preparation":{"score":90,"evidence":"x"}}',
    "夹带脏数据": '[{"key":"a","score":1}, "noise", 42]',
    "前后有寒暄": '好的，评分结果如下：\n{"indicators":[{"key":"c","score":75}]}\n希望有帮助。',
}


def main() -> int:
    failures = 0
    for name, raw in CASES.items():
        try:
            out = _as_indicator_list(_parse_json(raw))
            ok = bool(out) and all(isinstance(i, dict) for i in out)
        except Exception as e:
            out, ok = f"异常 {e}", False
        status = "ok  " if ok else "FAIL"
        failures += not ok
        print(f"  [{status}] {name:10s} -> {out}")

    print("\n一级分校验:")
    graded = [
        {"assessed": True, "score": 70, "weight": 1.0},
        {"assessed": True, "score": 90, "weight": 1.0},
    ]
    dim_cases = [
        ("范围内", 78, 78),
        ("上沿放宽 5 分", 95, 95),
        ("飞出范围", 40, None),
        ("缺字段", None, None),
        ("非数字", "好", None),
    ]
    for name, raw, expect in dim_cases:
        got = _accept_llm_dimension_score(raw, graded)
        ok = got == expect
        failures += not ok
        print(f"  [{'ok  ' if ok else 'FAIL'}] {name:12s} {raw!r} -> {got} (期望 {expect})")

    w = _weighted_dimension_score(graded)
    ok = w == 80.0
    failures += not ok
    print(f"  [{'ok  ' if ok else 'FAIL'}] 加权平均         -> {w} (期望 80.0)")

    wrapped = '{"indicators":[{"key":"a","score":80}],"dimension_score":76,"dimension_rationale":"微格课"}'
    parsed = _parse_json(wrapped)
    items = _as_indicator_list(parsed)
    ok = items and parsed.get("dimension_score") == 76
    failures += not ok
    print(f"  [{'ok  ' if ok else 'FAIL'}] 整包 JSON 保留一级分")

    print()
    if failures:
        print(f"{failures} 个用例未通过")
        return 1
    print("全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
