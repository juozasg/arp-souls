extends Node

var ticks: Array[float] = []
var dticks: Array[float] = []
var tick0 = Time.get_ticks_msec()
var idle_dt = 0.0
var bpm = 0.0
var error_score = 0.0
var health = 100.0
var stamina = 0.0
var stamina_mult = 1.0
var mana = 0.0
var souls = 0.0
var error_mult = 0.0

const valid_notes = ['C4', 'G4', 'C5']
var last_note = ''

func _ready():
	OS.open_midi_inputs()
	print("MIDI OPEN", OS.get_connected_midi_inputs())
	print('tick0 ', tick0)

	#var tick0 = O)f
#
#
func _input(e):
	if not (e is InputEventMIDI):
		return

	var midi: InputEventMIDI = e
	if midi.message == MIDI_MESSAGE_NOTE_ON or midi.message == MIDI_MESSAGE_NOTE_OFF:
		%PianoPlayer.note_event(midi)
		
	if midi.message == MIDI_MESSAGE_NOTE_ON:
		tempo_input()
		var note_name = MIDIUtils.midi_note_int_to_string(midi.pitch)
		if note_name in valid_notes and note_name != last_note:
			good_note()
		else:
			bad_note()
		last_note = note_name
		

func good_note():
	mana = mana + stamina_mult
	#print('good note')
	

func bad_note():
	var damage = bpm / 5
	if bpm > 100:
		damage += (bpm - 100) / 2
	print("DAMAGE = ", damage)
	stamina = clamp(stamina - damage, 0.0, 100)
	health = clamp(health - damage, 0.0, 100)
	print("bad note")
	

func _process(dt: float):
	idle_dt += dt
	if idle_dt > 1.0:
		ticks.clear()
		calc_tempo()
		idle_dt = 0.0
	if error_score >= 7.0:
		error_mult = (1 + (error_score - 7.0)) ** 1.5 # winning from 1 to 8
	else:
		error_mult = (error_score - 8.0) / 2
	#error_mult = ((error_score - 7.0)) / 5.0
	stamina += (20 * dt * error_mult)
	stamina = clamp(stamina, 0.0, 100.0)
	
	if stamina >= 99.5:
		stamina_mult += (0.2 * dt * error_mult)
		stamina_mult = clamp(stamina_mult, 1.0, 15)
		health = clamp(health + (15 * dt), 0, 100.0)
	else:
		stamina_mult = 1.0
	
	%STAMINA.value = stamina
	%STAMINA_MULT.text = "%.1fx" % stamina_mult
	
	%HEALTH.value = health
	%MANA.text = "%d" % mana
	%SOULS.text = "%d" % souls
		
		

func tempo_input():
	var tick = Time.get_ticks_msec() - tick0
	if ticks.size() > 0:
		var lastdt = tick - ticks[-1]
		if(lastdt > 1000):
			ticks.clear()
		if(lastdt < 100):
			return
	
	idle_dt = 0.0	
	ticks.append(tick)
	calc_tempo()

func calc_tempo():
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
		bpm = 0
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

		bpm = 30_000 / mean
		

		%DebugLabel.text = "TS: %s\nDTS: %s   BPM: %.1f   dt_changes: %s \n error_mult=%f" % [ticks, dticks, bpm, dt_changes, error_mult]
	%RHYTHM.set_score(error_score)
	%BPM.text = "%d" % bpm
	if bpm > 100:
		pass
	else:
		pass



#func _physics_process(delta: float) -> void:
	
