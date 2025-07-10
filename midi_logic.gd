extends Node

var config = ConfigFile.new()


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

var valid_notes = []
var last_notes = []


func _ready():
	OS.open_midi_inputs()
	print("MIDI OPEN", OS.get_connected_midi_inputs())
	print('tick0 ', tick0)
	
	for i in range(0, 8):
		valid_notes.append("C%d" % i)
		valid_notes.append("G%d" % i)
	print(valid_notes)
	var err = config.load("user://scores.cfg")
	if err == OK:
		mana = config.get_value("Score", "mana", 0)
		souls = config.get_value("Score", "souls", 0)
		print("loaded scores")


func _input(e):
	if not (e is InputEventMIDI):
		return

	var midi: InputEventMIDI = e
	if midi.message == MIDI_MESSAGE_NOTE_ON or midi.message == MIDI_MESSAGE_NOTE_OFF:
		%PianoPlayer.note_event(midi)
		
	if midi.message == MIDI_MESSAGE_NOTE_ON:
		tempo_input()
		var note_name = MIDIUtils.midi_note_int_to_string(midi.pitch)
		if note_name in valid_notes and note_name not in last_notes:
			good_note()
		else:
			bad_note()
		# REAL LOGIC FOR CHORDS AND UI
		last_notes.push_front(note_name)
		if last_notes.size() > 1:
			last_notes.pop_back()
		
var is_dead = false

func good_note():
	if not is_dead:
		mana = mana + stamina_mult
		score_updated()
	#print('good note')
	

func bad_note():
	var damage = bpm / 5
	if bpm > 100:
		damage += (bpm - 100) / 1.5
	#print("DAMAGE = ", damage)
	stamina = clamp(stamina - damage, 0.0, 100)
	health = clamp(health - damage, 0.0, 100)
	if health == 0.0:
		died()
	#print("bad note")

func score_updated():
	config.set_value("Score", "mana", mana)
	config.set_value("Score", "souls", souls)
	config.save("user://scores.cfg")
	#print("saved scores")

func died():
	if not is_dead:
		var lost_mana = mana * 0.2
		mana = mana - lost_mana
		score_updated()
		if lost_mana > 1.0:
			%LOSTMANA.text = "-%d MANA" % lost_mana
		else:
			%LOSTMANA.text = "NO MANA LOST"
		is_dead = true
	
	

func _process(dt: float):
	idle_dt += dt
	if idle_dt > 1.0:
		ticks.clear()
		calc_tempo()
		idle_dt = 0.0
	if error_score >= 7.0:
		error_mult = (1 + (error_score - 7.0)) ** 1.5 # winning from 1 to 8
		if bpm > 100:
			var bpm_bump = clamp((bpm - 100) / 15, 0, 8)
			error_mult += bpm_bump
			
	else:
		error_mult = (error_score - 8.0) / 2
	#error_mult = ((error_score - 7.0)) / 5.0
	stamina += (20 * dt * error_mult)
	stamina = clamp(stamina, 0.0, 100.0)
	
	
	var extra_max_stamina_mult = 0
	if(bpm > 100):
		extra_max_stamina_mult = (bpm - 100) / 10.0
	if stamina >= 99.5:
		stamina_mult += (0.2 * dt * error_mult)
		stamina_mult = clamp(stamina_mult, 1.0, 15 + extra_max_stamina_mult)
		health = clamp(health + (15 * dt), 0, 100.0)
		is_dead = false
	else:
		stamina_mult = 1.0
	
	if(stamina_mult > 15.0):
		%STAMINA_MULT.set("theme_override_colors/font_color", Color.from_rgba8(255, 89, 89, 255))
	else:
		%STAMINA_MULT.set("theme_override_colors/font_color", Color.from_rgba8(58, 187, 62, 255))

	if error_score < 7.0:
		%LabelStamina.set("theme_override_colors/font_color", Color.from_hsv(0, 0, 1, 0.4))
	else:
		%LabelStamina.set("theme_override_colors/font_color", Color.from_hsv(0, 0, 1, 1.0))
		

	%STAMINA.value = stamina
	%STAMINA_MULT.text = "%.1fx" % stamina_mult
	
	%HEALTH.value = health
	%MANA.text = "%d" % mana
	%SOULS.text = "%d" % souls
	if is_dead:
		%DEAD.show()
	else:
		%DEAD.hide()
		
	#%DebugLabel.text = "error_mult=%f" % [error_mult]


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
	var window_size = 7

	if ticks.size() > window_size:
		ticks = ticks.slice(1, window_size + 1)
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

		var window_fullness = ticks.size() / window_size
		error_score = clamp(error_score, 0.0, 7.0 + (3 * window_fullness))

		bpm = 30_000 / mean
		

		%DebugLabel.text = "TS: %s DTS: %s\ndt_changes: %s \nerror_mult=%f" % [ticks, dticks, dt_changes, error_mult]
	%RHYTHM.set_score(error_score)
	%BPM.text = "%d" % bpm
	if bpm >= 100:
		%BPM.set("theme_override_colors/font_color", Color.from_rgba8(255, 89, 89, 255))
	else:
		%BPM.set("theme_override_colors/font_color", Color.from_rgba8(255,255,255, 255))




#func _physics_process(delta: float) -> void:
	
