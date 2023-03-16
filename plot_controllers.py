import csv
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from mpc.models.SWH import SWH, R_BOUNDARY, S_BOUNDARY
from mpc.data.base_data_module import BaseDataModule

DATA_DIR = BaseDataModule.data_dirname()

# https://pyimgui.readthedocs.io/en/latest/guide/first-steps.html (pyImgui)
# https://pyimgui.readthedocs.io/en/latest/reference/imgui.core.html?highlight=plot#imgui.core.plot_histogram
# If we want to draw dynamically
# Generally seems like create another thread an draw in parallel to send the data.
# Tinker https://stackoverflow.com/questions/5618620/create-dynamic-updated-graph-with-python
# https://stackoverflow.com/questions/10944621/dynamically-updating-plot-in-matplotlib
# SWH.get_boundaries = classmethod(SWH.get_boundaries())
# Bound = SWH.get_boundaries()
# R = Bound["R"]
# S = Bound["S"]
# data = s.loader_data()
# time = data["t"]

R = R_BOUNDARY
S = S_BOUNDARY


def preprocess_time_hr_24_after(times):
    return [float((t-24*60)/60) for t in times]


def plot_controllers_results():
    data = BaseDataModule()
    data_config = data.config()
    life_time = data_config["life_time"]
    start_time = data_config["start_time"]
    greedy = pd.read_csv(f"{DATA_DIR}/results_MPC.Greedy_data.csv")
    uppaal = pd.read_csv(f"{DATA_DIR}/results_MPC.Uppaal_data.csv")
    static_data = json.load(open(f"{DATA_DIR}/static_data.json"))
    set_point = static_data["Tg"]
    num_actions = static_data["num_actions"]
    standard_deviation = static_data["standard_deviation"]
    with open(f"{DATA_DIR}/uncontrollable_data_{standard_deviation}_{num_actions}.txt", 'r', newline='') as file:
        lines = file.readlines()
    u_actions = [float(line[0:-1]) for line in lines]
    u_actions = u_actions[start_time:start_time+len(greedy["t"])]
    # with plt.style.context('dark_background'): #ggplot

    ######### time preprocess to visualize #########
    time_plot = preprocess_time_hr_24_after(greedy["t"])
    start_time = float(start_time-24*60)/60
    life_time = float(life_time-24*60)/60
    ################################################

    ############### figure 1 #############################
    mean_T1 = 0
    mean_T2 = 0
    l = len(greedy["T"])
    for i in range(0, l):
        mean_T1 = mean_T1 + abs(greedy["T"][i]-55)
        mean_T2 = mean_T2 + abs(uppaal["T"][i]-55)
    print("Mean Temperature greedy: ", mean_T1/l)
    print("Mean Temperature uppaal: ", mean_T2/l)

    plt.axis([start_time, life_time, 0, 80])
    plt.plot(time_plot, greedy["T"], 'cyan',
             linewidth=0.8, label='Greedy')
    plt.plot(time_plot, uppaal["T"], 'red',
             linewidth=0.8, label='Uppaal')
    # plt.plot([start_time, life_time], [set_point, set_point], 'cyan',
    #          linewidth=0.4)
    plt.ylabel('Temperature(C)')
    plt.xlabel('time[hrs]')
    plt.legend()
    plt.grid(True, linewidth=0.6, linestyle='--')
    plt.savefig(
        './doc/ucsp-mcs-thesis-english-2018/images/controllers1.png')
    plt.show()

    ############### figure 2 #############################
    # mean_E = 0
    # l = len(smpc_local["E"])
    # for i in range(0, l):
    #     mean_E = mean_E + smpc_local["E"][i]-sompc_uppaal["E"][i]
    Ea = list(greedy["E"])
    Eb = list(uppaal["E"])
    print("Saved Energy: ", abs(Eb[-1]-Ea[-1]))

    plt.axis([start_time, life_time, 0, 25000])
    plt.plot(time_plot, greedy["E"], 'cyan',
             linewidth=0.8, label='Greedy')
    plt.plot(time_plot, uppaal["E"], 'red',
             linewidth=0.8, label='Uppaal')
    # plt.plot([start_time, life_time], [set_point, set_point], 'cyan',
    #          linewidth=0.4)
    plt.ylabel('Energy(KJ)')
    plt.xlabel('time[hrs]')
    plt.legend()
    plt.grid(True, linewidth=0.6, linestyle='--')
    plt.savefig(
        './doc/ucsp-mcs-thesis-english-2018/images/energycomparison.png')
    plt.show()
    ############### figure 3 #############################
    plt.figure(figsize=(10, 2))
    plt.axis([start_time, life_time, 0, 5])
    plt.plot(time_plot, u_actions, 'cyan', linewidth=0.8,
             label="valve", drawstyle='steps')
    plt.ylabel('Valve event')
    plt.xlabel('time[hrs]')
    plt.legend()
    plt.grid(True, linewidth=0.6, linestyle='--')
    plt.savefig(
        './doc/ucsp-mcs-thesis-english-2018/images/uncontrollable.png')
    plt.show()
    ############### figure 4 #############################
    with plt.style.context('dark_background'):  # ggplot
        fig = plt.figure(num='Simulation', figsize=(11, 11))
        grid = plt.GridSpec(4, 4, wspace=0.8, hspace=0.7)
        plt.subplot(grid[0:2, :4])
        plt.axis([start_time, life_time, 0, 80])
        plt.plot(time_plot, greedy["T"], 'cyan',
                 linewidth=0.8, label='Greedy')
        plt.plot(time_plot, uppaal["T"], 'red',
                 linewidth=0.8, label='Uppaal')
        # plt.plot([start_time, life_time], [set_point, set_point], 'cyan',
        #          linewidth=0.4)
        plt.ylabel('Temperature(C)')
        plt.xlabel('time[hrs]')
        plt.legend()
        plt.grid(True, linewidth=0.6, linestyle='--')

        plt.subplot(grid[2, :4])
        plt.plot(time_plot, greedy["E"], 'cyan',
                 linewidth=0.8, label="Greedy")
        plt.plot(time_plot, uppaal["E"], 'red',
                 linewidth=0.8, label="Uppaal")
        plt.ylabel('Energy[KJ]')
        plt.xlabel('time[hrs]')
        plt.legend()
        plt.grid(True, linewidth=0.6, linestyle='--')
        # plt.subplot(grid[2, :4])
        # plt.plot(smpc_local["t"], smpc_local["r"], 'red', linewidth=0.8,
        #          label="resistance", drawstyle='steps')
        # plt.plot(smpc_local["t"], smpc_local["f"], 'cyan', linewidth=0.8,
        #          label="exp/comp", drawstyle='steps')
        # plt.plot(smpc_local["t"], smpc_local["p"], 'orange', linewidth=0.8,
        #          label="piston", drawstyle='steps')
        # plt.ylabel('{r,f,p,v}')
        # plt.xlabel('t(hr)')
        # plt.legend()
        # plt.grid(True, linewidth=0.6, linestyle='--')

        # load other file
        plt.subplot(grid[3, :4])
        plt.plot(time_plot, u_actions, 'cyan', linewidth=0.8,
                 label="valve", drawstyle='steps')
        plt.ylabel('Valve event')
        plt.xlabel('time[hrs]')
        plt.legend()
        plt.grid(True, linewidth=0.6, linestyle='--')
        plt.show()
    return


