from .isolation_forest import IsolationForest
from .cblof import CBLOF
from .pca import PCA
from .kmeanstree import KMeansTree
from .ocsvm import OneClassSVM
from .knn import KNN
from .hbos import HBOS
from .ecod import ECOD

__all__ = ["IsolationForest", "CBLOF", 'PCA', 'KMeansTree',
           "OneClassSVM", 'KNN', "HBOS", 'ECOD', 'PiOD', 'od_name_items']

# od method config
od_name_items = {'if': 'IsolationForest',
                 'cb': 'CBLOF',
                 'pca': 'PCA',
                 'cbtree': 'KMeansTree',
                 'knn': 'KNN',
                 'hbos': 'HBOS',
                 'ocsvm': 'OneClassSVM',
                 'ecod': 'ECOD'}
PiOD = {'if': IsolationForest,
        'cb': CBLOF,
        'pca': PCA,
        'cbtree': KMeansTree,
        'knn': KNN,
        'hbos': HBOS,
        'ocsvm': OneClassSVM,
        'ecod': ECOD}
