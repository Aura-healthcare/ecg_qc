import sklearn
import xgboost
import pandas as pd
import numpy as np
from ecg_qc.ecg_qc import ecg_qc

time_window = 9
fs = 1000
sample_sqi_0 = [[0.83, 0.6, 6.17, 0.5, 0.57, -0.35]]

ecg_signal = pd.read_csv('tests/ecg_record_sample.csv')
ecg_signal = ecg_signal.iloc[:time_window * fs]['ecg_record'].values
ecg_qc_test = ecg_qc()


def test_init():

    assert isinstance(ecg_qc_test.data_encoder,
                      sklearn.compose.ColumnTransformer)

    assert isinstance(ecg_qc_test.model,
                      xgboost.sklearn.XGBClassifier)

    assert type(ecg_qc_test.sampling_frequency) == int


def test_compute_sqi_scores(ecg_signal=ecg_signal):

    sqi_scores = ecg_qc_test.compute_sqi_scores(ecg_signal)

    assert type(sqi_scores) == list
    assert np.array(sqi_scores).shape == (1, 6)


def test_predict_quality(sample_sqi=sample_sqi_0):

    pred_0 = ecg_qc_test.predict_quality(sample_sqi)

    assert type(pred_0) == int


def test_get_signal_quality(ecg_signal=ecg_signal):

    quality_predicted = ecg_qc_test.get_signal_quality(ecg_signal)
    assert type(quality_predicted) == int
