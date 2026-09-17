# OSS 服务端存储接入

目标 Bucket：`pku-askedu`；地域：`cn-beijing`；RAM 角色：`AskEduOssServerRole`。
购买的资源包为标准 ZRS 100GB，中国内地通用，一个月。
资源包编号不是 Bucket，实际 Bucket 应保持标准/ZRS、私有并开启阻止公共访问。

## 范围与生产边界

新增 `UPLOAD_STORAGE_BACKEND=local|oss`，未配置时仍默认本地。
OSS 模式的新原视频、快速音频/画面/清单、网盘导入落地视频、大纲、课件、讲稿和头像持久化到 OSS。
数据库记录实际 backend/key；任务材料保存 `oss://` 或 `oss-evidence://` 引用。
上传成功后释放本地源文件；Worker 按需恢复，终态释放源文件和大音频/检查点临时文件。
报告图片目前仍保留在服务器，随评估任务删除；它们还未切换为 OSS 持久化或 TTL 缓存。
不自动迁移历史文件，不删除现有业务数据，不自动配置生命周期删除规则。
报告正文、用户/任务数据仍在 PostgreSQL。浏览器仍经服务端上传，不是浏览器直传 OSS。

## 配置（无密钥）

配置在服务端环境中，SDK 使用实例 RAM 角色自动更新临时凭证，不接受浏览器提供的凭证。

```dotenv
UPLOAD_STORAGE_BACKEND=oss
OSS_BUCKET=pku-askedu
OSS_REGION=cn-beijing
OSS_RAM_ROLE_NAME=AskEduOssServerRole
OSS_USE_INTERNAL=true
OSS_CACHE_ROOT=/app/data/oss-cache
OSS_MAX_OBJECT_BYTES=10737418240
OSS_CACHE_MIN_FREE_BYTES=5368709120
```

ECS 与 Bucket 同地域时，用内网访问对象；用户短期下载链接使用公网 Endpoint。
本地没有实例角色，不应复制云端凭证到开发电脑；本地测试使用模拟 Bucket。
元数据服务强制 IMDSv2，不回退 IMDSv1，不打印凭证或签名 URL，不开启 SDK debug 日志。

## 已实现的接口

- `save(key, stream)`：分块读取，不把整个视频读入内存；禁止静默覆盖已有对象。
- `path_for(key)`：先查对象 ETag/大小；完整下载后原子发布本地缓存，供 FFmpeg/ASR 使用。
- 缓存命名按地域、Bucket、对象 key 哈希隔离，元数据与对象目录分离。
- SDK 启用 CRC 校验；下载使用 If-Match，检查对象大小、磁盘余量，并清理失败临时文件。
- `evict_cache(key)`：只移除这个对象的本地缓存，不删除 OSS 文件。
- `delete(key)`：删除这个 OSS 对象，成功后移除对应缓存；不遍历 Bucket 或删除其他文件。
- `signed_download_url(key, expires=300)`：公网短期 GET 签名，有效期 1–900 秒。
  **调用前必须在业务层检查文件归属，不能把任意 key 签名接口暴露给前端。**
- OSS 错误包装为安全文本，不输出 SDK 响应正文、凭证或带签名的 URL。
- 保留本地存储；修正本地路径检查，防止通过同名前缀目录的符号链接逃逸。

这些方法是同步 I/O，API 应通过 `asyncio.to_thread` 使用。
缓存目前由调用方显式清理，没有自动 TTL 回收；业务接入阶段必须补充容量与任务生命周期管理。
业务调用已在任务终态释放源文件缓存。头像下载缓存目前保留，未增加自动 TTL 清理。
快速画面伴随包完整保存规范清单和画面；恢复复用已有严格解包校验，缺失伴随包会报错，不降级为纯音频。
材料下载先校验当前用户/任务归属，再签发 5 分钟私有下载链接；不提供任意 key 的签名接口。
元数据在上传前提交，失败后标记删除；删除队列仅处理已删除的 OSS 记录，失败保留以便 Worker 重试。
重复完成不重新生成材料；已有对象禁止覆盖，遇到 409 仅允许内容相同的重试。

## 权限

RAM 角色只需当前 Bucket 下的 `oss:PutObject`、`oss:GetObject`、`oss:DeleteObject`、
`oss:ListParts`、`oss:AbortMultipartUpload`，资源为 `acs:oss:*:*:pku-askedu/*`。
无需账号全局 OSS 管理权限、ListBuckets、创建 Bucket 或修改 Bucket 权限。
当前权限不包含读取 Bucket 配置信息；标准/ZRS 设置需在控制台确认。

## 验证与回退

```sh
python -m unittest discover -s tests -p 'test_oss_storage.py' -v
python -m scripts.check_oss_storage
```

