extends Node

func _ready() -> void:
	print("AUTOLOAD")
	print(DisplayServer.screen_get_size())
	print("RESIZING")
	var width = DisplayServer.screen_get_size().x
	var scale_factor = clamp(floori(width/ 1000.0), 1, 4)
	if JavaScriptBridge.get_interface('window') != null:
		scale_factor = clamp(scale_factor, 1, 3)

	get_window().content_scale_size = Vector2i(640, 360)
	get_window().size = Vector2i(640 * scale_factor, 360 * scale_factor)
	get_window().position = Vector2i(DisplayServer.screen_get_size().x/2, 300 )
	#get_window().type
