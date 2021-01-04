import pandas as pd
import wfdb
from tqdm import tqdm
import sys
import re


patient = '103001'
target_annot = ['cons']
sampling_frequency = 1000
input_data_folder = 'datasets/0_physionet_ecg'
output_folder = 'datasets/1_ecg_and_annotation_creation'

i = 1
while i < len(sys.argv):
    if sys.argv[i] == '-patient' and i < len(sys.argv)-1:
        patient = sys.argv[i+1]
        i += 2
    elif sys.argv[i] == '-target_annot' and i < len(sys.argv)-1:
        target_annot = sys.argv[i+1].split(',')
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


def ecg_annoted_creation(patient: str = patient,
                         target_annot: str = target_annot,
                         sampling_frequency: str = sampling_frequency,
                         input_data_folder: str = input_data_folder,
                         output_folder: str = output_folder
                         ):

    print('Starting ecg_annoted_creation for patient {}'.format(patient))

    # Loading datasets

    df_ann = pd.read_csv('{}/{}_ANN.csv'.format(input_data_folder, patient),
                         header=None)
    df_ann.columns = ['anno1_start_sample', 'anno1_end_sample', 'anno1_tag',
                      'anno2_start_sample', 'anno2_end_sample', 'anno2_tag',
                      'anno3_start_sample', 'anno3_end_sample', 'anno3_tag',
                      'cons_start_sample', 'cons_end_sample', 'cons_tag']

    ecg_columns = ['anno1_start_sample', 'anno1_end_sample',
                   'anno2_start_sample', 'anno2_end_sample',
                   'anno3_start_sample', 'anno3_end_sample',
                   'cons_start_sample', 'cons_end_sample']

    for column in ecg_columns:
        df_ann[column] = df_ann[column] / sampling_frequency

    ecg_data = wfdb.rdrecord('{}/{}_ECG'.format(input_data_folder, patient))
    df_ecg = pd.DataFrame(ecg_data.p_signal)
    df_ecg.columns = ['ecg_signal']
    df_ecg['timestamp'] = df_ecg.index / sampling_frequency

    # Creation of annotation data

    line = 0
    target_annot_index = 0

    for annot in target_annot:
        df_ecg[annot] = ''

    for target_annot_index in range(len(target_annot)):

        for line in tqdm(
            range(int(df_ann['{}_end_sample'.format(
                target_annot[target_annot_index])].dropna().shape[0]))):
            start = df_ann['{}_start_sample'.format(
                    target_annot[target_annot_index])
                    ].iloc[line]
            end = df_ann['{}_end_sample'.format(
                target_annot[target_annot_index])
                ].iloc[line]
            label = df_ann['{}_tag'.format(
                target_annot[target_annot_index])
                ].iloc[line]

            df_ecg.loc[
                (df_ecg['timestamp'] >= start) &
                (df_ecg['timestamp'] < end),
                target_annot[target_annot_index]] = label

    # Cleaning and export

    df_ecg.drop(['timestamp'], axis=1, inplace=True)

    df_ecg = df_ecg.round(0)  # Limiting space taken on disk
    df_ecg['ecg_signal'] = df_ecg['ecg_signal'].astype(int)

    for column in df_ecg.columns[1:]:
        df_ecg = df_ecg[df_ecg[column] != '']

    df_ecg.to_pickle('{}/df_ecg_{}.pkl'.format(output_folder, patient))

    print('correctly exported!')


if __name__ == '__main__':

    ecg_annoted_creation(patient=patient,
                         target_annot=target_annot,
                         sampling_frequency=sampling_frequency,
                         input_data_folder=input_data_folder,
                         output_folder=output_folder)
