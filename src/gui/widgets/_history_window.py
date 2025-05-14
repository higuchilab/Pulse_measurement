import tkinter as tk
from tkinter.ttk import Treeview

from sqlalchemy import select
# from ...core.data_processing import ReferHistoryParam

from src.database.session_manager import session_scope
from src.database.models import History
from src.gui.widgets import CommonInputForm

class HistoryWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.pack(fill="both", expand=True, side="right")
        self.form_top = CommonInputForm(self)
        tree_view_history = TreeViewHistory(self)
        tree_view_history.pack()


class TreeViewHistory(Treeview):
    """
    測定履歴を表示
    """
    def __init__(self, master):
        self.columns = ("日時", "測定者", "物質名", "試料", "測定名", "備考")
        super().__init__(master=master, columns=self.columns, selectmode="browse", show="headings")

        for col in self.columns:
            self.heading(col, text=col, anchor=tk.CENTER)
            self.column(col, width=100, minwidth=50)

        self.load_data()
    
    # def load_history(self, param: ReferHistoryParam):
    #     for row in refer_history_table(param):
    #         self.insert("", "end", text="test2", values=row)
    def load_data(self):
        """
        データベースから履歴を取得して表示
        """
        with session_scope() as session:
            # データベースから履歴を取得
            stmt = select(History)
            history_data = session.scalars(stmt).all()
            
            for row in history_data:
                self.insert("", "end", values=row)

