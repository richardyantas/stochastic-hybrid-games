import numpy as np
import random
import matplotlib.pyplot as plt

# plt.axis([0, 1, 0, 1])

# for i in range(100):
#     y = np.random.random()
#     x = np.random.random()
#     plt.plot(i, y, '-ok', color='black')
#     plt.pause(0.05)
# plt.show()


'''
  Quizas se puede simular cocina, ducha, banio, 
  recordar que es en cualquier momento, no necesarimente durante el evento de control
'''
TAU = 5
dt = 1
life_time = 24*60

U_MODES = (np.zeros(int(life_time/int(TAU)))).tolist()
num_actions = random.randrange(5, 8)
standard_deviation = 1*3  # 1*60/5
for i in range(0, num_actions):
    U_MODES[int(random.gauss(7*60/5, standard_deviation))] = 1
    U_MODES[int(random.gauss(13*60/5, standard_deviation))] = 1
    U_MODES[int(random.gauss(19*60/5, standard_deviation))] = 1

plt.axis([0, 1440/5, 0, 10])
plt.plot(U_MODES, drawstyle='steps', linewidth=0.8)
plt.grid(True, linewidth=0.6, linestyle='--')
plt.show()

print("umodes:", len(U_MODES))
