~notes = Array.newClear(128);

(
SynthDef(\sin, {
	arg amp = 0.1, pitch = 440, gate = 1;
	var env, sig, out;
	env = EnvGen.kr(Env.adsr, gate, doneAction: 2);
	sig = SinOsc.ar(pitch, 0.0, amp) * env;
	Out.ar(0, sig!2);
}).add;
)

x = Synth.new(\sin, [\amp, 0.5]);
x.free;

(
OSCFunc({
	arg msg, time, addr, port;
	var noteIndex;
	msg.postln;
	noteIndex = msg[1].asInt;
	~notes[noteIndex] = Synth.new(\sin, [\pitch, noteIndex.midicps, \gate, 1]);
}, "/noteOn");

OSCFunc({
	arg msg, time, addr, port;
	var noteIndex;
	msg.postln;
	noteIndex = msg[1].asInt;
	~notes[noteIndex].set(\gate, 0);
	~notes[noteIndex] = nil;
}, "/noteOff");
)

m = NetAddr("127.0.0.1", NetAddr.langPort)
m.sendMsg("/noteOn", 60);
m.sendMsg("/noteOff", 60);
m.sendMsg("/noteOn", 69);
m.sendMsg("/noteOff", 69);
