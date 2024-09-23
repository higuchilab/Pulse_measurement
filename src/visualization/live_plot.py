import matplotlib.pyplot as plt
import time

def livegraph(plot, scatter):
    global livegraph_flag, time_list, A_list, V_list

    time.sleep(1.0)
    while 1:
        if livegraph_flag == True:
            break
        time_list_ = time_list

        V_list_ = [V_list[i] for i in range(len(time_list_)-1)] 
        A_list_ = [A_list[i] for i in range(len(time_list_)-1)]
        interval_list = [time_list[i+1]-time_list[i] for i in range(len(time_list)-2)]
        totaltime_list = [sum(interval_list[:i]) for i in range(len(interval_list)+1)]
        
        time.sleep(0.2)
        
        graph(totaltime_list, V_list_, A_list_, True, False)