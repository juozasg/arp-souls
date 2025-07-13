extends Node

var note_stream_players: Dictionary[int, AudioStreamPlayer] = {}
var fading_stream_players: Array[AudioStreamPlayer] = []

func _ready():
	var from = 12
	var to = 96
	for n in range(from, to+1):
		var player = AudioStreamPlayer.new()
		var note_name = MIDIUtils.note_name(n)
		player.stream = AudioStreamOggVorbis.load_from_file("res://grand-piano/%s.ogg" % note_name)
		note_stream_players[n] = player
		self.add_child(player)



func note_event(event: InputEventMIDI):
	var note = event.pitch
	var velocity = event.velocity
	var message = event.message
	
	var note_name = MIDIUtils.note_name(note)
	if message == MIDI_MESSAGE_NOTE_ON:
		var player = note_stream_players[note]
		player.play()
		print('ON ', note_name)
		player.volume_linear = clamp(0.1 + (0.9 * (velocity / 110.0)), 0.0, 1.0)
		#print(player.volume_linear)
		if fading_stream_players.has(player):
			fading_stream_players.erase(player)
		#print(MIDIUtils.midi_note_int_to_string(note))
	elif message == MIDI_MESSAGE_NOTE_OFF:
		print('      OFF ', note_name)
		var player = note_stream_players[note]
		if !fading_stream_players.has(player):
			fading_stream_players.append(player)
		#player.volume_linear = 0.5
		#player.stop()

func _process(delta: float) -> void:
	#print(delta)
	for p in fading_stream_players:
		p.volume_linear = clamp(p.volume_linear - (delta * 6), 0.0, 1.0)
		if p.volume_linear < 0.1:
			p.stop()
			fading_stream_players.erase(p)
