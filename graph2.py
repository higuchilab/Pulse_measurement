import matplotlib.pyplot as plt
import time
import algorithm

def graph(x_list, y1_list, y2_list, plot, scatter):
    def para(dic):
        return {f'{k1}.{k2}' : v for k1, d in dic.items() for k2, v in d.items()} 
    config = {
        "font" :{
            "family":"Times New Roman",
            "size":14
            },
        "xtick" :{
                "direction":"in",
                "top":True,
                "major.width":1.2,
                "labelsize":20.0
            },
        "ytick" :{
                "direction":"in",
                "right":True,
                "major.width":1.2,
                "labelsize":20.0
            },
        "axes" :{
            "linewidth":1.2,
            "labelpad":10
            },
        
        "figure" :{
            "dpi":150
                }
        }
    
    plt.rcParams.update(para(config))
    
    fig=plt.figure()
    ax1=fig.add_subplot(2, 1, 1)
    ax2=fig.add_subplot(2, 1, 2)
    
    if plot == True:
        ax1.plot(x_list, y1_list)
        ax2.plot(x_list, y2_list)
    if scatter == True:
        ax1.scatter(x_list, y1_list)
        ax2.scatter(x_list, y2_list)
    
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("Input Voltage [V]")
    ax2.set_xlabel("Time [s]")
    ax2.set_ylabel("Output Current [A]")
    plt.show()

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

class Graph_input():
    def _init_(self,V_list,time_list):
        self.V_list = V_list
        self.time_list = time_list


    

