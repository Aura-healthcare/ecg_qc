import pandas as pd
from ecg_qc.sqi_computing.sqi_power_spectrum import sSQI, kSQI

time_window = 9
fs = 1000

ecg_signal = pd.read_csv('tests/tests_datasets/ecg_record_sample.csv')
ecg_signal = ecg_signal.iloc[:time_window * fs]['ecg_record'].values


# Additional: several recordings?
def test_sSQI(ecg_signal=ecg_signal):

    sSQI_score = sSQI(ecg_signal)

    assert type(sSQI_score) == float


def test_kSQI(ecg_signal=ecg_signal):

    kSQI_score = kSQI(ecg_signal)

    assert type(kSQI_score) == float
