import tkinter as tk
from tkinter import Frame, Label, Button, DoubleVar, IntVar

from .common_item import EntryForm


class TabSweep(Frame):
    """
    スイープタブ
    """
    def __init__(self, master):
        super().__init__(master=master)
        self.tab_narma_left = TabSweepLeft(master=self)
        self.tab_narma_left.pack(side="left", expand=True, padx=5)

        self.tab_narma_right = TabSweepRight(master=self)
        self.tab_narma_right.pack(anchor=tk.N, side="right", expand=True, padx=5)


class TabSweepLeft(Frame):
    """
    スイープタブの左側
    """
    def __init__(self, master):
        super().__init__(master=master)
        parameter_inputs = ParameterInputs(master=self)
        parameter_inputs.pack(anchor=tk.W, expand=True)


class ParameterInputs(Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.label = Label(master=self, text="パラメーター")
        self.label.pack(anchor=tk.W, side="top")
        
        self.__max_voltage = DoubleVar()
        self.__min_voltage = DoubleVar()
        self.__voltage_step = DoubleVar()
        self.__loop_num = IntVar()
        self.__interval = DoubleVar()

        self.select_from_template_button = Button(master=self, text="テンプレートから選択")
        self.select_from_template_button.pack(anchor=tk.W, side="top", padx=10)
        self.__input_max_voltage = EntryForm(label_name="V_top [V]", input_width=5, master=self, value=self.max_voltage)
        self.__input_max_voltage.pack(anchor=tk.W, side="top", padx=10)
        self.__input_min_voltage = EntryForm(label_name="V_bot [V]", input_width=5, master=self, value=self.min_voltage)
        self.__input_min_voltage.pack(anchor=tk.W, side="top", padx=10)
        self.__input_voltage_step = EntryForm(label_name="step [V]", input_width=5, master=self, value=self.voltage_step)
        self.__input_voltage_step.pack(anchor=tk.W, side="top", padx=10)
        self.__input_loop_num = EntryForm(label_name="ループ回数", input_width=5, master=self, value=self.loop_num)
        self.__input_loop_num.pack(anchor=tk.W, side="top", padx=10)
        self.__input_interval = EntryForm(label_name="遅延 [s]", input_width=5, master=self, value=self.interval)
        self.__input_interval.pack(anchor=tk.W, side="top", padx=10)

    @property
    def max_voltage(self):
        return self.__max_voltage
    
    @property
    def min_voltage(self):
        return self.__min_voltage
    
    @property
    def voltage_step(self):
        return self.__voltage_step
    
    @property
    def loop_num(self):
        return self.__loop_num
    
    @property
    def interval(self):
        return self.__interval


class TabSweepRight(Frame):
    """
    スイープタブの右側
    """
    def __init__(self, master):
        super().__init__(master=master)


