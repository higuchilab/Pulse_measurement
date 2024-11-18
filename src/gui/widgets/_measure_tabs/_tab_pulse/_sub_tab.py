import tkinter as tk
from tkinter import Frame, Label, Button, IntVar, Misc
from tkinter.ttk import Treeview
from typing import Literal

from ._components import TreeViewBlocks
from .._common_item import EntryForm
from .....core import Cycle, MeasureBlocks


class WindowSub(tk.Toplevel):
    def __init__(self, pulse_blocks: MeasureBlocks, master: Misc):
        """サイクルウィンドウを初期化します。"""
        super().__init__(master)
        self.grab_set()
        # self.geometry("300x300")
        self.__pulse_blocks = pulse_blocks
        self.__cycles = pulse_blocks.cycles
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.__main_view = MainViews(master=self, pulse_blocks=self.pulse_blocks)
        self.__main_view.pack(side="top", expand=True, pady=5, padx=10)

        self.__buttons = CycleButtons(master=self, measure_blocks=self.pulse_blocks, treeview=self.main_view.cycle_tree)
        self.__buttons.pack(side="top", expand=True, pady=5)

    @property
    def pulse_blocks(self):
        return self.__pulse_blocks

    @property
    def cycles(self):
        return self.__cycles
    
    @property
    def main_view(self):
        return self.__main_view

    def destroy(self):
        self.master.focus_set()
        super().destroy()
        
    # def on_close(self) -> None:
    #     """ウィンドウを閉じる際の処理を行います。"""
    #     error_list = []
    #     for ins in Cycle.instances:
    #         index_list = [Measure_block.instances.index(block) for block in ins.cycle_contents]
    #         if not sum(index_list) == (len(index_list)-1) * len(index_list) / 2 + index_list[0] * len(index_list):
    #             error_list.append(ins)
    #     if len(error_list) == 0:
    #         CycleLabel.instances = []
    #         CycleLabel.num = 0
    #         BlockLabelSub.instances = []
    #         SpinboxSub.instances = []
    #         super().destroy()
    #     else:
    #         error_txt = ""
    #         for cycle in error_list:
    #             for label in CycleLabel.instances:
    #                 if label.cycle == cycle:
    #                     error_txt = error_txt + label.text.get() + " "
    #         messagebox.showerror("エラー", f"{error_txt}の選択に飛びがあります")


class MainViews(Frame):
    def __init__(self, master, pulse_blocks: MeasureBlocks):
        super().__init__(master=master)
        # ウィジット変数
        self.__start_index = IntVar()
        self.__start_index.trace_add("write", lambda *args: self.update_cycle_param(*args, "start_index"))
        self.__stop_index = IntVar()
        self.__stop_index.trace_add("write", lambda *args: self.update_cycle_param(*args, "stop_index"))
        self.__loop = IntVar()
        self.__loop.trace_add("write", lambda *args: self.update_cycle_param(*args, "loop"))

        self.__pulse_blocks = pulse_blocks
        
        self.__treeview_cycles = TreeViewCycles(master=self, cycles=self.pulse_blocks.cycles)
        self.__treeview_cycles.pack(side="left", expand=True, pady=5)
        self.__treeview_cycles.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.__input_params = InputCycleParameter(master=self, start_index=self.__start_index, stop_index=self.__stop_index, loop=self.__loop)
        self.__input_params.pack(side="left", expand=True, pady=5)

        self.__treeview_blocks = TreeViewBlocks(master=self, measure_blocks=self.pulse_blocks)
        self.__treeview_blocks.pack(side="left", expand=True, pady=5)

    @property
    def start_index(self) -> int:
        return self.__start_index.get()
    
    @start_index.setter
    def start_index(self, value):
        self.__start_index.set(value)

    @property
    def stop_index(self) -> int:
        return self.__stop_index.get()
    
    @stop_index.setter
    def stop_index(self, value):
        self.__stop_index.set(value)

    @property
    def loop(self) -> int:
        return self.__loop.get()
    
    @loop.setter
    def loop(self, value):
        self.__loop.set(value)

    @property
    def pulse_blocks(self) -> MeasureBlocks:
        return self.__pulse_blocks
    
    @property
    def cycles(self) -> Cycle:
        return self.pulse_blocks.cycles

    @property
    def cycle_tree(self):
        return self.__treeview_cycles
    
    def on_tree_select(self, event):
        selected_cycle = self.cycles[self.cycle_tree.index(self.cycle_tree.selection()[0])]
        self.start_index = selected_cycle.start_index
        self.stop_index = selected_cycle.stop_index
        self.loop = selected_cycle.loop

    def update_cycle_param(self, var, index, mode, attr_name: Literal["start_index", "stop_index", "loop"]):
        selected_index = self.cycle_tree.index(self.cycle_tree.selection()[0])
        selected_cycle = self.cycles[selected_index]
        if attr_name == "start_index":
            selected_cycle.start_index = self.start_index

        elif attr_name == "stop_index":
            selected_cycle.stop_index = self.stop_index

        elif attr_name == "loop":
            selected_cycle.loop = self.loop

        self.cycle_tree.item(self.cycle_tree.get_children()[selected_index], values=(selected_cycle.start_index, selected_cycle.stop_index, selected_cycle.loop))



