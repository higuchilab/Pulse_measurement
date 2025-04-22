from src.core.measurement_strategies._base import MeasurementStrategy

from ._base import MeasurementStrategy
from ..data_processing import TwoTerminalOutput, EchoStateParam
from ..measurement_model import MeasureModelTemplete, MeasureBlocks, PulseModel
from ...utils import plot_data

from ...echostate.model import generate_echostate_input_array


class EchoStateMeasurementStrategy(MeasurementStrategy):
    def __init__(self, params: EchoStateParam):
        self.parameters = params
        self.input_value = None
        self.correct_value = None
        self._prepare_dataset()

    def _prepare_dataset(self):
        self.input_value = generate_echostate_input_array(
            steps=self.parameters.discrete_time,
            inner_loop_num=self.parameters.inner_loop_num,
            outer_loop_num=self.parameters.outer_loop_num,
            top_voltage=self.parameters.top_voltage,
            base_voltage=self.parameters.base_voltage
        )

    def create_measure_model(self) -> MeasureModelTemplete:
        new_pulse_blocks = MeasureBlocks()
        new_pulse_model = PulseModel(new_pulse_blocks)
        new_pulse_model.make_model_from_echostate_input_array(
            # pulse_width=self.parameters.pulse_width,
            # off_width=self.parameters.off_width,
            # tick=self.parameters.tick,
            # base_voltage=self.parameters.base_voltage,
            # input_array=self.input_value
            echostate_param=self.parameters,
            input_array=self.input_value
        )
        return new_pulse_model
        # return PulseModel.make_model_from_echostate_input_array(
        #     pulse_width=self.parameters.pulse_width,
        #     off_width=self.parameters.off_width,
        #     tick=self.parameters.tick,
        #     base_voltage=self.parameters.base_voltage,
        #     input_array=self.x_test
        # )


    def get_measurement_type(self) -> str:
        return "EchoState"
        # ここではMeasurementType.EchoState.valueを直接返すように変更
        # ただし、MeasurementType.EchoState.valueを使用する場合は
        # MeasurementTypeをインポートする必要があります。
        # もしMeasurementTypeを使用する場合は以下のように変更してください
        return MeasurementType.EchoState.value

    def post_process(self, output: TwoTerminalOutput) -> None:
        plot_data(output)
        # EchoState特有の後処理があれば実装