真实检查仅创建随机 `_checks/<uuid>.bin` 小对象，验证写入、缓存读取/重取、
匿名公网请求拒绝、短期签名下载，并删除本次对象；本地临时缓存自动清理。
不访问数据库、不运行模型。若清理失败，按输出的唯一 `test_key` 处理，不进行宽泛目录删除。

2026-09-18：角色名称检查通过；本地 OSS 专项 16 项、工作区全量 80 项测试通过。
工作区全量包含其他未提交功能测试，独立发布快照需另行验证。
本阶段文件叠加已提交基线的隔离代码快照，全量 71 项测试通过。
生产容器缺少 OSS SDK；第一次隔离检查在 PyPI 下载依赖时等待，未进入 OSS 权限验证。
改用国内 HTTPS 软件源后 SDK 安装成功。隔离容器真实验证在上传环节失败，
尝试删除本次测试对象返回 HTTP 403，读写权限验证尚未通过，不可启用业务存储切换。
需检查该角色是否附加当前 Bucket 的对象权限策略，以及 Bucket 策略是否有显式拒绝。
仅尝试过以下随机诊断 key；清理未能确认，不能据此认定对象已创建或已删除：
`_checks/2cd5f0313c9d41eabb544503a00780b5.bin`、
`_checks/2e4d20df5ce1433a93a4a483f88611b8.bin`。
没有改动线上代码、环境变量、数据库或用户文件。
随后修正角色授权，真实内网上传/下载/缓存、公网匿名 403、签名下载和删除全部通过（25,600 字节检查用时 0.78 秒）。
业务隔离数据库验证也已通过：原视频及课件、原视频分片重试和幂等完成、快速材料恢复、
链接落地文件转 OSS、大纲、头像、旧本地兼容、模式回退后 OSS 可读、任务删除和测试对象清理。
业务验证的链接下载器及 AI 引擎为模拟实现；没有运行真实视频 ASR/LLM。

## 部署与回退边界

启用：在原命令基础上增加 `-f compose.oss.production.yml`。
镜像先在隔离数据库执行 `python -m scripts.check_oss_business`。
检查使用真实 OSS、API、数据库、Worker 材料恢复；ASR/LLM 和外部链接下载器模拟，避免昂贵模型任务。

```sh
docker compose --env-file .env.production -f compose.production.yml -f compose.oss.production.yml up -d --no-build backend worker
```

快速回退只改变新上传模式，**保留 OSS 可读代码**：

```sh
UPLOAD_STORAGE_BACKEND=local docker compose --env-file .env.production -f compose.production.yml -f compose.oss.production.yml up -d --no-build backend worker
```

已有 OSS 引用不随上传模式回退变成本地；仍由 OSS 适配器读取。
一旦创建 OSS 任务，不能直接回到不识别 OSS 引用的旧镜像：必须先恢复材料并转换数据库引用，或保留本版兼容层。
旧 Git 分支、镜像用于首次启用前回退；不删除历史 Git 记录或本地历史文件。

## 2026-09-18 发布记录

- 已启用服务器 `8.141.113.98` 的 OSS 上传模式；业务代码提交 `2d7d309`。
- 独立发布代码快照全量 80 项测试通过；正式镜像用非 root 用户通过真实 OSS/隔离数据库业务验证。
- 后端、Worker 配置均为 `oss` / `pku-askedu`；站点及 `/api/health` 均返回 HTTP 200。
- 生产容器再次验证内网读写/缓存、公网匿名 403、短期签名下载和删除（25,600 字节，0.72 秒）。
- Git 基线 `codex/pre-oss-2d7d309` 指向 `e769acc`；旧镜像为
  `pku2-backend:pre-oss-2d7d309`、`pku2-worker:pre-oss-2d7d309`。
- 正式业务镜像 `pku2-oss-release:2d7d309`，配置通过 `compose.oss.production.yml` 启用。
- 未迁移历史文件、未设置生命周期自动删除、未删除用户数据或 Git 历史。

## 后续阶段

1. 报告关键帧、课件渲染页的 OSS 持久化/按需缓存和头像缓存 TTL 管理。
2. 活跃上传会话仍在服务器磁盘；失败/取消任务的材料保留至用户删除，不自动设置生命周期过期。
3. 分片和快速材料改为浏览器直传 OSS，使用限用户、限任务、限时的授权。
4. 灰度启用后再决定历史数据迁移，保留本地文件与存储模式回退。

参考：[官方 ECS RAM 角色凭证配置](https://help.aliyun.com/zh/oss/python-configuration-access-credentials)、
[官方 RAM 权限策略](https://help.aliyun.com/zh/oss/user-guide/ram-policy/)。
