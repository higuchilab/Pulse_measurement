import pandas as pd
from pandas import Series
from numpy.typing import NDArray

def generate_imaginary_nodes(output_current: NDArray, input_voltages: NDArray, interval_number: int, node_number: int) -> Series:
    """
    出力電流から仮想ノードを生成する

    Parameters
    ----------
    output_current: NDArray
        リザバーの出力電流
    input_voltages: NDArray
        入力電圧のリスト
    interval_number: int
        1周期のデータ数
    node_number: int
        作成する仮想ノードの数

    Returns
    -------
    node_outputs_df: Series
        入力電圧に対する各ノードの出力値
    """
    if interval_number < 0:
        raise ValueError(f"interval_number: {interval_number} must be NATURAL number")
    
    if node_number < 0:
        raise ValueError(f"node_number: {node_number} must be NATURAL number")

    if interval_number < node_number:
        raise ValueError(f"The node_number: {node_number} must be SMALLER than the interval_number: {interval_number}.")

    columns = ["input"] + ["Node" + str(node) for node in range(node_number)]
    node_outputs_df = pd.DataFrame(columns=columns)

    for i, input_voltage in enumerate(input_voltages):
        nodes_output = [output_current[int(interval_number / node_number * node) + (interval_number * i)] for node in range(node_number)]
        new_row_df = pd.DataFrame([[input_voltage] + nodes_output], columns=columns)

        node_outputs_df = pd.concat([node_outputs_df, new_row_df], ignore_index=True)
    return node_outputs_df