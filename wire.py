"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).

This is the callback (non-blocking) version.
"""

import time
import pyaudio

WIDTH = 2
CHANNELS = 2
RATE = 44100

pa = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    return (in_data, pyaudio.paContinue)

stream = pa.open(
    format=pa.get_format_from_width(WIDTH),
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()

pa.terminate()