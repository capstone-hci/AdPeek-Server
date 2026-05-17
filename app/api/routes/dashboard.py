from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.analytics.aggregator import aggregate_ad_results

router = APIRouter()


@router.get("/dashboard/{ad_id}")
def get_dashboard(ad_id: str, db: Session = Depends(get_db)):
    try:
        result = aggregate_ad_results(db, ad_id)

        if not result:
            raise HTTPException(status_code=404, detail="해당 광고의 세션 데이터가 없습니다.")

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))