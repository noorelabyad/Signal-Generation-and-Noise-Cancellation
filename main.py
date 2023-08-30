import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.fftpack import fft
𝑡 = np.linspace(0 , 3 , 12*1024)

f_left = np.array([130.81, 146.83, 164.81, 130.81, 130.81, 146.83, 164.81, 130.81, 164.81, 174.61, 196])
#array for frequencies of notes played by the left hand
f_right = np.array([261.63, 293.66, 329.63, 261.63, 261.63, 293.66, 329.63, 261.63, 329.63, 349.23, 392])
#array for frequencies of notes played by the right hand
start_time = np.array([0, 0.27, 0.54, 0.81, 1.09, 1.36, 1.63, 1.9, 2.18, 2.45, 2.72])
duration = np.array([0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25])
#initializing output signal
x = 0
#iterating over the previous arrays adding to our output single in each iteration a new sinusoid of a #certain frequency, start time and duration
for i in range(len(duration)):
#xleft and xright are the sinusoids played by the left and right hands respectively
    xleft  = np.sin(2 * np.pi * f_left[i] * t)
    xright = np.sin(2 * np.pi * f_right[i] * t)
    ti =start_time[i]
    T = duration[i]
    xi = np.where(np.logical_and(t >= ti, t < (ti + T)), xleft + xright , 0)
    x += xi 
#creating an arrray of 2 random noise frequencies fn

fn = np.random.randint(0, 512, 2)
n = 0
for i in range (len(fn)):
    n += np.sin(2 * np.pi * fn[i] * t)
    
#generate new noise contaminated signal xn

xn = x + n

#generating fourier transform of the original signal (x_f) 
#and of the noise contaminated signal (xn_f)
#generating a frequency axis f

N = 3*1024
𝑓 = np. linspace(0 , 512 , int(N/2))

x_f = fft(x)
x_f = 2/N * np.abs(x_f [0:np.int(N/2)])

xn_f = fft(xn)
xn_f = 2/N * np.abs(xn_f [0:np.int(N/2)])

#intializing an array to store the frequencies of the noise in

noiseFrequencies = []

#max(x_f) is the highest amplitude achieved by a frequency
#in x_f plotted against f 
# xn_f[i] is the amplitude of xn_f at frequency i
#math.ciel(f[i])
# if the amplitude corresponding to a certain frequency in xn_f was found 
#to exceed the maximum amplitude achieved by any frequency in x_f, it 
#would be added to the noise frequency array

for i in range (len(f)):
    if (xn_f[i]> math.ceil(max(x_f))):
        noiseFrequencies += [int(f[i])]
        

#intitializing x_filtered variable to represent the filtered signal
#it would contain the signal with the found noise frequencies 
# subracted from the noise contaminated signal 

x_filtered = x + n
tmp = 0
for i in range (len(noiseFrequencies)):
    tmp += -1 * np.sin(2 * np.pi * noiseFrequencies[i] * t)

x_filtered += tmp
#finding fourier transfrom of x_filtered

xn_filtered = fft(x_filtered)
xn_filtered = 2/N * np.abs(xn_filtered [0:np.int(N/2)])

plt.subplot(3,1,1)
plt.plot(f,x_f)
plt.legend(['pure signal in freq domain'])
plt.subplot(3,1,2)
plt.plot(f,xn_f)
plt.legend(['noisy signal in freq domain'])
plt.subplot(3,1,3)
plt.plot(f,xn_filtered)
plt.legend(['filtered signal in freq domain'])

plt.figure()

plt.subplot(3,1,1)
plt.plot(t,x)
plt.legend(['pure signal in time domain'])
plt.subplot(3,1,2)
plt.plot(t,xn)
plt.legend(['noisy signal in time domain'])
plt.subplot(3,1,3)
plt.plot(t,x_filtered)
plt.legend(['filtered signal in time domain'])

#sd.play(x, 3*1024)
#sd.play(xn, 3*1024)
sd.play(x_filtered, 3*1024)









