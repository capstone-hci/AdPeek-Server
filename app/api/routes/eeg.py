from fastapi import APIRouter
from app.core.session_store import session_store
from brainflow.board_shim import BoardShim
import numpy as np

router = APIRouter()


@router.get("/eeg/connect")
def get_eeg_status():
    board_shim = session_store.board_shim
    board_id = session_store.board_id

    if not board_shim:
        return {
            "connected": False,
            "collecting": False,
            "signal_quality": None,
        }

    try:
        data = board_shim.get_current_board_data(256)
        eeg_channels = BoardShim.get_eeg_channels(board_id)

        signal_quality = {}
        channel_names = ["TP9", "AF7", "AF8", "TP10"]

        for i, ch in enumerate(eeg_channels):
            if i >= len(channel_names):
                break
            channel_data = data[ch]
            std = float(np.std(channel_data))

            if std < 1:
                quality = "no_signal"
            elif std < 10:
                quality = "poor"
            elif std < 50:
                quality = "good"
            else:
                quality = "excellent"

            signal_quality[channel_names[i]] = quality

        return {
            "connected": True,
            "collecting": True,
            "signal_quality": signal_quality,
        }

    except Exception as e:
        return {
            "connected": True,
            "collecting": False,
            "signal_quality": None,
            "error": str(e),
        }