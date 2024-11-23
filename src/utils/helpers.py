import os
import time
from numpy.typing import NDArray
from typing import Any, Dict, List, Callable
import tkinter as tk
from tkinter import filedialog

from src.core.data_processing import Datas, TwoTerminalOutput
from src.visualization import graph


def set_folder_func(textboxes: Any) -> callable:
    """フォルダ選択ダイアログを表示し、選択されたパスをテキストボックスに設定する関数を返します。"""
    def inner():
        dir = 'C:\\'
        folder_path = filedialog.askdirectory(initialdir=dir)
        textboxes.textbox["folderpath"].delete(0, tk.END)
        textboxes.textbox["folderpath"].insert(tk.END, folder_path)       
    return inner


def timer(measure_times: float, statusbar: Any, timer_flag: bool = False) -> None:
    """測定時間のカウントダウンを行い、ステータスバーに表示します。"""
    start_time = time.perf_counter()
    while time.perf_counter() - start_time < measure_times:
        if timer_flag:
            statusbar.swrite(f"合計時間: {time.perf_counter() - start_time:.1f} [s]")
            break
        statusbar.swrite(f"{time.perf_counter() - start_time:.1f}/{measure_times:.1f}")
        time.sleep(0.1)


def plot_data(output: TwoTerminalOutput) -> None:
    """データのプロットと保存を行います。"""
    # totaltime_list = calculate_total_time(output.time)
    graph(output.time, output.voltage, output.current)


def calculate_total_time(time_list: NDArray) -> List[float]:
    """累積時間リストを計算します。"""
    interval_list = [time_list[i+1] - time_list[i] for i in range(len(time_list) - 1)]
    return [sum(interval_list[:i]) for i in range(len(interval_list) + 1)]