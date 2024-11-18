import tkinter as tk
from tkinter import Frame, DoubleVar, IntVar, Misc
from typing import Literal

from ._common_item import ParameterInputsForm, TempletesWindow, TextVariables, RadioButtonForm
from ....core import SweepParam
from ....core.database import append_record_sweep_templetes, refer_sweep_templetes_table


class TabSweep(Frame):
    """
    スイープタブ
    """
    def __init__(self, master):
        super().__init__(master=master)
        self.tab_sweep_left = TabSweepLeft(master=self)
        self.tab_sweep_left.pack(side="left", expand=True, padx=5)

        self.tab_sweep_right = TabSweepRight(master=self)
        self.tab_sweep_right.pack(anchor=tk.N, side="right", expand=True, padx=5)

    @property
    def sweep_mode(self) -> Literal["one_way", "round_trip", "bidirection"]:
        return self.tab_sweep_left.sweep_mode
    
    @property
    def top_voltage(self) -> float:
        return self.tab_sweep_left.top_voltage
    
    @property
    def bottom_voltage(self) -> float:
        return self.tab_sweep_left.bottom_voltage
    
    @property
    def voltage_step(self) -> float:
        return self.tab_sweep_left.voltage_step
    
    @property
    def loop(self) -> int:
        return self.tab_sweep_left.loop
    
    @property
    def tick(self) -> float:
        return self.tab_sweep_left.tick


class SelectSweepMode(RadioButtonForm):
    """
    スイープモードの選択
    """
    def __init__(self, master):
        form_name = "スイープモード"
        values = [
            ("片道スイープ", "one_way"),
            ("往復スイープ", "round_trip"),
            ("双方向スイープ", "bidirection")
        ]
        init = "one_way"
        super().__init__(master, form_name, values, init)


class TabSweepLeft(Frame):
    """
    スイープタブの左側
    """
    def __init__(self, master):
        super().__init__(master=master)

        self.__select_sweep_mode = SelectSweepMode(self)
        self.__select_sweep_mode.pack(side="left", expand=True, padx=5)

        self.__top_voltage = DoubleVar()
        self.__bottom_voltage = DoubleVar()
        self.__voltage_step = DoubleVar()
        self.__loop_num = IntVar()
        self.__tick = DoubleVar()
        
        param_names = [
            "V_top [V]",
            "V_bot [V]",
            "V_step [V]",
            "ループ回数",
            "tick [s]"
            ]
        variables = [
            self.__top_voltage,
            self.__bottom_voltage,
            self.__voltage_step,
            self.__loop_num,
            self.__tick
        ]
        text_variables = TextVariables(param_names=param_names, variables=variables)

        parameter_inputs = SweepParameterInputs(self, text_variables)
        parameter_inputs.pack(anchor=tk.W, expand=True)

    @property
    def sweep_mode(self) -> Literal["one_way", "round_trip", "bidirection"]:
        return self.__select_sweep_mode.select_item
    
    @property
    def top_voltage(self) -> float:
        return self.__top_voltage.get()
    
    @property
    def bottom_voltage(self) -> float:
        return self.__bottom_voltage.get()
    
    @property
    def voltage_step(self) -> float:
        return self.__voltage_step.get()
    
    @property
    def loop(self) -> int:
        return self.__loop_num.get()
    
    @property
    def tick(self) -> float:
        return self.__tick.get()


class SweepTempletesWindow(TempletesWindow):
    def __init__(self, master: Misc, main_window: ParameterInputsForm, columns: list[str]):
        super().__init__(master, main_window, columns)

        rows = refer_sweep_templetes_table()
        for row in rows:
            self.tree.insert("", "end", values=row)


class SweepParameterInputs(ParameterInputsForm):
    def __init__(self, master: Misc, text_variables: TextVariables):
        super().__init__(master, text_variables)
        self.__value_max_voltage = text_variables.variables[0]
        self.__value_bottom_voltage = text_variables.variables[1]
        self.__value_voltage_step = text_variables.variables[2]
        self.__value_loop_num = text_variables.variables[3]
        self.__value_tick = text_variables.variables[4]

    @property
    def top_voltage(self) -> float:
        return self.__value_max_voltage.get()
    
    @top_voltage.setter
    def top_voltage(self, value):
        return self.__value_max_voltage.set(value)
    
    @property
    def bottom_voltage(self) -> float:
        return self.__value_bottom_voltage.get()
    
    @bottom_voltage.setter
    def bottom_voltage(self, value):
        return self.__value_bottom_voltage.set(value)
    
    @property
    def voltage_step(self) -> float:
        return self.__value_voltage_step.get()
    
    @voltage_step.setter
    def voltage_step(self, value) -> float:
        return self.__value_voltage_step.set(value)
        
    @property
    def loop(self) -> int:
        return self.__value_loop_num.get()
    
    @loop.setter
    def loop(self, value):
        return self.__value_loop_num.set(value)
    
    @property
    def tick_time(self) -> float:
        return self.__value_tick.get()
    
    @tick_time.setter
    def tick_time(self, value):
        return self.__value_tick.set(value)
    
    def open_select_templete_window(self):
        SweepTempletesWindow(self, self, self.param_names)

    def recall_templete(self, values):
        self.top_voltage = values[0]
        self.bottom_voltage = values[1]
        self.voltage_step = values[2]
        self.loop = values[3]
        self.tick_time = values[4]

    def register_templete(self):
        sweep_param = SweepParam(
            mode="one_way",
            top_voltage=self.top_voltage,
            bottom_voltage=self.bottom_voltage,
            voltage_step=self.voltage_step,
            loop=self.loop,
            tick_time=self.tick_time
            )
        append_record_sweep_templetes(sweep_param)
        print("テンプレートに追加しました")


class TabSweepRight(Frame):
    """
    スイープタブの右側
    """
    def __init__(self, master):
        super().__init__(master=master)


