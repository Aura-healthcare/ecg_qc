import pandas as pd
import numpy as np
import sys
from pathlib import Path
from tqdm import tqdm
sys.path.append(str(Path(sys.path[0]).parent.parent))
from ecg_qc.ecg_qc import ecg_qc

# sys arg

patient = '103001'
window = 9
sampling_frequency = 1000
input_data_folder = 'datasets/1_ecg_and_annotation_creation'
output_folder = 'datasets/2_dataset_creation'

i = 1
while i < len(sys.argv):
    if sys.argv[i] == '-patient' and i < len(sys.argv)-1:
        patient = sys.argv[i+1]
        i += 2
    elif sys.argv[i] == '-window' and i < len(sys.argv)-1:
        window = int(sys.argv[i+1])
        i += 2
    elif sys.argv[i] == '-sampling_frequency' and i < len(sys.argv)-1:
        sampling_frequency = int(sys.argv[i+1])
        i += 2
    elif sys.argv[i] == '-input_data_folder' and i < len(sys.argv)-1:
        input_data_folder = sys.argv[i+1]
        i += 2
    elif sys.argv[i] == '-output_folder' and i < len(sys.argv)-1:
        output_folder = sys.argv[i+1]
        i += 2
    else:
        print('Unknown argument' + str(sys.argv[i]))
        break


# Function declaration

def compute_sqi(patient: str = patient,
                window: str = window,
                sampling_frequency: str = sampling_frequency,
                input_data_folder: str = input_data_folder,
                output_folder: str = output_folder) -> [float]:

    df_ml = pd.DataFrame(columns=['timestamp_start', 'timestamp_end', 'qSQI_score', 'cSQI_score', 'sSQI_score', 'kSQI_score', 'pSQI_score', 'basSQI_score'])

    ecg_qc_class = ecg_qc()
    print('computing SQI')

    for i in tqdm(range(int(round(
            df_ecg.shape[0] / (window * sampling_frequency),
            0)))):

        start = i * window * sampling_frequency
        end = start + window * sampling_frequency
        sqi_scores = ecg_qc_class.compute_sqi_scores(
            ecg_signal=df_ecg['ecg_signal'][start:end].values)
        df_ml = df_ml.append({'timestamp_start': df_ecg['ecg_signal'][start:end].index[0],
                              'timestamp_end': df_ecg['ecg_signal'][start:end].index[-1],
                              'qSQI_score': sqi_scores[0][0],
                              'cSQI_score': sqi_scores[0][1],
                              'sSQI_score': sqi_scores[0][2],
                              'kSQI_score': sqi_scores[0][3],
                              'pSQI_score': sqi_scores[0][4],
                              'basSQI_score': sqi_scores[0][5]},
                             ignore_index=True)

        df_ml['timestamp_start'] = df_ml['timestamp_start'].astype(int)
        df_ml['timestamp_end'] = df_ml['timestamp_end'].astype(int)

    return df_ml


def binary_class_encoding(numeric_label):
    # In annotations, class 0 is non annotaed, class 1 is optimal,
    # class 2 has noise and 3 unusable

    if numeric_label >= 2:
        return 0
    return 1


def classification_correspondance(timestamp: int,
                                  sampling_frequency: int = 1000,
                                  window: int = 9):

    start = timestamp
    end = start + window * sampling_frequency - 1
    cons_value = df_ecg.loc[start:end]['cons'].unique()
    classif = binary_class_encoding(max(cons_value))

    return classif


def classification_correspondance_avg(timestamp,
                                      sampling_frequency=1000,
                                      window=9):

    start = timestamp
    end = start + window * sampling_frequency - 1
    cons_value = df_ecg.loc[start:end]['cons']

    classif_avg = np.mean([binary_class_encoding(x) for x in cons_value])

    return classif_avg


if __name__ == '__main__':

    df_ecg = pd.read_pickle(
        '{}/df_ecg_{}.pkl'.format(input_data_folder, patient))

    # removing signals without annotation

    for column in df_ecg.columns[1:]:
        df_ecg = df_ecg[df_ecg[column] > 0]

    df_ml = compute_sqi(patient=patient,
                        window=window,
                        sampling_frequency=sampling_frequency,
                        input_data_folder=input_data_folder,
                        output_folder=output_folder)

    print('Preparing ml_dataset for patient {}'.format(patient))

    df_ml['classif'] = df_ml['timestamp_start'].apply(
        lambda x: classification_correspondance(x))
    df_ml['classif_avg'] = df_ml['timestamp_start'].apply(
        lambda x: classification_correspondance_avg(x, window=9))

    df_ml.to_csv('{}/df_ml_{}.csv'.format(output_folder, patient),
                 index=False)

    print('done!')
