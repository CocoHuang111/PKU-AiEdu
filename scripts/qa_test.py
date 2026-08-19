"""问答链路测试：检索规划 → 召回 → 生成。

    PKU_MODE=local python -m scripts.qa_test "你的问题"
"""

from __future__ import annotations

import sys

from ai_engine.qa import ask_stream


def main() -> int:
    question = sys.argv[1] if len(sys.argv) > 1 else "课堂提问后应该等待多久？大班课怎么提高参与度？"
    print(f"问题: {question}\n")

    for event in ask_stream(question):
        if event["type"] == "plan":
            p = event["data"]
            print(f"[规划] planner={p['planner']}")
            print(f"       独立问题: {p['standalone_question']}")
            print(f"       关键词  : {p['queries']}")
            print(f"       语料库  : {p['corpora']}\n")
        elif event["type"] == "citations":
            print(f"[召回] {len(event['data'])} 条")
            for c in event["data"]:
                print(f"  [{c['index']}] {c['corpus_label']} · {c['source']} (score={c['score']})")
                print(f"      {c['snippet'][:80]}")
            print("\n[回答]")
        elif event["type"] == "chunk":
            print(event["data"], end="", flush=True)
        elif event["type"] == "done":
            print(f"\n\n[完成] 答案 {len(event['answer'])} 字")
    return 0


if __name__ == "__main__":
    sys.exit(main())
