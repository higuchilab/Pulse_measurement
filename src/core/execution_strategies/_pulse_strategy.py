from src.gui.widgets import TabPulse, Statusbar
from src.core.measurement import CommonParameters, MeasurementExecutor
from src.core.measurement_model import PulseParameters

from src.core.execution_strategies._base import ExecutionStrategy
from src.core.measurement_strategies import PulseMeasurementStrategy


class PulseExecutionStrategy(ExecutionStrategy):
    def __init__(self, tab_instance: TabPulse, status_bar: Statusbar):
        self.tab = tab_instance
        self.status_bar = status_bar

    def get_parameters(self) -> PulseParameters:
            # measure_type_index = fetch_measure_type_index(2-terminal Pulse")        
        return {
            'measure_blocks': self.tab.pulse_blocks
        }
    
    def get_strategy(self, parameters) -> PulseMeasurementStrategy:
        return PulseMeasurementStrategy(parameters)
    
    def get_total_time(self) -> None:
        standarded_pulse_blocks = self.tab.pulse_blocks.export_standarded_blocks()
        tot_time = sum((block.top_time + block.base_time) * block.loop + block.interval 
                      for block in standarded_pulse_blocks)
        
        return tot_time
