from ._base import MeasurementStrategy
from ..data_processing import TwoTerminalOutput, SweepParam
from ..measurement_model import MeasureModelTemplete, SweepModel
# from ..measurement import MeasurementType #クロスインポート
from ...utils import plot_data

class SweepMeasurementStrategy(MeasurementStrategy):
    def __init__(self, params: SweepParam):
        self.parameters = params

    def create_measure_model(self) -> MeasureModelTemplete:
        return SweepModel(self.parameters)
    
    def get_measurement_type(self) -> str:
        return "2-terminal I-Vsweep"
        # ここではMeasurementType.SWEEP.valueを直接返すように変更
        # ただし、MeasurementType.SWEEP.valueを使用する場合は
        # MeasurementTypeをインポートする必要があります。
        # もしMeasurementTypeを使用する場合は以下のように変更してください
        return MeasurementType.SWEEP.value
    
    def post_process(self, output: TwoTerminalOutput) -> None:
        plot_data(output)
