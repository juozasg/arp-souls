extends Node2D

var note_stream_players: Dictionary[int, AudioStreamPlayer] = {}
var fading_stream_players: Array[AudioStreamPlayer] = []

func _ready():
	OS.open_midi_inputs()
	var from = 12
	var to = 96
	for n in range(from, to+1):
		var player = AudioStreamPlayer.new()
		var note_name = MIDIUtils.midi_note_int_to_string(n)
		player.stream = AudioStreamOggVorbis.load_from_file("res://grand-piano/%s.ogg" % note_name)
		note_stream_players[n] = player
		self.add_child(player)
		


func _input(input_event):
	if not (input_event is InputEventMIDI):
		return

	var midi_event: InputEventMIDI = input_event
	var note = midi_event.pitch
	if midi_event.message == MIDI_MESSAGE_NOTE_ON:
		var player = note_stream_players[note]
		player.play()
		#print(midi_event.velocity)
		player.volume_linear = min(0.1 + (0.9 * (midi_event.velocity / 110.0)), 1.0)
		#print(player.volume_linear)
		if fading_stream_players.has(player):
			fading_stream_players.erase(player)
		#print(MIDIUtils.midi_note_int_to_string(note))
	elif midi_event.message == MIDI_MESSAGE_NOTE_OFF:
		var player = note_stream_players[note]
		if !fading_stream_players.has(player):
			fading_stream_players.append(player)
		#player.volume_linear = 0.5
		#player.stop()

func _process(delta: float) -> void:
	#print(delta)
	for p in fading_stream_players:
		p.volume_linear -= (delta * 6)
		if p.volume_linear < 0.1:
			p.stop()
			fading_stream_players.erase(p)
