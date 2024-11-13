import time
import threading
import os
import numpy as np
from typing import TypedDict

from typing import List, Dict, Any
from openpyxl import Workbook, load_workbook
from ..visualization import graph, livegraph
from .data_processing import Datas, PulseMeasureOutputSingle, NarmaParam, SweepParam
from .measurement_model import MeasureBlock, MeasureBlocks, PulseModel, MeasureModelTemplete, SweepModel
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


class PulseParameters(TypedDict):
    measure_blocks: MeasureBlocks


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
    
    prepare_device(dev)
    measure_model = PulseModel(parameters["measure_blocks"])
    # print(measure_model.input_V_list)
    output = measure(measure_model=measure_model, dev=dev)
    print("測定終了")
    plot_data(output)

    if common_param["file_path"] == "":
        return
    
    output_to_excel_file(common_param["file_path"], output=output)


def narma_run(
        parameters: NarmaParam,
        common_param: CommonParameters
        ):
    """NARMA測定を実行"""
    #パラメーターを取得 測定者，物質名，試料No，備考，model，パルス幅，休止幅，tick，仮想ノード，離散時間，電圧上限，電圧下限

    #入力列の作成or呼び出し
    x_train, y_train, x_test, y_test = use_narma_dataset(
        use_database=parameters.use_database,
        model=parameters.model,
        steps=parameters.discrete_time,
        input_range_bot=parameters.bot_voltage,
        input_range_top=parameters.top_voltage
    )

    #測定装置の準備
    VISA_DLL_PATH = r'C:\WINDOWS\system32\visa64.dll'
    GPIB_ADDRESS = 'GPIB1::1::INSTR'
    try:
        dev = device_connection(visa_dll_path=VISA_DLL_PATH, gpib_address=GPIB_ADDRESS)
    except:
        raise ConnectionError(f"Fail to connect device '{GPIB_ADDRESS}'")
    prepare_device(dev)
    #測定モデル作成
    measure_model_train = PulseModel
    measure_model_train.make_model_from_narma_input_array(
        pulse_width=parameters.pulse_width,
        off_width=parameters.off_width,
        tick=parameters.tick,
        base_voltage=parameters.base_voltage,
        input_array=x_train)

    measure_model_test = PulseModel
    measure_model_test.make_model_from_narma_input_array(
        pulse_width=parameters.pulse_width,
        off_width=parameters.off_width,
        tick=parameters.tick,
        base_voltage=parameters.base_voltage,
        input_array=x_test)

    #測定実行
    output_data_train = measure(measure_model=measure_model_train, dev=dev)
    output_data_test = measure(measure_model=measure_model_test, dev=dev)

    #データ保存

    #ファイル出力


def sweep_run(
        param: SweepParam,
        common_param: CommonParameters
    ):
    VISA_DLL_PATH = r'C:\WINDOWS\system32\visa64.dll'
    GPIB_ADDRESS = 'GPIB1::1::INSTR'
    try:
        dev = device_connection(visa_dll_path=VISA_DLL_PATH, gpib_address=GPIB_ADDRESS)
    except:
        raise ConnectionError(f"Fail to connect device '{GPIB_ADDRESS}'")
    
    prepare_device(dev)
    measure_model = SweepModel(param)
    output = measure(measure_model=measure_model, dev=dev)
    write_command("SBY", dev)
    print("測定終了")
    plot_data(output)

    if common_param["file_path"] == "":
        return
    
    output_to_excel_file(common_param["file_path"], output=output)


def measure(measure_model: MeasureModelTemplete, dev: any) -> PulseMeasureOutputSingle:
    V_list = []
    A_list = []
    time_list = []

    start_perfcounter = time.perf_counter()
    target_time = 0.0
    for voltage in measure_model.input_V_list:
        while True:
            elapsed_time = time.perf_counter() - start_perfcounter

            if elapsed_time >= target_time:
                dev.write(f"SOV{voltage}")
                dev.write("*TRG")
                time_list.append(time.perf_counter() - start_perfcounter)
                
                A=dev.query("N?")
                A_=float(A[3:-2])
                A_list.append(A_)
                
                V=dev.query("SOV?")
                V_=float(V[3:-2])
                V_list.append(V_)
                target_time += measure_model.tick
                break
        
        graph(time_list, V_list, A_list)

    output_data = PulseMeasureOutputSingle(voltage=V_list, current=A_list, time=time_list)

    return output_data


def output_to_excel_file(file_path: str, output: PulseMeasureOutputSingle):
    wb = Workbook()
    wb.save(file_path)
    wb = load_workbook(file_path)
    ws =wb['Sheet']
    ws = wb.active

    ws['A1'] = "Time"
    ws['B1'] = "Voltage"
    ws['C1'] = "Current"

    for i, (t, voltage, current) in enumerate(zip(output.time, output.voltage, output.current), 2):
        ws.cell(i, 1, t)
        ws.cell(i, 2, voltage)
        ws.cell(i, 3, current)

    wb.save(file_path)
    wb.close()
