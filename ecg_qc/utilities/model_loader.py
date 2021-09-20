from joblib import load
import pickle
import os


def load_model(model: str):
    """From a model path, checks the format and load it accordingly.

    Parameters
    ----------
    model : str
        Path to the model to load

    Returns
    -------
    model :
        Sklearn or XGboost model
    """
    model_name = os.path.basename(model)
    *_, model_extension = model_name.split('.')
    print(model)

    if model_extension == 'joblib':
        ml_model = load(model)

    elif model_extension == 'pkl':
        with open(model, 'rb') as file:
            ml_model = pickle.load(file)

    return ml_model
