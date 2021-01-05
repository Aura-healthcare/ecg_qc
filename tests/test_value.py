import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(sys.path[0]).parent))
import ecg_qc


sample_sqi_0 = [[0.83, 0.6, 6.17, 0.5, 0.57, -0.35]]
sample_sqi_1 = [[0.94, 0.59, 10.79, 0.51, 0.85, 2.97]]
sample_sqi_test = [[0.94, 0.59, 10.79, 0.51, 0.85, 2.97]]

def test():
    SQI_class = ecg_qc.ecg_qc()
    print(SQI_class.predict_quality(sample_sqi_0))
    print(SQI_class.predict_quality(sample_sqi_1))
    print(SQI_class.predict_quality(sample_sqi_test))

if __name__ == '__main__':
    test()
