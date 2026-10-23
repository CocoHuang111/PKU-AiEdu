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
from ai_engine.providers import get_embedder
from ai_engine.rag import add_chunks, collection_stats, delete_collection, reset_collection
from knowledge.index_records import iter_index_records


OBSOLETE_COLLECTIONS = ("course_syllabi",)


def ingest_corpus(name: str, reset: bool = False, dry_run: bool = False) -> int:
    meta = settings.corpus_meta(name)
    directory = settings.corpus_dir(name)
    directory.mkdir(parents=True, exist_ok=True)

    print(f"\n[{name}] {meta.get('label', name)}")
    print(f"  目录: {directory}")

    if reset and not dry_run:
        reset_collection(name)
        print("  已清空原有 collection")

    records = list(iter_index_records(name, directory))
    total_chunks = len(records)
    file_count = len({record.source for record in records})

    if not dry_run:
        batch_size = 64
        for start in range(0, len(records), batch_size):
            batch = records[start : start + batch_size]
            metadatas = []
            for offset, record in enumerate(batch):
                meta = {
                    "source": record.source,
                    "source_url": record.source_url,
                    "corpus": name,
                    "chunk_index": int(record.metadata.get("chunk_index", 0)),
                    "total_chunks": int(record.metadata.get("total_chunks", 1)),
                    **record.metadata,
                }
                metadatas.append(meta)
            add_chunks(name, [record.text for record in batch], metadatas)

    if file_count == 0:
        print("  (空目录，跳过。把文档放进去后重新运行即可)")
    else:
        kind = "索引记录" if name in {"course_cases", "teaching_cases"} else "语义段"
        action = "预检" if dry_run else "写入"
        print(f"  {action}: {file_count} 个来源, {total_chunks} 条{kind}")
    return total_chunks


def main() -> int:
    parser = argparse.ArgumentParser(description="构建 Chroma 向量库")
    parser.add_argument("--corpus", help="只处理指定语料库，默认处理全部")
    parser.add_argument("--reset", action="store_true", help="清空后重建")
    parser.add_argument("--dry-run", action="store_true", help="只检查和统计，不调用 embedding、不写向量库")
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
        # 全量重建会先删除旧 collection；提前验证 provider，避免网络/API
        # 配置错误把第一个库清空后才暴露。
        if args.reset and not args.dry_run:
            print("重建前检查 Embedding 服务...")
            get_embedder().embed(["知识库重建连通性检查"])
            print("Embedding 服务可用")
            for obsolete in OBSOLETE_COLLECTIONS:
                delete_collection(obsolete)
                print(f"已清理废弃 collection: {obsolete}")
        for name in names:
            ingest_corpus(name, reset=args.reset, dry_run=args.dry_run)
    except Exception as e:
        print(f"\n建库失败: {e}")
        print("提示：默认走云端 embedding，请确认 .env 里的 DASHSCOPE_API_KEY 已配置。")
        return 1

    if not args.dry_run:
        print("\n各语料库当前文本块数量：")
        for name, count in collection_stats().items():
            print(f"  {name:16s} {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
