"""Loopback-only UI test harness; never use in production.

Run from repo root: PYTHONPATH=. python tests/manual_cloud_drive_ui.py
No database, account login or evaluation model is used.
Provider metadata requests are real; task creation is deliberately disabled.
"""
from fastapi import FastAPI, HTTPException
from backend.app.core.cloud_drives import inspect_share
from backend.app.schemas import RemoteSourceForm

app = FastAPI(title="LOCAL TEST ONLY: cloud-drive UI")


@app.get("/api/auth/config")
def config():
    return {"auth_mode": "local", "registration_enabled": False}


@app.get("/api/auth/me")
def me():
    return {"id": "local-ui-validation", "name": "本地网盘界面测试", "role": "user", "status": "active"}


@app.get("/api/evaluation/tasks")
def tasks():
    return []


@app.post("/api/evaluation/remote-source")
async def inspect(form: RemoteSourceForm):
    return await inspect_share(form.url, form.password, form.path)


@app.post("/api/evaluation/tasks")
def no_tasks():
    raise HTTPException(400, "本地界面验证模式：不创建任务，不运行解析模型")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8010, access_log=False)
