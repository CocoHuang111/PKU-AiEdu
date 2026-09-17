# 北大网盘视频导入

当前网盘入口仅支持北大网盘公开分享，保留普通视频直链、本地快速上传和分片续传。
不支持百度网盘、夸克网盘和 Google Drive；后端在读取与下载之前明确拒绝这些链接。
无需配置专用账号或 Cookie。

## 使用与限制

粘贴 `https://disk.pku.edu.cn/link/分享ID` 或对应的 `/anyshare/zh-cn/link/分享ID`，
点击“读取链接”，在分享目录内选择视频，再开始导入。一次只导入一个视频。
导入过程：读取公开分享 → 获得匿名分享令牌 → 列出文件 → 校验选中文件归属 →
取得签名下载地址 → 服务器下载、校验视频 → 进入原有评估队列。

仅支持无需登录、无需访问密码、允许下载原文件的公开分享。
实名、手机验证、密码保护、失效分享、禁止原文件下载或要求水印处理会明确报错，不绕过权限。
目录导航通过模拟接口测试；真实公开单视频分享已完成下载，尚缺真实目录样本验证。

## 安全和资源

- 文件和目录 ID 必须属于该分享当前目录，导入时重新读取校验。
- 分享读取响应最多 4MiB、适配请求最多 100 次、目录深度最多 12 层。
- DNS/连接与每次重定向检查公网地址；保留 TLS 域名和证书验证，不使用环境代理。
- 直链仅允许默认 80/443。仅北大签名下载额外允许 `https://diskasu.pku.edu.cn:10002`。
- 下载前清除 API Cookie，分享令牌不传给对象存储；页面不接收令牌或签名下载地址。
- 保留原有最大文件大小、磁盘余量、视频时长、ffprobe 校验、取消检测和失败清理。
- 不修改网盘原文件，不转存到个人账号，不改变数据库结构。

## 验证记录

2026-09-17，本地真实公开分享：72,978,078 字节，时长 1,732.208 秒。
固定公网 IP 连接实现后的完整下载和 ffprobe 校验约 20.30 秒；不是服务器测速。
前端本地界面验证已覆盖读取、文件名/大小显示、选中视频、修改链接清除选择和多链接拒绝。
服务器真实下载与公网健康检查已通过；完整生产登录、发起评估和报告效果由用户验证。
仅北大网盘版本的工作区回归测试 64 项通过，前端生产构建通过。
首次测试遇到本机 Numba 缓存目录不可写；指定临时缓存目录后全量通过，未修改解析代码。
从 Git 已提交内容导出的独立发布目录：55 项测试通过（不包含工作区其他开发中的测试）。

```sh
python -m unittest discover -s tests -v
cd frontend && npm run build
```

## 部署与回退

发布分支：`codex/cloud-drive-video-import`。只部署已提交代码，不混入工作区其他开发改动。
部署前检查无活动任务、保留服务器原 Git 分支和后端/前端镜像标签。
不清空数据库、上传卷、模型缓存或 HTTPS 证书，不运行 `docker compose down -v`。
服务器发布结果和具体回退标签记录在本文后续发布记录中。

管理员可执行 `python -m scripts.check_pku_share 分享链接 --download`，
只进行真实分享读取、临时下载和 ffprobe 校验，不访问数据库、不运行 ASR，结束自动清理副本。

### 2026-09-17 服务器发布记录

- 代码版本：`60c1da8`，功能分支已推送 GitHub，不改写 `main` 或历史提交。
- 服务器新后端镜像中网盘/HTTP 接口测试：18 项通过。
- 用户授权的公开单视频分享：完整下载 72,978,078 字节，ffprobe 时长 1,732.232 秒，
  读取、下载及校验合计约 42.45 秒。临时副本已清理，未创建任务、未运行 ASR。
- 公网 HTTPS 证书验证正常，`/api/health` 返回 200，新版前端资源和仅北大网盘提示确认正常。
- 未登录请求 `/api/evaluation/remote-source` 返回 401。
- 服务器原 `main` 保留；实际运行代码基线对应 `c276ac0`，
  已建立服务器本地分支 `codex/pre-pku-cloud-60c1da8`。
- 后端、Worker、前端旧镜像均保留为对应镜像的 `pre-pku-cloud-60c1da8` 标签。

如需回退，先确认无活动任务和未提交代码，再在 `/opt/AskEdu` 执行：

```sh
git checkout codex/pre-pku-cloud-60c1da8
docker tag pku2-backend:pre-pku-cloud-60c1da8 pku2-backend:latest
docker tag pku2-worker:pre-pku-cloud-60c1da8 pku2-worker:latest
docker tag pku2-web:pre-pku-cloud-60c1da8 pku2-web:latest
docker compose --env-file .env.production -f compose.production.yml up -d --no-build backend worker web
```

回退不删除业务数据或上传文件；仅恢复旧代码和服务镜像。
