import numpy
import pyaudio

RATE = 44100

def sine(pitch, duration, rate):
	length = int(duration * rate)
	factor = float(pitch) * (numpy.pi * 2) / rate
	return numpy.sin(numpy.arange(length) * factor)

def play_tone(stream, pitch=440, volume=0.25, duration=1, rate=RATE):
	chunk = sine(pitch, duration, rate) * volume
	stream.write(chunk.astype(numpy.float32).tostring())

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=RATE, output=True)

play_tone(stream)

stream.close()
p.terminate()