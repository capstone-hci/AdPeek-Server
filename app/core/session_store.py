from typing import Optional
import numpy as np


class SessionStore:
    def __init__(self):
        self.board_shim = None
        self.board_id: Optional[int] = None
        self.sampling_rate: Optional[int] = None
        self.gaze_data: dict = {}
        self.eeg_data: dict = {}

    def set_board(self, board_shim, board_id: int, sampling_rate: int):
        self.board_shim = board_shim
        self.board_id = board_id
        self.sampling_rate = sampling_rate

    def clear_board(self):
        self.board_shim = None
        self.board_id = None
        self.sampling_rate = None

    def save_gaze(self, ad_id: str, data: list):
        self.gaze_data[ad_id] = data

    def get_gaze(self, ad_id: str):
        return self.gaze_data.get(ad_id)

    def save_eeg(self, ad_id: str, data: np.ndarray, sampling_rate: int, board_id: int):
        self.eeg_data[ad_id] = {
            "data": data,
            "sampling_rate": sampling_rate,
            "board_id": board_id,
        }

    def get_eeg(self, ad_id: str):
        return self.eeg_data.get(ad_id)


session_store = SessionStore()