from threading import Thread

from src.gui.widgets import TabEchoState, Statusbar
from src.core.measurement import CommonParameters, MeasurementExecutor
from src.core.data_processing import EchoStateParam
from src.utils import timer

from src.core.execution_strategies._base import ExecutionStrategy
from src.core.measurement_strategies import EchoStateMeasurementStrategy

class EchoStateExecutionStrategy(ExecutionStrategy):
    def __init__(self, tab_instance: TabEchoState, status_bar: Statusbar):
        self.tab = tab_instance
        self.param: EchoStateParam = tab_instance.config
        self.status_bar = status_bar

    def get_parameters(self) -> EchoStateParam:
        # measure_type_index = fetch_measure_type_index("EchoState")
        return self.param
        # return EchoStateParam(
        #     use_database=self.tab.is_use_prepared_array,
        #     model=self.tab.EchoState_model,
        #     pulse_width=self.tab.pulse_width,
        #     off_width=self.tab.off_width,
        #     tick=self.tab.tick,
        #     nodes=self.tab.nodes,
        #     discrete_time=self.tab.discrete_time,
        #     bot_voltage=self.tab.bot_voltage,
        #     top_voltage=self.tab.top_voltage,
        #     base_voltage=self.tab.base_voltage
        # )
    
    def run_measurement(self, parameters: EchoStateParam, common_param: CommonParameters):
        strategy = EchoStateMeasurementStrategy(parameters)
        executor = MeasurementExecutor(strategy, common_param)
        return executor.execute()
    
    # def pre_execute(self) -> None:
    #     tot_time = (self.tab.pulse_width + self.tab.off_width) * self.tab.discrete_time
    #     timer_thread = Thread(target=timer, args=(tot_time, self.status_bar))
    #     timer_thread.start()