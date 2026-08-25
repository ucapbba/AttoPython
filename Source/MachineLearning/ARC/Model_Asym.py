from Source.MachineLearning.ARC.AsymDataHelper import AsymDataHelper
from sklearn.linear_model import SGDClassifier

from Source.MachineLearning.Regression.ModelAnalyser import ModelAnalyser

path = '/Data/job/'
jobNum = 41044
filename = 'varAsymm_' + str(jobNum) + '_.out'
helper = AsymDataHelper(path, filename)
helper.load_to_array()
helper.create_data_frame()
helper.AssignColumnNames()

print("Running Analyser....")
models = [SGDClassifier()]
testSize = 0.25
analyser = ModelAnalyser(helper, models, testSize)
# analyser.CompareModels() Issues on type

# print("Output Results...")
# analyserIO = ModelAnalyserIO(analyser)
# analyserIO.printDataStructureToScreen()
# analyserIO.printModelPerformanceToScreen()
