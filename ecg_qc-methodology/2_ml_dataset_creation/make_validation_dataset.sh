for PATIENT in 103001 
do
	python ./ecg_qc-methodology/2_ml_dataset_creation/ml_dataset_creation.py -patient $PATIENT -normalized False -output_folder datasets/2_dataset_creation_2s -window 2
done
