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
next_event = track.next()
notes = [False] * 128

TEMPO = 120
RESOLUTION = pattern.resolution
TICK_RATE = float(TEMPO * RESOLUTION) / 60
FRAME_RATE = 44100

def tickToFrame(tick):
	return int(float(tick) / TICK_RATE * FRAME_RATE)

def osc(pitch, frame):
	t = frame / FRAME_RATE
	return numpy.sin(t * pitch * numpi.pi * 2)

def synthesize(frame):
	global notes
	global next_event

	print frame
	print tickToFrame(next_event.tick)

	while frame >= tickToFrame(next_event.tick):
		if type(next_event) is midi.NoteEvent:
			notes[next_event.get_pitch()] = (type(next_event) is midi.NoteOnEvent)

		next_event = track.next()

	amp = [osc(*note) for note in enumerate(notes) if note[1]]

	if amp:
		return numpy.mean(amp)
	else:
		return 0.0

def callback(in_data, frame_count, time_info, status):
	global current_frame
	global next_event
	global notes

	active_notes = [note for note in enumerate(notes) if note[1]]

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
