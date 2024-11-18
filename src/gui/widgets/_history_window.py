import tkinter as tk
from tkinter.ttk import Treeview

from ...core.data_processing import ReferHistoryParam

from ...core.database import refer_history_table

class HistoryWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.pack(fill="both", expand=True, side="right")
        tree_view_history = TreeViewHistory(self)
        tree_view_history.pack()


class TreeViewHistory(Treeview):
    """
    測定履歴を表示
    """
    def __init__(self, master):
        super().__init__(master=master, columns=("日時", "測定者", "物質名", "試料", "測定名", "備考"), selectmode="browse", show="headings")

        self.column("日時", width=50, minwidth=50)
        self.column("測定者", width=50, minwidth=50)
        self.column("物質名", width=50, minwidth=50)
        self.column("試料", width=50, minwidth=50)
        self.column("測定名", width=50, minwidth=50)
        self.column("備考", width=50, minwidth=50)

        self.heading("日時", text="日時", anchor=tk.CENTER)
        self.heading("測定者", text="測定者", anchor=tk.CENTER)
        self.heading("物質名", text="物質名", anchor=tk.CENTER)
        self.heading("試料", text="試料", anchor=tk.CENTER)
        self.heading("測定名", text="測定名", anchor=tk.CENTER)
        self.heading("備考", text="備考", anchor=tk.CENTER)

        self.load_history(param=ReferHistoryParam)
    
    def load_history(self, param: ReferHistoryParam):
        for row in refer_history_table(param):
            self.insert("", "end", text="test2", values=row)
