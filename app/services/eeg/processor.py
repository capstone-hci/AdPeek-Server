import numpy as np
from brainflow.board_shim import BoardShim
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations


def apply_bandpass_filter(data: np.ndarray, sampling_rate: int) -> np.ndarray:
    """
    밴드패스 필터 적용 (1~40Hz)
    - 불필요한 저주파/고주파 노이즈 제거
    """
    eeg_channels = [1, 2, 3, 4]  # TP9, AF7, AF8, TP10

    for channel in eeg_channels:
        DataFilter.perform_bandpass(
            data[channel],
            sampling_rate,
            1.0,   # 저주파 컷오프
            40.0,  # 고주파 컷오프
            4,
            FilterTypes.BUTTERWORTH.value,
            0,
        )

    return data


def extract_band_powers(data: np.ndarray, sampling_rate: int) -> dict:
    """
    Alpha / Beta / Theta 대역 파워 계산
    """
    eeg_channels = [1, 2, 3, 4]
    band_powers = {"alpha": [], "beta": [], "theta": []}

    for channel in eeg_channels:
        psd = DataFilter.get_psd_welch(
            data[channel],
            min(len(data[channel]), 256),
            min(len(data[channel]), 256) // 2,
            sampling_rate,
            WindowOperations.BLACKMAN_HARRIS.value,
        )

        alpha = DataFilter.get_band_power(psd, 8.0, 13.0)
        beta = DataFilter.get_band_power(psd, 13.0, 30.0)
        theta = DataFilter.get_band_power(psd, 4.0, 8.0)

        band_powers["alpha"].append(alpha)
        band_powers["beta"].append(beta)
        band_powers["theta"].append(theta)

    return {
        "alpha": float(np.mean(band_powers["alpha"])),
        "beta": float(np.mean(band_powers["beta"])),
        "theta": float(np.mean(band_powers["theta"])),
    }


def compute_indices(band_powers: dict) -> dict:
    """
    집중도(attention), 각성도(arousal) 지표 계산
    - attention: beta / (alpha + theta)
    - arousal: beta / alpha
    """
    alpha = band_powers["alpha"]
    beta = band_powers["beta"]
    theta = band_powers["theta"]

    attention = beta / (alpha + theta + 1e-6)
    arousal = beta / (alpha + 1e-6)

    return {
        "attention": round(float(attention), 4),
        "arousal": round(float(arousal), 4),
    }