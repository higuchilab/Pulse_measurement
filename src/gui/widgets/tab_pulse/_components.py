import tkinter as tk
from tkinter.ttk import Treeview

from ....core.measurement_model import MeasureBlock, MeasureBlocks


class TreeViewBlocks(Treeview):
    """
    測定ブロック一覧を表示
    """
    def __init__(self, master, measure_blocks: MeasureBlocks):
        super().__init__(master=master, columns=("V_top", "top_time", "V_base", "base_time", "loop", "interval"), selectmode="browse", show="headings")
        self.__measure_blocks = measure_blocks.blocks

        self.column("V_top", width=50, minwidth=50)
        self.column("top_time", width=50, minwidth=50)
        self.column("V_base", width=50, minwidth=50)
        self.column("base_time", width=50, minwidth=50)
        self.column("loop", width=50, minwidth=50)
        self.column("interval", width=50, minwidth=50)

        self.heading("V_top", text="V_top", anchor=tk.CENTER)
        self.heading("top_time", text="top_time", anchor=tk.CENTER)
        self.heading("V_base", text="V_base", anchor=tk.CENTER)
        self.heading("base_time", text="base_time", anchor=tk.CENTER)
        self.heading("loop", text="loop", anchor=tk.CENTER)
        self.heading("interval", text="interval", anchor=tk.CENTER)

        self.load_blocks()

    @property
    def measure_blocks(self) -> list[MeasureBlock]:
        return self.__measure_blocks
    
    def load_blocks(self):
        for block in self.measure_blocks:
            self.insert("", "end", text="test2", values=(block.V_top, block.top_time, block.V_base, block.base_time, block.loop, block.interval))

    def add_item(self, *arg):
        self.insert("", "end", text="test2", values=(self.measure_blocks[-1].V_top, self.measure_blocks[-1].top_time, self.measure_blocks[-1].V_base, self.measure_blocks[-1].base_time, self.measure_blocks[-1].loop, self.measure_blocks[-1].interval))

    def del_item(self, *arg):
        self.delete(self.focus())
