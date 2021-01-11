# ECG_QC (Quality Classification)


[![PyPI version](https://badge.fury.io/py/ecg-qc.svg)](https://badge.fury.io/py/ecg-qc)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Downloads](https://pepy.tech/badge/ecg-qc)](https://pepy.tech/project/ecg-qc)

**Website** : https://www.aura.healthcare
**Github** : https://github.com/Aura-healthcare
**Version** : 1.0b3

## Installation / Prerequisites

#### Dependencies

ecg_qc requires:

- Python (>= 3.6)
- biosppy>=0.6.1,
- pathtools>=0.1.2,
- py-ecg-detectors>=1.0.2
- scikit-learn>=0.23.2
- wfdb>=3.1.1
- xgboost>=1.3.1

#### User installation

The easiest way to install hrv-analysis is using ``pip`` :

    $ pip install ecg-qc

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