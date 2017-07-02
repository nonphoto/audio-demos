import time
import numpy
import pyaudio

RATE = 44100
PITCH = 440

current_frame = 0

def callback(in_data, frame_count, time_info, status):
	global current_frame
	factor = float(PITCH) * (numpy.pi * 2) / RATE
	chunk = numpy.sin((current_frame + numpy.arange(frame_count)) * factor)
	print chunk
	current_frame += frame_count
	out_data = chunk.astype(numpy.float32).tostring()
	return (out_data, pyaudio.paContinue)

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paFloat32, channels=1, rate=RATE, input=True, output=True, stream_callback=callback)

stream.start_stream()

try:
	while stream.is_active():
		time.sleep(0.1)
except Exception:
	raise e
except KeyboardInterrupt:
	print ''
	pass

stream.stop_stream()
stream.close()

pa.terminate()
