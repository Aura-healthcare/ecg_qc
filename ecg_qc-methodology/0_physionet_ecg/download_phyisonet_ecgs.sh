for PATIENT in 103001 111001 113001 124001
do
	wget -q --show-progress https://physionet.org/files/butqdb/1.0.0/$PATIENT/${PATIENT}_ANN.csv -O datasets/0_physionet_ecg/${PATIENT}_ANN.csv
	wget -q --show-progress https://physionet.org/files/butqdb/1.0.0/$PATIENT/${PATIENT}_ECG.hea -O datasets/0_physionet_ecg/${PATIENT}_ECG.hea
	wget -q --show-progress https://physionet.org/files/butqdb/1.0.0/$PATIENT/${PATIENT}_ECG.dat -O datasets/0_physionet_ecg/${PATIENT}_ECG.dat
done