FOLDER_PATH= .

generate_datasets_folder:
	. $(FOLDER_PATH)/env/bin/activate; \
	mkdir -p $(FOLDER_PATH)/datasets/0_physionet_ecg; \
	mkdir -p $(FOLDER_PATH)/datasets/1_ecg_and_annotation_creation; \
	mkdir -p $(FOLDER_PATH)/datasets/2_dataset_creation; \
	mkdir -p $(FOLDER_PATH)/datasets/3_ml_patients_consolidation; \

download_phyisonet_ecgs:
	. $(FOLDER_PATH)/env/bin/activate; \
	./ecg_qc-methodology/0_physionet_ecg/download_phyisonet_ecgs.sh

ml_datasets_batch:
	. $(FOLDER_PATH)/env/bin/activate; \
	./ecg_qc-methodology/3_ml_patients_consolidation/ml_dataset_creation_batch.sh 

