import math
from Source.MachineLearning.ARC.AsymDataHelper import AsymDataHelper
from Source.MachineLearning.ARC.AsymCalculator import AsymCalculator
from Source.Plotters.ContourPlot.ContourDataHelper import ContourDataHelper


def test_GetValuesFromFilename():
    somePath = "somePath"
    filename = "Amplitude_Grid_w2_1_1000_phi_0.025_750X750.dat"
    helper = AsymDataHelper(somePath, filename)
    values = helper.GetValuesFromFilename()
    Idiff = values.Idiff
    w2 = values.w2
    phi = values.phi
    assert w2 == str(1)
    assert Idiff == str(1000)
    assert phi == str(0.025)


def test_IsAmplitudeGrid():
    somePath = "somePath"
    filename = "Amplitude_Grid_w2_1_1000_phi_0.025_750X750.dat"
    helper = AsymDataHelper(somePath, filename)
    assert helper.IsAmpGrid()
    filename = "random_name"
    helper = AsymDataHelper(somePath, filename)
    assert not helper.IsAmpGrid()


def GetPathDetailsForTest():
    path = '/Data/'
    jobNum = 140603
    minTask = 10
    maxTask = 14
    xRange = 750
    yRange = 750
    return path, jobNum, minTask, maxTask, xRange, yRange


def test_GeARCDATAFilePath():
    _min = 10e-5
    _max = 10e-2
    path, jobNum, minTask, maxTask, xRange, yRange = GetPathDetailsForTest()
    helper = AsymCalculator(path, jobNum, minTask, maxTask, xRange, yRange, _min, _max)
    filePaths = helper.getFilePaths()
    assert len(filePaths) == 1
    filePath = filePaths[0].get_file_path()
    thePath = '/Data/140603.10/Data/Amplitude_Grid_w2_1_1000_phi_0.025_750X750.dat'
    assert filePath == thePath


def test_AsymmCalc():
    _min = 10e-5
    _max = 10e-2
    path, jobNum, minTask, maxTask, xRange, yRange = GetPathDetailsForTest()
    helper = AsymCalculator(path, jobNum, minTask, maxTask, xRange, yRange, _min, _max)
    filePaths = helper.getFilePaths()
    filePath = filePaths[0]
    contourHelper = ContourDataHelper(path=filePath.path, filename=filePath.filename, x_range=xRange, y_range=yRange, min=0, max=0)
    contourHelper.load_to_array()
    contourHelper.create_array(7)
    asym = helper.CalcualteAsymmetry(contourHelper.z_resi)
    assert math.isclose(asym, 1.0006104342748006)
