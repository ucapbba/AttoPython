import os
from Source.MachineLearning.ARC.AsymCalculator import AsymCalculator


class AsymCalculatorIO(AsymCalculator):
    def __init__(self, asymCalc: AsymCalculator):
        self.asymList = asymCalc.asymList
        self.jobNum = asymCalc.jobNum
        self.path = asymCalc.path

    def printToScreen(self):
        for var in self.asymList:
            print("w2 = " + str(var.w2) + " Idiff = " + str(var.Idiff) + " Phi = " + str(var.phi) +\
                  " Asym = " + str(var.asym))

    def printToFile(self):
        print('writing to file')
        cwd = os.getcwd()
        filename = 'varAsymm_' + str(self.jobNum) + '_.out'
        filepath = cwd + self.path + filename
        with open(filepath, 'w') as f:
            for var in self.asymList:
                print(str(var.w2) + ' ' + str(var.Idiff) + ' ' + str(var.phi) + ' ' + str(var.asym), file=f)
