import numpy as np


def sSQI(ecg_signal):
    num = np.mean((ecg_signal - np.mean(ecg_signal))**3)
    sSQI = num / (np.std(ecg_signal, ddof=1)**3)
    sSQI_cr = round(sSQI, 2)

    return sSQI_cr


def kSQI(ecg_signal):
    num = np.mean((ecg_signal - np.mean(ecg_signal))**4)
    kSQI = num / (np.std(ecg_signal, ddof=1)**4)
    kSQI_fischer = kSQI - 3.0
    kSQI_cr = round(kSQI_fischer, 2)

    return kSQI_cr
