import string
from numpy import ndarray, void
from Source.Plotters.TrajDataHelper import TrajDataHelper
from sklearn.cluster import DBSCAN


class ClusteringHelper(TrajDataHelper):
    eps: float
    samples: int

    def __init__(self, _path: string, _fname: string):
        TrajDataHelper.__init__(self, _path, _fname)

    def DropColumns(self) -> void:
        # Here we decide which columns NOT to use
        self.my_data_frame = self.my_data_frame.drop([self.t0_re, self.t0_im, self.orbit,\
                                                  'rf', 'rf_perp', 'stability', 'guoy'], axis=1)
        # self.myDataFrame = self.myDataFrame.drop([self.orbit,'rf', 'rf_perp', 'stability', 'guoy'], axis=1)

    def RunClustering(self, _eps: float, _samples: int) -> int:
        self.eps = _eps
        self.samples = _samples
        X = self.my_data_frame
        dbscan = DBSCAN(eps=_eps, min_samples=_samples)  # OPTICS performs well too
        y_pred = dbscan.fit_predict(X)
        X[self.orbit] = y_pred
        uniqueElements = self.uniqueElements(y_pred)
        self.my_data_frame = X
        return uniqueElements

    def uniqueElements(self, y_pred: ndarray) -> int:
        unique = []
        for element in y_pred:
            if element not in unique:
                unique.append(element)
        return len(unique)
