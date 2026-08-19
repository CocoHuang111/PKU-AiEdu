"""inventory 扫描与打分表匹配（不调大模型）。

    python -m scripts.test_eval_dataset
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.eval_dataset.inventory import (
    build_inventory,
    match_score_row,
)
from scripts.eval_dataset.xlsx import read_sheet_rows


def main() -> int:
    failures = 0

    def check(name: str, ok: bool, detail: str = "") -> None:
        nonlocal failures
        failures += not ok
        print(f"  [{'ok  ' if ok else 'FAIL'}] {name} {detail}")

    hits = match_score_row(
        "403-光华-肖潇",
        [{"姓名": "肖潇", "院系": "光华"}, {"姓名": "王翀", "院系": "光华"}],
        "姓名",
        "院系",
    )
    check("文件夹包含姓名即匹配", hits[0] is not None and hits[0]["姓名"] == "肖潇")

    none, reason = match_score_row(
        "城环-刘涛--后交",
        [{"姓名": "肖潇", "院系": "光华"}],
        "姓名",
        "院系",
    )
    check("表里没有的人记 no_score", none is None and reason == "no_score")

    root = ROOT / "test" / "2018春微格作业-32人"
    xlsx = root / "微格教学评审汇总-2018--汇总意见.xlsx"
    if not xlsx.exists():
        print("没有 2018 打分表，跳过实扫")
        return 1 if failures else 0

    rows = read_sheet_rows(xlsx)
    check("xlsx 能读出人", len(rows) >= 20, f"n={len(rows)}")
    check("有评语列", "评语" in rows[0])

    inv, man = build_inventory(root, xlsx)
    names = {r["name"] for r in man}
    skips = {}
    for r in inv:
        skips[r["skip"] or "ok"] = skips.get(r["skip"] or "ok", 0) + 1

    check("朱戎无视频被跳过", any(r["folder_name"].endswith("朱戎") and r["skip"] == "no_video" for r in inv))
    check("刘涛无打分被跳过", any("刘涛" in r["folder_name"] and r["skip"] == "no_score" for r in inv))
    check("肖潇进 manifest", "肖潇" in names)
    check("陈培永进 manifest", "陈培永" in names)
    check("未通过目录仍扫描", any("未通过" in r["folder_rel"] for r in inv))
    check("未通过的人都不进训练集", all("未通过" not in (r.get("folder_rel") or "") for r in man))
    check("manifest 大约 20+ 人", 18 <= len(man) <= 26, f"n={len(man)}")
    check("CSV 不含邮箱列", all("邮箱" not in r and "电子邮箱" not in r for r in inv))
    print("  skip 统计:", skips)
    print("  manifest:", sorted(names))

    # 曹志勋多视频应标 review
    cao = next((r for r in man if r["name"] == "曹志勋"), None)
    if cao:
        check("曹志勋标 multi_video", "multi_video" in (cao.get("review_needed") or ""))
    else:
        check("曹志勋在候选里", False)

    from io import StringIO

    from scripts.eval_dataset.progress import CliProgress, format_extra, format_progress_line

    extra_asr = format_extra("asr", {"done_sec": 480, "total_sec": 1200})
    check("ASR 附加信息是分钟", extra_asr == "8/20 分钟", extra_asr)
    extra_vlm = format_extra("vlm_describe", {"done": 6, "total": 24})
    check("VLM 附加信息是帧数", extra_vlm == "6/24", extra_vlm)
    extra_cw = format_extra("vlm_describe", {"done": 3, "total": 10, "kind": "courseware"})
    check("课件页带标记", extra_cw == "3/10 课件", extra_cw)
    line = format_progress_line(40, "asr", {"done_sec": 480, "total_sec": 1200})
    check("进度行含条和百分比", "[" in line and "40%" in line and "语音识别" in line)

    buf = StringIO()
    bar = CliProgress(stream=buf)
    bar._tty = False
    bar(16, "asr", {"done_sec": 100, "total_sec": 1000})
    bar(18, "asr", {"done_sec": 180, "total_sec": 1000})
    bar(25, "asr", {"done_sec": 250, "total_sec": 1000})
    check("非 TTY 下 ASR 按 10% 节流", buf.getvalue().count("\n") == 2, repr(buf.getvalue()))

    tty = StringIO()
    live = CliProgress(stream=tty)
    live._tty = True
    live(20, "asr", {"done_sec": 120, "total_sec": 600})
    live(40, "asr", {"done_sec": 240, "total_sec": 600})
    live.finish()
    check("TTY 上 ASR 用回车刷新", "\r" in tty.getvalue() and tty.getvalue().count("\n") == 1)

    print()
    if failures:
        print(f"{failures} 个用例未通过")
        return 1
    print("全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
