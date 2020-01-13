import math
import wave
import struct
import random

#
# The Karplus-Strong algorithm is a physics model intended for string synthesis. It models
# the string as a cyclic buffer, the initial displacement as a randomized initialization
# of the buffer, and decay as a low-pass filter.
#

# Stero, 16-bit audio with standard sampling rate
N_CHANNELS = 2
SAMP_WIDTH = 2
SAMP_RATE = 44100

output_file = wave.open('karplus_strong.wav', 'w')
output_file.setparams((N_CHANNELS, SAMP_WIDTH, SAMP_RATE, 0, 'NONE', 'not compresses'))

# Determines buffer length for desired frequency.
# There are 44100 samples/second.
# 440hz requires 440 cycles per second.
# This gives a period of 44100/440 samples.
# Rounding errors are ignored in the implementation.
FREQ = 440
BUFLEN = SAMP_RATE // FREQ

# Creates the buffer.
ABS_MAX_SAMPLE = 2 ** (8 * SAMP_WIDTH - 1) - 1
buf = [random.randint(-ABS_MAX_SAMPLE, ABS_MAX_SAMPLE) for i in range(BUFLEN)]

# Generates pluck sound.
decayed = False
while not decayed:
    last_sample = buf[0]
    run_length = 0
    for i in range(0, BUFLEN):
        # Checks if the signal has converged.
        sample = buf[i]
        if sample == last_sample:
            run_length = run_length + 1
            if run_length == BUFLEN:
                decayed = True;
                break;
        else:
            run_length = 1
            last_sample = sample
        # Writes next sample if not.
        packed_sample = struct.pack('h', sample)
        output_file.writeframes(packed_sample)
        output_file.writeframes(packed_sample)
        if i == 0:
            buf[0] = (buf[0] + buf[BUFLEN - 1]) // 2
        else:
            buf[i] = (buf[i] + buf[i - 1]) // 2

output_file.close()

