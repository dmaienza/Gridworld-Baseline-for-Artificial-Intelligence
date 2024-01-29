import numpy as np
from version6_3 import animate
# import matplotlib.pyplot as plt

start = [0, 0]
goal = [6, 6]

# possible actions
actionUp = 0
actionDown = 1
actionLeft = 2
actionRight = 3
actions = [actionUp, actionDown, actionLeft, actionRight]
world_height = 7
world_width = 7
c = np.array([[0, 0, 0, 0, 0, 0, 0],
              [1, 1, 1, 1, 0, 1, 1],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 1, 1, 1, 1, 1, 1],
              [0, 0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0]])
num_iter = 20
# R1 = np.zeros(num_iter - 1, dtype=int)
# R2 = np.zeros(num_iter - 1, dtype=int)
# d = np.arange(0, num_iter - 1, 1)
num_states = world_height * world_width     # 7*7=49
idx = range(num_states)
V = np.zeros((world_height, world_width))
V_old = V.copy()
gamma = 1


def move(state, action):

    i, j = state

    if action == actionUp:
        state_n = [max(i - 1, 0), j]
    elif action == actionDown:
        state_n = [min(i + 1, world_height - 1), j]
    elif action == actionLeft:
        state_n = [i, max(j - 1, 0)]
    elif action == actionRight:
        state_n = [i, min(j + 1, world_width - 1)]
    else:
        assert False

    # check for obstacles
    if c[state_n[0], state_n[1]] == 1:
        return state
    else:
        return state_n


def reward(state):
    if state == goal:
        return 10
    else:
        return -1


def random_agent(start_state):
    # R = 0
    T = np.zeros((2, 1))
    A = []
    state = start_state
    i = 0
    T[:, i] = state
    while state != goal:
        action_random = np.random.randint(0, 4)
        A.append(action_random)
        state = move(state, action_random)
        # R1[d[i + 1]] = reward(state) + R1[d[i]]
        # print(R1)
        T = np.append(arr=T, values=np.zeros((2, 1)), axis=1)
        # print(T)
        i += 1
        T[:, i] = state
    return T, A # , R


def coord_to_idx(row, col):
    return row * world_width + col


def idx_to_coord(idx):
    col = idx % world_width
    row = idx // world_width
    state = [row, col]
    return state


# Value Function
print("Value Function")
for t in range(num_iter):
    for idx in range(num_states):
        state = idx_to_coord(idx)
        sr, sc = state
        tmp = []
        if state != goal:
            for a in actions:
                sp = move(state, a)
                # R2[t] += reward(sp)
                tmp.append(reward(sp) + gamma * V_old[sp[0], sp[1]])
            V[sr, sc] = max(tmp)
        else:
            V[sr, sc] = 0
    V_old = V
    print(V)
    print("_______________________")

# Policy
P = np.zeros((world_height, world_width))
for idx in range(num_states):
    state = idx_to_coord(idx)
    sr, sc = state
    tmp = []
    for a in actions:
        sp = move(state, a)
        tmp.append(reward(sp) + gamma * V[sp[0], sp[1]])
    idx_best_action = np.argmax(tmp)
    best_action = actions[idx_best_action]
    P[sr, sc] = best_action

print("Policy")
print(P)
print("_______________________")


def path(start_state):
    # R2 = 0
    T = np.zeros((2, 1))
    A = []
    # print(T)
    state = start_state
    i = 0
    T[:, i] = state
    while state != goal:
        a, b = state
        action_policy = P[a, b]
        A.append(action_policy)
        state = move(state, action_policy)
        # R2 += reward(state)
        # R2[d[i]] = reward(state) + R2[d[i-1]]
        # print(R2)
        T = np.append(arr=T, values=np.zeros((2, 1)), axis=1)
        i += 1
        T[:, i] = state
        # print(T)
    return T, A # , R2


# trajectory, action = path(start)
trajectory, action = random_agent(start)
animate(trajectory, goal, action)

# R3 = np.zeros(20)
# for i in range(20):
#     trajectory, R2 = path(start)
#     R3[i] = R2

# plot reward value vs steps
# plt.plot(d, R1, 'o-', color='blue', label="Randomized")
# plt.plot(R2, 'o-', color='red', label="Learning Algorithm")
# plt.title('Sum of Reward During Episode Vs Number of Episodes')
# plt.legend()
# plt.xlabel('Number of Episodes')
# plt.ylabel('Sum of Reward During Episode')
# plt.axvline(x=0, color='red')
# plt.axhline(y=0, color='red')
# plt.show()
