from fastapi.testclient import TestClient
from main import app
import time

client = TestClient(app)


def test_eeg_status_before_session():
    # 세션 시작 전 → connected: False
    res = client.get("/api/eeg/connect")
    assert res.status_code == 200
    result = res.json()
    assert result["connected"] == False
    assert result["collecting"] == False
    print("before session:", result)


def test_eeg_status_during_session():
    # 세션 시작 후 → connected: True
    client.post("/api/session/start", json={"ad_id": "ad_001"})
    time.sleep(2)

    res = client.get("/api/eeg/connect")
    assert res.status_code == 200
    result = res.json()
    assert result["connected"] == True
    assert result["collecting"] == True
    assert result["signal_quality"] is not None
    
    print("during session:", result)

    client.post("/api/session/stop", json={"ad_id": "ad_001"})