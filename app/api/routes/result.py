from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.database.repository import get_session_by_ad_id

router = APIRouter()


@router.get("/result/{ad_id}")
def get_result(ad_id: str, db: Session = Depends(get_db)):
    try:
        session = get_session_by_ad_id(db, ad_id)

        if not session:
            raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다.")

        if not session.eeg_data:
            raise HTTPException(status_code=404, detail="EEG 데이터가 없습니다.")

        return {
            "ad_id": ad_id,
            "eeg": session.eeg_data,
            "frames": session.synced_frames or [],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))