import time
from fastapi.testclient import TestClient
from main import app
from app.core.database import SessionLocal
from app.database.models import Session as SessionModel, AdResult

client = TestClient(app)


def test_full_pipeline():
    # DB 초기화
    db = SessionLocal()
    db.query(SessionModel).filter(SessionModel.ad_id == "test_001").delete()
    db.query(AdResult).filter(AdResult.ad_id == "test_001").delete()
    db.commit()
    db.close()

    # 1. 세션 시작
    res = client.post("/api/session/start", json={"ad_id": "test_001"})
    assert res.status_code == 200

    time.sleep(3)

    # 2. gaze 데이터 전송
    res = client.post("/api/gaze", json={
        "ad_id": "test_001",
        "start_time": 1714900000.123,
        "data": [
            {"x_norm": 0.52, "y_norm": 0.34, "timestamp": 0.000, "elapsed_ms": 0},
            {"x_norm": 0.55, "y_norm": 0.36, "timestamp": 0.033, "elapsed_ms": 33},
        ]
    })
    assert res.status_code == 200

    # 3. 세션 종료
    res = client.post("/api/session/stop", json={"ad_id": "test_001"})
    assert res.status_code == 200

    # 4. 결과 조회
    res = client.get("/api/result/test_001")
    assert res.status_code == 200
    result = res.json()
    assert result["ad_id"] == "test_001"
    assert "eeg" in result
    assert "frames" in result
    print("result:", result)


def test_dashboard():
    # DB 초기화
    db = SessionLocal()
    db.query(SessionModel).filter(SessionModel.ad_id == "test_dash").delete()
    db.query(AdResult).filter(AdResult.ad_id == "test_dash").delete()
    db.commit()
    db.close()

    # 참여자 1
    client.post("/api/session/start", json={"ad_id": "test_dash"})
    time.sleep(3)
    client.post("/api/gaze", json={
        "ad_id": "test_dash",
        "start_time": 1714900000.0,
        "data": [
            {"x_norm": 0.52, "y_norm": 0.34, "timestamp": 0.000, "elapsed_ms": 0},
            {"x_norm": 0.55, "y_norm": 0.36, "timestamp": 0.033, "elapsed_ms": 33},
        ]
    })
    client.post("/api/session/stop", json={"ad_id": "test_dash"})

    # 참여자 2
    client.post("/api/session/start", json={"ad_id": "test_dash"})
    time.sleep(3)
    client.post("/api/gaze", json={
        "ad_id": "test_dash",
        "start_time": 1714900010.0,
        "data": [
            {"x_norm": 0.60, "y_norm": 0.40, "timestamp": 0.000, "elapsed_ms": 0},
            {"x_norm": 0.65, "y_norm": 0.45, "timestamp": 0.033, "elapsed_ms": 33},
        ]
    })
    client.post("/api/session/stop", json={"ad_id": "test_dash"})

    # 대시보드 조회
    res = client.get("/api/dashboard/test_dash")
    assert res.status_code == 200
    result = res.json()
    assert result["participant_count"] == 2
    assert "avg_attention" in result
    assert "heatmap_data" in result
    print("dashboard:", result)