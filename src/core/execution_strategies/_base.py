from typing import Protocol, Any
from threading import Thread

from src.core import CommonParameters
from src.core.measurement_strategies import MeasurementStrategy
from src.core.measurement import TwoTerminalOutput, MeasurementExecutor

class ExecutionStrategy(Protocol):
    def get_parameters(self) -> Any:
        """測定パラメータを取得"""
        pass

    def run_measurement(self, parameters: Any, common_param: CommonParameters) -> TwoTerminalOutput:
        pass

    def pre_execute(self) -> None:
        """実行前の準備（オプション）"""
        pass

    def execute(self, common_param: CommonParameters) -> None:
        """測定を実行"""
        self.pre_execute()  # 実行前の準備を呼び出す

        parameters = self.get_parameters()

        def target():
            try:
                self.run_measurement(
                    parameters=parameters,
                    common_param=common_param
                )
            except Exception as e:
                print(f"Error during execution: {e}")
        
        thread = Thread(target=target)
        thread.start()
