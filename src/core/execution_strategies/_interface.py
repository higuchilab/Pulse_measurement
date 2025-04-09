from typing import Protocol, Any
from src.core import CommonParameters

class ExecutionStrategy(Protocol):
    def get_parameters(self) -> Any:
        """測定パラメータを取得"""
        pass

    def execute(self, parameters: Any, common_param: CommonParameters) -> None:
        """測定を実行"""
        pass

    def pre_execute(self) -> None:
        """実行前の準備（オプション）"""
        pass
