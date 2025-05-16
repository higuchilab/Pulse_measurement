from numpy.typing import NDArray

from ._base import MeasurementStrategy
from ..data_processing import TwoTerminalOutput, SweepParam, CommonParameters
from ..measurement_model import MeasureModelTemplete, SweepModel
# from ..measurement import MeasurementType #クロスインポート
from ...utils import plot_data

from src.database.models import (
    User,
    Sample,
    MeasureType,
    History,
    TwoTerminalResult,
    ParamHistorySweep,
)
from src.database.session_manager import session_scope

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

    def save_to_db(self, common_param: CommonParameters, result: NDArray) -> None:
        # データベースに保存する処理を実装
        with session_scope() as session:
            # ここでデータベースに保存するレコードを定義
            user = session.query(User).filter_by(name=common_param.operator).first()
            sample = (
                session.query(Sample).filter_by(name=common_param.sample_name).first()
            )
            measure_type = (
                session.query(MeasureType)
                .filter_by(name=self.get_measurement_type())
                .first()
            )
            history = History(
                user=user,
                sample=sample,
                measure_type=measure_type,
                discription=common_param.option,
            )
            # rowは[voltage, current, elapsed_time]の形式
            two_terminal_result = [
                TwoTerminalResult(
                    history=history,
                    voltage=row[0],
                    current=row[1],
                    elapsed_time=row[2],
                )
                for row in result
            ]
            param_history_sweep = ParamHistorySweep(
                history=history,
                mode=self.parameters.mode,
                top_voltage=self.parameters.top_voltage,
                bottom_voltage=self.parameters.bottom_voltage,
                voltage_step=self.parameters.voltage_step,
                loop=self.parameters.loop,
                tick_time=self.parameters.tick_time,
            )
            session.add_all(
                [history]
                + two_terminal_result
                + [param_history_sweep]
            )
            session.commit()
        return None

    def post_process(self, output: TwoTerminalOutput) -> None:
        pass
        # plot_data(output)
