'''
CREATED BY DANIEL SHI
ANU SEMESTER 1 2025
'''
import math
import numpy as np
import matplotlib.pyplot as plt
rng = np.random.default_rng() # Creates a random number generator

# ----------------  INPUT PARAMETERS ---------------- #
## Empirically determined parameters
decay_time_us = 80 # Empirically determined decay time via observation of oscilloscope. This was 80us on average for the DMA-300.
sample_frequency_MHz = 0.025 # Empirically determined. 25kHz is the Nyquist criteria for the 12.5kHz signal for the Canberra HPGE.
tau_us = decay_time_us/5 # After 5 time constants, the system will be at approximately 1% of its initial value (i.e. near fully decayed). 
sample_period_us = math.floor(1/sample_frequency_MHz) # The sampling period, rounded down to minimum required microsecond

## User defined parameters
num_pulses = 5 # The number of step-rise and exponential decay pulses desired 
mean_pulse_spacing_us = 500 # The mean space desired between subsequent pulses
total_time_us = num_pulses * mean_pulse_spacing_us # The total time length of the preamplifier signal
amplitude_range = (0.5, 5) # Specify the range of (voltage) amplitudes in the preamplifier signal
window_length = 4 # Window length of the moving average filter
# --------------------------------------------------- #

# --------------  FUNCTION DEFINITIONS -------------- #
def generate_preamplifier_signal(t, tau_us, num_pulses, mean_pulse_spacing_us, amplitude_range):
    signal = np.zeros(len(t))
    pulse_starts = [0]
    for i in range(num_pulses): # Generate random start times for the pulses
        previous_time = pulse_starts[-1]
        gap = rng.random()*(mean_pulse_spacing_us/1.5)
        gap = mean_pulse_spacing_us                            # uncomment for constant spacing
        new_time = previous_time + gap
        pulse_starts.append(new_time)
    for start in pulse_starts: # For each of the start times, create a decaying exponential curve
        amplitude = amplitude_range[0]+rng.random()*(amplitude_range[1]-amplitude_range[0])
        amplitude = 1                                         # uncomment for constant amplitude
        for i, time in enumerate(t):
            if time >= start:
                decay_val=-amplitude*np.exp(-(time - start)/tau_us)
                signal[i]+=decay_val
    return signal

def sample_signal(t, preamp_signal, sample_period_us): # Creates a new array which are the samples of the preamplifier signal
    t_sampled = np.arange(0, t[-1], sample_period_us) 
    sampled_preamp_signal = np.interp(t_sampled, t, preamp_signal) 
    return t_sampled, sampled_preamp_signal

def apply_MAF_recursive(x, w): # Implementation of a recursive, moving average filter. Source: Stoica, 2012
    y = np.zeros_like(x)
    # For loop performs the recurse y[n]=y[n-1]+ 1/w*(x[n]-x[n-w-1])
    for k in range(1, len(x)):
        x_k = x[k]
        if k - w - 1 >= 0:
            x_old = x[k - w - 1] 
        else: # Edge case to avoid index error
            x_old = 0
        y[k] = y[k - 1] + (x_k - x_old)/w
    return y 
# --------------------------------------------------- #

# ---------------- CALLING FUNCTIONS ---------------- #
# Create a time array for the signal to live in. The large number of intervals approximate a continuous time space.
t = np.linspace(0, total_time_us, 10000) 
preamp_signal = generate_preamplifier_signal(t, tau_us, num_pulses, mean_pulse_spacing_us, amplitude_range)
t_sampled, sampled_preamp_signal = sample_signal(t, preamp_signal, sample_period_us)
filtered_samples = apply_MAF_recursive(sampled_preamp_signal, window_length)
# --------------------------------------------------- #

# -------------------- PLOTTING --------------------- #
plt.plot(t, preamp_signal, label="Preamplifier Signal", color='black', linewidth=2)
plt.scatter(t_sampled, sampled_preamp_signal, label="Sampled Signal (t_s="+ str(sample_period_us) +"μs)", color='blue', s=10) 
plt.plot(t_sampled, filtered_samples, label="MAF Signal ("+str(window_length)+" window length)", color='red', linewidth=2) 
plt.xlabel("Time (μs)")
plt.ylabel("Amplitude (units)")
plt.grid(True)
plt.legend()
plt.show()
# --------------------------------------------------- #