extends Node2D

var note_stream_players: Dictionary[int, AudioStreamPlayer] = {}
var fading_stream_players: Array[AudioStreamPlayer] = []

#func _ready():
	#pass

func _input(input_event):
	if input_event.is_action_pressed('ui_cancel') and not %WebPlatform.is_web():
		get_tree().quit()


#func _process(delta: float) -> void:
	#pass
	#
