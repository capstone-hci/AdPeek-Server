from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.survey import SurveyRequest
from app.database.models import Survey
import uuid

router = APIRouter()


@router.post("/survey")
def submit_survey(body: SurveyRequest, db: Session = Depends(get_db)):
    try:
        survey = Survey(
            id=str(uuid.uuid4()),
            ad_id=body.ad_id,
            session_id=body.session_id,
            recall=body.recall,
            brand_score=body.brand_score,
            emotion=body.emotion,
            comment=body.comment,
        )
        db.add(survey)
        db.commit()

        return {"message": "설문 저장 완료", "survey_id": survey.id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))