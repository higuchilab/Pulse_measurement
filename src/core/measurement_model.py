import numpy as np
from numpy.typing import NDArray
from operator import attrgetter
from typing import List

class MeasureBlock():
    def __init__(self, loop: int, V_top: float, V_base: float, top_time: float, base_time: float, interval: float):     
        self.__loop = loop
        self.__V_top = V_top
        self.__V_base = V_base
        self.__top_time = top_time
        self.__base_time = base_time
        self.__interval = interval

    @property
    def loop(self):
        return self.__loop

    @loop.setter
    def loop(self, value):
        if not isinstance(value, int):
            raise ValueError("loop must be an integer")
        self.__loop = value

    @property
    def V_top(self):
        return self.__V_top

    @V_top.setter
    def V_top(self, value):
        if not isinstance(value, float):
            raise ValueError("V_top must be a float")
        self.__V_top = value

    @property
    def V_base(self):
        return self.__V_base

    @V_base.setter
    def V_base(self, value):
        if not isinstance(value, float):
            raise ValueError("V_base must be a float")
        self.__V_base = value

    @property
    def top_time(self):
        return self.__top_time

    @top_time.setter
    def top_time(self, value):
        if not isinstance(value, float):
            raise ValueError("top_time must be a float")
        self.__top_time = value

    @property
    def base_time(self):
        return self.__base_time

    @base_time.setter
    def base_time(self, value):
        if not isinstance(value, float):
            raise ValueError("base_time must be a float")
        self.__base_time = value

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, value):
        if not isinstance(value, float):
            raise ValueError("interval must be a float")
        self.__interval = value


class Cycle():
    def __init__(self):
        self.__start_index = 0
        self.__stop_index = 0
        self.__loop = 2

    @property
    def start_index(self):
        return self.__start_index

    @start_index.setter
    def start_index(self, value):
        if not isinstance(value, int):
            raise ValueError("start_index must be an integer")
        self.__start_index = value
    
    @property
    def stop_index(self):
        return self.__stop_index

    @stop_index.setter
    def stop_index(self, value):
        if not isinstance(value, int):
            raise ValueError("stop_index must be an integer")
        self.__stop_index = value

    @property
    def loop(self):
        return self.__loop

    @loop.setter
    def loop(self, value):
        if not isinstance(value, int):
            raise ValueError("loop must be an integer")
        
        if value < 2:
            raise ValueError("loop must be more than '1'")
        self.__loop = value


class MeasureBlocks():
    def __init__(self):
        self.__blocks = []
        self.__cycles = []
        self.append_new_block()

    @property
    def blocks(self) -> List[MeasureBlock]:
        return self.__blocks
    
    @blocks.setter
    def blocks(self, value):
        if not isinstance(value, List):
            raise ValueError("blocks must be 'List'")
        self.__blocks = value
    
    @property
    def cycles(self) -> List[Cycle]:
        return self.__cycles
    
    @cycles.setter
    def cycles(self, value):
        if not isinstance(value, List):
            raise ValueError("cycles must be 'List")
        self.__cycles = value

    def append_new_block(self, *arg, loop: int=5, V_top: float=1.0, V_base: float=0.0, top_time: float=10.0, base_time: float=10.0, interval: float=10.0):
        new_block = MeasureBlock(loop, V_top, V_base, top_time, base_time, interval)
        self.__blocks.append(new_block)

    def del_block(self, *arg, index):
        self.__blocks.pop(index)

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


class MeasureModel():
    def __init__(self, blocks: MeasureBlock):
        self.__blocks = blocks
        self.__tick = 0.1

    @property
    def blocks(self) -> MeasureBlocks:
        return self.__blocks
    
    @blocks.setter
    def blocks(self, value):
        self.__blocks = value

    @property
    def tick(self):
        return self.__tick

    @tick.setter
    def tick(self, value):
        if not isinstance(value, float):
            raise ValueError("tick must be a float")
        self.__tick = value

    @property
    def input_V_list(self) -> list:
        return self.__make_measure_list()

    def __make_measure_list(self) -> NDArray:
        def block_measure_list(block: MeasureBlock) -> List[float]:
            v_list = []
            for _ in range(block.loop):
                base = [block.V_base for _ in range(int(block.base_time / self.tick))]
                top = [block.V_top for _ in range(int(block.top_time / self.tick))]
                interval = [block.V_base for _ in range(int(block.interval / self.tick))]
                v_list += base + top + interval
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
                interval=0.0)
