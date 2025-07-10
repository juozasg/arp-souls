extends Node

static func is_web() -> bool:
	return JavaScriptBridge.get_interface('window') != null

func reload():
	JavaScriptBridge.get_interface('location').reload()

func _ready() -> void:
	print("is_web=", is_web())
	if not is_web():
		process_mode = Node.PROCESS_MODE_DISABLED
		%ClickStartAudioUI.hide()
	else:
		%ClickStartAudioUI.show()
		%Howto.hide()
		%DebugLabel.hide()
	
func _input(e: InputEvent):
	#print("web input ", e)
	if e.is_action("reload"):
		reload()
	
	
func _on_enable_audio_gesture_pressed() -> void:
	%ClickStartAudioUI.hide()
	%Howto.show()
