"""inventory 扫描与打分表匹配（不调大模型）。

    python -m scripts.test_eval_dataset
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.eval_dataset.inventory import (
    FINDER_COPY_SUFFIX,
    build_inventory,
    collapse_long_score_table,
    comment_from_row,
    expert_total_100,
    expert_score_cols,
    is_valid_pptx,
    match_file_name_to_score,
    match_score_row,
    parse_flat_stem,
    parse_name_id_stem,
    pick_courseware,
)
from scripts.build_eval_dataset import _named_cache_dir, build_parser, lesson_is_actionable
from scripts.eval_dataset.xlsx import read_sheet_rows


def main() -> int:
    failures = 0

    def check(name: str, ok: bool, detail: str = "") -> None:
        nonlocal failures
        failures += not ok
        print(f"  [{'ok  ' if ok else 'FAIL'}] {name} {detail}")

    fixed_cache = _named_cache_dir(Path("dataset/2018_spring"), "cache_fixed_prompt", "甲/乙")
    check(
        "可把新版评分写入独立缓存",
        fixed_cache == Path("dataset/2018_spring/cache_fixed_prompt/甲_乙"),
        str(fixed_cache),
    )
    check("专家 2/4 对应百分制 50", expert_total_100(2.0, 2.0, 4.0) == 50.0)
    check("专家 3/4 对应百分制 75", expert_total_100(3.0, 2.0, 4.0) == 75.0)
    check("专家 4/4 对应百分制 100", expert_total_100(4.0, 2.0, 4.0) == 100.0)
    try:
        _named_cache_dir(Path("dataset/2018_spring"), "../outside", "甲")
    except ValueError:
        check("独立缓存不能逃出批次目录", True)
    else:
        check("独立缓存不能逃出批次目录", False)

    rejudge_args = build_parser().parse_args(
        [
            "rejudge",
            "--dir",
            "dataset/2018_spring",
            "--prompt-version",
            "v5-rules17",
            "--output-cache",
            "cache_fixed_prompt",
        ]
    )
    check("rejudge 接受 output-cache", rejudge_args.output_cache == "cache_fixed_prompt")

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
    if xlsx.exists():
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

        cao = next((r for r in man if r["name"] == "曹志勋"), None)
        if cao:
            check("曹志勋标 multi_video", "multi_video" in (cao.get("review_needed") or ""))
        else:
            check("曹志勋在候选里", False)

        wang = next((r for r in inv if "王菁" in r.get("folder_name", "")), None)
        if wang:
            check(
                "王菁课件改用完整 ppt",
                (wang.get("courseware_path") or "").endswith(".ppt")
                and "pptx_invalid_use_ppt" in (wang.get("review_needed") or ""),
                wang.get("courseware_path") or "",
            )
        else:
            check("扫描到王菁文件夹", False)
    else:
        print("没有 2018 打分表，跳过 2018 实扫")

    root19 = ROOT / "test" / "2019春微格作业-42人"
    xlsx19 = root19 / "微格教学评审意见汇总表-总表（排序）-2019春.xlsx"
    if xlsx19.exists():
        rows19 = read_sheet_rows(xlsx19)
        check("2019 表头从姓名行读", "姓名" in rows19[0] and len(rows19) >= 40, f"n={len(rows19)}")
        check("2019 不含标题行当姓名", rows19[0]["姓名"] not in {"序号", "姓名"})
        cmt = comment_from_row(rows19[0], "评语")
        check("2019 评语由优点+改进拼成", "优点：" in cmt and "改进：" in cmt)
        inv19, man19 = build_inventory(root19, xlsx19)
        check("2019 跳过 Finder (2) 目录", all(not r["folder_name"].endswith(FINDER_COPY_SUFFIX) for r in inv19))
        check("2019 CSV 不含邮箱", all("邮箱" not in r for r in inv19))
        check("2019 有视频的人进 manifest", len(man19) >= 8, f"n={len(man19)}")
        names19 = {r["name"] for r in man19}
        check("2019 胡岠进候选", "胡岠" in names19)
        check("2019 空文件夹不进候选", all(r.get("video_path") for r in man19))
    else:
        print("没有 2019 打分表，跳过 2019 实扫")

    parsed = parse_flat_stem("54-青教赛-李阿明-工学院")
    check(
        "平铺文件名拆出青教赛姓名",
        parsed == ("54", "李阿明", "工学院"),
        repr(parsed),
    )
    parsed2 = parse_flat_stem("01-楚健春-数学科学学院")
    check("平铺文件名拆出普通姓名", parsed2 == ("01", "楚健春", "数学科学学院"))
    check("一人一夹文件夹名不误判成平铺", parse_flat_stem("403-光华-肖潇") is None)

    cmt22 = comment_from_row(
        {"突出优点": "概念清晰", "需要改进": "加强总结"},
        "评语",
    )
    check("2022 评语由突出优点+改进拼成", "优点：" in cmt22 and "改进：" in cmt22)

    long_rows = [
        {
            "姓名": "甲",
            "突出优点": "清楚",
            "需要改进": "总结",
            "总体评价（满分4分，2分及格）": "3.5",
            "平均分数": "3.2",
            "专家": "刘",
        },
        {
            "姓名": "甲",
            "突出优点": "互动好",
            "需要改进": "",
            "总体评价（满分4分，2分及格）": "3",
            "平均分数": "",
            "专家": "孙",
        },
        {
            "姓名": "乙",
            "突出优点": "节奏稳",
            "需要改进": "板书",
            "总体评价（满分4分，2分及格）": "3.1",
            "平均分数": "3.1",
            "专家": "刘",
        },
        {
            "姓名": "乙",
            "突出优点": "目标清",
            "需要改进": "",
            "总体评价（满分4分，2分及格）": "3",
            "平均分数": "",
            "专家": "梁",
        },
    ]
    collapsed, col = collapse_long_score_table(long_rows, "姓名", "平均分")
    check("三人行打分表压成一人一行", len(collapsed) == 2, f"n={len(collapsed)}")
    check("压表后用平均分数", col == "平均分数")
    check(
        "压表后有专家分列",
        "专家1" in collapsed[0] and expert_score_cols(list(collapsed[0])) == ["专家1", "专家2"],
    )
    check("压表评语带专家名", "[刘]" in collapsed[0]["_merged_comment"])
    check("压表分数用均分不是单行", collapsed[0]["平均分数"] == "3.2")

    root22 = ROOT / "test" / "2022微格"
    xlsx22 = root22 / "2022春微格教学评审结果统计表-三位专家合并版本.xlsx"
    if xlsx22.exists():
        inv22, man22 = build_inventory(root22, xlsx22)
        names22 = {r["name"] for r in man22}
        check("2022 按姓名平铺配对进 manifest", len(man22) >= 60, f"n={len(man22)}")
        check("2022 楚健春进候选", "楚健春" in names22)
        check("2022 李阿明进候选", "李阿明" in names22)
        check("2022 赵扬进候选", "赵扬" in names22)
        check("2022 不是把备课/试讲整夹当一人", all(r.get("name") for r in man22))
        jia = next((r for r in man22 if r["name"] == "盖嘉"), None)
        check(
            "2022 盖嘉对上备课 PDF",
            bool(jia and str(jia.get("courseware_path") or "").endswith(".pdf")),
            (jia or {}).get("courseware_path", ""),
        )
        chu = next((r for r in man22 if r["name"] == "楚健春"), None)
        check(
            "2022 楚健春用表上平均分数",
            bool(chu and abs(float(chu["expert_avg"]) - 3.0333) < 0.01),
            str((chu or {}).get("expert_avg")),
        )
        check(
            "2022 楚健春缺两位专家分要标出来",
            bool(chu and "incomplete_experts" in (chu.get("review_needed") or "")),
        )
        cong = next((r for r in man22 if r["name"] == "丛治辰"), None)
        check(
            "2022 三人评语都进 comment",
            bool(
                cong
                and "[刘树华]" in cong["comment"]
                and "[孙华]" in cong["comment"]
                and "[梁波]" in cong["comment"]
            ),
        )
        check(
            "2022 丛治辰记下三位专家分",
            bool(cong and cong.get("n_experts") == 3 and cong.get("expert3")),
            str((cong or {}).get("n_experts")),
        )
        check("2022 CSV 不含邮箱", all("邮箱" not in r for r in inv22))
    else:
        print("没有 2022 打分表，跳过 2022 实扫")

    check("2024 文件名拆出姓名-学号", parse_name_id_stem("刘允-2140") == "刘允")
    check("2024 文件名拆出纯姓名视频", parse_name_id_stem("张亿") == "张亿")
    check(
        "2024 英文备课去掉学号",
        parse_name_id_stem("ALAA ELDIN MAMDOUH SAAD AHMED-3787")
        == "ALAA ELDIN MAMDOUH SAAD AHMED",
    )
    check("2024 不把 2022 编号文件当成姓名-学号", parse_name_id_stem("01-楚健春-数学科学学院") is None)
    check(
        "2024 英文名对上表里多出来的姓",
        match_file_name_to_score(
            "ALAA ELDIN MAMDOUH SAAD AHMED",
            ["ALAA ELDIN MAMDOUH SAAD AHMED AKEF", "黄炜"],
        )
        == "ALAA ELDIN MAMDOUH SAAD AHMED AKEF",
    )
    cmt24 = comment_from_row(
        {"汇总评语-ZX": "突出优点：清楚", "备注": "语速适当"},
        "汇总评语-ZX",
    )
    check("2024 评语带上备注", "突出优点" in cmt24 and "备注：语速适当" in cmt24)

    root24 = ROOT / "test" / "2024春微格作业-74人"
    xlsx24 = root24 / "24春微格试讲评分表.xlsx"
    if xlsx24.exists():
        inv24, man24 = build_inventory(root24, xlsx24)
        names24 = {r["name"] for r in man24}
        check("2024 扫描 74 人", len(inv24) == 74, f"n={len(inv24)}")
        check("2024 有视频的进 manifest", len(man24) == 3, f"n={len(man24)}")
        check("2024 黄炜进候选", "黄炜" in names24)
        check("2024 张亿进候选", "张亿" in names24)
        check("2024 王欢进候选", "王欢" in names24)
        wei = next((r for r in man24 if r["name"] == "黄炜"), None)
        check(
            "2024 黄炜用平均分不是单专家分",
            bool(wei and abs(float(wei["expert_avg"]) - 3.17) < 0.02),
            str((wei or {}).get("expert_avg")),
        )
        check(
            "2024 黄炜 expert1 是表上的分数列",
            bool(wei and abs(float(wei.get("expert1") or 0) - 3.5) < 0.02),
            str((wei or {}).get("expert1")),
        )
        check(
            "2024 黄炜 comment 含汇总评语和备注",
            bool(wei and "突出优点" in wei["comment"] and "备注：" in wei["comment"]),
        )
        alaa = next((r for r in inv24 if "ALAA" in (r.get("name") or "")), None)
        check(
            "2024 英文名对上备课 PDF",
            bool(alaa and str(alaa.get("courseware_path") or "").endswith(".pdf")),
            (alaa or {}).get("courseware_path", ""),
        )
        check("2024 无视频的人 skip=no_video", sum(1 for r in inv24 if r["skip"] == "no_video") == 71)
        check(
            "2024 CSV 不含邮箱电话列",
            all("邮件" not in r and "邮箱" not in r and "职工号" not in r for r in inv24),
        )
        liu = next((r for r in inv24 if r["name"] == "刘允"), None)
        check(
            "2024 刘允备课 PDF 当课件",
            bool(liu and str(liu.get("courseware_path") or "").endswith("刘允-2140.pdf")),
            (liu or {}).get("courseware_path", ""),
        )
    else:
        print("没有 2024 打分表，跳过 2024 实扫")

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

    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as raw:
        d = Path(raw)
        bad = d / "课.pptx"
        bad.write_bytes(b"PK\x03\x04" + b"\xff" * 120)
        ole = d / "课.ppt"
        ole.write_bytes(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" + b"\x00" * 64)
        check("截断 zip 不是合法 pptx", is_valid_pptx(bad) is False)
        chosen, note = pick_courseware([bad, ole], [])
        check(
            "损坏 pptx 改选旁边的 ppt",
            chosen == ole and "pptx_invalid_use_ppt" in note,
            note,
        )

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

    check(
        "可执行 lesson 通过",
        lesson_is_actionable("微格纯讲授中互动少只作建议，不作为效果维主缺陷"),
    )
    check(
        "含专家/听感的 lesson 丢弃",
        not lesson_is_actionable("教师是否读PPT需结合专家听感，不可仅凭画面判定"),
    )
    check(
        "对齐句式丢弃",
        not lesson_is_actionable("模型需对齐专家主缺陷判定，校准仪态与逻辑的评分尺度"),
    )

    frozen = ROOT / "dataset" / "lessons_frozen.md"
    bullets = [
        ln[1:].strip()
        for ln in frozen.read_text(encoding="utf-8").splitlines()
        if ln.strip().startswith("- ")
    ]
    check("冻结口径正好 8 条", len(bullets) == 8, f"n={len(bullets)}")
    check("冻结口径均可执行", all(lesson_is_actionable(b) for b in bullets))
    check("冻结口径每条不超过 40 字", all(len(b) <= 40 for b in bullets), str([len(b) for b in bullets]))

    print()
    if failures:
        print(f"{failures} 个用例未通过")
        return 1
    print("全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
