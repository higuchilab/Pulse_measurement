from typing import Protocol
from ..measurement_model import MeasureModelTemplete
from ..data_processing import TwoTerminalOutput

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
