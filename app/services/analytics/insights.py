import numpy as np
from typing import Optional


def compute_eeg_peaks(frames: list) -> dict:
    """
    EEG attention/arousal 피크 구간 계산
    """
    if not frames:
        return {"attentionPeakRange": None, "arousalPeakRange": None}

    attention_values = [f["eeg"]["attention"] for f in frames]
    arousal_values = [f["eeg"]["arousal"] for f in frames]
    timestamps = [f["elapsed_ms"] / 1000 for f in frames]

    def get_peak_range(values: list, timestamps: list) -> Optional[str]:
        if not values:
            return None
        peak_idx = int(np.argmax(values))
        start = max(0, peak_idx - 2)
        end = min(len(timestamps) - 1, peak_idx + 2)
        return f"{round(timestamps[start], 1)}–{round(timestamps[end], 1)}s"

    return {
        "attentionPeakRange": get_peak_range(attention_values, timestamps),
        "arousalPeakRange": get_peak_range(arousal_values, timestamps),
    }


def compute_gaze_insights(frames: list, aoi_rows: list) -> dict:
    """
    gaze 기반 주시 시간 최대 구간 + dwell time 계산
    """
    if not frames:
        return {
            "maxGazeRange": None,
            "maxDwellTime": None,
            "aoiRows": [],
        }

    timestamps = [f["elapsed_ms"] / 1000 for f in frames]
    window_size = 30  # 1초 윈도우 (30Hz)

    max_count = 0
    max_start = 0

    for i in range(len(frames) - window_size):
        if frames[i + window_size]["elapsed_ms"] - frames[i]["elapsed_ms"] <= 1100:
            max_count = window_size
            max_start = i

    max_dwell = max([float(row["dwell"].replace("초", "")) for row in aoi_rows], default=0)

    return {
        "maxGazeRange": f"{round(timestamps[max_start], 1)}–{round(timestamps[min(max_start + window_size, len(timestamps)-1)], 1)}s",
        "maxDwellTime": f"{max_dwell}초",
        "aoiRows": aoi_rows,
    }


def compute_survey_insights(surveys: list) -> dict:
    """
    설문 데이터 집계
    """
    if not surveys:
        return {
            "recallRate": None,
            "purchaseIntent": None,
            "positiveEmotion": None,
        }

    total = len(surveys)
    recall_count = sum(1 for s in surveys if s.recall == "yes")
    positive_count = sum(1 for s in surveys if s.emotion == "positive")
    avg_brand_score = round(sum(s.brand_score for s in surveys) / total, 1)

    return {
        "recallRate": f"{round(recall_count / total * 100)}%",
        "purchaseIntent": f"{avg_brand_score}/5",
        "positiveEmotion": f"{round(positive_count / total * 100)}%",
    }


def compute_attention_percent(avg_attention: float) -> int:
    """
    attention 지표를 0~100% 스케일로 변환
    시뮬레이터 기준 평균 ~4.7, 최대 ~10 기준으로 정규화
    """
    normalized = min(avg_attention / 10.0, 1.0)
    return round(normalized * 100)