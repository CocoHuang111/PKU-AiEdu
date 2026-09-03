"""环境自检：一次性告诉你还差什么。

    python -m scripts.check_env
"""

from __future__ import annotations

import shutil
import sys

OK, WARN, FAIL = "  [ok]  ", "  [warn]", "  [FAIL]"


def check_python() -> bool:
    v = sys.version_info
    text = f"{v.major}.{v.minor}.{v.micro}"
    if v.major == 3 and 10 <= v.minor <= 12:
        print(f"{OK} Python {text}")
        return True
    print(f"{FAIL} Python {text} —— 需要 3.11（3.13+ 缺 ctranslate2/chromadb 的 arm64 wheel）")
    print("        conda create -n pku2 python=3.11 -y && conda activate pku2")
    return False


def check_ffmpeg() -> bool:
    if shutil.which("ffmpeg"):
        print(f"{OK} ffmpeg")
        return True
    print(f"{FAIL} 未找到 ffmpeg —— brew install ffmpeg")
    return False


def check_package(module: str, hint: str, required: bool = True) -> bool:
    try:
        __import__(module)
        print(f"{OK} {module}")
        return True
    except ImportError:
        print(f"{FAIL if required else WARN} {module} 未安装 —— {hint}")
        return not required


def check_api_key() -> bool:
    from ai_engine.config import settings

    if settings.mode == "local":
        print(f"{WARN} mode=local，大模型走 Ollama 而非云端 API")
        print("        如需云端：在 .env 中设置 PKU_MODE=cloud")
        return True
    key = settings.provider_config("llm").get("api_key", "")
    if key:
        print(f"{OK} DASHSCOPE_API_KEY 已配置（{key[:6]}...{key[-4:]}）")
        return True
    print(f"{FAIL} 未配置 DASHSCOPE_API_KEY")
    print("        cp .env.example .env 然后填入 key")
    print("        获取地址 https://bailian.console.aliyun.com/")
    return False


def check_llm() -> bool:
    from ai_engine.providers import ProviderError, get_llm

    try:
        reply = get_llm().complete("回复两个字：正常")
        print(f"{OK} LLM 连通，返回：{reply.strip()[:20]}")
        return True
    except ProviderError as e:
        print(f"{FAIL} LLM 调用失败：{str(e)[:150]}")
        return False
    except Exception as e:
        print(f"{FAIL} LLM 异常：{str(e)[:150]}")
        return False


def check_embedding() -> bool:
    from ai_engine.providers import get_embedder

    try:
        dim = get_embedder().dim
        print(f"{OK} Embedding 连通，向量维度 {dim}")
        return True
    except Exception as e:
        print(f"{FAIL} Embedding 失败：{str(e)[:150]}")
        return False


def check_corpora() -> bool:
    from ai_engine.rag import collection_stats

    try:
        stats = collection_stats()
    except Exception as e:
        print(f"{WARN} 向量库读取失败：{str(e)[:120]}")
        return True
    total = sum(stats.values())
    detail = ", ".join(f"{k}={v}" for k, v in stats.items())
    if total:
        print(f"{OK} 向量库已建（{detail}）")
    else:
        print(f"{WARN} 向量库为空（{detail}）—— 运行 make ingest")
    return True


def main() -> int:
    print("\n=== 基础环境 ===")
    base = [check_python(), check_ffmpeg()]

    print("\n=== Python 依赖 ===")
    deps = [
        check_package("fastapi", "pip install -r requirements.txt"),
        check_package("chromadb", "pip install -r requirements.txt"),
        check_package("faster_whisper", "pip install faster-whisper"),
        check_package("librosa", "pip install librosa soundfile"),
        check_package("lxml", "pip install lxml"),
        check_package("zhconv", "pip install zhconv（中文转写繁转简）"),
        check_package("pandas", "pip install pandas（训 GB 用）", required=False),
        check_package("sklearn", "pip install scikit-learn（训 GB 用）", required=False),
    ]

    print("\n=== AI 能力 ===")
    from ai_engine.config import settings

    print(f"  大模型模式（LLM/VLM/Embedding）: {settings.mode}")
    if settings.mode == "cloud":
        print(f"  {OK} 默认走云端 API（通义千问）")
    else:
        print(f"  {WARN} 当前为 local 模式（Ollama）；大模型功能未走云端 API")
        print("        如需云端：在 .env 中设置 PKU_MODE=cloud")
    print(f"  {OK} ASR 固定本地 faster-whisper（语音识别，非大模型）")
    ai = [check_api_key()]
    if ai[0]:
        ai.append(check_llm())
        ai.append(check_embedding())

    print("\n=== 知识库 ===")
    check_corpora()

    failed = [r for r in (*base, *deps, *ai) if not r]
    print("\n" + "=" * 46)
    if failed:
        print(f"{len(failed)} 项未通过，请按上面的提示处理后重试。")
        return 1
    print("全部通过，可以 make backend 启动了。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
