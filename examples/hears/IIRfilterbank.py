'''
Example of the use of the class IIRfilterbank available in the library. 
In this example, a white noise is filtered by a  bank of chebyshev bandpass filters and lowpass filters which are different for every channels. The centre frequencies of 
the filters are linearly taken between 100kHz and 1000kHz and its bandwidth or cutoff frequency increases linearly with frequency.
'''
from brian import *
from brian.hears import *

dBlevel=50*dB  # dB level of the input sound in rms dB SPL
sound=whitenoise(100*ms,samplerate=44*kHz).ramp() #generation of a white noise
sound=sound.atlevel(dBlevel) #set the sound to a certain dB level


### example of a bank of bandpass filter ################
nchannels=50
center_frequencies=linspace(200*Hz,1000*Hz, nchannels)  #center frequencies 
bw=linspace(50*Hz,300*Hz, nchannels)  #bandwidth of the filters
gpass=1. #The maximum loss in the passband in dB. Can be a scalar or an array of length nchannels
gstop=10. #The minimum attenuation in the stopband in dB. Can be a scalar or an array of length nchannels

passband=vstack((center_frequencies-bw/2,center_frequencies+bw/2)) #arrays of shape (2 x nchannels) defining the passband frequencies (Hz)
stopband=vstack((center_frequencies-1.1*bw,center_frequencies+1.1*bw)) ##arrays of shape (2 x nchannels) defining the stopband frequencies (Hz)

filterbank =IIRFilterbank(sound,nchannels, passband, stopband, gpass, gstop, 'bandstop','cheby1') #instantiation of the filterbank

filterbank_mon=filterbank.process() #processing

print filterbank.order

figure()
subplot(211)
imshow(flipud(filterbank_mon.T),aspect='auto')    


#### example of a bank of lowpass filter ################
nchannels=50
cutoff_frequencies=linspace(100*Hz,1000*Hz, nchannels)  #center frequencies 
width_transition=linspace(50*Hz,300*Hz, nchannels)  #bandwidth of the transition region between the en of the pass band and the begin of the stop band
gpass=1. #The maximum loss in the passband in dB. Can be a scalar or an array of length nchannels
gstop=10. #The minimum attenuation in the stopband in dB. Can be a scalar or an array of length nchannels

passband=cutoff_frequencies-width_transition/2 #
stopband=cutoff_frequencies+width_transition/2 #

filterbank =IIRFilterbank(sound,nchannels, passband, stopband, gpass, gstop, 'low','cheby1') #instantiation of the filterbank

filterbank_mon=filterbank.process()#processing

print filterbank.order

subplot(212)
imshow(flipud(filterbank_mon.T),aspect='auto')    
show()