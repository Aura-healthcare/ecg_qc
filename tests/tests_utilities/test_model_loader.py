from ecg_qc.utilities.model_loader import load_model
import sklearn
import xgboost

joblib_model = 'ecg_qc/trained_models/xgb_9s.joblib'
pkl_model = 'ecg_qc/trained_models/rfc_2s.pkl'
pkl_model_short = 'rfc_2s.pkl'


def test_load_joblib(joblib_model: str = joblib_model):

    ml_model = load_model(joblib_model)
    assert isinstance(ml_model, xgboost.sklearn.XGBClassifier)


def test_load_pkl(pkl_model: str = pkl_model):

    ml_model = load_model(pkl_model)
    assert isinstance(ml_model, sklearn.model_selection._search.GridSearchCV)


def test_included_model_loading(pkl_model: str = pkl_model,
                                pkl_model_short: str = pkl_model_short):

    ml_model = load_model(str(pkl_model))
    ml_model_short = load_model(pkl_model_short)
    assert str(ml_model) == str(ml_model_short)
