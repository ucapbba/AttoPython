from Source.Base.BaseDataHelper import BaseDataHelper


class Values_Map(BaseDataHelper):
    def __init__(self, _path, _fname, _w2, _Idiff, _phi, _asym):
        BaseDataHelper.__init__(self, path=_path, filename=_fname)
        self.w2 = _w2
        self.Idiff = _Idiff
        self.phi = _phi
        self.asym = _asym


class AsymDataHelper(BaseDataHelper):
    def __init__(self, _path, _fname):
        BaseDataHelper.__init__(self, path=_path, filename=_fname)
        self.w2 = 'w2'
        self.Idiff = 'Idiff'
        self.phi = 'phi'
        self.asym = 'asym'

    def AssignColumnNames(self):
        self.my_data_frame.columns = [self.w2, self.Idiff, self.phi, self.asym]

    def GetColumnsToDrop(self) -> list:
        columnsToDrop = []
        columnsToDrop.append(self.asym)
        columnsToDrop.append(self.Idiff)
        columnsToDrop.append(self.phi)
        return columnsToDrop

    def GetTargetColumns(self) -> list:
        targetColumns = []
        targetColumns.append(self.asym)
        return targetColumns

    def GetValuesFromFilename(self):
        fname = self.filename
        index = fname.find("w2")
        w2 = fname[index + 3: index + 4]
        substring = fname[index + 5: 50]
        index = substring.find("_")
        Idiff = substring[0: index]
        index = fname.find("phi")
        substring = fname[index + 4: 50]
        index = substring.find("_")
        phi = substring[0: index]
        return Values_Map(self.path, self.filename, w2, Idiff, phi, 0)

    def IsAmpGrid(self):
        fname = self.filename
        index = fname.find("w2")
        if index == -1:
            return False
        else:
            return True
