from threading import Thread
from src.gui.widgets import TabSweep
from src.core import sweep_run
from src.core.measurement import CommonParameters
from src.core.measurement import SweepParam

from _interface import ExecutionStrategy

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

    def execute(self, parameters: SweepParam, common_param: CommonParameters) -> None:
        def target(parameters, common_param):
            try:
                sweep_run(parameters, common_param)
            except Exception as e:
                print(f"Error in Sweep execution: {e}")
        
        thread = Thread(target=target, args=(parameters, common_param))
        thread.start()
