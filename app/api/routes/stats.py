from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.database.models import Session as SessionModel, Ad, AdResult

router = APIRouter()


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    try:
        total_participants = db.query(SessionModel).filter(
            SessionModel.eeg_data.isnot(None)
        ).count()

        total_ads = db.query(Ad).count()

        avg_attention_result = db.query(
            func.avg(AdResult.avg_attention)
        ).scalar()

        avg_attention = round(float(avg_attention_result), 2) if avg_attention_result else 0.0

        return {
            "total_participants": total_participants,
            "total_ads": total_ads,
            "avg_attention": avg_attention,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))