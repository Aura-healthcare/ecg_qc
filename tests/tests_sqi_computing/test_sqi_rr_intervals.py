import pandas as pd
from ecg_qc.sqi_computing.sqi_rr_intervals import cSQI, qSQI

time_window = 9
fs = 1000

ecg_signal = pd.read_csv('tests/tests_datasets/ecg_record_sample.csv')
ecg_signal = ecg_signal.iloc[:time_window * fs]['ecg_record'].values


# Additional: several recordings?
def test_qSQI(ecg_signal=ecg_signal, fs=fs):

    qSQI_score = qSQI(ecg_signal, fs)

    assert type(qSQI_score) == float


def test_cSQI(ecg_signal=ecg_signal, fs=fs):

    cSQI_score = cSQI(ecg_signal, fs)

    assert type(cSQI_score) == float
