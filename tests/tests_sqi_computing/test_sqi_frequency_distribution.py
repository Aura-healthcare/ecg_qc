import pandas as pd
from ecg_qc.sqi_computing.sqi_frequency_distribution import ssqi, ksqi

time_window = 9
fs = 1000

ecg_signal = pd.read_csv('tests/tests_datasets/ecg_record_sample.csv')
ecg_signal = ecg_signal.iloc[:time_window * fs]['ecg_record'].values


# Additional: several recordings?
def test_ssqi(ecg_signal=ecg_signal):

    s_sqi_score = ssqi(ecg_signal)

    assert isinstance(s_sqi_score, float)


def test_ksqi(ecg_signal=ecg_signal):

    k_sqi_score = ksqi(ecg_signal)

    assert isinstance(k_sqi_score, float)
