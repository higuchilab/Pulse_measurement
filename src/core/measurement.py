import time
from typing import TypedDict, Protocol, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from openpyxl import Workbook, load_workbook

from ..visualization import graph
from .data_processing import TwoTerminalOutput, NarmaParam, SweepParam, CommonParameters, HistoryParam
from .measurement_model import MeasureBlocks, PulseModel, MeasureModelTemplete, SweepModel
from ..utils import plot_data
from .device_control import write_command, prepare_device, device_connection
from ..database import append_two_terminal_results, append_record_history

from ..narma.model import use_narma_input_array

# 定数の分離
class Constants:
    VISA_DLL_PATH = r'C:\WINDOWS\system32\visa64.dll'
    GPIB_ADDRESS = 'GPIB1::1::INSTR'
    INTERVAL_TIME = 0.041463354054055365

# 測定タイプの列挙
class MeasurementType(Enum):
    PULSE = "2-terminal Pulse"
    NARMA = "NARMA"
    SWEEP = "2-terminal I-Vsweep"


def stop_func(statusbar: Any) -> None:
    """測定を中断し、ステータスバーに表示します。"""
    statusbar.swrite("測定中断")


class PulseParameters(TypedDict):
    measure_blocks: MeasureBlocks

# 測定戦略のインターフェース
class MeasurementStrategy(Protocol):
    def create_measure_model(self) -> MeasureModelTemplete:
        """測定モデルを作成"""
        pass

    def get_measurement_type(self) -> str:
        """測定タイプを取得"""
        pass

    def post_process(self, output: TwoTerminalOutput) -> None:
        """測定後の追加処理"""
        pass

# 具体的な測定戦略の実装
class PulseMeasurementStrategy:
    def __init__(self, params: PulseParameters):
        self.parameters = params

    def create_measure_model(self) -> MeasureModelTemplete:
        return PulseModel(self.parameters["measure_blocks"])

    def get_measurement_type(self) -> str:
        return MeasurementType.PULSE.value

    def post_process(self, output: TwoTerminalOutput) -> None:
        plot_data(output)


class SweepMeasurementStrategy:
    def __init__(self, params: SweepParam):
        self.parameters = params

    def create_measure_model(self) -> MeasureModelTemplete:
        return SweepModel(self.parameters)
    
    def get_measurement_type(self) -> str:
        return MeasurementType.SWEEP.value
    
    def post_process(self, output: TwoTerminalOutput) -> None:
        plot_data(output)


class NarmaMeasurementStrategy:
    def __init__(self, params: NarmaParam):
        self.parameters = params
        self.input_value = None
        self.correct_value = None
        self._prepare_dataset()

    def _prepare_dataset(self):
        self.input_value = use_narma_input_array(
            use_database=self.parameters.use_database,
            model=self.parameters.model,
            steps=self.parameters.discrete_time,
            input_range_bot=self.parameters.bot_voltage,
            input_range_top=self.parameters.top_voltage
        )

    def create_measure_model(self) -> MeasureModelTemplete:
        return PulseModel.make_model_from_narma_input_array(
            pulse_width=self.parameters.pulse_width,
            off_width=self.parameters.off_width,
            tick=self.parameters.tick,
            base_voltage=self.parameters.base_voltage,
            input_array=self.input_value
        )
        return PulseModel.make_model_from_narma_input_array(
            pulse_width=self.parameters.pulse_width,
            off_width=self.parameters.off_width,
            tick=self.parameters.tick,
            base_voltage=self.parameters.base_voltage,
            input_array=self.x_test
        )


    def get_measurement_type(self) -> str:
        return MeasurementType.NARMA.value

    def post_process(self, output: TwoTerminalOutput) -> None:
        plot_data(output)
        # NARMA特有の後処理があれば実装

# メイン測定クラス
class MeasurementExecutor:
    def __init__(self, strategy: MeasurementStrategy, common_param: CommonParameters):
        self.strategy = strategy
        self.common_param = common_param
        self.device = None

    def _connect_device(self):
        """デバイスへの接続"""
        try:
            self.device = device_connection(
                visa_dll_path=Constants.VISA_DLL_PATH,
                gpib_address=Constants.GPIB_ADDRESS
            )
            prepare_device(self.device)
        except Exception as e:
            raise ConnectionError(f"Failed to connect device '{Constants.GPIB_ADDRESS}': {str(e)}")

    def _save_results(self, output: TwoTerminalOutput) -> None:
        """結果の保存"""
        history_param = HistoryParam(
            user_name=self.common_param.operator,
            sample_name=self.common_param.sample_name,
            measure_type=self.strategy.get_measurement_type(),
            option=self.common_param.option
        )
        history_id = append_record_history(history_param)
        save_data_to_database(history_id=history_id, output=output)

        if self.common_param.file_path:
            output_to_excel_file(self.common_param.file_path, output=output)

    def execute(self) -> TwoTerminalOutput:
        """測定の実行"""
        try:
            self._connect_device()
            measure_model = self.strategy.create_measure_model()
            print("測定開始")
            output = measure(measure_model=measure_model, dev=self.device)
            
            write_command("SBY", self.device)
            print("測定終了")

            self.strategy.post_process(output)
            self._save_results(output)

            return output

        finally:
            if self.device:
                write_command("SBY", self.device)

# 既存の関数をリファクタリング
def pulse_run(parameters: PulseParameters, common_param: CommonParameters):
    strategy = PulseMeasurementStrategy(parameters)
    executor = MeasurementExecutor(strategy, common_param)
    return executor.execute()

def narma_run(parameters: NarmaParam, common_param: CommonParameters):
    strategy = NarmaMeasurementStrategy(parameters)
    executor = MeasurementExecutor(strategy, common_param)
    return executor.execute()

def sweep_run(parameters: SweepParam, common_param: CommonParameters):
    strategy = SweepMeasurementStrategy(parameters)
    executor = MeasurementExecutor(strategy, common_param)
    return executor.execute()


def measure(measure_model: MeasureModelTemplete, dev: any) -> TwoTerminalOutput:
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

    output_data = TwoTerminalOutput(voltage=V_list, current=A_list, time=time_list)

    return output_data


def output_to_excel_file(file_path: str, output: TwoTerminalOutput):
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


def save_data_to_database(history_id: int, output: TwoTerminalOutput):
    data = [(history_id, time, voltage, current) for time, voltage, current in zip(output.time, output.voltage, output.current)]
    append_two_terminal_results(param=data)
