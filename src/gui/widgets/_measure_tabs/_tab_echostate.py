from pydantic import BaseModel, Field
import tkinter as tk
from tkinter import Variable, StringVar, BooleanVar, IntVar, DoubleVar, Radiobutton, Frame, Label, Button, Entry
from tkinter.ttk import Treeview
from typing import Literal

from ._common_item import EntryForm, RadioButtonForm
from src.core.data_processing import EchoStateParam


class TabEchoState(Frame):
    """
    echo_stateタブ

    """
    def __init__(self, master):
        super().__init__(master=master)
        self.param = EchoStateParam()
        self.tab_echo_state_left = TabEchoStateLeft(master=self, param=self.param)
        self.tab_echo_state_left.pack(side="left", expand=True, padx=5)

        # self.tab_echo_state_right = TabEchoStateRight(master=self, param=self.param)
        # self.tab_echo_state_right.pack(anchor=tk.N, side="right", expand=True, padx=5)


class TabEchoStateLeft(Frame):
    """
    echo_stateタブの左側
    """
    def __init__(self, master, param: EchoStateParam):
        super().__init__(master=master)
        self.param = param

        self.parameter_inputs = ParameterInputs(master=self, param=self.param)
        self.parameter_inputs.pack(anchor=tk.W, expand=True)


class ParameterInputs(Frame):
    """
    echo_state測定に関する必須入力事項
    """
    def __init__(self, master, param: EchoStateParam):
        super().__init__(master=master)
        self.param = param

        self.label = Label(master=self, text="パラメーター")
        self.label.pack(anchor=tk.W, side="top")
        self.select_from_template_button = Button(master=self, text="テンプレートから選択")
        self.select_from_template_button.pack(anchor=tk.W, side="top", padx=10)

        self.variables = {
            "pulse_width": DoubleVar(value=self.param.pulse_width),
            "duty_rate": DoubleVar(value=self.param.duty_rate),
            "tick": DoubleVar(value=self.param.tick),
            "discrete_time": IntVar(value=self.param.discrete_time),
            "top_voltage": DoubleVar(value=self.param.top_voltage),
            "base_voltage": DoubleVar(value=self.param.base_voltage),
            "inner_loop_idx": IntVar(value=self.param.inner_loop_idx),
            "outer_loop_idx": IntVar(value=self.param.outer_loop_idx),
        }

        self._create_entry(label_name="パルス幅", param_name="pulse_width", input_width=5)
        self._create_entry(label_name="休止幅", param_name="duty_rate", input_width=5)
        self._create_entry(label_name="tick", param_name="tick", input_width=5)
        self._create_entry(label_name="離散時間", param_name="discrete_time", input_width=5)
        self._create_entry(label_name="パルス電圧", param_name="top_voltage", input_width=5)
        self._create_entry(label_name="基準電圧", param_name="base_voltage", input_width=5)
        self._create_entry(label_name="内側のループ", param_name="inner_loop_idx", input_width=5)
        self._create_entry(label_name="外側のループ", param_name="outer_loop_idx", input_width=5)

    def _create_entry(self, label_name: str, param_name: str, input_width: float):
        var: Variable = self.variables[param_name]
        var.trace_add("write", lambda *args, name=param_name: self._update_param(name, var.get()))
        entry = EntryForm(
            label_name=label_name,
            input_width=input_width,
            master=self,
            value=var
        )
        entry.pack(anchor=tk.W, side="top", padx=10)

    def _update_param(self, param_name: str, value):
        """
        Update the parameter value
        """
        try:
            if param_name in self.variables:
                try:
                    setattr(self.param, param_name, value)
                except TypeError as e:
                    print(f"Invalid type for {param_name}: {value}")
                    raise e
                except Exception as e:
                    raise e
                
            else:
                raise ValueError(f"Invalid parameter name: {param_name}")
        except Exception as e:
            print(f"Error updating parameter {param_name}: {e}")


# class TabEchoStateRight(Frame):
#     """
#     echo_stateタブの右側
#     """
#     def __init__(self, master, param: EchoStateParam):
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
