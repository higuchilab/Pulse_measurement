from typing import TypedDict
from sqlalchemy import select
from numpy.typing import NDArray

from ._base import MeasurementStrategy
from ..data_processing import TwoTerminalOutput, CommonParameters
from ..measurement_model import MeasureModelTemplete, MeasureBlocks, PulseModel, PulseParameters
# from ..measurement import MeasurementType #クロスインポート
from ...utils import plot_data
from src.database.session_manager import session_scope
from src.database.models import (
    User,
    Sample,
    MeasureType,
    History,
    TwoTerminalResult,
    ParamHistoryPulseBlock,
    ParamHistoryPulseCycle
)

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
    
    def save_to_db(self, common_param: CommonParameters, result: NDArray) -> None:
        # データベースに保存する処理を実装
        with session_scope() as session:
            # ここでデータベースに保存するレコードを定義
            user = session.query(User).filter_by(name=common_param.operator).first()
            sample = session.query(Sample).filter_by(name=common_param.sample_name).first()
            measure_type = session.query(MeasureType).filter_by(name=self.get_measurement_type()).first()
            history = History(
                user=user,
                sample=sample,
                measure_type=measure_type,
                discription=common_param.option
            )
            # rowは[voltage, current, elapsed_time]の形式
            two_terminal_result = [
                TwoTerminalResult(
                    history=history,
                    elapsed_time=row[0],
                    voltage=row[1],
                    current=row[2],
                )
                for row in result
            ]
            param_history_blocks = [
                ParamHistoryPulseBlock(
                    history=history,
                    order_id=i,
                    top_voltage=block.V_top,
                    top_time=block.top_time,
                    base_voltage=block.V_base,
                    base_time=block.base_time,
                    loop=block.loop,
                    interval_time=block.interval
                )
                for i, block in enumerate(self.parameters["measure_blocks"].blocks)
            ]
            param_history_cycles = [
                ParamHistoryPulseCycle(
                    history=history,
                    order_idx=i,
                    start_idx=cycle.start_index,
                    end_idx=cycle.stop_index,
                    loop=cycle.loop
                )
                for i, cycle in enumerate(self.parameters["measure_blocks"].cycles)
            ]
            session.add_all([history] + two_terminal_result + param_history_blocks + param_history_cycles)
            session.commit()
        return None

    def post_process(self, output: TwoTerminalOutput) -> None:
        pass
        # plot_data(output)

