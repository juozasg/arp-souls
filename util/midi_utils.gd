class_name MIDIUtils

static func midi_note_int_to_string(note_int: int) -> String:
	if note_int < 0 or note_int > 127:
			return "Invalid MIDI Note"
	
	# Calculate octave and note name
	var octave = (note_int / 12) - 1
	var note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
	var note_name = note_names[note_int % 12]
	
	var name = "%s%s" % [note_name, octave]
	#print(note_int, name)
	return name

const chord_bottom_notes = {
	'F': ['F', 'C'],
	'a': ['A', 'E'] 
}

static func valid_note_in_chord(note_name: String, chord: String):
	note_name = note_name.substr(0, 1)
	return note_name in chord_bottom_notes[chord]
	
#for i in range(0, 8):
	#valid_notes.append("C%d" % i)
	#valid_notes.append("G%d" % i)
#print(valid_notes)
