from fastapi import APIRouter, HTTPException
from brainflow.board_shim import BoardShim
from app.core.session_store import session_store
from app.services.eeg.processor import apply_bandpass_filter, extract_band_powers, compute_indices
from app.services.eeg.formatter import format_eeg_result
from app.services.sync.synchronizer import synchronize

router = APIRouter()


@router.get("/result/{ad_id}")
def get_result(ad_id: str):
    try:
        gaze_data = session_store.get_gaze(ad_id)
        eeg_session = session_store.get_eeg(ad_id)

        if not gaze_data:
            raise HTTPException(status_code=404, detail="gaze 데이터가 없습니다.")
        if not eeg_session:
            raise HTTPException(status_code=404, detail="EEG 데이터가 없습니다.")

        data = eeg_session["data"]
        sampling_rate = eeg_session["sampling_rate"]
        board_id = eeg_session["board_id"]

        filtered = apply_bandpass_filter(data, sampling_rate)
        band_powers = extract_band_powers(filtered, sampling_rate)
        indices = compute_indices(band_powers)
        eeg_result = format_eeg_result(data, band_powers, indices, board_id)

        timestamp_channel = BoardShim.get_timestamp_channel(board_id)
        eeg_timestamps = data[timestamp_channel]

        synced = synchronize(gaze_data, data, eeg_timestamps, indices)

        return {
            "ad_id": ad_id,
            "eeg": eeg_result["eeg"],
            "frames": synced,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))