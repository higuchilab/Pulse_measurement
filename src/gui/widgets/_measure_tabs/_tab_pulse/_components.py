import tkinter as tk
from tkinter.ttk import Treeview

from .....core import MeasureBlock, MeasureBlocks


class TreeViewBlocks(Treeview):
    """
    測定ブロック一覧を表示
    """
    def __init__(self, master, measure_blocks: MeasureBlocks):
        super().__init__(master=master, columns=("V_top", "top_time", "V_base", "base_time", "loop", "interval"), selectmode="browse", show="headings")
        self.__measure_blocks = measure_blocks
        # self.__measure_blocks = measure_blocks.blocks

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

        self.dragged_item = None

        self.bind("<ButtonPress-1>", self.start_drag)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.end_drag)

    @property
    def measure_blocks(self) -> MeasureBlocks:
        return self.__measure_blocks
    
    def start_drag(self, event):
        # ドラッグ開始位置のアイテムを取得
        item = self.identify_row(event.y)
        if item:
            self.dragged_item = item

    def on_drag(self, event):
        # ドラッグ中の位置をハイライト表示
        item = self.identify_row(event.y)
        if item and item != self.dragged_item:
            self.selection_set(item)

    def end_drag(self, event):
        if not self.dragged_item:
            return

        # ドラッグ先のアイテムを取得
        target_item = self.identify_row(event.y)
        if target_item and target_item != self.dragged_item:
            # 元の位置とターゲット位置を取得
            dragged_index = self.index(self.dragged_item)
            target_index = self.index(target_item)

            # データを再配置
            self.measure_blocks.change_position_block(dragged_index, target_index)

            # Treeviewを更新
            self.load_blocks()

        # ドラッグのリセット
        self.dragged_item = None    
    
    def load_blocks(self, *arg):
        for item in self.get_children():
            self.delete(item)
        for block in self.measure_blocks.blocks:
            self.insert("", "end", text="test2", values=(block.V_top, block.top_time, block.V_base, block.base_time, block.loop, block.interval))

    def del_item(self, *arg):
        self.delete(self.focus())
