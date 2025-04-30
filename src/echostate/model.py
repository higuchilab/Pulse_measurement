import numpy as np
from typing import Literal
from numpy.typing import NDArray

from src.core.data_processing import EchoStateParam


def generate_echostate_input_array(
        param: EchoStateParam,
    ) -> NDArray:
    """
    echostate入力配列を生成する関数

    Attributes
    ----------
    param: EchoStateParam
        パラメータクラス

    Returns
    -------
    result: NDArray
        多次元配列
        - 各行が [input_voltage, discrete_time, inner_loop_idx, outer_loop_idx] の形
    """
    u = np.random.choice([param.top_voltage, param.base_voltage], param.discrete_time)
    inner_array = np.tile(u, param.inner_loop_idx)
    outer_array = np.tile(inner_array, param.outer_loop_idx)

    total_length = param.discrete_time * param.inner_loop_idx * param.outer_loop_idx
    discrete_time = np.arange(1, total_length + 1)
    inner_loop_idx = np.repeat(np.arange(param.inner_loop_idx), param.discrete_time)
    inner_loop_idx = np.tile(inner_loop_idx, param.outer_loop_idx)
    outer_loop_idx = np.repeat(np.arange(param.outer_loop_idx), param.discrete_time * param.inner_loop_idx)

    result = np.stack([outer_array, discrete_time, inner_loop_idx, outer_loop_idx], axis=1)

    return result
