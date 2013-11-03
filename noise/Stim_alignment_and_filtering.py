import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

# unit test utility functions
def genStim(nstim, tstim, ndim=1):
    assert nstim%1 == 0, "must specify an integer number of stim"
    stim_dt = np.arange(nstim+1)*tstim
    stim_rates = np.random.randn(nstim, ndim)
    return stim_dt, stim_rates

def genLoopback(nticks, tlb, dil_rate=2, maxTtoStart=.005, lb_tvar=None):
    measured_loopback_intervals = np.zeros(nticks)
    measured_loopback_intervals[0] = maxTtoStart
    #measured_loopback_intervals[0] = maxTtoStart*np.random.rand()
    measured_loopback_intervals[1:] = np.ones(nticks-1) * tlb * dil_rate
    if lb_tvar:
        measured_loopback_intervals[1:] = measured_loopback_intervals[1:] + lb_tvar * np.random.randn(nticks-1)
    return measured_loopback_intervals

def plotSequenceComparison(dt0, seq0, dt1, seq1, ls0=None, ls1='r--+'):
    assert len(dt0)==seq0.shape[0]+1, "length of first delta times must be length of first sequence + 1"
    assert len(dt1)==seq1.shape[0]+1, "length of second delta times must be length of second sequence + 1"
    assert seq0.shape[1] == seq1.shape[1], "sequences must have same dimentionality"
    
    dt0_toplot = np.zeros(seq0.shape[0]*2)
    dt0_toplot[0:-1:2] = dt0[0:-1]
    dt0_toplot[1::2]   = dt0[1:]
    seq0_toplot = np.zeros((seq0.shape[0]*2,ndim))
    seq0_toplot[0::2,:] = seq0
    seq0_toplot[1::2,:]  = seq0
    
    dt1_toplot = np.zeros(seq1.shape[0]*2)
    dt1_toplot[0:-1:2] = dt1[0:-1]
    dt1_toplot[1::2]   = dt1[1:]
    seq1_toplot = np.zeros((seq1.shape[0]*2,ndim))
    seq1_toplot[0::2,:] = seq1
    seq1_toplot[1::2,:] = seq1
    
    plt.plot(dt0_toplot, seq0_toplot)
    plt.plot(dt1_toplot, seq1_toplot, ls1, ms=12)
    # plt.tight_layout()

#############################################
# functions to test
def loopbackAlignStim(stim_dt, stim_rates, target_lb_interval, measured_lb_intervals):
    assert len(stim_dt) == stim_rates.shape[0]+1, "length of stim_dt times doesn't align to stim_rates data"
    tstim = stim_dt[1]-stim_dt[0]
    print '\nstim_dt:',stim_dt
    print 'stim_rates:',stim_rates.flatten()
    
    stim_dt_aligned = np.zeros(stim_dt.shape[0]) 
    stim_rates_aligned = np.zeros(stim_rates.shape)
    
    target_lb_dt = target_lb_interval * np.arange(len(measured_lb_intervals))
    print '\ntarget_lb_dt', target_lb_dt
    
    plt.figure()
    plotSequenceComparison(stim_dt, stim_rates, target_lb_dt, np.zeros((len(target_lb_dt)-1,1)), ls1='g--+')
    plt.title('Programmed stim sequence and loopback sequence')

    # first entry in measured_loopback_intervals is time for stim to start
    stim_dt_aligned[0] = measured_lb_intervals[0]    
    print 'stim_dt_aligned:',stim_dt_aligned
    print 'stim_rates_aligned:',stim_rates_aligned.flatten()
    
    current_exp_time = measured_lb_intervals[0]
    for i in range(len(measured_lb_intervals)-1):
        print '\nprocessing loopback tick %d'%i
        lb_tstart = target_lb_dt[i]
        lb_tstop  = target_lb_dt[i+1]
        if lb_tstart > stim_dt[-1]: break
        start_idx = np.where(lb_tstart<stim_dt[1:])[0][0]
        stop_idx = np.where(lb_tstop>stim_dt[0:-1])[0][-1]
        print 'Loopback %d: %0.2f to %.02f, start_idx:%d to stop_idx:%d go %0.2f to %0.2f'%(
                i, lb_tstart, lb_tstop, start_idx, stop_idx, stim_dt[start_idx], stim_dt[stop_idx+1])   
        lb_tstart_overlap = stim_dt[start_idx]<lb_tstart
        lb_tstop_overlap  = stim_dt[stop_idx+1]>lb_tstop
        print 'Overlap at beginning:',(stim_dt[start_idx]<lb_tstart), " Overlap at end:",(stim_dt[stop_idx+1]>lb_tstop)
        if lb_tstart_overlap:
            print 'start overlap:',stim_dt[start_idx+1]-lb_tstart 
        if lb_tstop_overlap:
            print 'stop overlap:',stim_dt[stop_idx+1] - lb_tstop

        dil_rate = measured_lb_intervals[i+1]/float(target_lb_interval)
        print 'dil_rate:',dil_rate

        stim_dt_aligned[start_idx+1:stop_idx+2] = (np.arange(stop_idx-start_idx+1)+1)*tstim*dil_rate + current_exp_time
        stim_rates_aligned[start_idx:stop_idx+1] = stim_rates[start_idx:stop_idx+1]/dil_rate
        # overlap at start edge case
        # overlap at end edge case
        current_exp_time = stim_dt_aligned[stop_idx+1]
        print 'stim_dt_aligned:',stim_dt_aligned
        print 'stim_rates_aligned:',stim_rates_aligned.flatten()
    
    return stim_dt_aligned, stim_rates_aligned

