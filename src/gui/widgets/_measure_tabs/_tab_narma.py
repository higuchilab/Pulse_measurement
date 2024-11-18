import tkinter as tk
from tkinter import StringVar, BooleanVar, IntVar, DoubleVar, Radiobutton, Frame, Label, Button, Entry
from tkinter.ttk import Treeview

from ._common_item import EntryForm, RadioButtonForm

class TabNarma(Frame):
    """
    NARMAタブ

    Attributes
    ----------
    narma_model: str
        使用するNARMAモデル
    pulse_width: float
        パルス入力時間
    off_width: float
        休止時間
    tick: float
        時間分解能
    nodes: int
        仮想ノード数
    base_voltage: float
        基準電圧
    is_use_prepared_input_array: bool
        既にある入力配列を使うかどうか
    discrete_time: int
        離散時間数
    top_voltage: float
        パルス電圧の最大値
    tot_voltage: float
        パルス電圧の最小値
    """
    def __init__(self, master):
        super().__init__(master=master)
        self.tab_narma_left = TabNarmaLeft(master=self)
        self.tab_narma_left.pack(side="left", expand=True, padx=5)

        self.tab_narma_right = TabNarmaRight(master=self)
        self.tab_narma_right.pack(anchor=tk.N, side="right", expand=True, padx=5)

    @property
    def narma_model(self) -> str:
        return self.tab_narma_left.narma_model
    
    @property
    def pulse_width(self) -> float:
        return self.tab_narma_left.pulse_width
    
    @property
    def off_width(self) -> float:
        return self.tab_narma_left.off_width
    
    @property
    def tick(self) -> float:
        return self.tab_narma_left.tick
    
    @property
    def nodes(self) -> int:
        return self.tab_narma_left.nodes
    
    @property
    def base_voltage(self) -> float:
        return self.tab_narma_left.base_voltage
    
    @property
    def is_use_prepared_array(self) -> bool:
        return self.tab_narma_right.is_use_prepared_array
    
    @property
    def discrete_time(self) -> int:
        return self.tab_narma_right.discrete_time
    
    @property
    def top_voltage(self) -> float:
        return self.tab_narma_right.top_voltage
    
    @property
    def bot_voltage(self) -> float:
        return self.tab_narma_right.bot_voltage


class TabNarmaLeft(Frame):
    """
    NARMAタブの左側
    """
    def __init__(self, master):
        super().__init__(master=master)
        self.select_narma_model = SelectNarmaModel(master=self)
        self.select_narma_model.pack(anchor=tk.W, expand=True)

        self.parameter_inputs = ParameterInputs(master=self)
        self.parameter_inputs.pack(anchor=tk.W, expand=True)

    @property
    def narma_model(self) -> str:
        return self.select_narma_model.select_item
    
    @property
    def pulse_width(self) -> float:
        return self.parameter_inputs.pulse_width
    
    @property
    def off_width(self) -> float:
        return self.parameter_inputs.off_width
    
    @property
    def tick(self) -> float:
        return self.parameter_inputs.tick
    
    @property
    def nodes(self) -> int:
        return self.parameter_inputs.nodes
    
    @property
    def base_voltage(self) -> float:
        return self.parameter_inputs.base_voltage


class SelectNarmaModel(RadioButtonForm):
    """
    NARMAモデルの選択
    """
    def __init__(self, master):
        form_name = "モデル"
        values = [
            ("NARMA2", "narma2"),
            ("NARMA10", "narma10")
        ]
        init = "narma2"
        super().__init__(master, form_name, values, init)


class ParameterInputs(Frame):
    """
    NARMA測定に関する必須入力事項
    """
    def __init__(self, master):
        super().__init__(master=master)
        self.label = Label(master=self, text="パラメーター")
        self.label.pack(anchor=tk.W, side="top")
        self.select_from_template_button = Button(master=self, text="テンプレートから選択")
        self.select_from_template_button.pack(anchor=tk.W, side="top", padx=10)

        self._pulse_width = DoubleVar(value=1.0)
        self.input_pulse_width = EntryForm(
            label_name="パルス幅", 
            input_width=5, 
            master=self, 
            value=self._pulse_width)
        self.input_pulse_width.pack(anchor=tk.W, side="top", padx=10)

        self._off_width = DoubleVar(value=1.0)
        self.input_off_width = EntryForm(
            label_name="休止幅", 
            input_width=5, 
            master=self,
            value=self._off_width)
        self.input_off_width.pack(anchor=tk.W, side="top", padx=10)

        self._tick = DoubleVar(value=0.5)
        self.input_tick = EntryForm(
            label_name="tick", 
            input_width=5, 
            master=self,
            value=self._tick)
        self.input_tick.pack(anchor=tk.W, side="top", padx=10)

        self._nodes = IntVar(value=1)
        self.input_nodes = EntryForm(
            label_name="仮想ノード数", 
            input_width=5,
            master=self,
            value=self._nodes)
        self.input_nodes.pack(anchor=tk.W, side="top", padx=10)

        self._base_voltage = DoubleVar(value=0.0)
        self.input_base_voltage = EntryForm(
            label_name="基準電圧", 
            input_width=5,
            master=self,
            value=self._base_voltage)
        self.input_base_voltage.pack(anchor=tk.W, side="top", padx=10)

    @property
    def pulse_width(self) -> float:
        return self._pulse_width.get()
    
    @property
    def off_width(self) -> float:
        return self._off_width.get()
    
    @property
    def tick(self) -> float:
        return self._tick.get()
    
    @property
    def nodes(self) -> int:
        return self._nodes.get()
    
    @property
    def base_voltage(self) -> float:
        return self._base_voltage.get()


