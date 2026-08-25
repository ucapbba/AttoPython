from dataclasses import dataclass, field
from numpy import ndarray, amax
from Source.Base.BaseDataHelper import BaseDataHelper


@dataclass(kw_only=True)
class ContourDataHelper(BaseDataHelper):
    """For importing and manipulating file data in contour plotter"""
    x_range: int
    y_range: int
    min: float
    max: float
    x_resi: ndarray = field(init=False, default=None)
    y_resi: ndarray = field(init=False, default=None)
    z_resi: ndarray = field(init=False, default=None)

    def create_array(self, amp_index: int) -> None:
        data = self.my_array
        if data is None:
            raise ValueError("my_array is empty - call load_to_array() first")
        if data.ndim < 2:
            raise ValueError(f"expected an array with at least 2 dimensions, got {data.ndim}D")
        if not 0 <= amp_index < data.shape[1]:
            raise ValueError(f"amp_index {amp_index} out of range for {data.shape[1]} columns")
        expected_size = self.x_range * self.y_range
        if data.shape[0] != expected_size:
            raise ValueError(
                f"cannot reshape {data.shape[0]} rows into x_range x y_range "
                f"({self.x_range} x {self.y_range} = {expected_size})"
            )
        self.x_resi = data[:, 0].reshape(self.x_range, self.y_range)
        self.y_resi = data[:, 1].reshape(self.x_range, self.y_range)
        self.z_resi = data[:, amp_index].reshape(self.x_range, self.y_range)

    def normalise(self) -> None:
        if self.z_resi is None:
            raise ValueError("z_resi is empty - call create_array() first")
        max_val = amax(self.z_resi)
        if max_val == 0:
            raise ValueError("cannot normalise: max value of z_resi is 0")
        self.z_resi = self.z_resi / max_val
        self.z_resi[self.z_resi < self.min] = 0
