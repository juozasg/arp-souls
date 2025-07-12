extends Node

var valid_notes = []
var last_notes = []


func _ready():
	OS.open_midi_inputs()
	print("MIDI OPEN", OS.get_connected_midi_inputs())
	print('tick0 ', %Tempo.tick0)
	
	for i in range(0, 8):
		valid_notes.append("C%d" % i)
		valid_notes.append("G%d" % i)
	print(valid_notes)


func _input(e):
	if not (e is InputEventMIDI):
		return

	var midi: InputEventMIDI = e
	if midi.message == MIDI_MESSAGE_NOTE_ON or midi.message == MIDI_MESSAGE_NOTE_OFF:
		%PianoPlayer.note_event(midi)
		
	if midi.message == MIDI_MESSAGE_NOTE_ON:
		%Tempo.tempo_input()
		var note_name = MIDIUtils.midi_note_int_to_string(midi.pitch)
		if note_name in valid_notes and note_name not in last_notes:
			%ScoreLogic.good_note()
		else:
			%ScoreLogic.bad_note()
		# REAL LOGIC FOR CHORDS AND UI
		last_notes.push_front(note_name)
		if last_notes.size() > 1:
			last_notes.pop_back()


	
