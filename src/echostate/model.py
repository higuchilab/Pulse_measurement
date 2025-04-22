import numpy as np
from typing import Literal
from numpy.typing import NDArray

# def use_echostate_input_array(use_database: bool, model: Literal["echostate2", "echostate10"], steps: int=None, input_range_bot: float=None, input_range_top: float=None) -> NDArray:
#     """
#     echostateデータセットを使う

#     Parameters
#     ----------
#     use_database: bool
#         データベースから呼び出すかどうか
#     model: 'narma2', 'narma10'
#         モデル選択
#     steps: int
#         離散時間数
#     input_range_bot: float
#         入力値の下限
#     input_range_top: float
#         入力値の上限

#     Returns
#     -------
#     u: NDArray
#         入力配列
#     y: NDArray
#         出力配列
#     """

#     return generate_echostate_dataset(model, steps, input_range_bot, input_range_top)


def generate_echostate_input_array(
        steps: int, 
        inner_loop_num: int, 
        outer_loop_num: int,
        top_voltage: float,
        base_voltage: float
    ) -> NDArray:
    """
    echostateデータセットを作成する

    Attributes
    ----------
    model: 'echostate2', 'echostate10'
        モデル選択
    steps: int
        離散時間数
    input_range_bot: float
        入力値の下限
    input_range_top: float
        入力値の上限

    Returns
    -------
    u: NDArray
        入力配列
    """    
    # echostate_templete_id = append_record_echostate_templetes(param=(steps, input_range_top, input_range_bot))

    u = np.random.choice([top_voltage, base_voltage], steps)
    inner_array = np.tile(u, inner_loop_num)
    outer_array = np.tile(inner_array, outer_loop_num)

    return outer_array
