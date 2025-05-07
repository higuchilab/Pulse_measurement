import numpy as np

from src.core.measurement_strategies._base import MeasurementStrategy

from ._base import MeasurementStrategy
from ..data_processing import TwoTerminalOutput, EchoStateParam
from ..measurement_model import MeasureModelTemplete, MeasureBlocks, PulseModel
from ...utils import plot_data

from ...echostate.model import generate_echostate_input_array


class EchoStateMeasurementStrategy(MeasurementStrategy):
    def __init__(self, params: EchoStateParam):
        self.parameters = params
        self.input_array = None
        self.correct_value = None
        print(f"Parameters: {self.parameters}")
        self._prepare_dataset()

    def _prepare_dataset(self):
        self.input_array = generate_echostate_input_array(
            param=self.parameters
        )

    def create_measure_model(self) -> MeasureModelTemplete:
        new_pulse_blocks = MeasureBlocks()
        new_pulse_model = PulseModel(new_pulse_blocks)
        new_pulse_model.make_model_from_echostate_input_array(
            echostate_param=self.parameters,
            input_array=self.input_array[:, 0]
        )
        return new_pulse_model

    def get_measurement_type(self) -> str:
        return "EchoState"
        # ここではMeasurementType.EchoState.valueを直接返すように変更
        # ただし、MeasurementType.EchoState.valueを使用する場合は
        # MeasurementTypeをインポートする必要があります。
        # もしMeasurementTypeを使用する場合は以下のように変更してください
        return MeasurementType.EchoState.value

    def data_formatting(self, output: TwoTerminalOutput):
        """
        測定結果のフォーマットを整える
        """
        plot_data(output)

        discrete_idx = np.repeat(
            self.input_array[:, 1],
            self.parameters.pulse_width / self.parameters.tick,
            axis=0,
        )
        inner_loop_idx = np.repeat(
            self.input_array[:, 2],
            self.parameters.pulse_width / self.parameters.tick,
            axis=0,
        )
        outer_loop_idx = np.repeat(
            self.input_array[:, 3],
            self.parameters.pulse_width / self.parameters.tick,
            axis=0,
        )

        node_idx_single = np.arange(1, self.parameters.pulse_width / self.parameters.tick + 1)
        node_idx_one_loop = np.tile(node_idx_single, self.parameters.discrete_time)
        node_idx_inner_loop = np.tile(node_idx_one_loop, self.parameters.inner_loop_idx)
        node_idx = np.tile(node_idx_inner_loop, self.parameters.outer_loop_idx)

        result = np.stack(
            [
                np.array([output.voltage]).reshape(-1),
                np.array([output.current]).reshape(-1),
                np.array([output.time]).reshape(-1),
                discrete_idx,
                node_idx,
                inner_loop_idx,
                outer_loop_idx,
            ],
            axis=1,
        )

        return result

    def get_header(self) -> list[str]:
        """
        echostate測定結果のヘッダーを取得\n
        Returns:
            list[str]: 測定結果のヘッダー
        """
        return [
            "Voltage",
            "Current",
            "Time",
            "Discrete",
            "Node",
            "InnerLoop",
            "OuterLoop",
        ]

    def post_process(self, output: TwoTerminalOutput) -> None:
        pass
        # EchoState特有の後処理があれば実装
