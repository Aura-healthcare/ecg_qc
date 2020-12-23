import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(sys.path[0]).parent))
import ecg_qc


def main():

    sampling_frequency = 1000
    window_size_sec = 9
    window_size_sample = window_size_sec * sampling_frequency
    test_sample = pd.read_csv('tests/ecg_record_sample.csv').values
    offset_start = 0
    last_sample = 100 * window_size_sample
    SQI_class = ecg_qc.ecg_qc()
    for offset in list(range(offset_start, last_sample, window_size_sample)):
        ecg_data = test_sample[offset: offset + window_size_sample, 0]
        print(SQI_class.get_signal_quality(ecg_data))


main()
