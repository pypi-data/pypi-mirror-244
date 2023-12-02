from .glm import GLMRegressor, GLMClassifier
from .gam import GAMRegressor, GAMClassifier
from .tree import TreeClassifier, TreeRegressor
from .figs import FIGSClassifier, FIGSRegressor
from .xgb1 import XGB1Classifier, XGB1Regressor
from .xgb2 import XGB2Classifier, XGB2Regressor
from .ebm import ExplainableBoostingRegressor, ExplainableBoostingClassifier
from .gaminet import GAMINetClassifier, GAMINetRegressor
from .reludnn import ReluDNNClassifier, ReluDNNRegressor


PIREGRESSOR = {"glm": GLMRegressor,
               "gam": GAMRegressor,
               "tree": TreeRegressor,
               "figs": FIGSRegressor,
               "xgb1": XGB1Regressor,
               "xgb2": XGB2Regressor,
               "ebm": ExplainableBoostingRegressor,
               "gaminet": GAMINetRegressor,
               "reludnn": ReluDNNRegressor}

PICLASSIFIER = {"glm": GLMClassifier,
                "gam": GAMClassifier,
                "tree": TreeClassifier,
                "figs": FIGSClassifier,
                "xgb1": XGB1Classifier,
                "xgb2": XGB2Classifier,
                "ebm": ExplainableBoostingClassifier,
                "gaminet": GAMINetClassifier,
                "reludnn": ReluDNNClassifier}

PIREGRESSOR_name = {key: str(model.__name__) for key, model in PIREGRESSOR.items()}
PICLASSIFIER_name = {key: str(model.__name__) for key, model in PICLASSIFIER.items()}
INTERPRET_MODEL_LIST = list(PIREGRESSOR_name.values()) + list(PICLASSIFIER_name.values())


def get_model_name(estimator):

    if estimator.__class__.__name__ in ["GLMRegressor", "GLMClassifier"]:
        return 'glm'
    elif estimator.__class__.__name__ in ["GAMRegressor", "GAMClassifier"]:
        return 'gam'
    elif estimator.__class__.__name__ in ["TreeRegressor", "TreeClassifier"]:
        return "tree"
    elif estimator.__class__.__name__ in ["XGB2Regressor", "XGB2Classifier"]:
        return "xgb2"
    elif estimator.__class__.__name__ in ["XGB1Regressor", "XGB1Classifier"]:
        return "xgb1"
    elif estimator.__class__.__name__ in ["FIGSRegressor", "FIGSClassifier"]:
        return "figs"
    elif estimator.__class__.__name__ in ["ReluDNNRegressor", "ReluDNNClassifier"]:
        return 'reludnn'
    elif estimator.__class__.__name__ in ["GAMINetRegressor", "GAMINetClassifier"]:
        return 'gaminet'
    elif estimator.__class__.__name__ in ["ExplainableBoostingRegressor", "ExplainableBoostingClassifier"]:
        return "ebm"
    else:
        return 'arbitrary'


__all__ = ['GLMRegressor', 'GLMClassifier',
           'GAMRegressor', 'GAMClassifier',
           'TreeClassifier', 'TreeRegressor',
           'FIGSClassifier', 'FIGSRegressor',
           'XGB1Classifier', 'XGB1Regressor',
           'XGB2Classifier', 'XGB2Regressor',
           'ExplainableBoostingRegressor', 'ExplainableBoostingClassifier',
           'GAMINetClassifier', 'GAMINetRegressor',
           'ReluDNNClassifier', 'ReluDNNRegressor',
           'INTERPRET_MODEL_LIST']


def get_all_supported_models():
    return sorted(__all__)