class TreeViewCycles(Treeview):
    """
    サイクル一覧を表示
    """
    def __init__(self, master: Misc, cycles: list[Cycle]):
        super().__init__(master=master, columns=("start_index", "stop_index", "loop"), selectmode="browse", show="headings")
        self.__cycles = cycles

        self.column("start_index", width=80, minwidth=80)
        self.column("stop_index", width=80, minwidth=80)
        self.column("loop", width=40, minwidth=40)

        self.heading("start_index", text="start_index", anchor=tk.CENTER)
        self.heading("stop_index", text="stop_index", anchor=tk.CENTER)
        self.heading("loop", text="loop", anchor=tk.CENTER)

        self.load_cycles()

    @property
    def cycles(self) -> list[Cycle]:
        return self.__cycles
    
    def load_cycles(self):
        for cycle in self.cycles:
            self.insert("", "end", text="test2", values=(cycle.start_index, cycle.stop_index, cycle.loop))

    def add_item(self, *arg):
        self.insert("", "end", text="test2", values=(self.cycles[-1].start_index, self.cycles[-1].stop_index, self.cycles[-1].loop))

    def del_item(self, *arg):
        self.delete(self.focus())


class InputCycleParameter(Frame):
    def __init__(
            self,
            master: Misc,
            start_index: IntVar,
            stop_index: IntVar,
            loop: IntVar
            ):
        super().__init__(master=master)
        self.label = Label(master=self, text="パラメーター")
        self.label.pack(anchor=tk.W, side="top")
        # self.select_from_template_button = Button(master=self, text="テンプレートから選択", cursor='hand1')
        # self.select_from_template_button.pack(anchor=tk.W, side="top", padx=10)

        self.__start_index = EntryForm(label_name="開始", input_width=5, master=self, value=start_index)
        self.__start_index.pack(anchor=tk.W, side="top", padx=10)

        self.__stop_index = EntryForm(label_name="終了 [s]", input_width=5, master=self, value=stop_index)
        self.__stop_index.pack(anchor=tk.W, side="top", padx=10)

        self.__loop = EntryForm(label_name="ループ回数", input_width=5, master=self, value=loop)
        self.__loop.pack(anchor=tk.W, side="top", padx=10)


class CycleButtons(Frame):
    """
    サイクル設定のボタン
    """
    def __init__(self, master, measure_blocks: MeasureBlocks, treeview: TreeViewCycles):
        super().__init__(master=master)
        self.__add_block_button = Button(master=self, text="サイクルを追加", cursor='hand1')
        self.__add_block_button.bind("<Button-1>", measure_blocks.append_new_cycle)
        self.__add_block_button.bind("<Button-1>", treeview.add_item, add='+')
        self.__add_block_button.pack(side="left", padx=2)

        self.__del_block_button = Button(master=self, text="サイクルを削除", cursor='hand1')
        self.__del_block_button.bind("<Button-1>", lambda event: measure_blocks.del_cycle(index=treeview.index(treeview.selection()[0])))
        self.__del_block_button.bind("<Button-1>", treeview.del_item, add='+')
        self.__del_block_button.pack(side="left", padx=2)

        # self.__close_cycle_setting = Button(master=self, text="サイクル設定を終わる", cursor='hand1', command=master.destroy())
        # self.__close_cycle_setting.pack(side="left", padx=2)
