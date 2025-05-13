import tkinter as tk
from tkinter import Frame, Button, DoubleVar, IntVar, Misc
from typing import Literal

from ._components import TreeViewBlocks
from ._sub_tab import WindowSub
from .._common_item import make_check_buttons, TempletesWindow, ParameterInputsForm, BaseParameterInputs
from .....core import PulseBlockParam, MeasureBlocks
from .....database import append_record_pulse_templetes, refer_pulse_templetes_table


class TabPulse(Frame):
    """
    パルスタブ
    """
    def __init__(self, master):
        super().__init__(master=master)
        self.__pulse_blocks = MeasureBlocks()

        self.variables = {
            "V_top [V]": DoubleVar(),
            "top_time [s]": DoubleVar(),
            "V_base [V]": DoubleVar(),
            "base_time [s]": DoubleVar(),
            "ループ回数": IntVar(),
            "おしり [s]": DoubleVar(),
        }

        self.parameter_inputs = BaseParameterInputs(
            master=self,
            param_names=list(self.variables.keys()),
            variables=list(self.variables.values())
        )
        self.parameter_inputs.pack(anchor=tk.W, expand=True)

        self.__tab_pulse_left = TabPulseLeft(master=self, measure_blocks=self.__pulse_blocks)
        self.__tab_pulse_left.pack(side="left", expand=True, padx=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.__tab_pulse_center = TabPulseCenter(self, self.variables)
        self.__tab_pulse_center.pack(side="left", expand=True, padx=5)

        # self.__tab_pulse_right = TabPulseRight(master=self)
        # self.__tab_pulse_right.pack(anchor=tk.N, side="right", expand=True, padx=5)

    @property
    def tree(self) -> TreeViewBlocks:
        return self.__tab_pulse_left.treeview

    @property
    def pulse_blocks(self) -> MeasureBlocks:
        return self.__pulse_blocks

    @property
    def max_voltage(self) -> float:
        return self.variables["V_top [V]"].get()
    
    @max_voltage.setter
    def max_voltage(self, value: float):
        self.variables["V_top [V]"].set(value)
    
    @property
    def pulse_width(self) -> float:
        return self.variables["top_time [s]"].get()
    
    @pulse_width.setter
    def pulse_width(self, value: float):
        self.variables["top_time [s]"].set(value)

    @property
    def min_voltage(self) -> float:
        return self.variables["V_base [V]"].get()
    
    @min_voltage.setter
    def min_voltage(self, value: float):
        self.variables["V_base [V]"].set(value)

    @property
    def off_width(self) -> float:
        return self.variables["base_time [s]"].get()
    
    @off_width.setter
    def off_width(self, value: float):
        self.variables["base_time [s]"].set(value)

    @property
    def loop_num(self) -> int:
        return self.variables["ループ回数"].get()
    
    @loop_num.setter
    def loop_num(self, value: int):
        self.variables["ループ回数"].set(value)

    @property
    def interval(self) -> float:
        return self.variables["おしり [s]"].get()
    
    @interval.setter
    def interval(self, value: float):
        self.variables["おしり [s]"].set(value)
    
    def on_tree_select(self, event):
        selected_block = self.pulse_blocks.blocks[self.tree.index(self.tree.selection()[0])]
        self.max_voltage = selected_block.V_top
        self.pulse_width = selected_block.top_time
        self.min_voltage = selected_block.V_base
        self.off_width = selected_block.base_time
        self.loop_num = selected_block.loop
        self.interval = selected_block.interval

    def update_block_param(self, var, index, mode, attr_name: Literal["V_top", "top_time", "V_base","base_time", "loop", "interval"]):
        selected_index = self.tree.index(self.tree.selection()[0])
        selected_block = self.pulse_blocks.blocks[selected_index]
        if attr_name == "V_top":
            selected_block.V_top = self.max_voltage

        elif attr_name == "top_time":
            selected_block.top_time = self.pulse_width

        elif attr_name == "V_base":
            selected_block.V_base = self.min_voltage

        elif attr_name == "base_time":
            selected_block.base_time = self.off_width

        elif attr_name == "loop":
            selected_block.loop = self.loop_num

        elif attr_name == "interval":
            selected_block.interval = self.interval

        self.tree.item(self.tree.get_children()[selected_index], values=(selected_block.V_top, selected_block.top_time, selected_block.V_base, selected_block.base_time, selected_block.loop, selected_block.interval))


class TabPulseCenter(Frame):
    """
    パルスタブの中央
    """
    def __init__(self, master: Misc, text_variables: dict):
        super().__init__(master=master)
        self.__parameter_inputs = PulseParameterInputs(self, text_variables)
        self.__parameter_inputs.pack(anchor=tk.W, expand=True)


class PulseTempletesWindow(TempletesWindow):
    """
    パルスブロックの設定値のテンプレートを表示するサブウィンドウ
    """
    def __init__(self, master: Misc, main_window: BaseParameterInputs, columns: list[str]):
        super().__init__(master, main_window, columns)

        rows = refer_pulse_templetes_table()
        for row in rows:
            self.tree.insert("", "end", values=row)


# ParameterInputsFormを継承したクラスを作成し、そこにPulseParameterInputsを渡す
class PulseParameterInputs(ParameterInputsForm):
    """
    パルスブロックの設定値の入力フィールド
    """
    def __init__(self, master: Misc, text_variables: dict):
        super().__init__(master, param_names=list(text_variables.keys()), variables=list(text_variables.values()))
        self.__value_max_voltage = text_variables["V_top [V]"]
        self.__value_pulse_width = text_variables["top_time [s]"]
        self.__value_min_voltage = text_variables["V_base [V]"]
        self.__value_off_width = text_variables["base_time [s]"]
        self.__value_loop_num = text_variables["ループ回数"]
        self.__value_interval = text_variables["おしり [s]"]

    @property
    def top_voltage(self) -> float:
        return self.__value_max_voltage.get()
    
    @top_voltage.setter
    def top_voltage(self, value):
        return self.__value_max_voltage.set(value)
    
    @property
    def pulse_width(self) -> float:
        return self.__value_pulse_width.get()
    
    @pulse_width.setter
    def pulse_width(self, value):
        return self.__value_pulse_width.set(value)
    
    @property
    def base_voltage(self) -> float:
        return self.__value_min_voltage.get()
    
    @base_voltage.setter
    def base_voltage(self, value):
        return self.__value_min_voltage.set(value)
    
    @property
    def off_time(self) -> float:
        return self.__value_off_width.get()
    
    @off_time.setter
    def off_time(self, value):
        return self.__value_off_width.set(value)
    
    @property
    def loop(self) -> int:
        return self.__value_loop_num.get()
    
    @loop.setter
    def loop(self, value):
        return self.__value_loop_num.set(value)
    
    @property
    def interval(self) -> float:
        return self.__value_interval.get()
    
    @interval.setter
    def interval(self, value):
        return self.__value_interval.set(value)
    
    def open_select_templete_window(self):
        PulseTempletesWindow(self, self, self.param_names)

    def recall_templete(self, values):
        self.top_voltage = values[0]
        self.pulse_width = values[1]
        self.base_voltage = values[2]
        self.off_time = values[3]
        self.loop = values[4]
        self.interval = values[5]

    def register_templete(self):
        pulse_block_param = PulseBlockParam(
            top_voltage=self.top_voltage,
            top_time=self.pulse_width,
            base_voltage=self.base_voltage,
            base_time=self.off_time,
            loop=self.loop,
            interval_time=self.interval
            )
        append_record_pulse_templetes(pulse_block_param)
        print("テンプレートに追加しました")


class TabPulseLeft(Frame):
    """
    パルスタブの左側
    """
    def __init__(self, master: Misc, measure_blocks: MeasureBlocks):
        super().__init__(master=master)
        self.__treeview_input_array = TreeViewBlocks(master=self, measure_blocks=measure_blocks)
        self.__treeview_input_array.pack(side="bottom", expand=True, pady=5)
        self.__buttons = TabPulseLeftButtons(master=self, measure_blocks=measure_blocks, treeview=self.treeview)
        self.__buttons.pack(anchor=tk.W, side="top", expand=True, pady=5)

    @property
    def treeview(self):
        return self.__treeview_input_array


class TabPulseLeftButtons(Frame):
    """
    パルスタブ左上のボタン
    """
    def __init__(self, master: Misc, measure_blocks: MeasureBlocks, treeview: TreeViewBlocks):
        super().__init__(master=master)
        self.__add_block_button = Button(master=self, text="ブロックを追加", cursor='hand1')
        self.__add_block_button.bind("<Button-1>", measure_blocks.append_new_block)
        self.__add_block_button.bind("<Button-1>", treeview.load_blocks, add='+')

        self.__add_block_button.pack(side="left", padx=2)
        self.__del_block_button = Button(master=self, text="プロックを削除", cursor='hand1')
        self.__del_block_button.bind("<Button-1>", lambda event: measure_blocks.del_block(index=treeview.index(treeview.selection()[0])))
        self.__del_block_button.bind("<Button-1>", treeview.del_item, add='+')

        self.__del_block_button.pack(side="left", padx=2)
        self.__open_cycle_setting = Button(master=self, text="サイクル設定", cursor='hand1')
        self.__open_cycle_setting.pack(side="left", padx=2)
        self.__open_cycle_setting.bind("<Button-1>", lambda event: self.open_set(measure_blocks=measure_blocks))

    def open_set(self, *arg, measure_blocks):
        WindowSub(pulse_blocks=measure_blocks, master=self)


class TabPulseRight(Frame):
    """
    パルスタブの右側
    """
    def __init__(self, master: Misc):
        super().__init__(master=master)
        make_check_buttons(self)
