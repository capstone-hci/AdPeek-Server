from fastapi import APIRouter, HTTPException
from app.models.gaze import GazeSessionData
from app.core.session_store import session_store

router = APIRouter()


@router.post("/gaze")
def receive_gaze(gaze_session: GazeSessionData):
    try:
        session_store.save_gaze(gaze_session.ad_id, gaze_session.data)

        return {
            "ad_id": gaze_session.ad_id,
            "start_time": gaze_session.start_time,
            "gaze_count": len(gaze_session.data),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))