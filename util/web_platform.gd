extends Node

func is_web() -> bool:
	return JavaScriptBridge.get_interface('window') != null

func reload():
	JavaScriptBridge.get_interface('location').reload()

func _ready() -> void:
	print("is_web=", is_web())
	if not is_web():
		process_mode = Node.PROCESS_MODE_DISABLED
	
func _input(e: InputEvent):
	print("web input ", e)
	if e.is_action("reload"):
		reload()
	
	
