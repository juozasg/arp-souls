extends Node

var config = ConfigFile.new()

var health = 100.0
var stamina = 0.0
var stamina_mult = 1.0
var mana = 0.0
var souls = 0.0

var mana_timed_scores = []
var souls_timed_scores = []
var mana_rate = 0.0
var souls_rate = 0.0

var score_rate_dt = 0.0


var is_dead = false

var tick0 = 0


func _ready():
	tick0 = Time.get_ticks_msec()
	var err = config.load("user://scores.cfg")
	if err == OK:
		mana = config.get_value("Score", "mana", 0)
		souls = config.get_value("Score", "souls", 0)
		#mana = 0
		discrete_update_labels()
		print("loaded scores")


func good_note():
	if not is_dead:
		var win_mana = stamina_mult
		mana += win_mana
		mana_timed_scores.append([Time.get_ticks_msec(), win_mana])

		score_updated()
	#print('good note')
	discrete_update_labels()

func bad_note():
	#print("BAD NOTE")
	var damage = %Tempo.bpm / 5
	if %Tempo.bpm > 100:
		damage += (%Tempo.bpm - 100) / 1.5
	#print("DAMAGE = ", damage)
	stamina = clamp(stamina - damage, 0.0, 100)
	health = clamp(health - damage, 0.0, 100)
	if health == 0.0:
		died()
	#print("bad note")
	discrete_update_labels()

func chord_change():
	if not is_dead:
		var win_souls = stamina_mult
		souls += win_souls
		souls_timed_scores.append([Time.get_ticks_msec(), win_souls])
		score_updated()

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
		%Tempo.died()
	
func _process(dt: float):
	#error_mult = ((tempo_score - 7.0)) / 5.0
	stamina += (20 * dt * %Tempo.error_mult)
	stamina = clamp(stamina, 0.0, 100.0)
	
	var extra_max_stamina_mult = 0
	if(%Tempo.bpm > 100):
		extra_max_stamina_mult = (%Tempo.bpm - 100) / 10.0
	if stamina >= 99.5:
		stamina_mult += (0.2 * dt * %Tempo.error_mult)
		stamina_mult = clamp(stamina_mult, 1.0, 15 + extra_max_stamina_mult)
		health = clamp(health + (15 * dt), 0, 100.0)
		is_dead = false
	else:
		stamina_mult = 1.0
	
	score_rate_dt += dt
	if score_rate_dt >= 1.0:
		var last_10_secs = Time.get_ticks_msec() - 10_000
		souls_timed_scores = souls_timed_scores.filter(func(e): return e[0] > last_10_secs)
		mana_timed_scores = mana_timed_scores.filter(func(e): return e[0] > last_10_secs)
		var souls_window_sum = souls_timed_scores.reduce(func(accum, e): return e[1] + accum, 0)
		var mana_window_sum = mana_timed_scores.reduce(func(accum, e): return e[1] + accum, 0)
		
		var window_length = 10.0
		if last_10_secs < tick0:
			window_length = (Time.get_ticks_msec() - tick0) / 1000.0
		souls_rate = souls_window_sum / window_length
		mana_rate = mana_window_sum / window_length
		
		score_rate_dt = 0
		score_rate_update_labels()
		
	#Time.get_ticks_msec()
	
	smooth_update_labels()

# updating labels on each note should be more visceral feedback
func discrete_update_labels():
	if %Tempo.tempo_score < 7.0 and %Tempo.tempo_score > 0.0:
		%LabelStamina.set("theme_override_colors/font_color", Color.from_hsv(0, 0, 1, 0.4))
	else:
		%LabelStamina.set("theme_override_colors/font_color", Color.from_hsv(0, 0, 1, 1.0))

	if is_dead:
		%LabelHealth.set("theme_override_colors/font_color", Color.from_hsv(0, 0, 1, 0.4))
	else:
		%LabelHealth.set("theme_override_colors/font_color", Color.from_hsv(0, 0, 1, 1.0))		
	
	%STAMINA_MULT.text = "%.1fx" % stamina_mult
	if(stamina_mult > 15.0):
		%STAMINA_MULT.set("theme_override_colors/font_color", Color.from_rgba8(255, 89, 89, 255))
	else:
		%STAMINA_MULT.set("theme_override_colors/font_color", Color.from_rgba8(58, 187, 62, 255))
	
	%MANA.text = "%d" % mana
	%SOULS.text = "%d" % souls
	
	score_rate_update_labels()
	
func score_rate_update_labels():
	if mana_rate == 0:
		%MANARATE.text = "0/s"
	else:
		%MANARATE.text = "%.1f/s" % mana_rate
	
	if souls_rate == 0:
		%SOULSRATE.text = "0/s"
	else:
		%SOULSRATE.text = "%.1f/s" % souls_rate
	
	
func smooth_update_labels():
	%STAMINA.value = stamina
	%HEALTH.value = health
	if is_dead:
		%DEAD.show()
	else:
		%DEAD.hide()
