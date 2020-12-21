# ecg_sqi_private

Patient used:
patient: 103001

Frame intéressant:
57623.665

## I - Streamlit viz helper:


1) Download the dataset
```bash
make download_streamlit_dataset_103001
```

2) Extract for streamlit 

```bash
make install_streamlit_dataset_103001
```

3) Run Streamlit

```bash
make run
```

Works also with:
- 111001
- 113001
- 124001

Next step:
Modify target_id in app.py 

# Preparing dataframe for results
```bash
python ecg_sqi/compute_sqi.py -s 'source picke' -w 'time window' -f 'fs' -o 'output_path'
```

Exemple
```bash
python ecg_sqi/compute_sqi.py -s 'dataset_streamlit/Backup/df_full_ecg_data_merge_124001.pkl' -w 3 -f 1000 -o 'notebooks/results_124001_3s.csv'
```