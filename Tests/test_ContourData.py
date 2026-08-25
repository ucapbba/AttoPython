from Source.Plotters.ContourPlot.ContourDataHelper import ContourDataHelper


def test_filepath():
    path = "../../../Data/"
    filename = "Binned_Initial_Condition_Grid_1e+07"
    obj = ContourDataHelper(path=path, filename=filename, x_range=0, y_range=0, min=0, max=0)
    assert obj.get_file_path() == path + filename


# TODO - decrease size of data file to speed up test
def test_createarrays():
    xRange = 750
    yRange = 750
    _min = 0
    _max = 0
    path = "/Data/"
    filename = "Amplitude_Grid_w2_1_1000_phi_0.025_750X750.dat"
    obj = ContourDataHelper(path=path, filename=filename, x_range=xRange, y_range=yRange, min=_min, max=_max)
    obj.load_to_array()
    obj.create_array(7)
    XRESI = obj.x_resi
    YRESI = obj.y_resi
    ZRESI = obj.z_resi
    if not XRESI.any():
        assert False
    if not YRESI.any():
        assert False
    if not ZRESI.any():
        assert False
    assert True
