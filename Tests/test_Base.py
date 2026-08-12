from Source.Base.BaseDataHelper import BaseDataHelper


def test_filepath():
    path = "/Data/"
    filename = "Binned_Initial_Condition_Grid_1e+07"
    obj = BaseDataHelper(path=path, filename=filename)
    assert obj.get_file_path() == "/Data/Binned_Initial_Condition_Grid_1e+07"


def test_loadToArray():
    path = "/Data/"
    filename = "Binned_Initial_Condition_Grid_trunc"
    dataHelper = BaseDataHelper(path=path, filename=filename)
    dataHelper.load_to_array()
    myArray = dataHelper.get_array()
    if not myArray.any():
        assert False
    assert True
