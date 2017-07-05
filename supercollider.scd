s.boot;
s.reboot;

(
SynthDef(\sin, {
	arg amp = 0.01, pitch = 440, trig = True;
	var env, sig;
	env = EnvGen.kr(Env.asr(1.0, 0.9, 1.0), trig, doneAction: 0);
	sig = SinOsc.ar(pitch, 0.0, amp) * env;
	Out.ar([0], sig * 0.6);
}).add;
)

h = Synth(\sin, [\amp, 0.4]);

(
x = OSCFunc({
	arg msg, time, addr, port;
	var pitch, trig;

	msg.postln;

	pitch = msg[1].asFloat;
	trig = msg[2].asBoolean;

	h.set(\pitch, pitch);
	h.set(\trig, trig);
}, '/event');
)

m = NetAddr("127.0.0.1", NetAddr.langPort)
m.sendMsg("/event", 440, 1);
m.sendMsg("/event", 440, 0);