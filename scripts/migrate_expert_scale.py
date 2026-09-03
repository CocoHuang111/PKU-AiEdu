"""把当前批次 CSV 从旧的区间拉伸分改为真实百分制。

只处理 dataset/<year>_spring/ 直属 CSV，不触碰 eval_snapshots、fixed_prompt、
effect_inferred 等历史实验目录。首次执行会把原文件备份到
dataset/scale_backup_legacy_20260902/。
"""
from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path

from ai_engine.config import ROOT

BATCHES = ("2018_spring", "2019_spring", "2022_spring", "2024_spring")
FILES = ("inventory.csv", "manifest.csv", "training_gb.csv", "training_detail.csv", "alignment.csv")


def _float(value: str | None) -> float | None:
    try:
        text = str(value or "").strip()
        return float(text) if text else None
    except ValueError:
        return None


def migrate(path: Path, backup: Path) -> tuple[int, int]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = list(reader.fieldnames or [])
    if "expert_avg" not in fields or "expert_total_100" not in fields:
        return 0, 0

    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        shutil.copy2(path, backup)

    changed = invalid = 0
    for row in rows:
        avg = _float(row.get("expert_avg"))
        if avg is None:
            continue
        total = round(avg / 4.0 * 100.0, 2)
        if avg <= 0 or avg > 4:
            invalid += 1
        if row.get("expert_total_100") != str(total):
            changed += 1
        row["expert_total_100"] = str(total)
        overall = _float(row.get("llm_overall"))
        if "residual" in fields and overall is not None:
            row["residual"] = str(round(total - overall, 2))

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return changed, invalid


def migrate_review_audit(path: Path, backup: Path) -> int:
    """修正规则抽取审计表中的展示百分制；规则判断仍以 score_raw 为准。"""
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = list(reader.fieldnames or [])
    if "score_raw" not in fields or "score_100" not in fields:
        return 0
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        shutil.copy2(path, backup)
    changed = 0
    for row in rows:
        raw = _float(row.get("score_raw"))
        if raw is None:
            continue
        value = str(round(raw / 4.0 * 100.0, 2))
        changed += row.get("score_100") != value
        row["score_100"] = value
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description="修正专家 4 分制到百分制的换算")
    parser.add_argument("--dataset-dir", type=Path, default=ROOT / "dataset")
    args = parser.parse_args()
    base = args.dataset_dir.resolve()
    backup_base = base / "scale_backup_legacy_20260902"
    for batch in BATCHES:
        for name in FILES:
            path = base / batch / name
            if not path.exists():
                continue
            changed, invalid = migrate(path, backup_base / batch / name)
            print(f"{batch}/{name}: 更新 {changed} 行，无效原分 {invalid} 行")
    reviews = base / "expert_rules" / "expert_reviews_long.csv"
    if reviews.exists():
        changed = migrate_review_audit(
            reviews, backup_base / "expert_rules" / reviews.name
        )
        print(f"expert_rules/{reviews.name}: 更新 {changed} 行")
    print(f"旧表备份：{backup_base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
