import numpy as np
from app.models.gaze import GazePoint
from app.services.sync.synchronizer import synchronize

# 테스트용 gaze 데이터 (30Hz, 5개)
gaze_data = [
    GazePoint(x_norm=0.52, y_norm=0.34, timestamp=0.000, elapsed_ms=0),
    GazePoint(x_norm=0.55, y_norm=0.36, timestamp=0.033, elapsed_ms=33),
    GazePoint(x_norm=0.53, y_norm=0.35, timestamp=0.066, elapsed_ms=66),
    GazePoint(x_norm=0.51, y_norm=0.33, timestamp=0.099, elapsed_ms=99),
    GazePoint(x_norm=0.54, y_norm=0.37, timestamp=0.132, elapsed_ms=132),
]

# 테스트용 EEG timestamps (256Hz)
eeg_timestamps = np.linspace(0, 0.132, 34)

indices = {
    "attention": 0.72,
    "arousal": 0.65,
}

result = synchronize(gaze_data, None, eeg_timestamps, indices)

for frame in result:
    print(frame)