import numpy as np
from typing import List
from app.models.gaze import GazePoint


def resample_eeg_to_gaze(
    eeg_timestamps: np.ndarray,
    eeg_values: np.ndarray,
    gaze_timestamps: np.ndarray,
) -> np.ndarray:
    """
    EEG 256Hz → gaze 30Hz 기준으로 리샘플링 (선형 보간)
    """
    from scipy import interpolate

    interp_func = interpolate.interp1d(
        eeg_timestamps,
        eeg_values,
        kind="linear",
        bounds_error=False,
        fill_value="extrapolate",
    )

    return interp_func(gaze_timestamps)


def synchronize(
    gaze_data: List[GazePoint],
    eeg_data: np.ndarray,
    eeg_timestamps: np.ndarray,
    indices: dict,
) -> list:
    """
    gaze + EEG 데이터를 elapsed_ms 기준으로 동기화
    """
    gaze_timestamps = np.array([g.timestamp for g in gaze_data])

    resampled_attention = resample_eeg_to_gaze(
        eeg_timestamps,
        np.full(len(eeg_timestamps), indices["attention"]),
        gaze_timestamps,
    )

    resampled_arousal = resample_eeg_to_gaze(
        eeg_timestamps,
        np.full(len(eeg_timestamps), indices["arousal"]),
        gaze_timestamps,
    )

    result = []
    for i, gaze in enumerate(gaze_data):
        result.append({
            "timestamp": gaze.timestamp,
            "elapsed_ms": gaze.elapsed_ms,
            "gaze": {
                "x_norm": gaze.x_norm,
                "y_norm": gaze.y_norm,
            },
            "eeg": {
                "attention": round(float(resampled_attention[i]), 4),
                "arousal": round(float(resampled_arousal[i]), 4),
            },
        })

    return result