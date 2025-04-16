from typing import TypedDict

from ._base import MeasurementStrategy
from ..data_processing import TwoTerminalOutput
from ..measurement_model import MeasureModelTemplete, MeasureBlocks, PulseModel, PulseParameters
# from ..measurement import MeasurementType #クロスインポート
from ...utils import plot_data

class PulseMeasurementStrategy(MeasurementStrategy):
    def __init__(self, params: PulseParameters):
        self.parameters = params

    def create_measure_model(self) -> MeasureModelTemplete:
        return PulseModel(self.parameters["measure_blocks"])

    def get_measurement_type(self) -> str:
        return "2-terminal Pulse"
        # ここではMeasurementType.PULSE.valueを直接返すように変更
        # ただし、MeasurementType.PULSE.valueを使用する場合は
        # MeasurementTypeをインポートする必要があります。
        # もしMeasurementTypeを使用する場合は以下のように変更してください
        return MeasurementType.PULSE.value

    def post_process(self, output: TwoTerminalOutput) -> None:
        plot_data(output)

