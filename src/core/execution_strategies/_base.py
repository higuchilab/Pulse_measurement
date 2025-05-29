from typing import Protocol, Any
from threading import Thread
from abc import abstractmethod

from src.core import CommonParameters
from src.core.measurement_strategies import MeasurementStrategy
from src.core.measurement import TwoTerminalOutput, MeasurementExecutor

class ExecutionStrategy(Protocol):
    def get_parameters(self) -> Any:
        """測定パラメータを取得"""
        pass

    def run_measurement(self, parameters: Any, common_param: CommonParameters, stop_event: Any) -> TwoTerminalOutput:
        strategy = self.get_strategy(parameters)
        executer = MeasurementExecutor(strategy, common_param, stop_event=stop_event)
        return executer.execute()

    def pre_execute(self) -> None:
        """実行前の準備（オプション）"""
        pass

    @abstractmethod
    def get_strategy(self, parameters: Any) -> MeasurementStrategy:
        """測定戦略を取得"""
        pass

    def execute(self, common_param: CommonParameters, stop_event) -> None:
        """測定を実行"""
        self.pre_execute()  # 実行前の準備を呼び出す

        parameters = self.get_parameters()

        def target():
            try:
                self.run_measurement(
                    parameters=parameters,
                    common_param=common_param,
                    stop_event=stop_event
                )
            except Exception as e:
                print(f"Error during execution: {e}")
                raise e
        
        thread = Thread(target=target)
        thread.start()
