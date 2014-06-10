from numpy.random import rand
from numpy import zeros
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
print 'using backend', plt.get_backend()
from matplotlib import animation
import time
import threading
import thread

data1 = zeros(3)
data2 = zeros(3)

def run_gui():
    fig = plt.figure(figsize=(16,6))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    line1, = ax1.plot([], [], 'bo', ms=6)
    line2, = ax2.plot([], [], 'bo', ms=6)
    
    def init():
        print 'calling init'
        ax1.set_ylim(0,1)
        ax1.set_xlim(0,1)
        ax2.set_ylim(0,1)
        ax2.set_xlim(0,1)
        line2.set_data([], [])
        line2.set_data([], [])
        return ax1, ax2, line1, line2,
    
    def animate(i):
        line1.set_data([.1, .5, .9], data1)
        line2.set_data([.1, .5, .9], data2)
        return line1, line2, 

    ani = animation.FuncAnimation(
        fig, animate, interval=0, blit=True, init_func=init)
    #plt.ion()
    plt.show()
    #plt.pause(1.)

if __name__ == "__main__":
    thread.start_new_thread(run_gui, ())
    #threading.Thread(target=run_gui)
    #plt.ion()
    #plt.show()
    idx = 0
    while True:
        data1[idx] = rand()
        data2[idx] = rand()
        time.sleep(1.)
        idx = (idx+1) % 3
