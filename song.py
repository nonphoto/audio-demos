import sys
import itertools
import time
import numpy
import pyaudio
import midi

if len(sys.argv) != 2:
    print "Usage: {0} <midifile>".format(sys.argv[0])
    sys.exit(2)

midifile = sys.argv[1]
pattern = midi.read_midifile(midifile)
track = iter(pattern[2])

current_frame = 0
current_tick = 0
next_event = track.next()
notes = [False] * 128

TEMPO = 120
RESOLUTION = pattern.resolution
TICK_RATE = float(TEMPO * RESOLUTION) / 60
FRAME_RATE = 44100

def tickToFrame(tick):
	return float(tick) / TICK_RATE * FRAME_RATE

def noteToPitch(note):
	return (2 ** (float(note - 69) / 12)) * 440

def osc(pitch, frame):
	t = float(frame) / FRAME_RATE
	return numpy.sin(t * pitch * numpy.pi * 2)

def synthesize(frame):
	global notes
	global next_event
	global current_tick

	while frame >= tickToFrame(current_tick + next_event.tick):
		if type(next_event) is midi.NoteOnEvent:
			notes[next_event.get_pitch()] = (type(next_event) is midi.NoteOnEvent)

		current_tick += next_event.tick
		next_event = track.next()

	amp = [osc(noteToPitch(note[0]), frame) for note in enumerate(notes) if note[1]]

	if amp:
		return numpy.mean(amp)
	else:
		return 0.0

def callback(in_data, frame_count, time_info, status):
	global current_frame
	global next_event

	frames = range(current_frame, current_frame + frame_count)
	chunk = numpy.array([synthesize(frame) for frame in frames])

	current_frame += frame_count
	out_data = chunk.astype(numpy.float32).tostring()
	return (out_data, pyaudio.paContinue)

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paFloat32, channels=1, rate=FRAME_RATE, input=True, output=True, stream_callback=callback)

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
