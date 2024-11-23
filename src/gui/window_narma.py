import tkinter as tk
from threading import Thread
from tkinter import messagebox, filedialog
from tkinter.ttk import Notebook
import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Protocol, Any
from dataclasses import dataclass

project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.gui.widgets import common_input_form, TabNarma, TabPulse, TabSweep, Statusbar, Sidebar, HistoryWindow

from src.core.database import create_users_table, append_record_users, refer_users_table, create_materials_table, append_record_materials, refer_materials_table, create_samples_table, append_record_samples, refer_samples_table, create_pulse_templetes_table, create_sweep_templetes_table, create_measures_types_table, create_history_table, append_record_measure_types, fetch_measure_type_index

from src.core import narma_run, CommonParameters, PulseParameters, SweepParam, NarmaParam, pulse_run, sweep_run

from src.utils import timer


# 測定実行の戦略インターフェース
class ExecutionStrategy(Protocol):
    def get_parameters(self) -> Any:
        """測定パラメータを取得"""
        pass

    def execute(self, parameters: Any, common_param: CommonParameters) -> None:
        """測定を実行"""
        pass

    def pre_execute(self) -> None:
        """実行前の準備（オプション）"""
        pass

# 具体的な実行戦略
class NarmaExecutionStrategy:
    def __init__(self, tab_instance: TabNarma, status_bar: Statusbar):
        self.tab = tab_instance
        self.status_bar = status_bar

    def get_parameters(self) -> NarmaParam:
        # measure_type_index = fetch_measure_type_index("NARMA")        
        return NarmaParam(
            use_database=self.tab.is_use_prepared_array,
            model=self.tab.narma_model,
            pulse_width=self.tab.pulse_width,
            off_width=self.tab.off_width,
            tick=self.tab.tick,
            nodes=self.tab.nodes,
            discrete_time=self.tab.discrete_time,
            bot_voltage=self.tab.bot_voltage,
            top_voltage=self.tab.top_voltage,
            base_voltage=self.tab.base_voltage
        )
    
    def pre_execute(self) -> None:
        tot_time = (self.tab.pulse_width + self.tab.off_width) * self.tab.discrete_time
        timer_thread = Thread(target=timer, args=(tot_time, self.status_bar))
        timer_thread.start()

    def execute(self, parameters: NarmaParam, common_param: CommonParameters) -> None:
        thread = Thread(target=narma_run, args=(parameters, common_param))
        thread.start()

class PulseExecutionStrategy:
    def __init__(self, tab_instance: TabPulse, status_bar: Statusbar):
        self.tab = tab_instance
        self.status_bar = status_bar

    def get_parameters(self) -> PulseParameters:
            # measure_type_index = fetch_measure_type_index(2-terminal Pulse")        
        return {
            'measure_blocks': self.tab.pulse_blocks
        }

    def pre_execute(self) -> None:
        standarded_pulse_blocks = self.tab.pulse_blocks.export_standarded_blocks()
        tot_time = sum((block.top_time + block.base_time) * block.loop + block.interval 
                      for block in standarded_pulse_blocks)
        
        timer_thread = Thread(target=timer, args=(tot_time, self.status_bar))
        timer_thread.start()

    def execute(self, parameters: PulseParameters, common_param: CommonParameters) -> None:
        thread = Thread(target=pulse_run, args=(parameters, common_param))
        thread.start()

class SweepExecutionStrategy:
    def __init__(self, tab_instance: TabSweep):
        self.tab = tab_instance

    def get_parameters(self) -> SweepParam:
            # measure_type_index = fetch_measure_type_index("2-terminal I-Vsweep")        
        return SweepParam(
            mode=self.tab.sweep_mode,
            top_voltage=self.tab.top_voltage,
            bottom_voltage=self.tab.bottom_voltage,
            voltage_step=self.tab.voltage_step,
            loop=self.tab.loop,
            tick_time=self.tab.tick
        )

    def execute(self, parameters: SweepParam, common_param: CommonParameters) -> None:
        thread = Thread(target=sweep_run, args=(parameters, common_param))
        thread.start()


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

        tab_classes = [TabNarma, TabPulse, TabSweep]
        tab_name = ["NARMA", "Pulse", "I-Vsweep"]

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
            2: lambda: SweepExecutionStrategy(self.tab_instances[2])
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
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
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
        if hasattr(strategy, 'pre_execute'):
            strategy.pre_execute()

        # パラメータの取得と実行
        parameters = strategy.get_parameters()
        strategy.execute(parameters, common_param)


if __name__ == "__main__":
    create_users_table()
    create_materials_table()
    create_samples_table()
    create_pulse_templetes_table()
    create_sweep_templetes_table()
    create_measures_types_table()
    append_record_measure_types("NARMA")
    append_record_measure_types("2-terminal I-Vsweep")
    append_record_measure_types("2-terminal Pulse")
    create_history_table()
    root = tk.Tk()
    # root.geometry("530x300")
    # root.resizable(False, False)#ウィンドウサイズをフリーズ
    root.lift()#最前面に表示
    app = Application(master=root)
    app.mainloop()

