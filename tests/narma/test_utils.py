import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

from src.narma.utils import generate_imaginary_nodes

def test_generate_imaginary_nodes():
    
    d = {"input": [0, 0.1, 0.2, 0.3, 0.4],
         "Node0": [0.0, 1.0, 2.0, 3.0, 4.0],
         "Node1": [0.3, 1.3, 2.3, 3.3, 4.3],
         "Node2": [0.6, 1.6, 2.6, 3.6, 4.6]
        }

    output_current = np.arange(0, 5.0, 0.1)
    input_voltages = np.arange(0, 0.5, 0.1)
    output = generate_imaginary_nodes(output_current, input_voltages, 10, 3)
    assert_frame_equal(output, pd.DataFrame(d))