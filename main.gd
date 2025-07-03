extends Node2D

@export var sound: VASynthConfiguration
var note_contexts = {}
var synth

func _ready():
	OS.open_midi_inputs()
	# Create a synth player
	
	synth = AudioSynthPlayer.new()
	synth.configuration = sound
	add_child(synth)
	
	# Play a note
	var context = synth.get_context()
	context.note_on(60, 0.8)  # MIDI note 60 (C4) with velocity 0.8
	
	# Stop the note after 1 second
	await get_tree().create_timer(1.0).timeout
	context.note_off(context.absolute_time)
	

func _input(input_event):
	if not (input_event is InputEventMIDI):
		return

	var midi_event: InputEventMIDI = input_event
	var note = midi_event.pitch
	if midi_event.message == MIDI_MESSAGE_NOTE_ON:
		note_contexts[note] = synth.get_context()
		note_contexts[note].note_on(note, midi_event.velocity)
	else:
		note_contexts[note].note_off(0)

	#add_child(synth)
#
#func initialize_synth() -> void:
	#synth = AudioSynthPlayer.new()
	#synth.configuration = sound
	#add_child(synth)
#
#func _ready() -> void:
	#initialize_synth()
	#
	#$PlayButton.pressed.connect(play_note)
#
#
#func play_note():
	#var context = synth.get_context()
	#context.note_on(62, 100)  # Start a note
	#context.note_off(1)           	# Release a note
	#context = null                   # Release the context object from memory
