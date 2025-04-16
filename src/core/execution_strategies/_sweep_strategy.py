from threading import Thread
from src.gui.widgets import TabSweep
from src.core.measurement import CommonParameters, MeasurementExecutor
from src.core.data_processing import SweepParam

from src.core.execution_strategies._base import ExecutionStrategy
from src.core.measurement_strategies import SweepMeasurementStrategy

class SweepExecutionStrategy(ExecutionStrategy):
    def __init__(self, tab_instance: TabSweep):
        self.tab = tab_instance

    def get_parameters(self) -> SweepParam:
            # measure_type_index = fetch_measure_type_index("2-terminal I-Vsweep")      
        return SweepParam(
            mode=self.tab.sweep_mode,
            top_voltage=self.tab.top_voltage,
            bottom_voltage=self.tab.bottom_voltage,
            voltage_step=self.tab.voltage_step,
            loop=self.tab.loop,
            tick_time=self.tab.tick
        )
    
    def run_measurement(parameters, common_param: CommonParameters):
        strategy = SweepMeasurementStrategy(parameters)
        executor = MeasurementExecutor(strategy, common_param)
        return executor.execute()
