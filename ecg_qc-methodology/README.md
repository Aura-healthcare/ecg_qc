# ECG_QC METHODOLOGY


ECG_QC (ECG Quality Classifier) aims at creating a library to detect ECG quality through the computation of SQI (Signal Quality Indexes). To do so, we used physionet library to create a dataset to train a machine learning model.

## I - From Physionet To Machine Learning Model

### Creating Proper Folders

In ecq_qc (root folder):

```
make generate_datasets_folder
```

This create the proper folder structure.

### 0 - Download Raw Patient Data From Physionet

In ecg_qc-methodology/0_physionet_ecg/download_phyisonet_ecgs.sh, add up the target patients line 1. 

Then, in ecq_qc (root folder), use bash command:

```
make download_phyisonet_ecgs
```

This download 3 files by patients: 
- id_ECG.dat and id_ECG.head : the ECG data, with 1000 Hz frequency
- id_ANN.csv: annotations with timestamps of ECG quality change:
    - 1: optimal
    - 2: suspicious
    - 3: unqualified

### 1 - Merge ECG data with annotations

In ecg_qc-methodology/2_ml_dataset_creation/ml_dataset_creation_batch.sh, add up the target patients line 1.

Then, in ecq_qc (root folder), after you create "env" python environnement, use bash command:

```
make ecg_and_annotation_creation_batch
```

If you lack the permission, you can add it with:
```
chmod +x  ./ecg_qc-methodology/1_ecg_and_annotation_creation/ecg_and_annotation_creation_batch.sh
```

This merge the ECG signal data with annotations and output a pickle file.


### 2 - Create ML dataset with SQIs by patient

In ecg_qc-methodology/2_ml_dataset_creation/ml_dataset_creation_batch.sh, add up the target patients line 1.

Then, in ecq_qc (root folder), after you create "env" python environnement, use bash command:

```
make ml_datasets_batch
```

If you lack the permission, add it with:
```
chmod +x  ./ecg_qc-methodology/2_ml_dataset_creation/ml_dataset_creation_batch.sh
```

From the ECG signal and annotation file, the scirpt compute SQIs over a time window (9sec of 1000 hz by default) and output a ML dataset by patient.

For machine learning purpose, the 3 orignal labels are transposed in two:
- 1: optimal (nothing changes)
- 0: suspicious or unqualified, former 2 and 3

From this, we generate two metrics
- classif: value at 1 if all  the values over the time windows are 1, else 0
- classif_avg : the average of the classifications over a time window, ie the percentage of optimal

### 3 - Merge All Patients Datasets

The notebook create the final machine learning models:
- All patients are merged in a same dataset
- A threshold of quality is applied: if classif_avg >= 95%, classif_threshold = 1
- The class by patient is equalized to have balanced classes

Then, the final dataset is exported. You can find an exemple with patients [103001, 111001, 113001, 124001] at:
https://drive.google.com/file/d/1ZzspnXa-jFStvEx7hAzFj3rkSJhnwlt4/view?usp=sharing


### 4 - Machine Learning Training

From the dataset, make a pipeline of machine learning. The highlights:
- Preprocessing: a train/test split of 80% is selected
- 3 algoriths are tested with Grid Search and Cross Validation = 5:
    - Logistic Regression
    - Random Forest Classifier
    - XGBoost (Random Forest + Boosting)
- For Grid Search, target metrics is ROC_AUC.

Best performance is achieved with xgboost.

The models can be exported to:
- feature encoder : data/data_encoder/data_encoder.joblib
- model : data/models/xgb.joblib

## II - Analysis of the results

Best performance is achieved with xgboost.

[correlation matrix]

# Acknowledgments

Nemcova, A., Smisek, R., Opravilová, K., Vitek, M., Smital, L., & Maršánová, L. (2020). Brno University of Technology ECG Quality Database (BUT QDB) (version 1.0.0). PhysioNet. https://doi.org/10.13026/kah4-0w24.