def viz2(states, c_actions, u_actions, data_config, disturbs, control_times, state_times):
    T = []
    V = []
    E = []
    r = []
    p = []
    f = []
    v = []
    control_times_hr = []
    state_times_hr = []
    for time in control_times:
        control_times_hr.append(time/(60))
    for time in state_times:
        state_times_hr.append(time/(60))

    for state in states:  # we chat the offspring ..
        T.append(state[2])
        V.append(state[1])
        E.append(state[0])
    for c_action in c_actions:
        r.append(c_action[1])
        p.append(c_action[0]+8)
        f.append(c_action[2]+4)
    for u_action in u_actions:
        v.append(u_action)

    with plt.style.context('dark_background'):
        fig = plt.figure(num='Simulation', figsize=(11, 11))
        grid = plt.GridSpec(4, 4, wspace=0.8, hspace=0.7)

        plt.subplot(grid[0, :4])
        plt.plot(state_times_hr, T, 'gold',
                 linewidth=0.8, label='Zero Strategy')
        # plt.gcf().autofmt_xdate()                       # ?
        plt.ylabel('T(C)')
        plt.xlabel('t(hr)')
        plt.legend()
        plt.grid(True, linewidth=0.6, linestyle='--')

        plt.subplot(grid[1, :4])
        plt.plot(state_times_hr, E, 'tomato',
                 linewidth=0.8, label="Zero Strategy")
        plt.ylabel('E(Kj)')
        plt.xlabel('t(hr)')
        plt.legend()
        plt.grid(True, linewidth=0.6, linestyle='--')

        plt.subplot(grid[2, :4])
        plt.plot(control_times_hr, r, 'red', linewidth=0.8,
                 label="resistance", drawstyle='steps')
        plt.plot(control_times_hr, f, 'cyan', linewidth=0.8,
                 label="exp/comp", drawstyle='steps')
        plt.plot(control_times_hr, p, 'orange', linewidth=0.8,
                 label="piston", drawstyle='steps')
        plt.ylabel('{r,f,p,v}')
        plt.xlabel('t(hr)')
        plt.legend()
        plt.grid(True, linewidth=0.6, linestyle='--')

        plt.subplot(grid[3, :4])
        plt.plot(state_times_hr, v, 'yellow', linewidth=0.8,
                 label="valve", drawstyle='steps')

        plt.grid(True, linewidth=0.6, linestyle='--')
        plt.show()
    return


if __name__ == '__main__':
    plot_controllers_results()
