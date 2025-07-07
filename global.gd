extends Node

const res_x = 640
const res_y = 360
func _ready() -> void:
	print("AUTOLOAD")
	print(DisplayServer.screen_get_size())
	print("RESIZING")
	var width = DisplayServer.screen_get_size().x
	var scale_factor = clamp(floori(width/ 1000.0), 1, 4)
	if JavaScriptBridge.get_interface('window') != null:
		scale_factor = clamp(scale_factor, 1, 3)

	get_window().content_scale_size = Vector2i(res_x, res_y)
	get_window().size = Vector2i(res_x * scale_factor, res_y * scale_factor)
	get_window().position = Vector2i(DisplayServer.screen_get_size().x/2, 300 )
	#get_window().type