def resampleStim(stim_dt, stim_rates, tsample, nsample):
    assert tsample * nsample <= stim_dt[-1], "not enough data for requested nsample and tsample"
    assert len(stim_dt) == stim_rates.shape[0] + 1, "stim_dt times doesn't align to stim_rates data"
    assert nsample%1 == 0, "must specify an integer number of samples, specified %f"%nsample
    ndim = stim_rates.shape[1]
    
    sample_dt = np.arange(nsample+1)*tsample
    sample_rates = np.zeros((nsample, ndim))

    for i in range(len(sample_rates)):
        sample_tstart = sample_dt[i]
        sample_tstop  = sample_dt[i+1]
        sample_start_idx = np.where(sample_tstart<stim_dt[1:])[0][0]
        sample_stop_idx = np.where(sample_tstop>stim_dt[0:-1])[0][-1]
        #print 'Sample %d: %0.2f to %.02f, Stim %d to %d: %0.2f to %0.2f'%(
        #i, sample_tstart, sample_tstop, sample_start_idx, sample_stop_idx, stim_dt[sample_start_idx], stim_dt[sample_stop_idx+1])
        weights = np.ones(sample_stop_idx - sample_start_idx + 1) * tstim
        weights[0] = stim_dt[sample_start_idx+1] - sample_tstart
        weights[-1] = sample_tstop - stim_dt[sample_stop_idx]
        sample_rates[i,:] = np.average(stim_rates[sample_start_idx:sample_stop_idx+1], weights=weights, axis=0)
    
    return sample_dt, sample_rates
    
def filterSamples(sample_rates, tsample, tau=.1):
    b = [1-np.exp(-tsample/tau)]
    a = [1, -np.exp(-tsample/tau)]
    filtered_rates = signal.lfilter(b, a, sample_rates, axis=0)
    return filtered_rates

plt.close('all')
# scratchpad for getting things to work
tstim = .1
tsample = .01

nstim = 4
ndim = 1
nsample = int(nstim*tstim/tsample)

nlbtick = 4
target_lb_interval = .15
maxTtoStart = 0.01
dil_rate = 2.
lb_tvar = 0.

measured_lb_intervals = genLoopback(nlbtick, target_lb_interval, dil_rate, maxTtoStart=maxTtoStart, lb_tvar=lb_tvar)
print 'measured_lb_intervals', measured_lb_intervals

stim_dt, stim_rates = genStim(nstim, tstim, ndim)

stim_dt_aligned, stim_rates_aligned = loopbackAlignStim(stim_dt, stim_rates, target_lb_interval, measured_lb_intervals)

sample_dt, sample_rates = resampleStim(stim_dt, stim_rates, tsample, nsample)

sample_rates_filtered = filterSamples(sample_rates, tsample)
# plt.figure()
# plotSequenceComparison(stim_dt, stim_rates, sample_dt, sample_rates)

# plt.figure()
# plotSequenceComparison(sample_dt, sample_rates, sample_dt, sample_rates_filtered)

plt.show()
