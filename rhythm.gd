extends Label

const min_hue = 356
const max_hue = 360+103
const range_hue = max_hue - min_hue

func set_score(score: float):
	if score >= 9.9:
		text = "10"
	elif score <= 0.0:
		text = "X"
	else:
		text = "%.1f" % score
		
	var hue = (int((min_hue + (range_hue * (score / 10.0)))) % 360) / 360.0
	var color = Color.from_hsv(hue, 1.0, 0.61)
	print(hue, " ", color)
	set("theme_override_colors/font_color", color)


	
