import tkinter as tk
from tkinter import filedialog
import time
import threading
import os

from typing import List, Dict, Any
from graph import graph, livegraph
from data import Datas
from algorithm import MeasureBlock
from utils import plot_and_save_data
from device_control import write_command, prepare_device

# 定数
INTERVAL_TIME = 0.041463354054055365  # [s] 実行環境によって異なるので適時調整

def stop_func(statusbar: Any) -> None:
    """測定を中断し、ステータスバーに表示します。"""
    statusbar.swrite("測定中断")

def timer(measure_times: float, statusbar: Any, timer_flag: bool = False) -> None:
    """測定時間のカウントダウンを行い、ステータスバーに表示します。"""
    start_time = time.perf_counter()
    while time.perf_counter() - start_time < measure_times:
        if timer_flag:
            statusbar.swrite(f"合計時間: {time.perf_counter() - start_time:.1f} [s]")
            break
        statusbar.swrite(f"{time.perf_counter() - start_time:.1f}/{measure_times:.1f}")
        time.sleep(0.1)

def run_func(read_widgets: List[Any], blocks: Any, datas: Datas, statusbar: Any) -> None:
    """測定を実行します。"""
    global timer_flag, livegraph_flag

    # パラメータの取得
    paras = get_parameters(read_widgets)
    
    # エラーチェック
    if not error_check(paras, blocks, statusbar):
        return

    # 測定装置の準備
    prepare_device()

    # 測定タイマー起動
    start_timer(paras, blocks, statusbar, datas)

    # ライブ描画起動
    start_live_graph(paras)

    # 測定実行
    execute_measurement(blocks, datas)

    # 測定終了処理
    finish_measurement(paras, statusbar)

    # グラフ描画とファイル出力
    plot_and_save_data(datas, paras)

def get_parameters(read_widgets: List[Any]) -> Dict[str, Any]:
    """ウィジェットから測定パラメータを取得します。"""
    paras = {}
    for widget in read_widgets:
        try:
            paras.update(widget.get())
        except TypeError as e:
            print("エラー内容:", e)
    return paras

def error_check(paras: Dict[str, Any], blocks: Any, statusbar: Any) -> bool:
    """測定パラメータのエラーチェックを行います。"""
    if not paras["ファイルに出力しない"].get():
        if not check_file_path(paras, statusbar):
            return False

    return check_block_parameters(blocks, statusbar)

def check_file_path(paras: Dict[str, Any], statusbar: Any) -> bool:
    """ファイルパスの有効性をチェックします。"""
    folderpath = paras["folderpath"].get()
    if not os.path.exists(folderpath):
        statusbar.swrite("無効なフォルダーパスです")
        return False
    return True

def check_block_parameters(blocks: Any, statusbar: Any) -> bool:
    """測定ブロックのパラメータをチェックします。"""
    for block in blocks.blocks:
        if not check_time_parameters(block, statusbar):
            return False
        if not check_loop_parameter(block, statusbar):
            return False
    return True

def check_time_parameters(block: MeasureBlock, statusbar: Any) -> bool:
    """時間パラメータをチェックします。"""
    if block.params["bot_time"] < INTERVAL_TIME:
        statusbar.swrite("bot_timeが短すぎます")
        return False
    if block.params["top_time"] < INTERVAL_TIME:
        statusbar.swrite("top_timeが短すぎます")
        return False
    return True

def check_loop_parameter(block: MeasureBlock, statusbar: Any) -> bool:
    """ループパラメータをチェックします。"""
    if not block.params["loop"].is_integer():
        statusbar.swrite("ループ回数は整数値を設定してください")
        return False
    return True

def start_timer(paras: Dict[str, Any], blocks: Any, statusbar: Any, datas: Datas) -> None:
    """測定タイマーを開始します。"""
    global timer_flag
    if not paras["タイマーを無効にする"].get():
        statusbar.swrite("timer start")
        timer_flag = False
        t1 = threading.Thread(target=timer, args=(blocks.cluc_tot_time(), statusbar, datas))
        t1.start()
    else:
        statusbar.swrite("測定中")

def start_live_graph(paras: Dict[str, Any]) -> None:
    """ライブグラフを開始します。"""
    global livegraph_flag
    if paras["ライブ描画を有効にする"].get():
        livegraph_flag = False
        t2 = threading.Thread(target=livegraph, args=(paras["測定終了後、プロットを表示する"].get(), paras["測定終了後、散布図を表示する"].get()))
        t2.start()

def execute_measurement(blocks: Any, datas: Datas) -> None:
    """測定を実行します。"""
    datas.reset()
    blocks.run(dev, datas)

def finish_measurement(paras: Dict[str, Any], statusbar: Any) -> None:
    """測定を終了し、後処理を行います。"""
    global timer_flag, livegraph_flag
    if not paras["タイマーを無効にする"].get():
        timer_flag = True
    else:
        statusbar.swrite("測定終了")
    if paras["ライブ描画を有効にする"].get():
        livegraph_flag = True
    write_command("SBY")

def exc_run_func(read_widgets: List[Any], blocks: Any, datas: Datas, statusbar: Any) -> callable:
    """実行関数をスレッドで実行するラッパー関数を返します。"""
    def inner():
        t = threading.Thread(target=run_func, args=(read_widgets, blocks, datas, statusbar))
        t.start()
    return inner