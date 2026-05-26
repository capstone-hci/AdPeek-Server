from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.session_store import session_store
from app.models.gaze import GazeSessionData
from app.database.repository import update_session_gaze

router = APIRouter()


@router.post("/gaze")
def receive_gaze(gaze_session: GazeSessionData, db: Session = Depends(get_db)):
    try:
        gaze_list = [g.model_dump() for g in gaze_session.data]

        session_store.save_gaze(gaze_session.ad_id, gaze_session.data)
        update_session_gaze(db, gaze_session.ad_id, gaze_list)

        return {
            "ad_id": gaze_session.ad_id,
            "start_time": gaze_session.start_time,
            "gaze_count": len(gaze_session.data),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))