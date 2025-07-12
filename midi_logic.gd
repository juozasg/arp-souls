extends Node

var last_note = ''

var current_chord = 'F'
var next_chord = 'a'

func _ready():
	OS.open_midi_inputs()
	print("MIDI OPEN", OS.get_connected_midi_inputs())
	print('tick0 ', %Tempo.tick0)
	

func _input(e):
	if not (e is InputEventMIDI):
		return

	var midi: InputEventMIDI = e
	if midi.message == MIDI_MESSAGE_NOTE_ON or midi.message == MIDI_MESSAGE_NOTE_OFF:
		%PianoPlayer.note_event(midi)
		
	if midi.message == MIDI_MESSAGE_NOTE_ON:
		%Tempo.tempo_input()
		var note_name = MIDIUtils.midi_note_int_to_string(midi.pitch)
		if note_name == last_note:
			%ScoreLogic.bad_note()
		elif MIDIUtils.valid_note_in_chord(note_name, current_chord):
			%ScoreLogic.good_note()
		elif MIDIUtils.valid_note_in_chord(note_name, current_chord) and MIDIUtils.valid_note_in_chord(note_name, next_chord):
			# TODO: flash both chords
			%ScoreLogic.good_note()
		elif MIDIUtils.valid_note_in_chord(note_name, next_chord):
			%ScoreLogic.good_note()
			%ScoreLogic.chord_change()
			chord_change()
		else:
			%ScoreLogic.bad_note()

			

			
		# REAL LOGIC FOR CHORDS AND UI
		last_note = note_name

func chord_change():
	var old_chord = current_chord
	current_chord = next_chord
	next_chord = old_chord

func _process(dt: float):
	%CHORD.text = current_chord
	%CHORD2.text = next_chord


	
