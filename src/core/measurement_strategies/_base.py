import time
from typing import Protocol
from ..measurement_model import MeasureModelTemplete
from ..data_processing import TwoTerminalOutput
from src.visualization._graph import graph

# 測定戦略のインターフェース
class MeasurementStrategy(Protocol):
    def create_measure_model(self) -> MeasureModelTemplete:
        """測定モデルを作成"""
        pass

    def get_measurement_type(self) -> str:
        """測定タイプを取得"""
        pass

    def measure(self, measure_model: MeasureModelTemplete, dev: any) -> TwoTerminalOutput:
        """測定を実行"""
        V_list = []
        A_list = []
        time_list = []

        start_perfcounter = time.perf_counter()
        target_time = 0.0
        for i, voltage in enumerate(measure_model.input_V_list):
            while True:
                elapsed_time = time.perf_counter() - start_perfcounter
                if elapsed_time >= target_time:
                    dev.write(f"SOV{voltage}")
                    dev.write("*TRG")
                    time_list.append(time.perf_counter() - start_perfcounter)

                    A = dev.query("N?")
                    A_ = float(A[3:-2])
                    A_list.append(A_)

                    V = dev.query("SOV?")
                    V_ = float(V[3:-2])
                    V_list.append(V_)
                    target_time += measure_model.tick
                    if i % 100 == 0:
                        graph(time_list, V_list, A_list)

                    break

        output_data = TwoTerminalOutput(voltage=V_list, current=A_list, time=time_list)

        return output_data
    
    def data_formatting(self, output: TwoTerminalOutput) -> any:
        """測定結果のフォーマットを整える"""
        return output
    
    def get_header(self) -> list[str]:
        """
        測定結果のヘッダーを取得\n
        デフォルトではNoneを返す\n
        ヘッダーを指定する場合は、リストを返すこと\n
        例: ["Time", "Voltage", "Current"]\n
        ヘッダーを指定しない場合は、Noneを返すこと\n
        例: None

        Returns:
            list[str]: 測定結果のヘッダー
        """
        return None

    def post_process(self, output: TwoTerminalOutput) -> None:
        """測定後の追加処理"""
        pass
