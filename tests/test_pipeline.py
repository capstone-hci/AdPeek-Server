import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_full_pipeline():
    # 1. 세션 시작
    res = client.post("/api/session/start", json={"ad_id": "test_001"})
    assert res.status_code == 200

    # EEG 데이터 수집 대기
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
    print(result)