import os
import string
import math
from numpy import void
from Source.MachineLearning.ARC.AsymDataHelper import AsymDataHelper, Values_Map
from Source.Base.BaseDataHelper import BaseDataHelper
from Source.Base.BasePlotter import BasePlotter
from Source.Plotters.ContourPlot.ContourDataHelper import ContourDataHelper
from typing import List


class AsymCalculator(object):
    helpers: List[ContourDataHelper] = []
    asymList: List[Values_Map] = []

    def __init__(self, _path: string, _jobNum: string, _minTask: int, _maxTask: int,\
                 _xrange: int, _yrange: int, _min: float, _max: float):
        self.path = _path
        self.jobNum = _jobNum
        self.minTask = _minTask
        self.maxTask = _maxTask
        self.xRange = _xrange
        self.yRange = _yrange
        self.min = _min
        self.max = _max

    def CreateContourHelpers(self) -> void:
        filePaths = self.getFilePaths()
        for filepath in filePaths:
            print(" processing file " + filepath.filename)
            contourHelper = ContourDataHelper(path=filepath.path, filename=filepath.filename,\
                                              x_range=self.xRange, y_range=self.yRange,\
                                              min=self.min, max=self.max)
            contourHelper.load_to_array()
            contourHelper.create_array(7)
            # contourHelper.Normalise() leads to 0s due to erroneaous very large numbers
            self.helpers.append(contourHelper)

    def CalculateAsymmetries(self) -> void:
        if len(self.helpers) == 0:
            print("Contour Helpers not populated!!")
            return
        for contourHelper in self.helpers:
            thisasym = self.CalcualteAsymmetry(contourHelper.z_resi)
            helper = AsymDataHelper(contourHelper.path, contourHelper.filename)
            imageValues = helper.GetValuesFromFilename()
            imageValues.asym = thisasym
            self.asymList.append(imageValues)

    def plotColourMeshAsym(self) -> void:
        for value, helper in zip(self.asymList, self.helpers):
            plotter = BasePlotter(helper)
            plotter.PlotColourMesh("w2 = " + str(value.w2) + " Idiff = " + str(value.Idiff)\
                                   + " phi = " + str(value.phi) + " asym = " + str(value.asym))

    def getFilePaths(self) -> List[BaseDataHelper]:
        filePaths = []
        cwd = os.getcwd()
        for task in range(self.minTask, self.maxTask + 1):
            path = self.path + str(self.jobNum) + '.' + str(task) + '/Data/'
            fullPath = cwd + path
            if not os.path.exists(fullPath):
                print('path ' + fullPath + ' does not exisit - moving on....')
                continue
            for fileName in os.listdir(fullPath):
                if os.path.isfile(os.path.join(fullPath, fileName)):
                    helper = AsymDataHelper("", fileName)
                    if helper.IsAmpGrid() is False:
                        continue
                    baseData = BaseDataHelper(path=path, filename=fileName)
                    filePaths.append(baseData)
        return filePaths

    def CalcualteAsymmetry(self, amplitudeValues) -> float:
        rhsSum = 0
        lhsSum = 0
        lineSum = 0
        count = 0
        for amplitudeRow in amplitudeValues:
            count += 1
            if count > self.xRange / 2:
                rhsSum += lineSum
            else:
                lhsSum += lineSum
            lineSum = 0
            for amplitude in amplitudeRow:
                if amplitude == 0:
                    continue
                lineSum += math.log(amplitude)
        asym = rhsSum / lhsSum
        print("asym = " + str(asym))
        return asym
