from Source.Plotters.TrajDataHelper import TrajDataHelper
from sklearn import metrics
from sklearn.model_selection import train_test_split
import numpy as np


class ModelAnalyser(object):

    def __init__(self, _helper: TrajDataHelper, models: list, _testSize: float):
        self.helper = _helper
        self.models = models
        self.modelKeys = map(lambda model: str(model).replace('()', ''), models)
        self.modelsDict = dict.fromkeys(self.modelKeys, [])
        self.testSize = _testSize

    def CreateStatsDict(self, y_test, test_preds):
        stats = ['precision', 'accuracy', 'sensitivity', 'specificity']
        statsDict = dict.fromkeys(stats)
        cnf_matrix = metrics.confusion_matrix(y_test, test_preds)
        statsDict['precision'] = metrics.precision_score(y_test, test_preds, average='macro')
        statsDict['accuracy'] = metrics.accuracy_score(y_test, test_preds)
        statsDict['sensitivity'] = metrics.recall_score(y_test, test_preds, average='macro')
        statsDict['specificity'] = cnf_matrix[0][0] / (cnf_matrix[0][0] + cnf_matrix[0][1])
        return statsDict

    def CreateTestTrain(self):
        df = self.helper.get_data_frame()
        y = df[self.helper.GetTargetColumns()]
        X = df.drop(self.helper.GetColumnsToDrop(), axis=1)
        return train_test_split(X, y, test_size=self.testSize, random_state=4)

    def CalculateModelStats(self, model):
        X_train, X_test, y_train, y_test = self.CreateTestTrain()
        model.fit(X_train, y_train)
        test_preds = model.predict(X_test)
        test_preds = np.array([int(i) for i in test_preds])
        return self.CreateStatsDict(y_test, test_preds)

    def CompareModels(self):
        for model, modelKey in zip(self.models, self.modelsDict):
            statsDict = self.CalculateModelStats(model)
            self.modelsDict[modelKey] = statsDict
