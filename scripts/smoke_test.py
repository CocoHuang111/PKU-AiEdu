"""链路冒烟测试：不碰视频，只验证「客观特征 → 五维打分 → 报告」这条主链路。

    python -m scripts.smoke_test              # 用 config.yaml 的当前模式
    python -m scripts.smoke_test --reference  # 附带课程大纲文本，对照大纲评完整性
    PKU_MODE=local python -m scripts.smoke_test   # 强制走本地 Ollama

只想验证本地特征计算（不花 API 额度）请用 scripts.check_features。
"""

from __future__ import annotations

import sys

SAMPLE = """
同学们好，我们开始上课。上节课我们讲了监督学习的基本框架，今天来看一个更具体的问题：
为什么需要正则化？先想一想，如果我们的模型参数非常多，训练集上误差降到了零，这是好事吗？
大家可以讨论一下。……好，这位同学说可能过拟合了，很好，那么问题来了，过拟合到底是什么？
我们来看这张图。左边这条曲线穿过了每一个训练样本点，右边这条相对平滑。哪一条在新数据上
表现更好？为什么？请举手回答。……对，右边这条。这就引出了偏差—方差权衡的概念。
接下来我们从数学上看。假设我们的损失函数是均方误差，加上一个 L2 惩罚项之后会发生什么？
注意到这个惩罚项会把参数往零的方向拉。那么如果惩罚系数取无穷大，模型会变成什么样？
这个问题留给大家课后思考。首先我们把目标函数写出来，其次求它的梯度，最后分析这个梯度
和不加正则时有什么区别。这里是本节的重点，也是难点，大家注意听。
在实际工业界，比如推荐系统里的 CTR 预估模型，参数量动辄上亿，正则化几乎是标配。
最近两年的一些研究还发现，在大模型微调场景下，正则化的作用机制和传统认识有所不同。
好，我们总结一下今天讲的内容：第一，过拟合的成因；第二，L2 正则化的形式；第三，
偏差方差权衡。有问题吗？没有的话，今天就到这里，下课。
""".strip()

REFERENCE = """
1. 过拟合的成因与判别
2. L2 正则化的数学形式与梯度
3. 偏差—方差权衡
4. 交叉验证选择正则系数
""".strip()


def main() -> int:
    from ai_engine.config import settings
    from ai_engine.evaluation import evaluate_transcript

    use_ref = "--reference" in sys.argv
    print(f"模式: {settings.mode} | LLM: {settings.provider_config('llm').get('model')}")
    print(f"样本长度: {len(SAMPLE)} 字 | 课程大纲: {'有' if use_ref else '无'}\n")

    from scripts.eval_dataset.progress import CliProgress

    on_progress = CliProgress()

    # 样本只有 500 多字，按 45 分钟算语速会低到失真，这里按真实语速反推一个时长
    try:
        result = evaluate_transcript(
            SAMPLE,
            duration_sec=150,
            progress=on_progress,
            reference=REFERENCE if use_ref else None,
        )
    except Exception as e:
        on_progress.finish()
        print(f"\n失败: {e}")
        return 1

    on_progress.finish()
    overall = result["overall"]
    print(f"\n综合得分 {overall['score']}/100  {overall['grade']} 级 · {overall['grade_label']}")
    print(f"未评估的二级指标: {overall['skipped_indicators']} 项\n")

    print("五维得分:")
    for d in result["dimensions"]:
        score = f"{d['score']:5.1f}  {d['grade']} · {d['grade_label']}" if d["assessed"] else "  —  未评估"
        print(f"  {d['label']:6s} {score}  [{d.get('score_source') or '—'}]")
        if d.get("dimension_rationale"):
            print(f"         {d['dimension_rationale'][:80]}")

    print("\n客观特征:")
    for group, rows in result["objective_features"].items():
        if rows:
            print(f"  [{group}]")
            for f in rows[:8]:
                print(f"    {f['label']:24s} {f['value']}{f['unit']}")

    print("\n二级指标示例（教学方法）:")
    method = next(d for d in result["dimensions"] if d["key"] == "teaching_method")
    for ind in method["indicators"][:3]:
        print(f"  {ind['label']} {ind['score']} 分（置信 {ind['confidence']}）")
        print(f"    依据: {ind['evidence'][:70]}")

    completeness = next(
        i
        for d in result["dimensions"]
        for i in d["indicators"]
        if i["key"] == "completeness"
    )
    print(f"\n内容完整性: {'已评 ' + str(completeness['score']) + ' 分' if completeness['assessed'] else '未评估'}")
    print(f"  {completeness['evidence'][:100]}")

    print(f"\n报告字数: {len(result['report'])}")
    print("=" * 46)
    print(result["report"][:400])
    print("...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
