

"""
References: https: // locuslab.github.io/mpc.pytorch/
"""


def plot_safe_behaviour():
    data = SOLAR(args=None)
    start_time = data.config()["start_time"]
    print(start_time)
    model = SWH(data_config=data.config(), disturbs=data.loader_data())
    controller = SMPC_LOCAL(
        data_config=data.config(), disturbs=data.loader_data(), model=model, args=None)
    safe_res = json.load(open(f"{DATA_DIR}/pattern.json"))
    static_data = json.load(open(f"{DATA_DIR}/static_data.json"))
    tau = static_data["tau"]
    nrSteps = controller.get_nrSteps()
    life_time = (24+8)*60  # data.config()["life_time"]
    start_time = (24+6)*60  # data.config()["start_time"]
    state_times = [start_time]
    control_times = []
    u_actions = model.get_uncontrollable_actions()
    state = [0.0, 0.13, 50.0]
    states = [list(state)]
    index = start_time
    set_pattern = []
    for i in range(start_time, life_time):
        if i % (tau) == 0:
            if i + nrSteps*tau >= life_time:  # regresar el tamanio del ultimo patron IMPORTANTE !!!
                break
            controllable_mode = controller.control(state, i)
            control_times.append(i)
        state = model.update(controllable_mode, u_actions[i], state, i)
        state_times.append(i)
        states.append(list(state))
    print("Simulation completed!")
    print("Plotting ..")
    V = [float(states[i][1]) for i in range(0, len(states))]
    T = [float(states[i][2]) for i in range(0, len(states))]
    plt.plot(V, T, linewidth=1.0, color="blue")

    # for i in range(0, 3):
    #     patterns = query_safe_patterns(state)
    #     pattern = patterns[int(len(patterns)/2)]
    #     plt.plot(state[1], state[2], "ro")
    #     for mode in pattern:
    #         for i in range(index, index+tau):
    #             state = model.post(mode, 0, state, i)
    #             states.append(list(state))
    #         index = index + tau
    #     print(pattern)
    #     print(state)
    #     set_pattern.append(list(pattern))
    # colors = ["olive", "deepskyblue", "goldenrod", "cyan"]
    # ind = 0
    # for pat in set_pattern:
    #     print(pat)
    #     l = len(pat)*tau
    #     V = [float(states[i][1])
    #          for i in range(ind, ind + l+1)]  # para que cierre los puntos
    #     T = [float(states[i][2]) for i in range(ind, ind + l+1)]
    #     ind += l
    #     plt.plot(V, T, linewidth=1.0, color=colors.pop(0))

    # plt.axis([0.0, 0.4, 20.0, 90.0])
    plt.plot([R[1][0], R[1][0], R[1][1], R[1][1], R[1][0]], [
             R[0][0], R[0][1], R[0][1], R[0][0], R[0][0]], "gray", linewidth=1.2, linestyle='--', label="R")
    plt.plot([S[1][0], S[1][0], S[1][1], S[1][1], S[1][0]], [
             S[0][0], S[0][1], S[0][1], S[0][0], S[0][0]], "teal", linewidth=0.9, linestyle='--', label="S")
    plt.xlabel("Volume")
    plt.ylabel("Temperature")
    plt.grid(True, linewidth=0.6, linestyle='--')
    plt.savefig(
        './doc/ucsp-mcs-thesis-english-2018/images/safe_post_pattern_perturb.png')
    plt.show()
    # plot states with R, S
    return


# if __name__ == '__main__':
#     plot_safe_behaviour()
