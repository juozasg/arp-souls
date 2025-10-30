extends Node

class_name MidiLogic

enum ChordType {MAJOR, MINOR}

class Chord:
	var root_semitone: int = 0
	var chord_type: ChordType = ChordType.MAJOR
	
	func _init(r: int, ct: ChordType = ChordType.MAJOR):
		root_semitone = r
		chord_type = ct
		

enum GameState {OUTPUT_QUESTION, INPUT_ANSWER, QUESTION_COMPLETED}

#var chord_pool = [5, 9, 10, 0] # F, A, A#, C
#var chord_pool = [5, 7] # F, G
var chord_pool = [4, 5, 6, 7] # E, F, F#, G
var current_chord = Chord.new(5)
var next_chord = Chord.new(7)
var gamestate: GameState = GameState.QUESTION_COMPLETED



func _ready():
	OS.open_midi_inputs()
	print("MIDI OPEN", OS.get_connected_midi_inputs())


func _input(e):
	if not (e is InputEventMIDI):
		return

	var midi: InputEventMIDI = e
	if midi.message == MIDI_MESSAGE_NOTE_ON or midi.message == MIDI_MESSAGE_NOTE_OFF:
		%PianoPlayer.note_event(midi)
		
	if midi.message == MIDI_MESSAGE_NOTE_ON:
		var note = midi.pitch % 12
		if(note == current_chord.root_semitone):
			print("you got it!")
		#if note == last_note0 && note == last_note1:
			#%ScoreLogic.bad_note()
			##%NoteHints/Hint1/Label.text
		#elif MIDIUtils.valid_note_in_chord(current_chord, note):
			#%Anim.play("flash_chord_green")
			#%ScoreLogic.good_note()
		#elif MIDIUtils.valid_note_in_chord(current_chord, note) and MIDIUtils.valid_note_in_chord(next_chord, note):
			## TODO: flash both chords
			#%Anim.play("flash_chord_green")
			#%Anim.play("flash_chord2_green")
			#%ScoreLogic.good_note()
		#elif MIDIUtils.valid_note_in_chord(next_chord, note):
			#%ScoreLogic.good_note()
			#%ScoreLogic.chord_change()
			#%Anim.play("flash_chord2_green")
			#%Anim.play("fade_out_chord")
			#%Anim.play("flash_arrow")
			#chord_change()
		#else:
			#%ScoreLogic.bad_note()
			#%Anim.play("flash_red")



func chord_change():
	current_chord = next_chord
	var different_pool = chord_pool.duplicate()
	different_pool.erase(current_chord)
	next_chord = different_pool.pick_random()


#func _process(dt: float):
	#pass



	
