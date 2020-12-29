# ECG_QC (Quality Classification)

**Website** : https://www.aura.healthcare

**Github** : https://github.com/Aura-healthcare
**Version** : 1.0b1

## Installation / Prerequisites

#### User installation

The easiest way to install hrv-analysis is using ``pip`` :

    $ pip install ecg-qc==1.0b1

you can also clone the repository:

    $ git clone https://github.com/Aura-healthcare/ecg_qc.git
    $ python setup.py install


## Getting started

### Usage

Import:

```python
from ecg_qc import ecg_qc
```

Class initialization:

```python
ecg_qc = ecg_qc()
```

Default parameters

```python
ecg_qc = ecg_qc(data_encoder='{}/ml/data_encoder/data_encoder.joblib'.format(
                     lib_path),
                 model='{}/ml/models/xgb.joblib'.format(lib_path),
                 sampling_frequency=1000))
```

Predicting the quality of the signal


```python
ecg_data = [1905.72, ... -150.75995323, -134.14559104] # ECG values with same sampling frequency as class declaration

signal_quality = ecg_qc.get_signal_quality(ecg_data)
```

## Authors

**Alexandre CHIROUZE** - (https://github.com/achirouze)
**Alexis COMTE** - (https://github.com/alexisgcomte)
**Laura DUMONT** - (https://github.com/laudmt)

## License

This project is licensed under the *GNU GENERAL PUBLIC License* - see the [LICENSE.md](https://github.com/Aura-healthcare/ecg_qc/blob/main/LICENSE) file for details


## Acknowledgments

to complete