# 北大问教 2.0：2 核 8GB 服务器公网 IP 内测部署

本方案建立全新的业务数据库和向量索引，不迁移本机历史评估任务、问答任务、
大纲优化任务、上传视频或历史评估报告。会随代码带上知识库原始语料与线上 GB
评分模型，并在服务器上重新生成知识库索引。

不要求提前购买域名。Caddy 2.11 会使用 Let's Encrypt 的 `shortlived` ACME profile
为固定公网 IP 申请浏览器可信的 HTTPS 证书，并自动续签。用户最终通过
`https://服务器公网IP` 访问。

## 一、运行边界

- Ubuntu 24.04，2 vCPU / 8GB 内存可用于小范围内测。
- LLM、VLM、Embedding 必须使用云端模式，不要在这台机器上运行 Ollama。
- 视频评估最多同时执行 1 个；其他视频任务保存在 PostgreSQL 队列中等待。
- 问答和大纲优化使用独立线程池，默认分别同时执行 4 个和 2 个，可在 `.env.production` 中通过 `QA_MAX_CONCURRENCY`、`SYLLABUS_MAX_CONCURRENCY` 调整（必须为正整数，修改后重建后端容器）。上限按后端进程计算；当前部署为 1 个进程。
- 大纲超额任务保持“排队中”，等待大纲线程空位；不会占用问答线程。问答超额请求等待问答线程。两类等待队列仍在后端进程内，不具备视频 Worker 的重启恢复机制。
- 线程隔离只隔离执行名额，CPU、内存、数据库和云端模型配额仍然共享；并发数不是压测确认的服务容量。
- `backend` 只处理网站请求，`worker` 独立执行视频评估。Worker 异常退出后，租约过期的任务会自动重新排队。
- 建议添加 8GB swap，避免首次构建或视频处理时因瞬时内存不足退出。

## 二、服务器初始化

SSH 登录服务器后，先更新系统并创建 swap：

```bash
sudo apt update
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

按照 Docker 官方 Ubuntu 安装方式配置 apt 仓库并安装：

```bash
sudo apt install -y ca-certificates curl git
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

## 三、从 GitHub 获取项目

项目远程仓库为：

- HTTPS：`https://github.com/CocoHuang111/PKU_AskEdu.git`
- SSH：`git@github.com:CocoHuang111/PKU_AskEdu.git`

如果仓库是公开的，直接在服务器使用 HTTPS 克隆：

```bash
sudo mkdir -p /opt/AskEdu
sudo chown "$USER":"$USER" /opt/AskEdu
git clone https://github.com/CocoHuang111/PKU_AskEdu.git /opt/AskEdu
cd /opt/AskEdu
git branch --show-current
```

最后一条命令应显示 `main`。如果仓库是私有的，先把服务器 SSH 公钥添加为 GitHub
Deploy Key，再使用 SSH 地址：

```bash
ssh-keygen -t ed25519 -f ~/.ssh/pku2_deploy -C "pku2-deploy"
cat ~/.ssh/pku2_deploy.pub
GIT_SSH_COMMAND="ssh -i $HOME/.ssh/pku2_deploy -o IdentitiesOnly=yes" git clone git@github.com:CocoHuang111/PKU_AskEdu.git /opt/AskEdu
cd /opt/AskEdu
git config core.sshCommand "ssh -i $HOME/.ssh/pku2_deploy -o IdentitiesOnly=yes"
```

Deploy Key 只需要仓库读取权限，不要开启写权限。Git 只会拉取已经提交的仓库内容，
不会带上本机被 `.gitignore` 排除的 `.env`、历史上传视频、数据库和旧向量索引。

## 四、配置公网 IP 与密钥

确认实例已经绑定固定公网 IPv4，然后在服务器创建生产环境配置。不要填写内网 IP；
如果云厂商会在关机后更换公网 IP，应先改为固定/弹性公网 IP。

