from sthocastic_hybrid_game.src.models.SWH import SWH, R_BOUNDARY, S_BOUNDARY
import matplotlib.pyplot as plt
from matplotlib import style
# https://pyimgui.readthedocs.io/en/latest/guide/first-steps.html (pyImgui)
# https://pyimgui.readthedocs.io/en/latest/reference/imgui.core.html?highlight=plot#imgui.core.plot_histogram

# SWH.get_boundaries = classmethod(SWH.get_boundaries())
# Bound = SWH.get_boundaries()
# R = Bound["R"]
# S = Bound["S"]

#data = s.loader_data()
#time = data["t"]
R = R_BOUNDARY
S = S_BOUNDARY


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
        r.append(c_action[0])
        p.append(c_action[1]+8)
        f.append(c_action[2]+4)
    for u_action in u_actions:
        v.append(u_action+6)

    with plt.style.context('dark_background'):
        fig = plt.figure(figsize=(11, 11))
        fig.canvas.set_window_title('Simulation')
        # fig.suptitle('<Simulation>', fontsize=10)
        # plt.style.use(['dark_background'])
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

        # ctimes.pop()
        #print("action times len:", len(ctimes), len(r))
        # but have shapes (2881,) and (576,)
        plt.subplot(grid[2, :4])
        plt.plot(control_times_hr, r, 'red', linewidth=0.8,
                 label="resistance", drawstyle='steps')
        plt.plot(control_times_hr, f, 'cyan', linewidth=0.8,
                 label="exp/comp", drawstyle='steps')
        plt.plot(control_times_hr, p, 'orange', linewidth=0.8,
                 label="piston", drawstyle='steps')
        plt.plot(control_times_hr, v, 'yellow', linewidth=0.8,
                 label="valve", drawstyle='steps')
        plt.ylabel('{r,f,p,v}')
        plt.xlabel('t(hr)')
        plt.legend()
        plt.grid(True, linewidth=0.6, linestyle='--')
        plt.show()
    return
