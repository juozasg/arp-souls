extends Node

var ticks: Array[float] = []
var dticks: Array[float] = []
var tick0 = Time.get_ticks_msec()
var idle_dt = 0.0
var bpm = 0.0
var tempo_score = 0.0
var error_mult = 0.0

func _process(dt: float):
	idle_dt += dt
	if idle_dt > 1.0:
		ticks.clear()
		calc_tempo()
		idle_dt = 0.0
	if tempo_score >= 7.0:
		error_mult = (1 + (tempo_score - 7.0)) ** 1.5 # winning from 1 to 8
		if bpm > 100:
			var bpm_bump = clamp((bpm - 100) / 15, 0, 8)
			error_mult += bpm_bump
			
	else:
		error_mult = (tempo_score - 8.0) / 2

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
		tempo_score = 0.0
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
		var new_tempo_score = 10.5 - (dt_changes_mean * 20)
		if tempo_score == 0.0:
			tempo_score = new_tempo_score
		else:
			tempo_score = (new_tempo_score * 0.3) + (tempo_score * 0.7)

		var window_fullness = ticks.size() / window_size
		tempo_score = clamp(tempo_score, 0.0, 7.0 + (3 * window_fullness))

		bpm = 30_000 / mean
		

		%DebugLabel.text = "TS: %s DTS: %s\ndt_changes: %s \nerror_mult=%f" % [ticks, dticks, dt_changes, error_mult]
	%RHYTHM.set_score(tempo_score)
	%BPM.text = "%d" % bpm
	if bpm >= 100:
		%BPM.set("theme_override_colors/font_color", Color.from_rgba8(255, 89, 89, 255))
	else:
		%BPM.set("theme_override_colors/font_color", Color.from_rgba8(255,255,255, 255))
