import numpy as np
from numpy import pi
from numpy.fft import fft, ifft, fftfreq, fftshift
from scipy.optimize import leastsq
import matplotlib.pyplot as plt

import pdb

dt = .005
t_end = 5.

freq = 0.8 # Hz
phase = 30. # deg
amp = 1.
noise_amp = .5

time = np.arange(0., t_end, dt)
n = len(time)

signal = amp * np.sin(2*pi*freq*time + phase*pi/180.)
noise = noise_amp*np.random.randn(n)
noisy_signal = signal+noise


# do dft 
ft_signal = fft(signal)
ft_noisy_signal = fft(noisy_signal)
freq = fftfreq(n, dt)

# find freq with max power
fit_idx = np.argmax(abs(ft_noisy_signal[:n/2]))
ft_fit = np.zeros(n, dtype=complex)
ft_fit[fit_idx] = ft_noisy_signal[fit_idx]
ft_fit[-fit_idx] = ft_noisy_signal[-fit_idx]

ft_fit_signal = ifft(ft_fit).real # we know signal is real

freq_fit = freq[fit_idx]
print 'frequency with highest power:', freq_fit

amp_guess = max(abs(ft_fit_signal))
phase_guess = np.angle(ft_fit[fit_idx], deg=True) + 90.
offset_guess = 0.
print 'amp,phase,offset guesses:', amp_guess, phase_guess, offset_guess

fit_signal_guess = amp_guess * np.sin(2*pi*freq_fit*time + phase_guess*pi/180.)
optimize_func = lambda x: x[0]*np.sin(2*pi*freq_fit*time + x[1]*pi/180.) + x[2] - noisy_signal
amp_est, phase_est, offset_est = leastsq(optimize_func, [amp_guess, phase_guess, offset_guess])[0]
print 'amp,phase,offset estimates:', amp_est, phase_est, offset_est

fit_signal = amp_est * np.sin(2*pi*freq_fit*time + phase_est*pi/180.) + offset_est

# plotting
plt.figure(figsize=(12,16))

plt.subplot(2,1,1)
plt.plot(time, signal, label='signal')
plt.plot(time, noisy_signal, label='noisy signal')
plt.plot(time, fit_signal_guess, '-x', label='ft fit signal guess')
plt.plot(time, fit_signal, '-o', label='fit signal')
plt.xlabel('time')
plt.legend()

plt.subplot(2,1,2)
plt.plot(fftshift(freq), fftshift(abs(ft_signal)), label='signal')
plt.plot(fftshift(freq), fftshift(abs(ft_noisy_signal)), label='noisy signal')
plt.plot(fftshift(freq), fftshift(abs(ft_fit)), label='ft fit signal')
plt.xlabel('freq')

plt.show()
