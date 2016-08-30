#!/usr/bin/env python

""" 
    This module performs equalification filtering for the Sensimetrics system. Original script based filtering is only
    implemented for MATLAB, this is the python adaptation of that. Testing only performed by comparison of resulting
    wave-files to both MATLAB and official EQ Filtering application of Sensimetrics.

    Implementation for 16bit wave-files only due to write limitations as well as compatibility with general audio
    systems.
"""

# built-in modules
import os
import sys

# third-party modules
import numpy as np
from scipy.io import wavfile


__author__ = "Niels R Disbergen"
__email__ = "niels@nielsdisbergen.net"
__version__ = "0.1"
__status__ = "Development"
__license__ = "MIT"


def filter_wav(audio_file, filt_dir, filt_left, filt_right):

    left_imp = np.fromfile(os.path.join(filt_dir, filt_left), dtype=float)
    right_imp = np.fromfile(os.path.join(filt_dir, filt_right), dtype=float)

    [fs, wav_dat] = wavfile.read(audio_file)

    # Error if not 16bit wave-file
    if wav_dat.dtype != 'int16':
        raise NotImplementedError("input wav-file is \"%s\" format, code implemented for 16bit files only" % wav_dat.dtype)

    # Handle number channels wave-file
    if np.size(wav_dat.shape) == 1:  # single channel, left copy for filtering
        wav_out = np.stack((wav_dat, wav_dat), axis=1)
        print("Wave-data \"%s\" is single-channel, left channel copied before filtering" % os.path.split(audio_file)[1])
    elif np.size(wav_dat.shape) == 2 & wav_dat.shape[1] == 2:  # 2-channel keep original
        wav_out = wav_dat
    else:  # Not equal 1 or 2 channel, raise error
        raise NotImplementedError("Wave-data \"%s\" is %s-channels, code built for 1 or 2 channel wave-files only"
                                  % (os.path.split(audio_file)[1], wav_dat.shape[1]))

    # Convolve wave-data with impulse and truncate overflow
    # data converted to int16, as bit-depth determines wave-file bit-rate (8,16,or 32)
    conv_wav_left = np.int16(np.convolve(left_imp, wav_out[:,0], mode='full'))
    conv_wav_right = np.int16(np.convolve(right_imp, wav_out[:,1], mode='full'))

    # re-merge channels and write new wave-file
    wav_out = np.stack((conv_wav_left[:np.size(wav_dat,0)], conv_wav_right[:np.size(wav_dat,0)]), axis=1)
    wavfile.write(("%s_sensFilt%s.wav" % (audio_file[:-4], lab_suffix)), fs, wav_out)

    return sys.exit(0)
