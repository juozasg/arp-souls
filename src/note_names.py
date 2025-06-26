NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#' 'A', 'A#', 'B']

def midi_code_to_name(midi_code: int) -> str:
    midi_code = int(midi_code) % 12
    return NOTE_NAMES[midi_code]
