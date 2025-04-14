from src.core.measurement_strategies._base import MeasurementStrategy

from ._base import MeasurementStrategy
from ..data_processing import TwoTerminalOutput, NarmaParam
from ..measurement_model import MeasureModelTemplete, MeasureBlocks, PulseModel
from ...utils import plot_data

from ...narma.model import use_narma_input_array


class NarmaMeasurementStrategy(MeasurementStrategy):
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
        new_pulse_blocks = MeasureBlocks()
        new_pulse_model = PulseModel(new_pulse_blocks)
        new_pulse_model.make_model_from_narma_input_array(
            pulse_width=self.parameters.pulse_width,
            off_width=self.parameters.off_width,
            tick=self.parameters.tick,
            base_voltage=self.parameters.base_voltage,
            input_array=self.input_value
        )
        return new_pulse_model
        # return PulseModel.make_model_from_narma_input_array(
        #     pulse_width=self.parameters.pulse_width,
        #     off_width=self.parameters.off_width,
        #     tick=self.parameters.tick,
        #     base_voltage=self.parameters.base_voltage,
        #     input_array=self.x_test
        # )


    def get_measurement_type(self) -> str:
        return "NARMA"
        # ここではMeasurementType.NARMA.valueを直接返すように変更
        # ただし、MeasurementType.NARMA.valueを使用する場合は
        # MeasurementTypeをインポートする必要があります。
        # もしMeasurementTypeを使用する場合は以下のように変更してください
        return MeasurementType.NARMA.value

    def post_process(self, output: TwoTerminalOutput) -> None:
        plot_data(output)
        # NARMA特有の後処理があれば実装
