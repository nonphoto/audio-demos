~samplePath = thisProcess.nowExecutingPath.dirname +/+ "samples/drums/";
~sampleNames = Array.with("kick", "snare");

(
SynthDef(\playBuffer, {
	arg buffer, amp = 1.0, rate = 1.0, t_trig = 0;
	var sig;
	sig = PlayBuf.ar(1, buffer, BufRateScale.kr(buffer) * rate, t_trig);
	sig = Pan2.ar(sig, 0);
	Out.ar(0, sig * amp)
}).add;
)

(
x = Buffer.read(s, ~samplePath ++ "kick" ++ "-acoustic01.wav");
y = Synth.new(\playBuffer, [\buffer, x]);
)

y.set(\t_trig, 1);

(
x.free;
y.free;
)

d = Dictionary.new();

(
~sampleNames.do({
	arg name;
	var buffer, synth;
	buffer = Buffer.read(s, ~samplePath ++ name ++ "-acoustic01.wav");
	synth = Synth.new(\playBuffer, [\buffer, buffer]);
	d.put(name, synth);
});
)

d["kick"].set(\t_trig, 1);
d["snare"].set(\t_trig, 1);