""" dummy script to call matlab and cvx in parallel"""
import numpy as np
import scipy.io as sci_io
from multiprocessing import Process, Pool
from subprocess import call

def main():
    """calls matlab"""
    matlab_path = 'matlab' # assumes system has symlink(shortcut) to matlab available
    num_decodes = 20

    num_neurons = 8#24*32
    num_samples = 512
    num_dim = 1

    print "packaging and saving data for matlab"
    for i in range(num_decodes):
        FPGA_MAX = 1.
        beta = 0. #np.random.random()
        gamma = 10. #np.random.random()
        min_weight = -1.
        params = np.array([FPGA_MAX, beta, gamma, min_weight])
        sci_io.savemat('decode_params'+str(i)+'.mat', {'params': params}, oned_as='column')

        A = np.random.random((num_samples, num_neurons))
        y = np.random.random((num_samples, num_dim))
        sci_io.savemat('A'+str(i)+'.mat', {'A': A})
        sci_io.savemat('y'+str(i)+'.mat', {'y': y})
    
    print "data saved! calling matlab"
    calls = []
    for i in range(num_decodes):
        #calls.append([matlab_path, '-nodesktop', '-nosplash', '-nojvm', 
        #                  '-r', "hello; exit;"])
        calls.append([matlab_path, '-nodesktop', '-nosplash', '-nojvm', 
                          '-r', "cdw_cvx('"+str(i)+"'); exit;"])

    ###### sequential version ##################################################
    #for i in range(num_decodes):
    #    call(calls[i])

    ###### multiprocess version with single process per job ####################
    #processes = []
    #for i in range(num_decodes):
    #    processes.append(Process(target=foo, args=(calls[i],)))
    #    #processes.append(Process(target=call, args=(calls[i],)))
    #    processes[i].start()
    #for i in range(num_decodes):
    #    processes[i].join()

    ###### multiprocess with pool of workers ###################################
    workers = Pool(8)
    workers.map(call, calls)
    workers.close()
    workers.join()

    # get my command line cursor back!
    call(['stty', 'echo'])


if __name__ == "__main__":
    main()
