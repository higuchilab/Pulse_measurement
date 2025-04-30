import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.ttk import Notebook
import sys
from pathlib import Path
# from abc import ABC, abstractmethod
# from dataclasses import dataclass

project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.gui.widgets import (
    common_input_form, 
    TabNarma, 
    TabPulse, 
    TabSweep,
    TabEchoState,
    Statusbar, 
    Sidebar, 
    HistoryWindow
)

from src.database import append_record_users, refer_users_table, append_record_materials, refer_materials_table, append_record_samples, refer_samples_table

from src.core import CommonParameters

from src.core.execution_strategies import NarmaExecutionStrategy, PulseExecutionStrategy, SweepExecutionStrategy, EchoStateExecutionStrategy

from src.utils import timer


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
        self.sidebar = Sidebar(master=self, contents=[self.measure_window, self.history_window])

    @property
    def status_bar(self):
        return self.statusbar


class MeasureWindow(tk.Frame):
    def __init__(self, statusbar, master):
        super().__init__(master=master)
        self.pack(fill="both", expand=True, side="right")
        self.statusbar = statusbar
        self.form_top = common_input_form(self)

        tab_classes = [TabNarma, TabPulse, TabSweep, TabEchoState]
        tab_name = ["NARMA", "Pulse", "I-Vsweep", "EchoState"]

        self.notebook = Notebook(master=self)

        self.tab_instances = []
        for cls, name in zip(tab_classes, tab_name):
            instance = cls(master=self.notebook)
            self.tab_instances.append(instance)
            self.notebook.add(instance, text=name)

        self.notebook.pack(fill="both", expand=True)

        self.exe_button = tk.Button(master=self, text="実行", command=self.click_exe_button)
        self.exe_button.pack(side="top", pady=10)

        # 戦略の初期化
        self.execution_strategies = {
            0: lambda: NarmaExecutionStrategy(self.tab_instances[0], self.statusbar),
            1: lambda: PulseExecutionStrategy(self.tab_instances[1], self.statusbar),
            2: lambda: SweepExecutionStrategy(self.tab_instances[2]),
            3: lambda: EchoStateExecutionStrategy(self.tab_instances[3], self.statusbar)
        }

    def _get_common_parameters(self, file_path: str) -> CommonParameters:
        return CommonParameters(
            operator=self.form_top.input_measure_person,
            material=self.form_top.input_material_name,
            sample_name=self.form_top.input_sample_num,
            option=self.form_top.input_option,
            file_path=file_path
        )

    def _update_database_records(self, common_param: CommonParameters) -> None:
        if common_param.operator:
            append_record_users(common_param.operator)
            self.form_top.user_name_list = refer_users_table()

        if common_param.material:
            append_record_materials(common_param.material)
            self.form_top.materials = refer_materials_table()

        if common_param.sample_name:
            append_record_samples(common_param.material, common_param.sample_name)
            self.form_top.samples = refer_samples_table(common_param.material)

    def click_exe_button(self):
        """実行ボタン押下後の処理"""
        # ファイル出力の確認と設定
        file_path = ""
        if messagebox.askyesno("確認", "ファイル出力しますか？"):
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Comma Separate files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialdir=f'C:/Users/higuchi/Desktop/{self.form_top.input_measure_person}',
                initialfile=f'{self.form_top.input_material_name}_{self.form_top.input_sample_num}_{self.form_top.input_option}'
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
        strategy.execute(common_param)
