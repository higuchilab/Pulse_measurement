import numpy as np
from numpy.testing import assert_array_equal
from src.echostate.model import generate_echostate_input_array
from src.core.data_processing import EchoStateParam

def test_generate_echostate_input_array():
    # ランダム性を排除するために乱数シードを設定
    np.random.seed(42)

    # テスト用のパラメータを設定
    param = EchoStateParam(
        top_voltage=0.8,
        base_voltage=0.0,
        discrete_time=3,
        inner_loop_num=3,
        outer_loop_num=2,
    )

    # 関数を実行
    result = generate_echostate_input_array(param)

    # 期待される出力を作成
    expected = np.array(
        [
            [0.8, 1, 0, 0],
            [0., 2, 0, 0],
            [0.8, 3, 0, 0],
            [0.8, 4, 1, 0],
            [0., 5, 1, 0],
            [0.8, 6, 1, 0],
            [0.8, 7, 2, 0],
            [0., 8, 2, 0],
            [0.8, 9, 2, 0],
            [0.8, 10, 0, 1],
            [0., 11, 0, 1],
            [0.8, 12, 0, 1],
            [0.8, 13, 1, 1],
            [0., 14, 1, 1],
            [0.8, 15, 1, 1],
            [0.8, 16, 2, 1],
            [0., 17, 2, 1],
            [0.8, 18, 2, 1],
        ]
    )

    # 結果を検証
    print(f"result: {result}")
    assert result.shape == expected.shape, "結果の形状が期待値と異なります"
    assert_array_equal(result, expected, f"結果の内容が期待値と異なります\n{result} != {expected}")
