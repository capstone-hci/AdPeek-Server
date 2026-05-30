import time
from fastapi.testclient import TestClient
from main import app
from app.core.database import SessionLocal
from app.database.models import Session as SessionModel, AdResult, Survey

client = TestClient(app)

# 30초 광고 기준 gaze 데이터 (30Hz, 약 900프레임 시뮬레이션)
def make_gaze_data(ad_id: str, start_time: float) -> dict:
    data = []
    for i in range(90):  # 3초치 데이터 (30Hz × 3s)
        elapsed_ms = i * 33
        data.append({
            "x_norm": round(0.3 + (i % 9) * 0.05, 2),
            "y_norm": round(0.3 + (i % 6) * 0.06, 2),
            "timestamp": round(elapsed_ms / 1000, 3),
            "elapsed_ms": elapsed_ms,
        })
    return {
        "ad_id": ad_id,
        "start_time": start_time,
        "data": data,
    }


def test_full_pipeline():
    # DB 초기화
    db = SessionLocal()
    db.query(SessionModel).filter(SessionModel.ad_id == "test_001").delete()
    db.query(AdResult).filter(AdResult.ad_id == "test_001").delete()
    db.query(Survey).filter(Survey.ad_id == "test_001").delete()
    db.commit()
    db.close()

    # 1. EEG 연결 확인
    res = client.get("/api/eeg/connect")
    assert res.status_code == 200
    print("eeg connect:", res.json())

    # 2. 세션 시작
    res = client.post("/api/session/start", json={"ad_id": "test_001"})
    assert res.status_code == 200

    time.sleep(3)

    # 3. gaze 데이터 전송
    res = client.post("/api/gaze", json=make_gaze_data("test_001", 1714900000.0))
    assert res.status_code == 200
    print("gaze count:", res.json()["gaze_count"])

    # 4. 세션 종료
    res = client.post("/api/session/stop", json={"ad_id": "test_001"})
    assert res.status_code == 200

    # 5. 단일 결과 조회
    res = client.get("/api/result/test_001")
    assert res.status_code == 200
    result = res.json()
    assert result["ad_id"] == "test_001"
    assert "eeg" in result
    assert "frames" in result
    assert len(result["frames"]) > 0
    print("frames count:", len(result["frames"]))

    # 6. 설문 제출
    res = client.post("/api/survey", json={
        "ad_id": "test_001",
        "recall": "yes",
        "brand_score": 4,
        "emotion": "positive",
        "comment": "인상적이었습니다.",
    })
    assert res.status_code == 200
    print("survey:", res.json())

    print("✅ test_full_pipeline 완료")


def test_dashboard():
    # DB 초기화
    db = SessionLocal()
    db.query(SessionModel).filter(SessionModel.ad_id == "ad_001").delete()
    db.query(AdResult).filter(AdResult.ad_id == "ad_001").delete()
    db.query(Survey).filter(Survey.ad_id == "ad_001").delete()
    db.commit()
    db.close()

    for i, (recall, score, emotion) in enumerate([
        ("yes", 5, "positive"),
        ("yes", 4, "positive"),
        ("unsure", 3, "neutral"),
        ("no", 2, "negative"),
    ]):
        # 세션 시작
        client.post("/api/session/start", json={"ad_id": "ad_001"})
        time.sleep(3)

        # gaze 전송
        client.post("/api/gaze", json=make_gaze_data("ad_001", 1714900000.0 + i * 100))

        # 세션 종료
        client.post("/api/session/stop", json={"ad_id": "ad_001"})

        # 설문 제출
        client.post("/api/survey", json={
            "ad_id": "ad_001",
            "recall": recall,
            "brand_score": score,
            "emotion": emotion,
        })

    # 대시보드 조회
    res = client.get("/api/dashboard/ad_001")
    assert res.status_code == 200
    result = res.json()

    assert result["participant_count"] == 4
    assert "avg_attention" in result
    assert "heatmap_data" in result
    assert "scenes" in result
    assert len(result["scenes"]) > 0
    assert "insights" in result
    assert "gaze" in result["insights"]
    assert "eeg" in result["insights"]
    assert "survey" in result["insights"]
    assert result["insights"]["survey"]["recallRate"] == "50%"

    print("participant_count:", result["participant_count"])
    print("avg_attention:", result["avg_attention"])
    print("insights:", result["insights"])
    print("✅ test_dashboard 완료")