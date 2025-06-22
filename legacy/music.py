def note_val(note_name: str) -> int:
    """
    Convert a note name (e.g., 'C4', 'F#5', 'Bb3') to its MIDI note value.

    Args:
        note_name (str): A string representing a musical note with format:
                         [note letter][accidental][octave]
                         where accidental is optional and can be # (sharp) or b (flat)

    Returns:
        int: The MIDI note value (0-127) or None if the note name is invalid
    """
    if not note_name or len(note_name) < 2:
        raise ValueError("Invalid note name", note_name)

    # Parse the note name
    note_letter = note_name[0].upper()

    # Check if there's an accidental
    idx = 1
    accidental = 0
    if idx < len(note_name) and (note_name[idx] == '#' or note_name[idx] == 'b'):
        if note_name[idx] == '#':
            accidental = 1
        else:  # flat
            accidental = -1
        idx += 1

    # Get the octave
    try:
        octave = int(note_name[idx:])
    except ValueError:
        raise ValueError("Invalid note name", note_name)

    # Base values for notes (C, D, E, F, G, A, B)
    base_values = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

    if note_letter not in base_values:
        raise ValueError("Invalid note name", note_name)

    # Calculate MIDI note value
    # MIDI note 60 is middle C (C4)
    midi_value = 12 * (octave + 1) + base_values[note_letter] + accidental

    # Ensure the note is within MIDI range (0-127)
    if 0 <= midi_value <= 127:
        return midi_value
    else:
        raise ValueError("Invalid note name", note_name)

def note_name(midi_value: int) -> str:
    if not isinstance(midi_value, int) or midi_value < 0 or midi_value > 127:
        raise ValueError("Invalid note MIDI value", midi_value)

    # Note names without accidentals
    note_names = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

    # Calculate octave and note index
    octave = (midi_value // 12) - 1
    note_idx = midi_value % 12

    # Construct the note name
    return f"{note_names[note_idx]}{octave}"
