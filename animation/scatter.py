import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import time
import thread

rate = 1e3
nneurons = 32 
dt = .01

spk_t = [0.]
spk_idx = [-1]

fig = plt.figure()
ax = plt.axes()
txt = ax.text(1.5, nneurons-1, '', fontsize=14, bbox=dict(facecolor='white', alpha=0.5))
dots, = ax.plot([], [], 'bo', ms=6)

def init():
    ax.set_ylim(0,nneurons)
    ax.set_xlim([0,3])
    ax.set_xticks([])
    ax.set_xticklabels([])

    dots.set_data([], [])

    return dots, ax, txt

def animate(i, spk_t, spk_idx):
    spk_t.append(dt + spk_t[-1])
    spk_idx.append(np.random.randint(0,nneurons))
    clip_idx = 0
    while spk_t[-1] - spk_t[clip_idx] > 3.:
        clip_idx += 1
    if clip_idx > 0:
        spk_t = spk_t[clip_idx:]
        spk_idx = spk_idx[clip_idx:]
    dots.set_data(np.array(spk_t)-spk_t[0], spk_idx)

    txt.set_text("T = %.1f"%spk_t[-1])
    return dots, txt, 

ani = animation.FuncAnimation(fig, animate, frames=600, fargs=(spk_t, spk_idx),
                              interval=0, blit=True, init_func=init)

plt.show()
