"""构建向量库。

用法：
    python -m knowledge.ingest                      # 增量构建所有语料库
    python -m knowledge.ingest --corpus edu_theory  # 只建某一个
    python -m knowledge.ingest --reset              # 清空后重建

往 knowledge/corpora/<语料库名>/ 目录里丢 pdf/docx/md/txt 文件即可，支持子目录。
新增语料库：在 config.yaml 的 corpora 下加一项，再建同名目录。
"""

from __future__ import annotations

import argparse
import sys

from ai_engine.config import settings
from ai_engine.rag import (
    add_chunks,
    collection_stats,
    iter_documents,
    reset_collection,
    split_text,
)


def ingest_corpus(name: str, reset: bool = False) -> int:
    meta = settings.corpus_meta(name)
    directory = settings.corpus_dir(name)
    directory.mkdir(parents=True, exist_ok=True)

    print(f"\n[{name}] {meta.get('label', name)}")
    print(f"  目录: {directory}")

    if reset:
        reset_collection(name)
        print("  已清空原有 collection")

    total_chunks = 0
    file_count = 0
    for path, text in iter_documents(directory):
        chunks = split_text(text)
        if not chunks:
            continue
        rel = path.relative_to(directory)
        metadatas = [
            {
                "source": str(rel),
                "corpus": name,
                "chunk_index": i,
                "total_chunks": len(chunks),
            }
            for i in range(len(chunks))
        ]
        add_chunks(name, chunks, metadatas)
        total_chunks += len(chunks)
        file_count += 1
        print(f"  + {rel}  ({len(chunks)} 块)")

    if file_count == 0:
        print("  (空目录，跳过。把文档放进去后重新运行即可)")
    else:
        print(f"  小计: {file_count} 个文件, {total_chunks} 个文本块")
    return total_chunks


def main() -> int:
    parser = argparse.ArgumentParser(description="构建 Chroma 向量库")
    parser.add_argument("--corpus", help="只处理指定语料库，默认处理全部")
    parser.add_argument("--reset", action="store_true", help="清空后重建")
    args = parser.parse_args()

    # eval_reports 由系统在评估完成后自动写入，不从目录建
    names = settings.corpus_names(include_auto=False)
    if args.corpus:
        if args.corpus not in settings.corpus_names():
            print(f"未知语料库: {args.corpus}")
            print(f"可选: {', '.join(settings.corpus_names())}")
            return 1
        names = [args.corpus]

    print(f"Embedding 模式: {settings.mode}")
    print(f"向量库目录: {settings.chroma_dir}")

    try:
        for name in names:
            ingest_corpus(name, reset=args.reset)
    except Exception as e:
        print(f"\n建库失败: {e}")
        print("提示：默认走云端 embedding，请确认 .env 里的 DASHSCOPE_API_KEY 已配置。")
        return 1

    print("\n各语料库当前文本块数量：")
    for name, count in collection_stats().items():
        print(f"  {name:16s} {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
