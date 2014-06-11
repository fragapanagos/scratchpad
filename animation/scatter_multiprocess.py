from numpy.random import rand
from numpy import zeros
import matplotlib
matplotlib.use('Qt4Agg')
#matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
print 'using backend', plt.get_backend()
from matplotlib import animation
import time
import multiprocessing as mp

initted = False

def run_gui(conn):
    fig = plt.figure(figsize=(16,6))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    line1, = ax1.plot([], [], 'bo', ms=6)
    line2, = ax2.plot([], [], 'bo', ms=6)
    ax1.set_ylim(0,1)
    ax1.set_xlim(0,1)
    ax2.set_ylim(0,1)
    ax2.set_xlim(0,1)
    
    def init():
        global initted
        if initted:
            return ()
        print 'calling init'
        line1.set_data([.1, .5, .9], [-1, -1, -1])
        line2.set_data([.1, .5, .9], [-1, -1, -1])
        initted = True
        return ax1, ax2, line1, line2
    
    def animate(i):
        data1, data2 = conn.recv()
        print(data1, data2)
        line1.set_data([.1, .5, .9], data1)
        line2.set_data([.1, .5, .9], data2)
        return line1, line2, 

    ani = animation.FuncAnimation(
        fig, animate, interval=0, blit=True, init_func=init)
    plt.show()

if __name__ == "__main__":
    parent_conn, child_conn = mp.Pipe()
    gui_proc = mp.Process(target=run_gui, args=(child_conn,))
    gui_proc.start()
    idx = 0
    data1 = zeros(3)
    data2 = zeros(3)
    while True:
        try:
            data1[idx] = rand()
            data2[idx] = rand()
            time.sleep(1.)
            idx = (idx+1) % 3
            parent_conn.send([data1, data2])
        except KeyboardInterrupt:
            print("exiting")
            gui_proc.terminate()
            break
