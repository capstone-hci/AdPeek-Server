from fastapi import APIRouter, HTTPException
from app.models.gaze import GazeSessionData

router = APIRouter()


@router.post("/gaze")
def receive_gaze(gaze_session: GazeSessionData):
    try:
        return {
            "ad_id": gaze_session.ad_id,
            "start_time": gaze_session.start_time,
            "gaze_count": len(gaze_session.data),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))