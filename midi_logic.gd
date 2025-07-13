extends Node

var last_note0 = -1
var last_note1 = -1


#var chord_pool = [5, 9, 10, 0] # F, A, A#, C
var chord_pool = [5, 7] # F, C

var current_chord = 5
var next_chord = 7

func _ready():
	OS.open_midi_inputs()
	print("MIDI OPEN", OS.get_connected_midi_inputs())
	print('tick0 ', %Tempo.tick0)
	%CHORD.text = MIDIUtils.note_name(current_chord, false)
	%CHORD2.text = MIDIUtils.note_name(next_chord, false)
	

func _input(e):
	if not (e is InputEventMIDI):
		return

	var midi: InputEventMIDI = e
	if midi.message == MIDI_MESSAGE_NOTE_ON or midi.message == MIDI_MESSAGE_NOTE_OFF:
		%PianoPlayer.note_event(midi)
		
	if midi.message == MIDI_MESSAGE_NOTE_ON:
		%Tempo.tempo_input()
		var note = midi.pitch % 12
		if note == last_note0 && note == last_note1:
			%ScoreLogic.bad_note()
			
		elif MIDIUtils.valid_note_in_chord(current_chord, note):
			%Anim.play("flash_chord_green")
			%ScoreLogic.good_note()
		elif MIDIUtils.valid_note_in_chord(current_chord, note) and MIDIUtils.valid_note_in_chord(next_chord, note):
			# TODO: flash both chords
			%Anim.play("flash_chord_green")
			%Anim.play("flash_chord2_green")
			%ScoreLogic.good_note()
		elif MIDIUtils.valid_note_in_chord(next_chord, note):
			%ScoreLogic.good_note()
			%ScoreLogic.chord_change()
			%Anim.play("flash_chord2_green")
			%Anim.play("fade_out_chord")
			%Anim.play("flash_arrow")
			chord_change()
		else:
			%ScoreLogic.bad_note()
			
		# REAL LOGIC FOR CHORDS AND UI
		last_note1 = last_note0
		last_note0 = note

func chord_change():
	current_chord = next_chord
	var different_pool = chord_pool.duplicate()
	different_pool.erase(current_chord)
	next_chord = different_pool.pick_random()
	
	%CHORD.text = MIDIUtils.note_name(current_chord, false)
	%CHORD2.text = MIDIUtils.note_name(next_chord, false)

#func _process(dt: float):
	#pass



	
