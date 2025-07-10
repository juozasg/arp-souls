extends Node2D

var note_stream_players: Dictionary[int, AudioStreamPlayer] = {}
var fading_stream_players: Array[AudioStreamPlayer] = []

#func _ready():
	#pass

func _input(e):
	if e.is_action_pressed('ui_cancel') and not %WebPlatform.is_web():
		get_tree().quit()
	if e is InputEventKey and e.pressed and e.keycode == KEY_D:
		%DebugLabel.visible = !%DebugLabel.visible
