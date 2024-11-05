import tkinter as tk
from tkinter import Frame, Label, Button, DoubleVar, IntVar, Misc
from tkinter.ttk import Treeview
from typing import Literal

from ._components import TreeViewBlocks
from ._sub_tab import WindowSub
from ..common_item import EntryForm, make_check_buttons
from ....core.measurement_model import MeasureBlock, Cycle, MeasureBlocks


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

        self.__tab_pulse_left = TabPulseLeft(master=self, measure_blocks=self.__pulse_blocks)
        self.__tab_pulse_left.pack(side="left", expand=True, padx=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.__tab_pulse_center = TabPulseCenter(
            master=self,
            value_max_voltage=self.__max_voltage,
            value_pulse_width=self.__pulse_width,
            value_min_voltage=self.__min_voltage,
            value_off_width=self.__off_width,
            value_loop_num=self.__loop_num,
            value_interval=self.__interval
            )
        self.__tab_pulse_center.pack(side="left", expand=True, padx=5)

        self.__tab_pulse_right = TabPulseRight(master=self)
        self.__tab_pulse_right.pack(anchor=tk.N, side="right", expand=True, padx=5)

    @property
    def tree(self):
        return self.__tab_pulse_left.treeview

    @property
    def pulse_blocks(self):
        return self.__pulse_blocks

    @property
    def max_voltage(self):
        return self.__max_voltage.get()
    
    @max_voltage.setter
    def max_voltage(self, value):
        self.__max_voltage.set(value)
    
    @property
    def pulse_width(self):
        return self.__pulse_width.get()
    
    @pulse_width.setter
    def pulse_width(self, value):
        self.__pulse_width.set(value)

    @property
    def min_voltage(self):
        return self.__min_voltage.get()
    
    @min_voltage.setter
    def min_voltage(self, value):
        self.__min_voltage.set(value)

    @property
    def off_width(self):
        return self.__off_width.get()
    
    @off_width.setter
    def off_width(self, value):
        self.__off_width.set(value)

    @property
    def loop_num(self):
        return self.__loop_num.get()
    
    @loop_num.setter
    def loop_num(self, value):
        self.__loop_num.set(value)

    @property
    def interval(self):
        return self.__interval.get()
    
    @interval.setter
    def interval(self, value):
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
    def __init__(
            self,
            master,
            value_max_voltage,
            value_pulse_width,
            value_min_voltage,
            value_off_width,
            value_loop_num,
            value_interval
            ):
        super().__init__(master=master)
        self.__parameter_inputs = ParameterInputs(
            master=self,
            value_max_voltage=value_max_voltage,
            value_pulse_width=value_pulse_width,
            value_min_voltage=value_min_voltage,
            value_off_width=value_off_width,
            value_loop_num=value_loop_num,
            value_interval=value_interval
            )
        self.__parameter_inputs.pack(anchor=tk.W, expand=True)


class ParameterInputs(Frame):
    def __init__(
            self,
            master,
            value_max_voltage,
            value_pulse_width,
            value_min_voltage,
            value_off_width,
            value_loop_num,
            value_interval
            ):
        super().__init__(master=master)
        self.label = Label(master=self, text="パラメーター")
        self.label.pack(anchor=tk.W, side="top")
        self.select_from_template_button = Button(master=self, text="テンプレートから選択", cursor='hand1')
        self.select_from_template_button.pack(anchor=tk.W, side="top", padx=10)

        self.__input_max_voltage = EntryForm(label_name="V_top [V]", input_width=5, master=self, value=value_max_voltage)
        self.__input_max_voltage.pack(anchor=tk.W, side="top", padx=10)

        self.__input_pulse_width = EntryForm(label_name="top_time [s]", input_width=5, master=self, value=value_pulse_width)
        self.__input_pulse_width.pack(anchor=tk.W, side="top", padx=10)

        self.__input_min_voltage = EntryForm(label_name="V_bot [V]", input_width=5, master=self, value=value_min_voltage)
        self.__input_min_voltage.pack(anchor=tk.W, side="top", padx=10)

        self.__input_off_width = EntryForm(label_name="bot_time [s]", input_width=5, master=self, value=value_off_width)
        self.__input_off_width.pack(anchor=tk.W, side="top", padx=10)

        self.__input_loop_num = EntryForm(label_name="ループ回数", input_width=5, master=self, value=value_loop_num)
        self.__input_loop_num.pack(anchor=tk.W, side="top", padx=10)

        self.__input_interval = EntryForm(label_name="おしり [s]", input_width=5, master=self, value=value_interval)
        self.__input_interval.pack(anchor=tk.W, side="top", padx=10)


class TabPulseLeft(Frame):
    """
    パルスタブの左側
    """
    def __init__(self, master, measure_blocks: MeasureBlocks):
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
    def __init__(self, master, measure_blocks: MeasureBlocks, treeview: TreeViewBlocks):
        super().__init__(master=master)
        self.__add_block_button = Button(master=self, text="ブロックを追加", cursor='hand1')
        self.__add_block_button.bind("<Button-1>", measure_blocks.append_new_block)
        self.__add_block_button.bind("<Button-1>", treeview.add_item, add='+')

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
    def __init__(self, master):
        super().__init__(master=master)
        make_check_buttons(self)


