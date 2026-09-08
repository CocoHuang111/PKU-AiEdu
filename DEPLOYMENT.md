# 北大问教 2.0：2 核 8GB 服务器内测部署

本方案建立全新的业务数据库和向量索引，不迁移本机历史评估任务、问答任务、
大纲优化任务、上传视频或历史评估报告。会随代码带上知识库原始语料与线上 GB
评分模型，并在服务器上重新生成知识库索引。

## 一、运行边界

- Ubuntu 24.04，2 vCPU / 8GB 内存可用于小范围内测。
- LLM、VLM、Embedding 必须使用云端模式，不要在这台机器上运行 Ollama。
- 视频评估最多同时执行 1 个；其他视频任务在应用进程内等待。
- 后端固定为 1 个进程。评估任务当前不是独立任务队列，更新或重启后端前应确认没有任务正在处理。
- 建议添加 8GB swap，避免首次构建或视频处理时因瞬时内存不足退出。

## 二、服务器初始化

SSH 登录服务器后，先更新系统并创建 swap：

```bash
sudo apt update
sudo apt upgrade -y
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

按照 Docker 官方 Ubuntu 安装方式配置 apt 仓库并安装：

```bash
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

sudo tee /etc/apt/sources.list.d/docker.sources > /dev/null <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
```

退出 SSH 后重新登录，让 Docker 用户组生效。云服务器安全组和系统防火墙只开放：

- TCP 22：SSH，最好只允许管理员固定 IP。
- TCP 80：HTTP，用于跳转和证书签发。
- TCP/UDP 443：HTTPS 与 HTTP/3。
- 不要开放 5432、8010；PostgreSQL 和后端都只在 Docker 内部网络访问。

## 三、传输项目

当前仓库没有 Git 远程地址。推荐先在本机提交准备上线的代码，再只打包 Git 跟踪的
文件，这样不会带上 `.env`、`data/`、测试视频、历史数据库和旧向量索引：

```bash
git status
git add Dockerfile Dockerfile.frontend .dockerignore compose.production.yml deploy/Caddyfile .env.production.example DEPLOYMENT.md backend/app/workers/tasks.py
git commit -m "Add production deployment for internal beta"
git archive --format=tar.gz --output=pku2-deploy.tar.gz HEAD
scp pku2-deploy.tar.gz 用户名@服务器公网IP:/tmp/
```

在服务器解压：

```bash
sudo mkdir -p /opt/pku2
sudo chown "$USER":"$USER" /opt/pku2
tar -xzf /tmp/pku2-deploy.tar.gz -C /opt/pku2
cd /opt/pku2
```

## 四、配置域名与密钥

把域名的 A 记录解析到服务器公网 IP。DNS 生效后，在服务器创建生产环境配置。
正式内测需要域名：生产环境 Session 使用 Secure Cookie，不能把 `http://公网IP`
作为登录入口。

```bash
cd /opt/pku2
cp .env.production.example .env.production
openssl rand -hex 32
openssl rand -hex 32
```

编辑 `.env.production`：

```bash
nano .env.production
```

至少修改：

- `SITE_ADDRESS`：已经解析到服务器公网 IP 的正式域名，不要带路径。
- `POSTGRES_PASSWORD` 和 `DATABASE_URL`：使用同一个仅含字母数字的随机密码。
- `DASHSCOPE_API_KEY`：通义千问 API Key。
- `SESSION_SECRET`：另一条随机值。
- `LOCAL_REGISTRATION_INVITE_CODE`：仅发给内测用户的邀请码。

生产配置不得提交到 Git，也不要通过聊天或截图发送。

## 五、首次启动

构建并启动三个服务：

```bash
cd /opt/pku2
docker compose --env-file .env.production -f compose.production.yml up -d --build
docker compose --env-file .env.production -f compose.production.yml ps
```

后端启动时会自动运行 Alembic 数据库迁移。首次加载 ASR 时还会下载 Whisper base
模型到持久卷。先执行环境自检：

```bash
docker compose --env-file .env.production -f compose.production.yml exec backend python -m scripts.check_env
```

重新建立知识库索引，不复制旧 `data/chroma`：

```bash
docker compose --env-file .env.production -f compose.production.yml exec backend python -m knowledge.ingest --reset
```

创建首个管理员：

```bash
docker compose --env-file .env.production -f compose.production.yml exec backend python -m scripts.create_admin --username admin --display-name 管理员
```

打开 `https://你的域名`，依次验证：登录、问答、大纲优化、短视频评估、报告下载。
查看状态和日志：

```bash
docker compose --env-file .env.production -f compose.production.yml ps
docker compose --env-file .env.production -f compose.production.yml logs --tail=200 backend
docker compose --env-file .env.production -f compose.production.yml logs --tail=100 web
```

## 六、发布更新

确认没有视频或大纲任务正在处理后，把新版归档上传并覆盖解压到 `/opt/pku2`，然后：

```bash
cd /opt/pku2
docker compose --env-file .env.production -f compose.production.yml up -d --build
docker compose --env-file .env.production -f compose.production.yml ps
```

命令不会删除 PostgreSQL、上传文件、向量索引、Whisper 缓存或 HTTPS 证书，它们存放在
固定命名的 Docker volumes 中。不要执行 `docker compose down -v`。

## 七、备份与容量

每天备份 PostgreSQL；上传数据是否备份按内测隐私策略决定。数据库备份示例：

```bash
mkdir -p /opt/pku2-backups
docker compose --env-file /opt/pku2/.env.production -f /opt/pku2/compose.production.yml exec -T postgres pg_dump -U pku2 -d pku2 -Fc > /opt/pku2-backups/pku2.dump
```

虽然本次不迁移历史数据，上线后产生的新账号和任务仍在 PostgreSQL 中。建议：

- 磁盘达到 70% 时告警，达到 85% 前清理。
- 明确告知内测用户视频保存期限，建议 14～30 天。
- 每天数据库备份，保留最近 7～14 份，并定期复制到服务器之外。
- 服务器重启或升级前先确认没有 `processing` 状态的长任务。

## 八、完整清空内测环境

只有确实要删除所有内测账号、任务、上传文件和索引时，才停止服务并删除以下固定卷：

- `pku2_pgdata`
- `pku2_app_data`
- `pku2_hf_cache`

这项操作不可恢复，普通发布和重启不需要删除卷。
