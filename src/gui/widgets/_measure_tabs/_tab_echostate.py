from pydantic import BaseModel, Field
import tkinter as tk
from tkinter import StringVar, BooleanVar, IntVar, DoubleVar, Radiobutton, Frame, Label, Button, Entry
from tkinter.ttk import Treeview

from ._common_item import EntryForm, RadioButtonForm
from src.core.data_processing import EchoStateParam

# class EchoStateParam(BaseModel):
#     """
#     echo_state測定に関する必須入力事項
#     """
#     pulse_width: float = Field(default=1.0, gt=0., description="パルス幅")
#     duty_rate: float = Field(default=0.5, gt=0., lt=1, description="デューティ比")
#     tick: float = Field(default=0., gt=0., description="時間分解能")
#     base_voltage: float = Field(default=0., gt=-30., lt=30., description="基準電圧")
#     top_voltage: float = Field(default=0.5, gt=-30., lt=30., description="パルス電圧値")
#     inner_loop_num: int = Field(default=1, gt=0, description="内側のループ数")
#     outer_loop_num: int = Field(default=1, gt=0, description="外側のループ数")


class TabEchoState(Frame):
    """
    echo_stateタブ

    """
    def __init__(self, master):
        super().__init__(master=master)
        self.config = EchoStateParam()
        self.tab_echo_state_left = TabEchoStateLeft(master=self, config=self.config)
        self.tab_echo_state_left.pack(side="left", expand=True, padx=5)

        # self.tab_echo_state_right = TabEchoStateRight(master=self, config=self.config)
        # self.tab_echo_state_right.pack(anchor=tk.N, side="right", expand=True, padx=5)


class TabEchoStateLeft(Frame):
    """
    echo_stateタブの左側
    """
    def __init__(self, master, config: EchoStateParam):
        super().__init__(master=master)
        self.config = config

        self.parameter_inputs = ParameterInputs(master=self, config=self.config)
        self.parameter_inputs.pack(anchor=tk.W, expand=True)


class ParameterInputs(Frame):
    """
    echo_state測定に関する必須入力事項
    """
    def __init__(self, master, config: EchoStateParam):
        super().__init__(master=master)
        self.config = config

        self.label = Label(master=self, text="パラメーター")
        self.label.pack(anchor=tk.W, side="top")
        self.select_from_template_button = Button(master=self, text="テンプレートから選択")
        self.select_from_template_button.pack(anchor=tk.W, side="top", padx=10)

        self._pulse_width = DoubleVar(value=self.config.pulse_width)
        self.input_pulse_width = EntryForm(
            label_name="パルス幅",
            input_width=5, 
            master=self, 
            value=self._pulse_width
        )
        self.input_pulse_width.pack(anchor=tk.W, side="top", padx=10)

        self._duty_rate = DoubleVar(value=self.config.duty_rate)
        self.input_off_width = EntryForm(
            label_name="休止幅", 
            input_width=5, 
            master=self,
            value=self._duty_rate
        )
        self.input_off_width.pack(anchor=tk.W, side="top", padx=10)

        self._tick = DoubleVar(value=self.config.tick)
        self.input_tick = EntryForm(
            label_name="tick", 
            input_width=5, 
            master=self,
            value=self._tick
        )
        self.input_tick.pack(anchor=tk.W, side="top", padx=10)

        self._discrete_time = IntVar(value=self.config.discrete_time)
        self.input_discrete_time = EntryForm(
            label_name="離散時間",
            input_width=5,
            master=self,
            value=self._discrete_time,
        )
        self.input_discrete_time.pack(anchor=tk.W, side="top", padx=10)

        self._base_voltage = DoubleVar(value=self.config.base_voltage)
        self.input_base_voltage = EntryForm(
            label_name="基準電圧",
            input_width=5,
            master=self,
            value=self._base_voltage
        )
        self.input_base_voltage.pack(anchor=tk.W, side="top", padx=10)

        self._top_voltage = DoubleVar(value=self.config.top_voltage)
        self.input_top_voltage = EntryForm(
            label_name="パルス電圧", input_width=5, master=self, value=self._top_voltage
        )
        self.input_base_voltage.pack(anchor=tk.W, side="top", padx=10)

        self._inner_loop_num = IntVar(value=self.config.inner_loop_num)
        self.input_inner_loop_num = EntryForm(
            label_name="内側のループ", input_width=5, master=self, value=self._inner_loop_num
        )
        self.input_inner_loop_num.pack(anchor=tk.W, side="top", padx=10)

        self._outer_loop_num = IntVar(value=self.config.outer_loop_num)
        self.input_outer_loop_num = EntryForm(
            label_name="外側のループ",
            input_width=5,
            master=self,
            value=self._outer_loop_num,
        )
        self.input_outer_loop_num.pack(anchor=tk.W, side="top", padx=10)


