import time
from .data_processing import graph, TwoTerminalOutput
from .measurement_model import MeasureModelTemplete

cdef TwoTerminalOutput measure(MeasureModelTemplete measure_model, void dev):
    V_list = []
    A_list = []
    time_list = []

    start_perfcounter = time.perf_counter()
    target_time = 0.0
    for voltage in measure_model.input_V_list:
        while True:
            elapsed_time = time.perf_counter() - start_perfcounter

            if elapsed_time >= target_time:
                dev.write(f"SOV{voltage}")
                dev.write("*TRG")
                time_list.append(time.perf_counter() - start_perfcounter)
                
                A=dev.query("N?")
                A_=float(A[3:-2])
                A_list.append(A_)
                
                V=dev.query("SOV?")
                V_=float(V[3:-2])
                V_list.append(V_)
                target_time += measure_model.tick
                break
        
        graph(time_list, V_list, A_list)

    output_data = TwoTerminalOutput(voltage=V_list, current=A_list, time=time_list)

    return output_data
