extends Node

var times: Array[float] = []
var dtimes: Array[float] = []
var tick0 = Time.get_ticks_msec()

func _ready():
	OS.open_midi_inputs()
	print("MIDI OPEN", OS.get_connected_midi_inputs())
	print('tick0 ', tick0)

	#var tick0 = O)f


func _input(input_event):
	if not (input_event is InputEventMIDI):
		return

	var midi_event: InputEventMIDI = input_event
	if midi_event.message == MIDI_MESSAGE_NOTE_ON or midi_event.message == MIDI_MESSAGE_NOTE_OFF:
		%PianoPlayer.note_event(midi_event)
		
	if midi_event.message == MIDI_MESSAGE_NOTE_ON:
		var tick = Time.get_ticks_msec() - tick0
		times.append(tick)
		if times.size() > 4:
			times = times.slice(1, 5)
		dtimes.clear()
		for i in range(0, times.size() - 1):
			dtimes.append(times[i+1] - times[1])
		print('dtick ' , tick)



#func _physics_process(delta: float) -> void:
	

func _process(delta: float) -> void:
	pass
