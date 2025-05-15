import tkinter as tk
from tkinter.ttk import Treeview
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sqlalchemy import select

from src.database.session_manager import session_scope
from src.database.models import (
    History,
    TwoTerminalResult,
    FourTerminalResult,
    MeasureType,
)
from src.gui.widgets import CommonInputForm
from src.visualization import pulse_graph

class HistoryWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.pack(fill="both", expand=True, side="right")
        self.form_top = CommonInputForm(self)
        self.tree_view_history = TreeViewHistory(self)
        self.tree_view_history.pack()
        self.tree_view_history.bind("<<TreeviewSelect>>", self.on_select)

    def on_select(self, event):
        """
        Treeviewの選択イベント
        選択された行のmeasure_typeから、参照するテーブルを決定、
        選択された行のhistory_idから、テーブルからデータを取得してグラフを表示する
        """
        selected_item = self.tree_view_history.selection()
        if selected_item:
            item = self.tree_view_history.item(selected_item)
            history_id = item["values"][0]
            measure_type_id = item["values"][2]
            print(f"Selected history_id: {history_id}, measure_type_id: {measure_type_id}")
            # 3. measure_type_idから参照するテーブルを決定
            table = self._get_table_by_measure_type(measure_type_id)

            if table:
                # 4. 参照するテーブルからhistory_idに基づいてデータを取得
                with session_scope() as session:
                    stmt = select(table).where(table.history_id == history_id)
                    data = session.scalars(stmt).all()

                # 5. データをグラフに表示
                if data:
                    self._plot_data(data)

    def _get_table_by_measure_type(self, measure_type_id):
        """
        measure_type_idに基づいて参照するテーブルを決定
        """
        with session_scope() as session:
            measure_type = session.query(MeasureType).filter_by(id=measure_type_id).first()
            if measure_type:
                if measure_type.name == "2-terminal Pulse":
                    return TwoTerminalResult
                elif measure_type.name == "4-terminal Pulse":
                    return FourTerminalResult
                # 他の測定タイプに応じたテーブルを追加
        return None

    def _plot_data(self, data):
        """
        データをグラフに表示
        """
        # データを時系列形式に変換してプロット
        times = [row.elapsed_time for row in data]
        voltages = [row.voltage for row in data]
        currents = [row.current for row in data]

        # グラフを表示 (仮にpulse_graphを使用)
        fig, ax = pulse_graph(times, voltages, currents)
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="bottom", fill="both", expand=True)


class TreeViewHistory(Treeview):
    """
    測定履歴を表示
    """
    def __init__(self, master):
        # self.columns = ("日時", "測定者", "物質名", "試料", "測定名", "備考")
        self.columns = ("id", "日時", "測定法", "測定者", "試料", "備考")
        super().__init__(master=master, columns=self.columns, selectmode="browse", show="headings")

        for col in self.columns:
            self.heading(col, text=col, anchor=tk.CENTER)
            self.column(col, width=100, minwidth=50)

        self.load_data()

    def load_data(self):
        """
        データベースから履歴を取得して表示
        """
        with session_scope() as session:
            # データベースから履歴を取得
            stmt = select(History)
            history_data = session.scalars(stmt).all()
            
            for row in history_data:
                self.insert("", "end", values=(row.id, row.created_at, row.measure_type_id, row.user_id, row.sample_id, row.discription))
