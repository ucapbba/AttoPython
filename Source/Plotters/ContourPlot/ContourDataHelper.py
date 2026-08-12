from dataclasses import dataclass, field
from numpy import array, ndarray, amax
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

    def create_array(self, amp_index) -> None:
        data = self.my_array
        self.x_resi = data[:, 0].reshape(self.x_range, self.y_range)
        self.y_resi = data[:, 1].reshape(self.x_range, self.y_range)
        self.z_resi = (data[:, amp_index]).reshape(self.x_range, self.y_range)

    def normalise(self) -> None:
        max_val = amax(self.z_resi)
        self.z_resi = [x / max_val for x in self.z_resi]
        self.z_resi = array(self.z_resi)  # array creates an ndarray
        self.z_resi[self.z_resi < self.min] = 0
