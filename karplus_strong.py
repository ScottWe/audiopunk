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
N_CHANNELS = 1
SAMP_WIDTH = 2
SAMP_RATE = 44100

# Creates a stereo, 16-bit WAV file. The name of the file is `fn`.
def create_wav(fn):    
    out = wave.open(fn, 'w')
    out.setparams((N_CHANNELS, SAMP_WIDTH, SAMP_RATE, 0, 'NONE', 'not compresses'))
    return out

# Writes a stereo sample to an open wav file.
def write_wav(wav, buf):
    out = bytes()
    for i in range(0, len(buf)):
        out = out + struct.pack('h', buf[i])
    output_file.writeframes(out)

# Creates a buffer for a string of frequency freq. The buffer length is computed
# from the length of one period.
def displace_string(freq):
    BUFLEN = SAMP_RATE // freq
    BUFMAX = 2 ** (8 * SAMP_WIDTH - 1) - 1

    return [random.randint(-BUFMAX, BUFMAX) for i in range(BUFLEN)]

def is_in_equilibrium(string):
    for i in range(1, len(string)):
        if (string[i] != string[i - 1]):
            return False
    return True

def apply_karplus_iteration(string):
    for i in range(0, len(string)):
        string[i] = (string[i] + string[i - 1]) // 2

# Generates pluck sound.
output_file = create_wav("string.wav")
string = displace_string(440)
while not is_in_equilibrium(string):
    write_wav(output_file, string)
    apply_karplus_iteration(string)
output_file.close()

