import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.ttk import Notebook
import sys
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from src.database.models import User, Material, Sample
from sqlalchemy import create_engine
import threading
from concurrent.futures import ThreadPoolExecutor, wait
# from abc import ABC, abstractmethod

project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.gui.widgets import (
    CommonInputForm,
    TabNarma,
    TabPulse,
    TabSweep,
    TabEchoState,
    Statusbar,
    Sidebar,
    HistoryWindow,
)

from src.core import CommonParameters

from src.core.execution_strategies import (
    NarmaExecutionStrategy,
    PulseExecutionStrategy,
    SweepExecutionStrategy,
    EchoStateExecutionStrategy,
)

from src.utils import timer
from src.database.session_manager import session_scope


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Pulse ver2.1")
        self.pack(fill="both", expand=True)
        self.__statusbar = Statusbar(master=self)
        self.main_window = MainWindow(statusbar=self.status_bar, master=self)

    @property
    def status_bar(self):
        return self.__statusbar


class MainWindow(tk.Frame):
    def __init__(self, statusbar, master=None):
        super().__init__(master=master)
        self.master = master
        self.statusbar = statusbar
        self.pack(fill="both", expand=True)
        self.measure_window = MeasureWindow(statusbar=self.status_bar, master=self)
        self.history_window = HistoryWindow(master=self)
        self.sidebar = Sidebar(
            master=self, contents=[self.measure_window, self.history_window]
        )

    @property
    def status_bar(self):
        return self.statusbar


class MeasureWindow(tk.Frame):
    def __init__(self, statusbar: Statusbar, master):
        super().__init__(master=master)
        self.pack(fill="both", expand=True, side="right")
        self.stop_event = threading.Event()
        self.statusbar = statusbar
        self.form_top = CommonInputForm(self)

        tab_classes = [TabNarma, TabPulse, TabSweep, TabEchoState]
        tab_name = ["NARMA", "Pulse", "I-Vsweep", "EchoState"]

        self.notebook = Notebook(master=self)

        self.tab_instances = []
        for cls, name in zip(tab_classes, tab_name):
            instance = cls(master=self.notebook)
            self.tab_instances.append(instance)
            self.notebook.add(instance, text=name)

        self.notebook.pack(fill="both", expand=True)

        self.exe_button = tk.Button(
            master=self, text="実行", command=self.click_exe_button
        )
        self.exe_button.pack(side="top", pady=10)

        self.interrapt_button = tk.Button(
            master=self, 
            text="中断",
            command=self.click_interrapt_button,
            state=tk.DISABLED
        )
        self.interrapt_button.pack(side="top", pady=10)

        # 戦略の初期化
        self.execution_strategies = {
            0: lambda: NarmaExecutionStrategy(self.tab_instances[0], self.statusbar),
            1: lambda: PulseExecutionStrategy(self.tab_instances[1], self.statusbar),
            2: lambda: SweepExecutionStrategy(self.tab_instances[2]),
            3: lambda: EchoStateExecutionStrategy(
                self.tab_instances[3], self.statusbar
            ),
        }

    def _get_common_parameters(self, file_path: str) -> CommonParameters:
        return CommonParameters(
            operator=self.form_top.input_measure_person,
            material=self.form_top.input_material_name,
            sample_name=self.form_top.input_sample_num,
            option=self.form_top.input_option,
            file_path=file_path,
        )

    def _update_database_records(self, common_param: CommonParameters) -> None:
        """
        データベースにデータを追加し、関連するリストを更新する
        """
        with session_scope() as session:
            # ユーザーの追加
            if common_param.operator:
                user = session.query(User).filter_by(name=common_param.operator).first()
                if not user:
                    user = User(name=common_param.operator)
                    session.add(user)
                # ユーザーリストの更新
                # 現在はここの処理でtkinterのリストボックスに直接値をセットしているが、データベースの内容と同期させるようにしたい
                self.form_top.user_name_list = [u.name for u in session.query(User).all()]

            # マテリアルの追加
            if common_param.material:
                material = session.query(Material).filter_by(name=common_param.material).first()
                if not material:
                    material = Material(name=common_param.material)
                    session.add(material)
                # マテリアルリストの更新
                # 現在はここの処理でtkinterのリストボックスに直接値をセットしているが、データベースの内容と同期させるようにしたい
                self.form_top.materials = [m.name for m in session.query(Material).all()]

            # サンプルの追加
            if common_param.sample_name:
                material = session.query(Material).filter_by(name=common_param.material).first()
                if material:
                    sample = session.query(Sample).filter_by(
                        material_id=material.id, name=common_param.sample_name
                    ).first()
                    if not sample:
                        sample = Sample(material_id=material.id, name=common_param.sample_name)
                        session.add(sample)
                    # サンプルリストの更新
                    # 現在はここの処理でtkinterのリストボックスに直接値をセットしているが、データベースの内容と同期させるようにしたい
                    self.form_top.samples = [
                        s.name for s in session.query(Sample).filter_by(material_id=material.id).all()
                    ]

    def click_exe_button(self):
        """実行ボタン押下後の処理"""
        # ファイル出力の確認と設定
        self.exe_button.config(state=tk.DISABLED)
        self.interrapt_button.config(state=tk.NORMAL)

        file_path = ""
        if messagebox.askyesno("確認", "ファイル出力しますか？"):
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[
                    ("Comma Separate files", "*.csv"),
                    ("Excel files", "*.xlsx"),
                    ("All files", "*.*"),
                ],
                initialdir=f"C:/Users/higuchi/Desktop/{self.form_top.input_measure_person}",
                initialfile=f"{self.form_top.input_material_name}_{self.form_top.input_sample_num}_{self.form_top.input_option}",
            )

        # 共通パラメータの設定とデータベース更新
        common_param = self._get_common_parameters(file_path)
        self._update_database_records(common_param)

        # 選択されたタブに応じた戦略の実行
        selected_tab = self.notebook.index(self.notebook.select())
        strategy = self.execution_strategies[selected_tab]()

        # 実行前の準備（必要な場合）
        # if hasattr(strategy, 'pre_execute'):
        #     strategy.pre_execute()

        # パラメータの取得と実行
        # parameters = strategy.get_parameters()
        try:
            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = [
                    executor.submit(
                        strategy.execute, common_param, stop_event=self.stop_event
                    )
                ]
                if hasattr(strategy, 'get_total_time'):
                    futures.append(
                        executor.submit(
                            timer, 
                            strategy.get_total_time(), 
                            self.statusbar, 
                            self.stop_event
                        )
                    )

                wait(futures)
        
        except Exception as e:
            raise e
        finally:
            self.exe_button.config(state=tk.NORMAL)
            self.interrapt_button.config(state=tk.DISABLED)

    def click_interrapt_button(self):
        """中断ボタン押下後の処理"""
        # 各タブの実行戦略に中断処理を呼び出す
        # for strategy in self.execution_strategies.values():
        #     if hasattr(strategy(), 'interrupt'):
        #         strategy().interrupt()
        self.stop_event.set()

        # ステータスバーに中断メッセージを表示
        self.statusbar.swrite("実行が中断されました。")
