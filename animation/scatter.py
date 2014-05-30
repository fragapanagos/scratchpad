import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

rate = 1e3
nneurons = 32 
dt = .01

t = []
spk_idx = []

fig = plt.figure()
ax = plt.axes()
dots, = ax.plot([], [], 'bo', ms=6)

def init():
    t.append(0.)
    spk_idx.append(0)
    ax.set_xlim(0,3)
    ax.set_ylim(0,nneurons)
    dots.set_data([], [])
    return dots, ax

def animate(i):
    global t
    global spk_idx
    t.append(dt + t[-1])
    spk_idx.append(np.random.randint(0,nneurons))
    if t[-1] - t[0] > 3.:
        idx = np.argmax(t[-1] - np.array(t) < 3.)
        t = t[idx:]
        spk_idx = spk_idx[idx:]
    dots.set_data(t, spk_idx)
    if t[-1]>3.:
        ax.set_xlim(t[0],t[-1])
    return dots, ax

ani = animation.FuncAnimation(fig, animate, frames=600, 
                              interval=0, blit=True, init_func=init)

plt.show()
