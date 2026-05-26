import time
import numpy as np
from brainflow.board_shim import BoardShim


def format_eeg_result(
    data: np.ndarray,
    band_powers: dict,
    indices: dict,
    board_id: int,
) -> dict:
    """
    EEG 처리 결과를 FastAPI 응답 형태로 포맷
    """
    timestamp_channel = BoardShim.get_timestamp_channel(board_id)
    timestamps = data[timestamp_channel].tolist()

    return {
        "timestamp": timestamps[-1] if timestamps else time.time(),
        "eeg": {
            "attention": indices["attention"],
            "arousal": indices["arousal"],
            "bands": {
                "alpha": band_powers["alpha"],
                "beta": band_powers["beta"],
                "theta": band_powers["theta"],
            },
        },
    }


def format_session_result(
    gaze_data: list[dict],
    eeg_result: dict,
) -> dict:
    """
    gaze + EEG 결과를 합쳐서 최종 응답 구조로 포맷
    """
    return {
        "timestamp": eeg_result["timestamp"],
        "gaze": gaze_data,
        "eeg": eeg_result["eeg"],
    }