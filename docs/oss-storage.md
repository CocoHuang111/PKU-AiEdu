# OSS 服务端存储适配（第一阶段）

目标 Bucket：`pku-askedu`；地域：`cn-beijing`；RAM 角色：`AskEduOssServerRole`。
购买的资源包为标准 ZRS 100GB，中国内地通用，一个月。
资源包编号不是 Bucket，实际 Bucket 应保持标准/ZRS、私有并开启阻止公共访问。

## 范围与生产边界

本阶段实现独立 OSS 存储后端与解析本地缓存，不改变现有业务上传路由。
`get_storage()` 和现有上传仍默认 `local`；只有显式 `get_storage("oss")` 使用 OSS。
不自动迁移历史文件，不删除现有业务数据，不自动配置生命周期删除规则。
这不是“全站文件已迁移 OSS”，也不是“浏览器已经直传 OSS”。

## 配置（无密钥）

配置在服务端环境中，SDK 使用实例 RAM 角色自动更新临时凭证，不接受浏览器提供的凭证。

```dotenv
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

## 下一阶段（尚未接入）

1. 新上传文件持久化到 OSS，数据库记录 backend/key；处理任务按需恢复本地材料。
2. 完成用户删除、取消/失败清理、报告附件读取以及缓存回收的全链路验证。
3. 分片和快速材料改为浏览器直传 OSS，使用限用户、限任务、限时的授权。
4. 灰度启用后再决定历史数据迁移，保留本地文件与存储模式回退。

参考：[官方 ECS RAM 角色凭证配置](https://help.aliyun.com/zh/oss/python-configuration-access-credentials)、
[官方 RAM 权限策略](https://help.aliyun.com/zh/oss/user-guide/ram-policy/)。
