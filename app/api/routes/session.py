from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class SessionStartRequest(BaseModel):
    ad_id: str


class SessionStopRequest(BaseModel):
    ad_id: str


@router.post("/session/start")
def start_session(body: SessionStartRequest):
    try:
        return {"message": "세션 시작", "ad_id": body.ad_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session/stop")
def stop_session(body: SessionStopRequest):
    try:
        return {"message": "세션 종료", "ad_id": body.ad_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))