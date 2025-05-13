import tkinter as tk
from tkinter import Frame, Button, DoubleVar, IntVar, Misc
from typing import Literal

from ._components import TreeViewBlocks
from ._sub_tab import WindowSub
from .._common_item import make_check_buttons, ParameterInputsForm, TextVariables, TempletesWindow
from .....core import PulseBlockParam, MeasureBlocks
from .....database import append_record_pulse_templetes, refer_pulse_templetes_table


class TabPulse(Frame):
    """
    パルスタブ
    """
    def __init__(self, master):
        super().__init__(master=master)
        self.__pulse_blocks = MeasureBlocks()

        self.__max_voltage = DoubleVar()
        self.__max_voltage.trace_add("write", lambda *args: self.update_block_param(*args, "V_top"))
        self.__pulse_width = DoubleVar()
        self.__pulse_width.trace_add("write", lambda *args: self.update_block_param(*args, "top_time"))
        self.__min_voltage = DoubleVar()
        self.__min_voltage.trace_add("write", lambda *args: self.update_block_param(*args, "V_base"))
        self.__off_width = DoubleVar()
        self.__off_width.trace_add("write", lambda *args: self.update_block_param(*args, "base_time"))
        self.__loop_num = IntVar()
        self.__loop_num.trace_add("write", lambda *args: self.update_block_param(*args, "loop"))
        self.__interval = DoubleVar()
        self.__interval.trace_add("write", lambda *args: self.update_block_param(*args, "interval"))

        param_names = [
            "V_top [V]",
            "top_time [s]",
            "V_bot [V]",
            "bot_time [s]",
            "ループ回数",
            "おしり [s]"
            ]
        variables = [
            self.__max_voltage,
            self.__pulse_width,
            self.__min_voltage,
            self.__off_width,
            self.__loop_num,
            self.__interval
        ]
        text_variables = TextVariables(param_names=param_names, variables=variables)

        self.__tab_pulse_left = TabPulseLeft(master=self, measure_blocks=self.__pulse_blocks)
        self.__tab_pulse_left.pack(side="left", expand=True, padx=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.__tab_pulse_center = TabPulseCenter(self, text_variables)
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
        return self.__max_voltage.get()
    
    @max_voltage.setter
    def max_voltage(self, value: float):
        self.__max_voltage.set(value)
    
    @property
    def pulse_width(self) -> float:
        return self.__pulse_width.get()
    
    @pulse_width.setter
    def pulse_width(self, value: float):
        self.__pulse_width.set(value)

    @property
    def min_voltage(self) -> float:
        return self.__min_voltage.get()
    
    @min_voltage.setter
    def min_voltage(self, value: float):
        self.__min_voltage.set(value)

    @property
    def off_width(self) -> float:
        return self.__off_width.get()
    
    @off_width.setter
    def off_width(self, value: float):
        self.__off_width.set(value)

    @property
    def loop_num(self) -> int:
        return self.__loop_num.get()
    
    @loop_num.setter
    def loop_num(self, value: int):
        self.__loop_num.set(value)

    @property
    def interval(self) -> float:
        return self.__interval.get()
    
    @interval.setter
    def interval(self, value: float):
        self.__interval.set(value)
    
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
    def __init__(self, master: Misc, text_variables: TextVariables):
        super().__init__(master=master)
        self.__parameter_inputs = PulseParameterInputs(self, text_variables)
        self.__parameter_inputs.pack(anchor=tk.W, expand=True)


class PulseTempletesWindow(TempletesWindow):
    """
    パルスブロックの設定値のテンプレートを表示するサブウィンドウ
    """
    def __init__(self, master: Misc, main_window: ParameterInputsForm, columns: list[str]):
        super().__init__(master, main_window, columns)

        rows = refer_pulse_templetes_table()
        for row in rows:
            self.tree.insert("", "end", values=row)


class PulseParameterInputs(ParameterInputsForm):
    """
    パルスブロックの設定値の入力フィールド
    """
    def __init__(self, master: Misc, text_variables: TextVariables):
        super().__init__(master, text_variables)
        self.__value_max_voltage = text_variables.variables[0]
        self.__value_pulse_width = text_variables.variables[1]
        self.__value_min_voltage = text_variables.variables[2]
        self.__value_off_width = text_variables.variables[3]
        self.__value_loop_num = text_variables.variables[4]
        self.__value_interval = text_variables.variables[5]

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


