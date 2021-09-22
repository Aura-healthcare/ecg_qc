from joblib import load
import pickle
import os


file_path = os.path.dirname(__file__)
lib_path = os.path.dirname(file_path)


def load_model(model_file: str):
    """From an included model name or a model path, checks the format (pkl or
    joblib) and loads it accordingly.

    Parameters
    ----------
    model_file : str
        Path to the model to load or included model filename

    Returns
    -------
    model :
        Sklearn or XGboost model
    """
    _model_included = f'{lib_path}/trained_models/{model_file}'

    if os.path.exists(_model_included):
        model_to_load = _model_included
    else:
        model_to_load = model_file

    model_name = os.path.basename(model_to_load)
    *_, model_extension = model_name.split('.')

    if model_extension == 'joblib':
        ml_model = load(model_to_load)

    elif model_extension == 'pkl':
        with open(model_to_load, 'rb') as file:
            ml_model = pickle.load(file)

    return ml_model
