# coding: utf-8

# spectral subtraction: one of noise reduction method
#                       This is a simple python script, is not advanced one.
#
# Usage:
#    specify wav file names below,
#       infile: input wav file including noise
#       outfile: output wav file
#       noisefile: noise only wav file, that is some (noise only) portion of input wav edited by manual (ex: Audacity)
# 
#     then, python3 ss1.py

# Check version:
# 
#  Python 3.6.4 win32 64bit
#  Windows 10, 64bit
#  numpy (1.14.0)
#  scipy (1.0.0)
#  librosa (0.6.0)

import numpy as np
import scipy
import librosa

# edit following wav file name
infile='mantram_short.wav'
outfile='output_short.wav'
noisefile='noise_short.wav'

# load input file, and stft (Short-time Fourier transform)
print ('load wav', infile)
w, sr = librosa.load( infile, sr=None, mono=True) # keep native sr (sampling rate) and trans into mono
s= librosa.stft(w)    # Short-time Fourier transform
ss= np.abs(s)         # get magnitude
angle= np.angle(s)    # get phase
b=np.exp(1.0j* angle) # use this phase information when Inverse Transform

# load noise only file, stft, and get mean
print ('load wav', noisefile)
nw, nsr = librosa.load( noisefile, sr=None, mono=True)
ns= librosa.stft(nw) 
nss= np.abs(ns)
mns= np.mean(nss, axis=1) # get mean

# subtract noise spectral mean from input spectral, and istft (Inverse Short-Time Fourier Transform)
sa= ss - mns.reshape((mns.shape[0],1))  # reshape for broadcast to subtract
sa0= sa * b  # apply phase information
y= librosa.istft(sa0) # back to time domain signal

# save as a wav file
scipy.io.wavfile.write(outfile, sr, (y * 32768).astype(np.int16)) # save signed 16-bit WAV format
#librosa.output.write_wav(outfile, y , sr)  # save 32-bit floating-point WAV format, due to y is float 
print ('write wav', outfile)