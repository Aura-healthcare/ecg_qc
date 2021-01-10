import sklearn
import xgboost
import pandas as pd
import numpy as np
from ecg_qc.ecg_qc import ecg_qc

from ecg_qc.sqi_computing.sqi_rr_intervals import cSQI, qSQI
from ecg_qc.sqi_computing.sqi_power_spectrum import sSQI, kSQI
from ecg_qc.sqi_computing.sqi_frequency_distribution import basSQI, pSQI


time_window = 9
fs = 1000

sample_sqi_0 = [[0.57, 0.6, -0.35, 6.17, 0.5, 0.83]]
sample_sqi_1 = [[0.85, 0.59, 2.97, 10.79, 0.51, 0.94]]

# sample_sqi_0 = [[0.83, 0.6, 6.17, 0.5, 0.57, -0.35]]
# sample_sqi_1 = [[0.94, 0.59, 10.79, 0.51, 0.85, 2.97]]

ecg_signal = pd.read_csv('tests/tests_datasets/ecg_record_sample.csv')
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


def test_validate_prediction(sample_sqi_0=sample_sqi_0,
                             sample_sqi_1=sample_sqi_1):

    pred_0 = ecg_qc_test.predict_quality(sample_sqi_0)
    assert pred_0 == 0

    pred_1 = ecg_qc_test.predict_quality(sample_sqi_1)
    assert pred_1 == 1


def test_sqi_order(ecg_signal=ecg_signal):

    sqi_scores = ecg_qc_test.compute_sqi_scores(ecg_signal)

    qSQI_score = qSQI(ecg_signal, fs)
    cSQI_score = cSQI(ecg_signal, fs)
    sSQI_score = sSQI(ecg_signal)
    kSQI_score = kSQI(ecg_signal)
    pSQI_score = pSQI(ecg_signal, fs)
    basSQI_score = basSQI(ecg_signal, fs)

    assert sqi_scores == [[qSQI_score, cSQI_score, sSQI_score,
                           kSQI_score, pSQI_score, basSQI_score]]
