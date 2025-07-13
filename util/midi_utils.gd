class_name MIDIUtils

static func note_name(note: int, with_octave = true) -> String:
	if note < 0 or note > 127:
			return "Invalid MIDI Note"
	
	# Calculate octave and note name
	var names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
	var name = names[note % 12]
	
	if not with_octave:
		return name
	
	var octave = (floor(note) / 12) - 1
	name = "%s%s" % [name, octave]
	#print(note_int, name)
	return name

#const chord_bottom_notes = {
	#'F': ['F', 'C'],
	#'a': ['A', 'E'] 
#}

const intervals_bottom = [0, 7]
const intervals_major = [0, 4, 7]
const intervals_minor = [0, 3, 7]

static func chord_bottom_notes(root_note: int):
	return intervals_bottom.map(func(st): return (root_note + st) % 12)
	

static func valid_note_in_chord(chord_root_note: int, note: int):
	chord_root_note = chord_root_note % 12
	note = note % 12
	return note in chord_bottom_notes(chord_root_note)

#note_name = note_name.substr(0, 1)
#return note_name in chord_bottom_notes[chord]
	
#for i in range(0, 8):
	#valid_notes.append("C%d" % i)
	#valid_notes.append("G%d" % i)
#print(valid_notes)