class TabNarmaRight(Frame):
    """
    NARMAタブの右側
    """
    def __init__(self, master):
        super().__init__(master=master)
        self._is_use_prepared_array = BooleanVar(value=True)
        self._is_use_prepared_array.trace_add("write", self.__on_change_is_use_prepared_array)
        self.select_input_array = SelectInputArray(master=self, use_input_array=self._is_use_prepared_array)
        self.select_input_array.pack(anchor=tk.W, side="top", expand=True)

        self.parameter_input_array = ParameterInputArray(master=self)
        self.parameter_input_array.pack(anchor=tk.W, side="top", expand=True)

        self.treeview_input_array = TreeViewInputArray(master=self)
        self.treeview_input_array.pack(anchor=tk.W, side="top", expand=True, pady=5)

        self.__on_change_is_use_prepared_array()

    @property
    def is_use_prepared_array(self):
        return self._is_use_prepared_array.get()
    
    @property
    def discrete_time(self) -> int:
        return self.parameter_input_array.discrete_time
    
    @property
    def top_voltage(self) -> float:
        return self.parameter_input_array.top_voltage
    
    @property
    def bot_voltage(self) -> float:
        return self.parameter_input_array.bot_voltage

    def __on_change_is_use_prepared_array(self, *arg):
        self.treeview_input_array.pack_forget()
        self.parameter_input_array.pack_forget()

        if self.is_use_prepared_array:
            self.treeview_input_array.pack(anchor=tk.W, side="top", expand=True)
        else:
            self.parameter_input_array.pack(anchor=tk.W, side="top", expand=True)


class SelectInputArray(Frame):
    """
    入力配列をどうするか
    """
    def __init__(self, master, use_input_array: BooleanVar):
        super().__init__(master=master)
        self.radio_button_use = Radiobutton(master=self, text="既にある入力列を使用", variable=use_input_array, value=True)
        self.radio_button_use.pack(anchor=tk.W, side="top")
        self.radio_button_make = Radiobutton(master=self, text="入力列を新規作成", variable=use_input_array, value=False)
        self.radio_button_make.pack(anchor=tk.W, side="top")


class ParameterInputArray(Frame):
    """
    入力配列を新規作成するときの入力項目
    """
    def __init__(self, master):
        super().__init__(master=master)
        self._discrete_time = IntVar(value=100)
        self.input_discrete_time = EntryForm(
            label_name="離散時間",
            input_width=5,
            master=self,
            value=self._discrete_time)
        self.input_discrete_time.pack(anchor=tk.W, side="top", padx=10)

        self._top_voltage = DoubleVar(value=0.5)
        self.input_top_voltage = EntryForm(
            label_name="電圧上限",
            input_width=5,
            master=self,
            value=self._top_voltage)
        self.input_top_voltage.pack(anchor=tk.W, side="top", padx=10)

        self._bot_voltage = DoubleVar(value=0.1)
        self.input_bot_voltage = EntryForm(
            label_name="電圧下限",
            input_width=5,
            master=self,
            value=self._bot_voltage)
        self.input_bot_voltage.pack(anchor=tk.W, side="top", padx=10)

    @property
    def discrete_time(self) -> int:
        return self._discrete_time.get()
    
    @property
    def top_voltage(self) -> float:
        return self._top_voltage.get()
    
    @property
    def bot_voltage(self) -> float:
        return self._bot_voltage.get()


class TreeViewInputArray(Treeview):
    """
    入力配列を再利用するときの選択肢
    """
    def __init__(self, master):
        super().__init__(master=master, columns=("離散時間", "電圧上限", "電圧下限"), selectmode="browse", show="headings")

        self.column("離散時間", width=50, minwidth=50)
        self.column("電圧上限", width=50, minwidth=50)
        self.column("電圧下限", width=50, minwidth=50)

        self.heading("離散時間", text="離散時間", anchor=tk.CENTER)
        self.heading("電圧上限", text="電圧上限", anchor=tk.CENTER)
        self.heading("電圧下限", text="電圧下限", anchor=tk.CENTER)

        self.insert("", "end", text="test2", values=(1000, 0.5, 0.1))
        self.insert("", "end", text="test1", values=(800, 0.4, 0.2))