```bash
cd /opt/AskEdu
cp .env.production.example .env.production
openssl rand -hex 32
openssl rand -hex 32
```

编辑 `.env.production`：

```bash
nano .env.production
```

至少修改：

- `SITE_ADDRESS`：固定公网 IPv4，只写数字地址，不带协议、端口或路径。
- `POSTGRES_PASSWORD` 和 `DATABASE_URL`：使用同一个仅含字母数字的随机密码。
- `DASHSCOPE_API_KEY`：通义千问 API Key。
- `SESSION_SECRET`：另一条随机值。
- `LOCAL_REGISTRATION_INVITE_CODE`：仅发给内测用户的邀请码。

生产配置不得提交到 Git，也不要通过聊天或截图发送。

## 五、首次启动

构建并启动四个服务（PostgreSQL、后端、评估 Worker、网站）：

```bash
cd /opt/AskEdu
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

首次启动后查看 `web` 日志，确认出现证书签发成功信息：

```bash
docker compose --env-file .env.production -f compose.production.yml logs --tail=100 web
```

然后打开 `https://服务器公网IP`，依次验证：登录、问答、大纲优化、短视频评估、
报告下载。不要使用 `http://`；Caddy 会将 HTTP 自动跳转到 HTTPS。

公网 IP 证书有效期约 6 天，Caddy 会自动续签。必须持续保留 `pku2_caddy_data` 卷，
并保持 80/443 端口可从公网访问。如果公网 IP 改变，需要修改 `SITE_ADDRESS` 后重建
`web` 服务，新 IP 会申请新证书。
查看状态和日志：

```bash
docker compose --env-file .env.production -f compose.production.yml ps
docker compose --env-file .env.production -f compose.production.yml logs --tail=200 backend
docker compose --env-file .env.production -f compose.production.yml logs --tail=200 worker
docker compose --env-file .env.production -f compose.production.yml logs --tail=100 web
```

## 六、发布更新

先在开发电脑完成修改、测试并推送到远程仓库。确认服务器上没有视频或大纲任务正在
处理后，在服务器检查并拉取 `main` 的最新提交：

```bash
cd /opt/AskEdu
git status --short
git fetch origin main
git log --oneline HEAD..origin/main
git pull --ff-only origin main
docker compose --env-file .env.production -f compose.production.yml up -d --build
docker compose --env-file .env.production -f compose.production.yml ps
```

`git status --short` 正常情况下不应显示任何代码改动；`.env.production` 已被忽略，
不会被拉取覆盖。如果服务器代码有未提交修改，应先停止更新并查明来源，不要直接强制
覆盖。

命令不会删除 PostgreSQL、上传文件、向量索引、Whisper 缓存或 HTTPS 证书，它们存放在
固定命名的 Docker volumes 中。不要执行 `docker compose down -v`。

## 七、备份与容量

每天备份 PostgreSQL；上传数据是否备份按内测隐私策略决定。数据库备份示例：

```bash
mkdir -p /opt/AskEdu-backups
docker compose --env-file /opt/AskEdu/.env.production -f /opt/AskEdu/compose.production.yml exec -T postgres pg_dump -U pku2 -d pku2 -Fc > /opt/AskEdu-backups/pku2.dump
```

虽然本次不迁移历史数据，上线后产生的新账号和任务仍在 PostgreSQL 中。建议：

- 磁盘达到 70% 时告警，达到 85% 前清理。
- 明确告知内测用户视频保存期限，建议 14～30 天。
- 每天数据库备份，保留最近 7～14 份，并定期复制到服务器之外。
- 更新前仍建议等待长任务结束；如果 Worker 意外重启，`processing` 任务会在租约超时后自动重新排队。

## 八、完整清空内测环境

只有确实要删除所有内测账号、任务、上传文件和索引时，才停止服务并删除以下固定卷：

- `pku2_pgdata`
- `pku2_app_data`
- `pku2_hf_cache`

这项操作不可恢复，普通发布和重启不需要删除卷。
