import numpy as np
from typing import Literal
from numpy.typing import NDArray

def use_narma_dataset(use_database: bool, model: Literal["narma2", "narma10"], steps: int=None, input_range_bot: float=None, input_range_top: float=None) -> tuple[NDArray, NDArray, NDArray, NDArray]:
    """
    NARMAデータセットを使う

    Parameters
    ----------
    use_database: bool
        データベースから呼び出すかどうか
    model: 'narma2', 'narma10'
        モデル選択
    steps: int
        離散時間数
    input_range_bot: float
        入力値の下限
    input_range_top: float
        入力値の上限

    Returns
    -------
    u_train: NDArray
        入力配列(訓練用)
    y_train: NDArray
        出力配列(訓練用)
    u_test: NDArray
        入力配列(テスト用)
    u_test: NDArray
        出力配列(テスト用)
    """
    if use_database:
        return call_narma_dataset()

    return generate_narma_dataset(model, steps, input_range_bot, input_range_top)



def generate_narma2(u: NDArray[np.float64], steps: int) -> NDArray[np.float64]:
    y = np.zeros(steps)
    for t in range(10, steps):
        y[t] = 0.4 * y[t-1] + 0.4 * y[t-1] * y[t-2] + 0.6 * u[t-1] ** 3 + 0.1
    return y


def generate_narma10(u: NDArray[np.float64], steps: int) -> NDArray[np.float64]:
    y = np.zeros(steps)
    for t in range(10, steps):
        y[t] = 0.3 * y[t-1] + 0.05 * y[t-1] * sum(y[t-i-1] for i in range(10)) + 1.5 * u[t-10] * u[t-1] + 0.1
    return y


def generate_narma_dataset(model: Literal["narma2", "narma10"], steps: int, input_range_bot: float, input_range_top: float) -> tuple[NDArray, NDArray, NDArray, NDArray]:
    """
    NARMAデータセットを作成する

    Attributes
    ----------
    model: 'narma2', 'narma10'
        モデル選択
    steps: int
        離散時間数
    input_range_bot: float
        入力値の下限
    input_range_top: float
        入力値の上限

    Returns
    -------
    u_train: NDArray
        入力配列(訓練用)
    y_train: NDArray
        出力配列(訓練用)
    u_test: NDArray
        入力配列(テスト用)
    u_test: NDArray
        出力配列(テスト用)
    """

    if model not in ["narma2", "narma10"]:
        raise ValueError(f"Invalid model: {model}. Allowed values are 'narma2', 'narma10'.")

    u = np.random.uniform(input_range_bot, input_range_top, steps)

    # NARMAデータの生成
    if model == "narma2":
        y = generate_narma2(u, steps)

    if model == "narma10":
        y = generate_narma10(u, steps)

    #訓練データとテストデータに分割
    train_size = int(steps * 0.8)  # 80%を訓練データに

    u_train, u_test = u[:train_size], u[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    print("訓練データのサイズ:", len(u_train))
    print("テストデータのサイズ:", len(u_test))

    return u_train, y_train, u_test, y_test


def call_narma_dataset() -> tuple[NDArray, NDArray, NDArray, NDArray]:
    pass