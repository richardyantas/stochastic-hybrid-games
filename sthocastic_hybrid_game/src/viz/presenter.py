import matplotlib.pyplot as plt
import matplotlib.dates as md


def plot(data):
    T = []
    V = []
    E = []
    r = []
    p = []
    v = []
    time = []
    for i in data["s"]:  # we chat the offspring ..
        T.append(i.T)
        V.append(i.V)
        E.append(i.E)
        time.append(i.t)
    for i in data["a"]:
        r.append(i.r)
        p.append(i.p+4)
        v.append(i.v+2)
    plt.figure(figsize=(11, 11))
    grid = plt.GridSpec(4, 4, wspace=0.8, hspace=0.7)
    plt.subplot(grid[0, :2])
    plt.plot(time, T, 'red', linewidth=0.8, label='Zero Strategy')
    plt.gcf().autofmt_xdate()                       # ?
    plt.ylabel('T(Celsius)')
    plt.xlabel('time(s)')
    plt.legend()
    plt.grid(True)
    plt.subplot(grid[0:1, 2:4])
    plt.plot(time, E, 'red', linewidth=0.8, label="Zero Strategy")
    plt.ylabel('Energy(kJ)')
    plt.xlabel('time(s)')
    plt.legend()
    plt.grid(True)
    plt.subplot(grid[1:3, 0:2])
    plt.plot(V, T, 'black', linewidth=0.5)
    plt.plot([R[0][0], R[0][0], R[0][1], R[0][1], R[0][0]],
             [R[1][0], R[1][1], R[1][1], R[1][0], R[1][0]],
             'red', label="R region")
    plt.plot([S[0][0], S[0][0], S[0][1], S[0][1], S[0][0]],
             [S[1][0], S[1][1], S[1][1], S[1][0], S[1][0]],
             'purple', label="S region")
    # plt.axis([10,100,0,0.4])
    plt.axis([0, 0.4, 10, 100])
    plt.title('zero Strategy')
    plt.ylabel('T(L)')
    plt.xlabel('V(C)')
    plt.legend()
    plt.grid(True)
    # but have shapes (2881,) and (576,)
    plt.subplot(grid[3, :2])
    plt.plot(time, r, 'red', linewidth=0.8, label="resistance")
    plt.plot(time, v, 'purple', linewidth=0.8, label="valve")
    plt.plot(time, p, 'orange', linewidth=0.8, label="piston")
    plt.axis([0, data["H"], 0, 8])
    plt.ylabel('{r,v,p}')
    plt.xlabel('time(s)')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot2(data, data2):
    T = []
    V = []
    E = []
    r = []
    p = []
    v = []

    T2 = []
    V2 = []
    E2 = []
    r2 = []
    p2 = []
    v2 = []

    time = []
    for i in data["s"]:
        T.append(i.T)
        V.append(i.V)
        E.append(i.E)
        time.append(i.t)

    for i in data["a"]:
        r.append(i.r)
        p.append(i.p+4)
        v.append(i.v+2)

    for i in data2["s"]:
        T2.append(i.T)
        V2.append(i.V)
        E2.append(i.E)

    for i in data2["a"]:
        r2.append(i.r)
        p2.append(i.p+4)
        v2.append(i.v+2)

    plt.figure(figsize=(11, 11))
    grid = plt.GridSpec(4, 4, wspace=0.8, hspace=0.7)
    plt.subplot(grid[0, :2])
    plt.plot(time, T, 'red', linewidth=0.8, label='Zero Strategy')
    plt.plot(time, T2, 'purple', linewidth=0.8, label='Learned Strategy')
    # plt.gcf().autofmt_xdate()                       # ?
    plt.ylabel('T(Celsius)')
    plt.xlabel('time(s)')
    plt.legend()
    plt.grid(True)
    plt.subplot(grid[0:1, 2:4])
    plt.plot(time, E, 'red', linewidth=0.8, label="No Strategy")
    plt.plot(time, E2, 'purple', linewidth=0.8, label="Learned Strategy")
    plt.ylabel('Energy(kJ)')
    plt.xlabel('time(s)')
    plt.legend()
    plt.grid(True)
    plt.subplot(grid[1:3, 0:2])
    plt.plot(V, T, 'black', linewidth=0.5)
    plt.plot([R[0][0], R[0][0], R[0][1], R[0][1], R[0][0]],
             [R[1][0], R[1][1], R[1][1], R[1][0], R[1][0]],
             'red', label="R region")
    plt.plot([S[0][0], S[0][0], S[0][1], S[0][1], S[0][0]],
             [S[1][0], S[1][1], S[1][1], S[1][0], S[1][0]],
             'purple', label="S region")
    # plt.axis([10,100,0,0.4])
    plt.axis([0, 0.4, 10, 100])
    plt.title('No Strategy')
    plt.ylabel('Temperature(C)')
    plt.xlabel('Volume(L)')
    plt.legend()
    plt.grid(True)
    plt.subplot(grid[1:3, 2:4])
    plt.plot(V2, T2, 'black', linewidth=0.5)
    plt.plot([R[0][0], R[0][0], R[0][1], R[0][1], R[0][0]],
             [R[1][0], R[1][1], R[1][1], R[1][0], R[1][0]],
             'red', label="R region")
    plt.plot([S[0][0], S[0][0], S[0][1], S[0][1], S[0][0]],
             [S[1][0], S[1][1], S[1][1], S[1][0], S[1][0]],
             'purple', label="S region")
    # plt.axis([10,100,0,0.4])
    plt.axis([0, 0.4, 10, 100])
    plt.title('Learned Strategy')
    plt.ylabel('Temperature(C)')
    plt.xlabel('Volume(L)')
    plt.legend()
    plt.grid(True)
    # but have shapes (2881,) and (576,)
    plt.subplot(grid[3, :2])
    plt.plot(time, r, 'red', linewidth=0.8)
    plt.plot(time, v, 'purple', linewidth=0.8)
    plt.plot(time, p, 'orange', linewidth=0.8)
    plt.axis([0, data["H"], 0, 8])
    plt.ylabel('{r,v,p}')
    plt.xlabel('time(s)')
    plt.legend()
    plt.grid(True)
    plt.subplot(grid[3, 2:4])
    plt.plot(time, r2, 'red', linewidth=0.8, label="resistance")
    plt.plot(time, v2, 'purple', linewidth=0.8, label="valve")
    plt.plot(time, p2, 'orange', linewidth=0.8, label="piston")
    plt.axis([0, data2["H"], 0, 8])
    plt.ylabel('{r,v,p}')
    plt.xlabel('time(s)')
    plt.legend()
    plt.grid(True)
    plt.show()


valvesGeneration()
B = automaton()
data2 = B.simulation("uppaal")
A = automaton()
data = A.simulation("normal")
plot2(data, data2)
# plot(data)
