from fastapi import APIRouter, HTTPException
from app.core.session_store import session_store
from app.services.eeg.collector import collect_eeg
from app.services.eeg.processor import apply_bandpass_filter, extract_band_powers, compute_indices
from app.services.eeg.formatter import format_eeg_result
from app.services.sync.synchronizer import synchronize

router = APIRouter()


@router.get("/result/{ad_id}")
def get_result(ad_id: str):
    try:
        gaze_data = session_store.get_gaze(ad_id)

        if not gaze_data:
            raise HTTPException(status_code=404, detail="gaze 데이터가 없습니다.")

        board_shim = session_store.board_shim
        board_id = session_store.board_id
        sampling_rate = session_store.sampling_rate

        if not board_shim:
            raise HTTPException(status_code=400, detail="EEG 세션이 없습니다.")

        data = board_shim.get_board_data()

        filtered = apply_bandpass_filter(data, sampling_rate)
        band_powers = extract_band_powers(filtered, sampling_rate)
        indices = compute_indices(band_powers)
        eeg_result = format_eeg_result(data, band_powers, indices, board_id)

        import numpy as np
        timestamp_channel = board_shim.get_timestamp_channel(board_id)
        eeg_timestamps = data[timestamp_channel]

        synced = synchronize(gaze_data, data, eeg_timestamps, indices)

        return {
            "ad_id": ad_id,
            "eeg": eeg_result["eeg"],
            "frames": synced,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))