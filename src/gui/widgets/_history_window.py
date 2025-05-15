import tkinter as tk
from tkinter.ttk import Treeview
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Union, List
import uuid

from src.database.session_manager import session_scope
from src.database.models import (
    History,
    TwoTerminalResult,
    FourTerminalResult,
    MeasureType,
    Sample
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
            history_id = uuid.UUID(item["values"][0])
            measure_type = item["values"][2]

            # 3. measure_type_idから参照するテーブルを決定
            table = self._get_table_by_measure_type(measure_type)

            if table:
                # 4. 参照するテーブルからhistory_idに基づいてデータを取得
                with session_scope() as session:
                    stmt = select(table).where(table.history_id == history_id)
                    data = session.scalars(stmt).all()

                    # 5. データをグラフに表示 (TwoTerminalResultの場合のみ)
                    if isinstance(data, list) and data and isinstance(data[0], TwoTerminalResult):
                        self._plot_data(data)

    def _get_table_by_measure_type(self, measure_type: str) -> Union[type, None]:
        """
        measure_typeに基づいて参照するテーブルを決定
        """
        table_mapping = {
            "2-terminal Pulse": TwoTerminalResult,
            "4-terminal Pulse": FourTerminalResult,
            # 他の測定タイプを追加可能
        }
        return table_mapping.get(measure_type)

    def _plot_data(self, data: List[TwoTerminalResult]):
        """
        TwoTerminalResultのデータをグラフに表示
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
        self.columns = (
            "id",
            "日時",
            "測定法",
            "測定者",
            "物質名",
            "試料",
            "備考"
        )
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
            # Historyテーブルを関連テーブルと内部結合してデータを取得
            stmt = (
                select(History)
                .options(
                    joinedload(History.measure_type),  # MeasureTypeテーブルをロード
                    joinedload(History.user),         # Userテーブルをロード
                    joinedload(History.sample).joinedload(Sample.material),       # SampleとMaterialテーブルをロード
                )
            )
            history_data = session.scalars(stmt).all()

            for row in history_data:
                # 外部キーの名前を取得
                measure_type_name = row.measure_type.name if row.measure_type else "不明"
                user_name = row.user.name if row.user else "不明"
                if row.sample:
                    sample_name = row.sample.name
                    material_name = row.sample.material.name if row.sample.material else "不明"
                else:
                    sample_name = "不明"
                    material_name = "不明"

                # TreeViewにデータを挿入
                self.insert(
                    "",
                    "end",
                    values=(
                        row.id,
                        row.created_at,
                        measure_type_name,
                        user_name,
                        material_name,
                        sample_name,
                        row.discription,
                    ),
                )
