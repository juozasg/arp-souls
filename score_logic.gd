extends Node

var config = ConfigFile.new()

var health = 100.0
var stamina = 0.0
var stamina_mult = 1.0
var mana = 0.0
var souls = 0.0
var is_dead = false


func _ready():
	var err = config.load("user://scores.cfg")
	if err == OK:
		mana = config.get_value("Score", "mana", 0)
		souls = config.get_value("Score", "souls", 0)
		print("loaded scores")


func good_note():
	if not is_dead:
		mana = mana + stamina_mult
		score_updated()
	#print('good note')
	

func bad_note():
	var damage = %Tempo.bpm / 5
	if %Tempo.bpm > 100:
		damage += (%Tempo.bpm - 100) / 1.5
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
	
	if(stamina_mult > 15.0):
		%STAMINA_MULT.set("theme_override_colors/font_color", Color.from_rgba8(255, 89, 89, 255))
	else:
		%STAMINA_MULT.set("theme_override_colors/font_color", Color.from_rgba8(58, 187, 62, 255))

	if %Tempo.tempo_score < 7.0:
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
