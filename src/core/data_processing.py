from dataclasses import dataclass
from typing import Any
from typing_extensions import Literal
from numpy.typing import NDArray
from pydantic import BaseModel
from pydantic.fields import Field

from openpyxl import Workbook, load_workbook

class Datas():
    def __init__(self, time_list: NDArray, current_list: NDArray, voltage_list: NDArray):
        self.__time_list = time_list
        self.__current_list = current_list
        self.__voltage_list = voltage_list

    @property
    def time_list(self):
        return self.__time_list
    
    @property
    def current_list(self):
        return self.__current_list
    
    @property
    def voltage_list(self):
        return self.__voltage_list
    
    def output(self, filepath):
        folderpath = 'C:Users/higuchi/Desktop/パルス測定'
        wb = Workbook()
        wb.save(filepath)
        wb = load_workbook(filepath)
        ws =wb['Sheet']
        ws = wb.active

        for i, (t, voltage, current) in enumerate(zip(self.time_list, self.voltage_list, self.current_list), 1):
            ws.cell(i, 1, t)
            ws.cell(i, 2, voltage)
            ws.cell(i, 3, current)

        wb.save(filepath)
        wb.close()


class CommonParameters(BaseModel):
    operator: str
    material: str
    sample_name: str
    option: str
    file_path: str


@dataclass(frozen=True)
class TwoTerminalOutput:
    voltage: NDArray
    current: NDArray
    time: NDArray


class EchoStateOutput(BaseModel):
    """
    Output data for Echo State Network
    """
    voltage: Any
    current: Any
    time: Any
    descrete_time: Any
    internal_loop: Any
    external_loop: Any


class PulseBlockParam(BaseModel):
    top_voltage: float
    top_time: float
    base_voltage: float
    base_time: float
    loop: int
    interval_time: float


class SweepParam(BaseModel):
    # mode: Literal["one_way", "round_trip", "bidirection"]
    mode: str
    top_voltage: float
    bottom_voltage: float
    voltage_step: float
    loop: int
    tick_time: float


class NarmaParam(BaseModel):
    use_database: bool
    model: str
    pulse_width: float
    off_width: float
    tick: float
    nodes: int
    discrete_time: int
    bot_voltage: float
    top_voltage: float
    base_voltage: float


class HistoryParam(BaseModel):
    user_name: str
    sample_name: str
    measure_type: str
    option: str


class ReferHistoryParam(BaseModel):
    operator: str
    material: str
    sample: str
    measure_type: str