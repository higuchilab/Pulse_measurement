# import tkinter as tk
# from tkinter import filedialog
import time
import threading
import os
import numpy as np
from typing import TypedDict

from typing import List, Dict, Any
from openpyxl import Workbook, load_workbook
from ..visualization.graph import graph
from ..visualization.live_plot import livegraph
from .data_processing import Datas, PulseMeasureOutputSingle
from .measurement_model import MeasureBlock, MeasureBlocks, MeasureModel
from ..utils import plot_data
from .device_control import write_command, prepare_device, device_connection

from ..narma.model import use_narma_dataset

# 定数
INTERVAL_TIME = 0.041463354054055365  # [s] 実行環境によって異なるので適時調整

# パラメータの型を定義
class CommonParameters(TypedDict):
    user_name: str
    material: str
    sample_num: str
    file_path: str


class NarmaParameters(TypedDict):
    use_database: bool
    model: str
    pulse_width: float
    off_width: float
    tick: float
    nodes: int
    discrete_time: int
    bot_voltage: float
    top_voltage: float
    base_voltage: float


class PulseParameters(TypedDict):
    measure_blocks: list[MeasureBlock]


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

def pulse_run(
        parameters: PulseParameters,
        common_param: CommonParameters
        ):
    """パルス測定を実行"""
    VISA_DLL_PATH = r'C:\WINDOWS\system32\visa64.dll'
    GPIB_ADDRESS = 'GPIB1::1::INSTR'
    try:
        dev = device_connection(visa_dll_path=VISA_DLL_PATH, gpib_address=GPIB_ADDRESS)
    except:
        raise ConnectionError(f"Fail to connect device '{GPIB_ADDRESS}'")
    
    output = measure(measure_model=parameters["measure_blocks"], dev=dev)

    plot_data(output)

    if common_param["file_path"] == "":
        return
    
    output_to_excel_file(common_param["file_path"], output=output)


def narma_run(
        parameters: NarmaParameters,
        common_param: CommonParameters
        ):
    """NARMA測定を実行"""
    #パラメーターを取得 測定者，物質名，試料No，備考，model，パルス幅，休止幅，tick，仮想ノード，離散時間，電圧上限，電圧下限

    #入力列の作成or呼び出し
    x_train, y_train, x_test, y_test = use_narma_dataset(
        use_database=parameters['use_database'],
        model=parameters['model'],
        steps=parameters['discrete_time'],
        input_range_bot=parameters['bot_voltage'],
        input_range_top=parameters['top_voltage'])

    #測定装置の準備
    VISA_DLL_PATH = r'C:\WINDOWS\system32\visa64.dll'
    GPIB_ADDRESS = 'GPIB1::1::INSTR'
    try:
        dev = device_connection(visa_dll_path=VISA_DLL_PATH, gpib_address=GPIB_ADDRESS)
    except:
        raise ConnectionError(f"Fail to connect device '{GPIB_ADDRESS}'")

    #測定モデル作成
    measure_model_train = MeasureModel
    measure_model_train.make_model_from_narma_input_array(
        pulse_width=parameters['pulse_width'],
        off_width=parameters['off_width'],
        tick=parameters['tick'],
        base_voltage=parameters['base_voltage'],
        input_array=x_train)

    measure_model_test = MeasureModel
    measure_model_test.make_model_from_narma_input_array(
        pulse_width=parameters['pulse_width'],
        off_width=parameters['off_width'],
        tick=parameters['tick'],
        base_voltage=parameters['base_voltage'],
        input_array=x_test)

    #測定実行
    output_data_train = measure(measure_model=measure_model_train, dev=dev)
    output_data_test = measure(measure_model=measure_model_test, dev=dev)

    #データ保存

    #ファイル出力



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
    # execute_measurement(blocks, datas)

    # 測定終了処理
    finish_measurement(paras, statusbar)

    # グラフ描画とファイル出力
    plot_data(datas, paras)


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


def measure(measure_model: MeasureModel, dev: any) -> PulseMeasureOutputSingle:
    V_list = []
    A_list = []
    time_list = []
    start_time = time.perf_counter()

    for voltage in measure_model.input_V_list:
        
        dev.write(f"SOV{voltage}")
        dev.write("*TRG")
        time_list.append(time.perf_counter() - start_time)
        
        A=dev.query("N?")
        A_=float(A[3:-2])
        A_list.append(A_)
        
        V=dev.query("SOV?")
        V_=float(V[3:-2])
        V_list.append(V_)

        time.sleep(measure_model.tick)

    output_data = PulseMeasureOutputSingle(voltage=np.ndarray(V_list), current=np.ndarray(A_list), time=np.ndarray(time_list))

    return output_data


def output_to_excel_file(file_path: str, output: PulseMeasureOutputSingle):
    wb = Workbook()
    wb.save(file_path)
    wb = load_workbook(file_path)
    ws =wb['Sheet']
    ws = wb.active

    for i, (t, voltage, current) in enumerate(zip(output.time, output.voltage, output.current), 1):
        ws.cell(i, 1, t)
        ws.cell(i, 2, voltage)
        ws.cell(i, 3, current)

    wb.save(file_path)
    wb.close()
