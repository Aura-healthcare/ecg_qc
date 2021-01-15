import pandas as pd
from ecg_qc.sqi_computing.sqi_rr_intervals import csqi, qsqi

time_window = 9
fs = 1000

ecg_signal = pd.read_csv('tests/tests_datasets/ecg_record_sample.csv')
ecg_signal = ecg_signal.iloc[:time_window * fs]['ecg_record'].values


# Additional: several recordings?
def test_qsqi(ecg_signal=ecg_signal, fs=fs):

    q_sqi_score = qsqi(ecg_signal, fs)

    assert isinstance(q_sqi_score, float)


def test_csqi(ecg_signal=ecg_signal, fs=fs):

    c_sqi_score = csqi(ecg_signal, fs)

    assert isinstance(c_sqi_score, float)
