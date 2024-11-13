import matplotlib.pyplot as plt
import time

def graph(x_list, y1_list, y2_list):
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
    
    # if plot == True:
    ax1.plot(x_list, y1_list)
    ax2.plot(x_list, y2_list)
    # if scatter == True:
    #     ax1.scatter(x_list, y1_list)
    #     ax2.scatter(x_list, y2_list)
    
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("Input Voltage [V]")
    ax2.set_xlabel("Time [s]")
    ax2.set_ylabel("Output Current [A]")
    plt.show()
