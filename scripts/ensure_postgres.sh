#!/bin/sh
# 优先使用本机已在监听的 PostgreSQL；只有 5432 没人听时才尝试 Docker。
set -eu

if pg_isready -h 127.0.0.1 -p 5432 >/dev/null 2>&1; then
  echo "本机 PostgreSQL 已在 127.0.0.1:5432 监听，不启动 Docker。"
else
  if docker info >/dev/null 2>&1; then
    docker compose up -d postgres
    i=0
    while [ "$i" -lt 30 ]; do
      if pg_isready -h 127.0.0.1 -p 5432 >/dev/null 2>&1; then
        break
      fi
      i=$((i + 1))
      sleep 1
    done
  else
    echo "5432 没有数据库，且 Docker 未运行。"
    echo "任选其一："
    echo "  1. 打开 Docker Desktop 后再执行 make db-up"
    echo "  2. 启动本机 Postgres，例如：brew services start postgresql@17"
    exit 1
  fi
fi

if psql -h 127.0.0.1 -d postgres -c "SELECT 1" >/dev/null 2>&1; then
  if ! psql -h 127.0.0.1 -d postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='pku2'" | grep -q 1; then
    psql -h 127.0.0.1 -d postgres -c "CREATE USER pku2 WITH PASSWORD 'pku2';"
  fi
  if ! psql -h 127.0.0.1 -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='pku2'" | grep -q 1; then
    psql -h 127.0.0.1 -d postgres -c "CREATE DATABASE pku2 OWNER pku2;"
  fi
fi

if PGPASSWORD=pku2 psql -h 127.0.0.1 -U pku2 -d pku2 -c "SELECT 1" >/dev/null 2>&1; then
  echo "数据库 pku2 已就绪。下一步：make db-migrate"
else
  echo "5432 已有 Postgres，但用 pku2/pku2 连不上。请检查 DATABASE_URL，或手动创建用户和库。"
  exit 1
fi
