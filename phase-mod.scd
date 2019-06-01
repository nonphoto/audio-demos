(
SynthDef(\phaseMod, {
	arg amp = 0.1, freq = 200, phaseAmp = 0.1, phaseFreq = 300, gate = 1;
	var env, modulator, carrier, out;
	env = EnvGen.kr(Env.adsr, gate, doneAction: 0);
	modulator = SinOsc.kr(phaseFreq, 0, phaseAmp);
	carrier = SinOsc.ar(freq, modulator, amp) * env;
	Out.ar(0, carrier!2);
}).add;
)

x = Synth.new(\phaseMod);
x.set(\gate, 1);
x.set(\phaseAmp, 1);
x.set(\phaseFreq, 400);

s.scope;