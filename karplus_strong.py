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

# Creates a stereo, 16-bit WAV file. The name of the file is `fn`.
def create_wav(fn):    
    out = wave.open(fn, 'w')
    out.setparams((N_CHANNELS, SAMP_WIDTH, SAMP_RATE, 0, 'NONE', 'not compresses'))
    return out

# Writes a stereo sample to an open wav file.
def write_wav(wav, lhs, rhs):
    packed_lhs = struct.pack('h', lhs)
    packed_rhs = struct.pack('h', rhs)
    output_file.writeframes(packed_lhs)
    output_file.writeframes(packed_rhs)


# Creates a buffer for a string of frequency freq. The buffer length is computed
# from the length of one period.
def gen_buffer(freq):
    BUFLEN = SAMP_RATE // freq
    BUFMAX = 2 ** (8 * SAMP_WIDTH - 1) - 1

    return [random.randint(-BUFMAX, BUFMAX) for i in range(BUFLEN)]

# Generates pluck sound.
output_file = create_wav("string.wav")
buf = gen_buffer(440)
decayed = False
while not decayed:
    last_sample = buf[0]
    run_length = 0
    for i in range(0, len(buf)):
        # Checks if the signal has converged.
        sample = buf[i]
        if sample == last_sample:
            run_length = run_length + 1
            if run_length == len(buf):
                decayed = True;
                break;
        else:
            run_length = 1
            last_sample = sample
        # Writes next sample if not.
        write_wav(output_file, sample, sample)
        if i == 0:
            buf[0] = (buf[0] + buf[len(buf) - 1]) // 2
        else:
            buf[i] = (buf[i] + buf[i - 1]) // 2

output_file.close()

