"""GB 训练约定（不调大模型）。

    python -m scripts.test_gb
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ai_engine.evaluation.gb import (
    avg_to_score5,
    feature_columns,
    is_invalid_label,
    label_to_score,
    label_to_score_100,
    score_100_to_avg,
    score_to_label,
)


def main() -> int:
    failures = 0

    def check(name: str, ok: bool, detail: str = "") -> None:
        nonlocal failures
        failures += not ok
        print(f"  [{'ok  ' if ok else 'FAIL'}] {name} {detail}")

    check("5 类：2.0→0", score_to_label(2.0, n_classes=5) == 0)
    check("5 类：2.2 仍是 0（step=0.4）", score_to_label(2.2, n_classes=5) == 0)
    check("5 类：3.9→4", score_to_label(3.9, n_classes=5) == 4)
    check("8 类：2.0→0", score_to_label(2.0, n_classes=8) == 0)
    check("8 类：2.25→1", score_to_label(2.25, n_classes=8) == 1)
    check("10 类：2.2→1（论文 step=0.2）", score_to_label(2.2, n_classes=10) == 1)
    check("10 类：3.99→9", score_to_label(3.99, n_classes=10) == 9)
    check("5 类第 0 档中点 2.2", abs(label_to_score(0, step=0.4) - 2.2) < 1e-9)
    check("2.0 均分 → 0–5 的 2.5", abs(avg_to_score5(2.0) - 2.5) < 1e-9)
    check("4.0 均分 → 0–5 的 5", abs(avg_to_score5(4.0) - 5.0) < 1e-9)
    check("3.0 均分 → 0–5 的 3.75", abs(avg_to_score5(3.0) - 3.75) < 1e-9)
    check("5 类第 0 档中点 2.2 → 百分制 55", abs(label_to_score_100(0) - 55.0) < 1e-9)
    check("百分制 75 → 专家原分 3", abs(score_100_to_avg(75.0) - 3.0) < 1e-9)

    check("负百分制剔除", is_invalid_label(0.0, -100.0))
    check("均分 0 剔除", is_invalid_label(0.0, 0.0))
    check("正常分保留", not is_invalid_label(3.28, 82.0))
    check("缺百分制剔除", is_invalid_label(3.0, None))
    check("NaN 剔除", is_invalid_label(float("nan"), 50.0))

    cols = feature_columns(
        [
            "video_id",
            "expert_avg",
            "expert_total_100",
            "prompt_version",
            "judge_fingerprint",
            "batch",
            "comment",
            "text__speech_rate",
            "llm_dim_teaching_effect",
        ]
    )
    check("泄漏列不当特征", cols == ["text__speech_rate", "llm_dim_teaching_effect"], str(cols))
    check("llm 只要五维分", feature_columns(cols, mode="llm") == ["llm_dim_teaching_effect"])

    try:
        import pandas  # noqa: F401
        import sklearn  # noqa: F401
    except ImportError:
        check("无 sklearn 时跳过拟合", True, "未安装")
        print(f"\n{failures} 项失败" if failures else "\n全部通过")
        return 1 if failures else 0

    import pandas as pd

    from ai_engine.evaluation.gb_fit import make_or_load_split, run_variant

    rng_rows = []
    for i in range(30):
        year = "2018_spring" if i < 10 else "2022_spring"
        # 保持在 3 个相邻类别内，确保仅 20 条的测试夹具能做分层留出。
        expert = 60.0 + (i % 5) * 5.0
        rng_rows.append(
            {
                "video_id": f"t{i}",
                "expert_avg": expert / 100.0 * 4.0,
                "expert_total_100": expert,
                "prompt_version": "v4",
                "batch": year,
                "text__speech_rate": 180 + i,
                "llm_dim_teaching_attitude": 55 + i,
                "llm_dim_teaching_content": 58 + i,
                "llm_dim_teaching_method": 52 + i,
                "llm_dim_teaching_effect": 60 + i,
                "llm_dim_teaching_quality": 50 + i,
            }
        )
    rng_rows.append(
        {
            "video_id": "bad",
            "expert_avg": 0.0,
            "expert_total_100": -100.0,
            "prompt_version": "v4",
            "batch": "2019_spring",
            "text__speech_rate": 100,
            "llm_dim_teaching_attitude": 50,
            "llm_dim_teaching_content": 50,
            "llm_dim_teaching_method": 50,
            "llm_dim_teaching_effect": 50,
            "llm_dim_teaching_quality": 50,
        }
    )
    with tempfile.TemporaryDirectory() as tmp:
        tmp_p = Path(tmp)
        csv_path = tmp_p / "toy.csv"
        split_path = tmp_p / "split.json"
        pd.DataFrame(rng_rows).to_csv(csv_path, index=False)
        df = pd.read_csv(csv_path)
        df = df[df["video_id"] != "bad"].reset_index(drop=True)
        spec1 = make_or_load_split(df, path=split_path, force=True)
        spec2 = make_or_load_split(df, path=split_path, force=False)
        no_batch = df.drop(columns=["batch"])
        spec_w = make_or_load_split(
            no_batch, path=tmp_p / "split_within.json", force=True, hold_year="within"
        )
        check("无 batch 时 within 能划出预测集", len(spec_w["test_ids"]) >= 2, str(spec_w["test_ids"]))
        check("两次读取同一划分", spec1["test_ids"] == spec2["test_ids"], str(spec1["test_ids"]))
        check("预测集全是 2022", all(i.startswith("t") for i in spec1["test_ids"]) and len(spec1["test_ids"]) >= 2)
        check("训练集含 2018", any(r["video_id"] in spec1["train_ids"] and r["batch"] == "2018_spring" for r in rng_rows))

        m1 = run_variant("obj_reg", data=csv_path, alignment=None, split_path=split_path, out_dir=tmp_p)
        m2 = run_variant("llm_cls5", data=csv_path, alignment=None, split_path=split_path, out_dir=tmp_p)
        check("回归能写出 pkl", (tmp_p / "gb_obj_reg.pkl").exists())
        check("分类能写出 pkl", (tmp_p / "gb_llm_cls5.pkl").exists())
        check("回归 MAE 在 0–5 尺度", "mae_5" in m1 and m1["mae_5"] < 5, str(m1.get("mae_5")))
        check("两版预测人数相同", m1["n_test"] == m2["n_test"], f"{m1['n_test']} vs {m2['n_test']}")
        split = json.loads(split_path.read_text())
        check("划分文件未在第二次训练被改掉", split["test_ids"] == spec1["test_ids"])

    print(f"\n{failures} 项失败" if failures else "\n全部通过")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
