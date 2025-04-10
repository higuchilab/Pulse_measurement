from threading import Thread

from src.gui.widgets import TabPulse, Statusbar
from src.core import pulse_run
from src.core.measurement import CommonParameters
from src.core.measurement import PulseParameters
from src.utils import timer

from src.core.execution_strategies._base import ExecutionStrategy


class PulseExecutionStrategy(ExecutionStrategy):
    def __init__(self, tab_instance: TabPulse, status_bar: Statusbar):
        self.tab = tab_instance
        self.status_bar = status_bar

    def get_parameters(self) -> PulseParameters:
            # measure_type_index = fetch_measure_type_index(2-terminal Pulse")        
        return {
            'measure_blocks': self.tab.pulse_blocks
        }

    def pre_execute(self) -> None:
        standarded_pulse_blocks = self.tab.pulse_blocks.export_standarded_blocks()
        tot_time = sum((block.top_time + block.base_time) * block.loop + block.interval 
                      for block in standarded_pulse_blocks)
        
        timer_thread = Thread(target=timer, args=(tot_time, self.status_bar))
        timer_thread.start()

    def execute(self, parameters: PulseParameters, common_param: CommonParameters) -> None:
        def target(parameters, common_param):
            try:
                pulse_run(parameters, common_param)
            except Exception as e:
                print(f"Error in Pulse execution: {e}")

        thread = Thread(target=target, args=(parameters, common_param))
        thread.start()