# class TabEchoStateRight(Frame):
#     """
#     echo_stateタブの右側
#     """
#     def __init__(self, master, config: EchoStateParam):
#         super().__init__(master=master)
#         self._is_use_prepared_array = BooleanVar(value=True)
#         self._is_use_prepared_array.trace_add("write", self.__on_change_is_use_prepared_array)
#         self.select_input_array = SelectInputArray(master=self, use_input_array=self._is_use_prepared_array)
#         self.select_input_array.pack(anchor=tk.W, side="top", expand=True)

#         self.parameter_input_array = ParameterInputArray(master=self)
#         self.parameter_input_array.pack(anchor=tk.W, side="top", expand=True)

#         self.treeview_input_array = TreeViewInputArray(master=self)
#         self.treeview_input_array.pack(anchor=tk.W, side="top", expand=True, pady=5)

#         self.__on_change_is_use_prepared_array()

#     @property
#     def is_use_prepared_array(self):
#         return self._is_use_prepared_array.get()

#     @property
#     def discrete_time(self) -> int:
#         return self.parameter_input_array.discrete_time

#     @property
#     def top_voltage(self) -> float:
#         return self.parameter_input_array.top_voltage

#     @property
#     def bot_voltage(self) -> float:
#         return self.parameter_input_array.bot_voltage

#     def __on_change_is_use_prepared_array(self, *arg):
#         self.treeview_input_array.pack_forget()
#         self.parameter_input_array.pack_forget()

#         if self.is_use_prepared_array:
#             self.treeview_input_array.pack(anchor=tk.W, side="top", expand=True)
#         else:
#             self.parameter_input_array.pack(anchor=tk.W, side="top", expand=True)


# class SelectInputArray(Frame):
#     """
#     入力配列をどうするか
#     """
#     def __init__(self, master, use_input_array: BooleanVar):
#         super().__init__(master=master)
#         self.radio_button_use = Radiobutton(master=self, text="既にある入力列を使用", variable=use_input_array, value=True)
#         self.radio_button_use.pack(anchor=tk.W, side="top")
#         self.radio_button_make = Radiobutton(master=self, text="入力列を新規作成", variable=use_input_array, value=False)
#         self.radio_button_make.pack(anchor=tk.W, side="top")


# class ParameterInputArray(Frame):
#     """
#     入力配列を新規作成するときの入力項目
#     """
#     def __init__(self, master):
#         super().__init__(master=master)
#         self._discrete_time = IntVar(value=100)
#         self.input_discrete_time = EntryForm(
#             label_name="離散時間",
#             input_width=5,
#             master=self,
#             value=self._discrete_time)
#         self.input_discrete_time.pack(anchor=tk.W, side="top", padx=10)

#         self._top_voltage = DoubleVar(value=0.5)
#         self.input_top_voltage = EntryForm(
#             label_name="電圧上限",
#             input_width=5,
#             master=self,
#             value=self._top_voltage)
#         self.input_top_voltage.pack(anchor=tk.W, side="top", padx=10)

#         self._bot_voltage = DoubleVar(value=0.1)
#         self.input_bot_voltage = EntryForm(
#             label_name="電圧下限",
#             input_width=5,
#             master=self,
#             value=self._bot_voltage)
#         self.input_bot_voltage.pack(anchor=tk.W, side="top", padx=10)

#     @property
#     def discrete_time(self) -> int:
#         return self._discrete_time.get()

#     @property
#     def top_voltage(self) -> float:
#         return self._top_voltage.get()

#     @property
#     def bot_voltage(self) -> float:
#         return self._bot_voltage.get()


# class TreeViewInputArray(Treeview):
#     """
#     入力配列を再利用するときの選択肢
#     """
#     def __init__(self, master):
#         super().__init__(master=master, columns=("離散時間", "電圧上限", "電圧下限"), selectmode="browse", show="headings")

#         self.column("離散時間", width=50, minwidth=50)
#         self.column("電圧上限", width=50, minwidth=50)
#         self.column("電圧下限", width=50, minwidth=50)

#         self.heading("離散時間", text="離散時間", anchor=tk.CENTER)
#         self.heading("電圧上限", text="電圧上限", anchor=tk.CENTER)
#         self.heading("電圧下限", text="電圧下限", anchor=tk.CENTER)

#         self.insert("", "end", text="test2", values=(1000, 0.5, 0.1))
#         self.insert("", "end", text="test1", values=(800, 0.4, 0.2))
