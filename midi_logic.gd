extends Node

var ticks: Array[float] = []
var dticks: Array[float] = []
var tick0 = Time.get_ticks_msec()
var bpm = 0.0

func _ready():
	OS.open_midi_inputs()
	print("MIDI OPEN", OS.get_connected_midi_inputs())
	print('tick0 ', tick0)

	#var tick0 = O)f


func _input(input_event):
	if not (input_event is InputEventMIDI):
		return

	var midi_event: InputEventMIDI = input_event
	if midi_event.message == MIDI_MESSAGE_NOTE_ON or midi_event.message == MIDI_MESSAGE_NOTE_OFF:
		%PianoPlayer.note_event(midi_event)
		
	if midi_event.message == MIDI_MESSAGE_NOTE_ON:
		calc_tempo()

		
		

func calc_tempo():
	var tick = Time.get_ticks_msec() - tick0
	if ticks.size() > 0:
		var lastdt = tick - ticks[-1]
		if(lastdt > 1000):
			ticks.clear()
	ticks.append(tick)
	if ticks.size() > 5:
		ticks = ticks.slice(1, 6)
	dticks.clear()
	for i in range(0, ticks.size() - 1):
		dticks.append(ticks[i+1] - ticks[i])
	#print('dtick ' , tick)
	%DebugLabel.text = "TS: %s\nDTS: %s   BPM: %.1f" % [ticks, dticks, bpm]
	
	if dticks.size() < 2:
		%RHYTHM.text = "X"
	else:
		var mean = dticks.reduce(func(t, sum): return sum + t) / dticks.size()
		bpm = 60_000 / mean
		var variance = dticks.reduce(func(t, sum): return (t - mean) ** 2) / (dticks.size())
		var stdev = (variance ** 0.5) / 100
		%RHYTHM.text = "%.1f" % stdev


#func _physics_process(delta: float) -> void:
	

func _process(delta: float) -> void:
	pass
