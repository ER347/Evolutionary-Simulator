import agentpy as ap
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import seaborn as sns
from simargs import *
from simfuncs import *
from arena import *

if vis:
    fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,figsize=(12,8))
    model = Arena()
    fig.set_animated(True)
    fig.tight_layout()
    def simsetup():
        model.setup(consts,repr_args,growth,growth_rate,max_growth)
    simsetup()
    data = model.plane.attr_grid(attr_key = "bloodline", otypes = "f")
    world = ap.gridplot(data,ax=ax1)
    ax1.set(animated=True)
    popL, = ax2.plot(0,0)
    ax2.set(xlabel='t',ylabel='Population size')
    gvL, = ax3.plot(0,0)
    ax3.set(xlabel='t',ylabel='Genetic Variance')
    meL, = ax4.plot(0,0)
    ax4.set(xlabel='t',ylabel='Maximum Energy')
    interval = consts['recording_interval']
    def simstep(frame):
        model.step(consts)
        data = model.plane.attr_grid(attr_key = "bloodline", otypes = "f")
        world.set(data=data)
        if model.t%interval==0 or model.t < 10:
            popL.set_xdata(model.log["t"])
            popL.set_ydata(model.log["population"])
            gvL.set_xdata(model.log["t"])
            gvL.set_ydata(model.log["gen_var"])
            meL.set_xdata(model.log["t"])
            meL.set_ydata(model.log["max_energy"])
            rescale = False
            if model.t%200 ==0 or model.t==1:
                ax2.set_xlim(0,model.t+200)
                ax3.set_xlim(0,model.t+200)
                ax4.set_xlim(0,model.t+200)
                rescale = True
            if model.log["population"][frame//interval]>ax2.get_ylim()[1]:
                ax2.set_ylim(0,model.log["population"][frame//interval]*1.1)
                rescale = True
            if model.log["gen_var"][frame//interval]>ax3.get_ylim()[1]:
                ax3.set_ylim(0,model.log["gen_var"][frame//interval]*1.1)
                rescale = True
            if model.log["max_energy"][frame//interval]>ax4.get_ylim()[1]:
                ax4.set_ylim(0,model.log["max_energy"][frame//interval]*1.1)
                rescale = True
            if rescale:
                fig.canvas.draw()
            return popL, ax1, gvL, meL
        else:
            return ax1,
    ani = animation.FuncAnimation(fig,simstep, interval = 1,blit=True,cache_frame_data=False)
    plt.show()
else:
    model = Arena()
    model.setup(consts,repr_args,growth,growth_rate,max_growth)
    while model.t<=steps and model.population != 0:
        model.step(consts)
        if model.t%(steps//50) == 0:
            print(model.t)
    if model.population == 0:
        print("extinction")
        print(model.t)

    sns.set_theme()
    simdata = pd.DataFrame(model.log)
    fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,figsize=(16,10))
    sns.lineplot(data=simdata,x="t",y="population",ax=ax1)
    sns.lineplot(data=simdata,x="t",y="gen_var",ax=ax2)
    sns.lineplot(data=simdata,x="t",y="num_bloodlines",ax=ax3)
    sns.lineplot(data=simdata,x="t",y="max_energy",ax=ax4)
    fig.tight_layout()
    plt.show()
agents = model.plane.agents.to_list()
data = []
for i in range(len(agents)):
    data.append([i,agents[i].genes])

avgs_list = []
for i in range(1,11):
    singles, clusters = cluster(data,i/10)
    clusterdata,avgs = clustereval(data, clusters)
    avgs_list.append(avgs)
    print(f'iteration: {i-1}')
    print(f'max_diff = {i/10}')    
    print(f'singles: {len(singles)}')
    print(f'clusterdata: {clusterdata}')

save_avgs = input("Save average Genes of clusters? (Yes/No)")
if save_avgs == "Yes":
    num_avg = input("Save average Genes from which iteration?")
    print("Saving average Genes...")
    concatenated_avgs = conc_avgs(avgs_list[int(num_avg)])
    pd.DataFrame(concatenated_avgs).to_csv('ap_output/avgs_out.csv', index=False)
    
pd.DataFrame(model.log).to_csv('ap_output/out.csv', index=False)