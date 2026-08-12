import os
from dataclasses import dataclass, field
from numpy import ndarray, loadtxt
from pandas import DataFrame


@dataclass(kw_only=True)
class BaseDataHelper:
    """For importing and manipulating file data"""
    path: str
    filename: str
    my_data_frame: DataFrame = field(init=False, default=None)
    my_array: ndarray = field(init=False, default=None)

    def create_data_frame(self):
        self.my_data_frame = DataFrame(self.my_array)

    def get_data_frame(self):
        return self.my_data_frame

    def get_file_path(self) -> str:
        return self.path + self.filename

    def load_to_array(self) -> None:
        cwd = os.getcwd()
        file_path = self.get_file_path()
        self.my_array = loadtxt(cwd + file_path)

    def truncate_array(self, size: int) -> None:
        self.my_array = self.my_array[:size]

    def get_array(self) -> ndarray:
        return self.my_array
