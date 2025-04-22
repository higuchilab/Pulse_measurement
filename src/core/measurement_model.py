import numpy as np
from numpy.typing import NDArray
from operator import attrgetter
from abc import ABCMeta, abstractmethod
from typing import List, TypedDict
from pydantic import BaseModel
from pydantic.fields import Field

from .data_processing import SweepParam, EchoStateParam


class MeasureBlock(BaseModel):
    loop: int = Field(default=5, ge=1)
    V_top: float = Field(default=1.0)
    V_base: float = Field(default=0.0)
    top_time: float = Field(default=10.0, gt=0)
    base_time: float = Field(default=10.0, gt=0)
    interval: float = Field(default=10.0)


class Cycle(BaseModel):
    start_index: int = Field(default=0, ge=0)
    stop_index: int = Field(default=0, gt=0)
    loop: int = Field(default=2, ge=2)

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "start_index": 0,
    #             "stop_index": 0,
    #             "loop": 2
    #         }
    #     }


class MeasureBlocks(BaseModel):
    blocks: List[MeasureBlock] = Field(default_factory=list)
    cycles: List[Cycle] = Field(default_factory=list)

    def append_new_block(
            self,
            *arg,
            loop: int=5, 
            V_top: float=1.0, 
            V_base: float=0.0, 
            top_time: float=10.0, 
            base_time: float=10.0, 
            interval: float=10.0
    ) -> None:
        new_block = MeasureBlock(
            loop=loop, 
            V_top=V_top, 
            V_base=V_base,
            top_time=top_time, 
            base_time=base_time, 
            interval=interval
        )
        self.blocks.append(new_block)

    def change_position_block(self, changed_item_index: int, target_index: int) -> None:
        self.blocks.insert(target_index, self.blocks.pop(changed_item_index))

    def del_block(self, *arg, index):
        self.blocks.pop(index)

    def append_new_cycle(self, *arg):
        new_cycle = Cycle()
        self.cycles.append(new_cycle)

    def del_cycle(self, *arg, index):
        self.cycles.pop(index)

    def export_standarded_blocks(self) -> List[MeasureBlock]:
        def flatten(nested_list):
            result = []
            for item in nested_list:
                if isinstance(item, list):
                    result.extend(flatten(item))  # 再帰的に展開
                else:
                    result.append(item)
            return result
        
        sorted_cycle = sorted(self.cycles, key=lambda cycle:cycle.stop_index, reverse=True)
        standarded_blocks = self.blocks.copy()
        for cycle in sorted_cycle:
            for _ in range(cycle.loop - 1):
                standarded_blocks.insert(cycle.stop_index + 1, self.blocks[cycle.start_index:cycle.stop_index + 1])

        flattened_standarded_blocks = flatten(standarded_blocks)

        return flattened_standarded_blocks


class PulseParameters(TypedDict):
    measure_blocks: MeasureBlocks


class MeasureModelTemplete(metaclass = ABCMeta):
    def __init__(self, tick):
        self.__tick = tick

    @property
    def tick(self) -> float:
        return self.__tick
    
    @tick.setter
    def tick(self, value):
        if not isinstance(value, float):
            raise ValueError("tick must be a float")
        self.__tick = value

    # @property
    @abstractmethod
    def input_V_list(self) -> list:
        pass


class PulseModel(MeasureModelTemplete):
    def __init__(self, blocks: MeasureBlocks):
        super().__init__(tick=0.5)
        self.__blocks = blocks

    @property
    def blocks(self) -> MeasureBlocks:
        return self.__blocks
    
    @blocks.setter
    def blocks(self, value):
        self.__blocks = value

    @property
    def input_V_list(self) -> list[float]:
        return self.__make_measure_list()
    
    def __make_measure_list(self) -> NDArray:
        def block_measure_list(block: MeasureBlock) -> List[float]:
            v_list = []
            for _ in range(block.loop):
                base = [block.V_base for _ in range(int(block.base_time / self.tick))]
                top = [block.V_top for _ in range(int(block.top_time / self.tick))]
                v_list += base + top

            interval = [block.V_base for _ in range(int(block.interval / self.tick))]
            v_list += interval
            return v_list
        
        standarded_block_list = self.blocks.export_standarded_blocks()

        voltage_array = [voltages for block in standarded_block_list for voltages in block_measure_list(block)]
        return voltage_array

        return np.ndarray(voltage_array)

    def make_model_from_narma_input_array(
            self,
            pulse_width: float,
            off_width: float,
            tick: float,
            base_voltage: float,
            input_array: NDArray
        ):
        self.tick = tick
        for voltage in input_array:
            self.blocks.append_new_block(
                loop=1,
                V_top=voltage,
                V_base=base_voltage,
                top_time=pulse_width,
                base_time=off_width,
                interval=0.0
            )
            
    def make_model_from_echostate_input_array(
            self,
            echostate_param: EchoStateParam,
            input_array: NDArray
        ):
        self.tick = echostate_param.tick
        for voltage in input_array:
            self.blocks.append_new_block(
                loop=1,
                V_top=voltage,
                V_base=echostate_param.base_voltage,
                top_time=echostate_param.pulse_width * echostate_param.duty_rate,
                base_time=echostate_param.pulse_width * (1 - echostate_param.duty_rate),
                interval=0.0
            )


class SweepModel(MeasureModelTemplete):
    def __init__(self, sweep_param: SweepParam):
        super().__init__(tick=sweep_param.tick_time)
        self.param = sweep_param

    @property
    def input_V_list(self) -> list:
        if self.param.mode == "one_way":
            return self.__one_way()
        if self.param.mode == "round_trip":
            return self.__round_trip()
        if self.param.mode == "bidirection":
            return self.__bidirection()

        raise ValueError("param.mode must be 'one_way', 'round_trip', 'bidirection'.")

    def __one_way(self) -> list:
        ndarray = np.arange(self.param.bottom_voltage, self.param.top_voltage + self.param.voltage_step, self.param.voltage_step)
        return ndarray.tolist()

    def __round_trip(self):
        ndarray_forth = np.arange(self.param.bottom_voltage, self.param.top_voltage, self.param.voltage_step)
        ndarray_back = np.arange(self.param.top_voltage, self.param.bottom_voltage - self.param.voltage_step, -self.param.voltage_step)
        return ndarray_forth.tolist() + ndarray_back.tolist()

    def __bidirection(self):
        ndarray_go = np.arange(0, self.param.top_voltage, self.param.voltage_step)
        ndarray_back = np.arange(self.param.top_voltage, self.param.bottom_voltage, -self.param.voltage_step)
        ndarray_return = np.arange(self.param.bottom_voltage, self.param.voltage_step, self.param.voltage_step)
        return ndarray_go.tolist() + ndarray_back.tolist() + ndarray_return.tolist()


class EchoStateModel(MeasureModelTemplete):
    def __init__(self, tick: float, external_loop: NDArray):
        super().__init__(tick)
        self.external_loop = external_loop

    @property
    def input_V_list(self) -> list:
        return self.external_loop.tolist()