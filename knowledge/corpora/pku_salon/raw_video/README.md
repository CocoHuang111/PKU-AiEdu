# 把沙龙录像 mp4 放在此目录。
#
# 命名约定：文件名前 8 位为标准日期 YYYYMMDD，例如：
#   20240315_大班课互动.mp4
#   20240315.mp4
#
# 处理命令（在项目根目录）：
#   make salon              # 转写（ASR small）+ 提取教学知识 → Markdown
#   make salon-transcribe   # 只做转写，结果在 ../.work/
#   make salon-structure    # 只做结构化（需先转写）
#   python -m knowledge.ingest --corpus pku_salon   # 写入向量库
#
# 正式语料输出到上级目录：../YYYYMMDD-描述.md
# 中间产物（音频、转写 JSON）在 ../.work/，不会进入向量库。
