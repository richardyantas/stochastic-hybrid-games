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


def viz(states, c_actions, u_actions, data_config, disturbs, times):
    T = []
    V = []
    E = []
    r = []
    p = []
    f = []
    v = []
    action_times = list(times)
    action_times.pop()
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

    plt.figure(figsize=(11, 11))
    # plt.style.use(['dark_background'])
    grid = plt.GridSpec(4, 4, wspace=0.8, hspace=0.7)

    plt.subplot(grid[0, :2])
    plt.plot(times, T, 'red', linewidth=0.8, label='Zero Strategy')
    plt.gcf().autofmt_xdate()                       # ?
    plt.ylabel('T(Celsius)')
    plt.xlabel('time(s)')
    plt.legend()
    plt.grid(True)

    plt.subplot(grid[0:1, 2:4])
    plt.plot(times, E, 'red', linewidth=0.8, label="Zero Strategy")
    plt.ylabel('Energy(kJ)')
    plt.xlabel('time(s)')
    plt.legend()
    plt.grid(True)

    plt.subplot(grid[1:3, 0:2])
    plt.plot(V, T, 'black', linewidth=0.5)
    plt.plot(
        [R[1][0], R[1][1], R[1][1], R[1][0], R[1][0]],
        [R[0][0], R[0][0], R[0][1], R[0][1], R[0][0]],
        'red', label="R region")
    plt.plot(
        [S[1][0], S[1][1], S[1][1], S[1][0], S[1][0]],
        [S[0][0], S[0][0], S[0][1], S[0][1], S[0][0]],
        'purple', label="S region")
    #plt.axis([10, 100, 0, 0.4])
    plt.axis([0, 0.4, 10, 100])
    plt.title('zero Strategy')
    plt.ylabel('T(L)')
    plt.xlabel('V(C)')
    plt.legend()
    plt.grid(True)

    # but have shapes (2881,) and (576,)
    plt.subplot(grid[3, :2])
    plt.plot(action_times, r, 'red', linewidth=0.8, label="resistance")
    plt.plot(action_times, f, 'purple', linewidth=0.8, label="exp/comp")
    plt.plot(action_times, p, 'orange', linewidth=0.8, label="piston")
    plt.plot(action_times, v, 'black', linewidth=0.8, label="valve")
    plt.axis([0, data_config["life_time"], 0, 10])
    plt.ylabel('{r,f,p,v}')
    plt.xlabel('time(s)')
    plt.legend()
    plt.grid(True)
    plt.show()

    return


def viz2(states, c_actions, u_actions, data_config, disturbs, mtimes):
    T = []
    V = []
    E = []
    r = []
    p = []
    f = []
    v = []
    times = []
    action_times = []
    for mtime in mtimes:
        times.append(mtime/(60*60))

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
        plt.plot(times, T, 'gold', linewidth=0.8, label='Zero Strategy')
        # plt.gcf().autofmt_xdate()                       # ?
        plt.ylabel('T(C)')
        plt.xlabel('t(hr)')
        plt.legend()
        plt.grid(True, linewidth=0.6, linestyle='--')

        plt.subplot(grid[1, :4])
        plt.plot(times, E, 'tomato', linewidth=0.8, label="Zero Strategy")
        plt.ylabel('E(Kj)')
        plt.xlabel('t(hr)')
        plt.legend()
        plt.grid(True, linewidth=0.6, linestyle='--')
        action_times = list(times)
        action_times.pop()
        print("action times len:", len(action_times), len(r))
        # but have shapes (2881,) and (576,)
        plt.subplot(grid[2, :4])
        plt.plot(action_times, r, 'red', linewidth=0.8,
                 label="resistance", drawstyle='steps')
        plt.plot(action_times, f, 'cyan', linewidth=0.8,
                 label="exp/comp", drawstyle='steps')
        plt.plot(action_times, p, 'orange', linewidth=0.8,
                 label="piston", drawstyle='steps')
        plt.plot(action_times, v, 'yellow', linewidth=0.8,
                 label="valve", drawstyle='steps')
        plt.ylabel('{r,f,p,v}')
        plt.xlabel('t(hr)')
        plt.legend()
        plt.grid(True, linewidth=0.6, linestyle='--')
        plt.show()
    return
