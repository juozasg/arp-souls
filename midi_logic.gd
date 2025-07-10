extends Node

var ticks: Array[float] = []
var dticks: Array[float] = []
var tick0 = Time.get_ticks_msec()
var bpm = 0.0
var error_score = 0.0

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
		if(lastdt < 100):
			return
		
	ticks.append(tick)
	if ticks.size() > 7:
		ticks = ticks.slice(1, 8)
	dticks.clear()
	for i in range(0, ticks.size() - 1):
		dticks.append((ticks[i+1] - ticks[i])/1.0)
	#print('dtick ' , tick)
	#dticks = [250, 250, 250, 255, 250, 250] # 0.01 = perfect score
	#dticks = [950, 50, 250, 755, 500, 250] # 1.5 = worst ever

	if dticks.size() < 2:
		%RHYTHM.text = "X"
		error_score = 0.0
	else:
		var mean = dticks.reduce(func(t, sum): return sum + t) / dticks.size()
		var dt_changes = []
		for i in range(0, dticks.size() - 1):
			var t = dticks[i]
			var t1 = dticks[i+1]
			var scale_down_older = (dticks.size() - 1 - i) / 3.0
			scale_down_older = 1.0
			
			dt_changes.append((absf(t1-t)/t)/scale_down_older)
		var dt_changes_mean = dt_changes.reduce(func(t, sum): return sum + t) / dt_changes.size()
		var new_error_score = 10.5 - (dt_changes_mean * 20)
		if error_score == 0.0:
			error_score = new_error_score
		else:
			error_score = (new_error_score * 0.3) + (error_score * 0.7)

		error_score = clamp(error_score, 0.0, 10.0)

		bpm = 60_000 / mean
		

			
		#%RHYTHM.text = "%.5f" % error_score

		%DebugLabel.text = "TS: %s\nDTS: %s   BPM: %.1f   dt_changes: %s " % [ticks, dticks, bpm, dt_changes]
	%RHYTHM.set_score(error_score)



#func _physics_process(delta: float) -> void:
	

func _process(delta: float) -> void:
	pass
