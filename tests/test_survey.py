from fastapi.testclient import TestClient
from main import app
from app.core.database import SessionLocal
from app.database.models import Survey

client = TestClient(app)


def test_submit_survey():
    # DB 초기화
    db = SessionLocal()
    db.query(Survey).filter(Survey.ad_id == "ad_001").delete()
    db.commit()
    db.close()

    res = client.post("/api/survey", json={
        "ad_id": "ad_001",
        "session_id": None,
        "recall": "yes",
        "brand_score": 4,
        "emotion": "positive",
        "comment": "광고가 인상적이었습니다."
    })

    assert res.status_code == 200
    result = res.json()
    assert result["message"] == "설문 저장 완료"
    assert "survey_id" in result
    print("survey:", result)