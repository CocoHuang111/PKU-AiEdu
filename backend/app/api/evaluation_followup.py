from fastapi import APIRouter, Depends, HTTPException
from ..core.auth import current_user
from ..core.report_mail import follow_up, subscribe, unsubscribe
import uuid

router = APIRouter()


def valid_id(task_id):
    try:
        return str(uuid.UUID(task_id))
    except ValueError:
        raise HTTPException(404, "任务不存在") from None


@router.get("/task/{task_id}/follow-up")
async def get_follow_up(task_id: str, user: dict = Depends(current_user)):
    return await follow_up(valid_id(task_id), user["id"])


@router.post("/task/{task_id}/email-notification")
async def request_email(task_id: str, user: dict = Depends(current_user)):
    return await subscribe(valid_id(task_id), user["id"])


@router.delete("/task/{task_id}/email-notification")
async def cancel_email(task_id: str, user: dict = Depends(current_user)):
    return await unsubscribe(valid_id(task_id), user["id"])
