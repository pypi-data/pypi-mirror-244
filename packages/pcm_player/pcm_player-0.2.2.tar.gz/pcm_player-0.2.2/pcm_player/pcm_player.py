import struct
import os
import time

import numpy as np
import soundfile as sf
import sounddevice as sd

class PcmPlayer:

    filename: str
    loop_point: int

    def __init__(self, file):
        self.filename = file

    def validate_file(self):

        if not self.filename:
            print("Input file is required. Use -f/--file to provide the file path.")
            return False

        if (not os.path.exists(self.filename)):
            print("Input file not found")
            return False

        with open(self.filename, 'rb') as f:
            first = f.read(4)
            self.loop_point = struct.unpack('i', f.read(4))[0]

        print("Loop point: " + str(self.loop_point))

        if first != b'MSU1':
            print("PCM file has invalid header")
            return False

        return True

    def test_loop(self):
        data_0, fs_0 = sf.read(self.filename, channels=2, samplerate=44100, format='RAW', subtype='PCM_16', start=-44100*5)
        data_1, fs_1 = sf.read(self.filename, channels=2, samplerate=44100, format='RAW', subtype='PCM_16', start=8 + self.loop_point, frames=44100*5)
        data = np.concatenate([data_0, data_1])
        sd.play(data, fs_0, blocking=True)
        print("Complete")

    def play_song(self):
        data_0, fs_0 = sf.read(self.filename, channels=2, samplerate=44100, format='RAW', subtype='PCM_16', start=8)
        data_1, fs_1 = sf.read(self.filename, channels=2, samplerate=44100, format='RAW', subtype='PCM_16', start=8 + self.loop_point, frames=44100*15)
        data = np.concatenate([data_0, data_1])
        sd.play(data, fs_0, blocking=True)
        print("Complete")

    def stop(self):
        sd.stop()


        