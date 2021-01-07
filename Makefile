FOLDER_PATH= .

SRC_PATH=./ecg_qc
TEST_PATH=./tests

generate_datasets_folder:
	mkdir -p $(FOLDER_PATH)/datasets/0_physionet_ecg; \
	mkdir -p $(FOLDER_PATH)/datasets/1_ecg_and_annotation_creation; \
	mkdir -p $(FOLDER_PATH)/datasets/2_dataset_creation; \
	mkdir -p $(FOLDER_PATH)/datasets/3_ml_patients_consolidation; \

download_phyisonet_ecgs:
	$(FOLDER_PATH)/ecg_qc-methodology/0_physionet_ecg/download_phyisonet_ecgs.sh

ecg_and_annotation_creation_batch:
	. $(FOLDER_PATH)/env/bin/activate; \
	$(FOLDER_PATH)/ecg_qc-methodology/1_ecg_and_annotation_creation/ecg_and_annotation_creation_batch.sh

ml_datasets_batch:
	. $(FOLDER_PATH)/env/bin/activate; \
	$(FOLDER_PATH)/ecg_qc-methodology/2_ml_dataset_creation/ml_dataset_creation_batch.sh

test:
	pytest -s -vvv $(TEST_PATH)

test_all:
	python -m pytest 

coverage:
	pytest --cov=$(SRC_PATH) --cov-report html $(TEST_PATH) 