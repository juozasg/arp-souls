import mido
import time
import threading
from typing import Any, Union

from game.midi.ports import get_output_port


def note_on(note=60, velocity=64):
    output_port = get_output_port()
    if output_port is None:
        print("Cannot play note: No valid MIDI output port provided")
        return

    try:
        # Send note on message
        note_on_msg = mido.Message('note_on', note=note, velocity=velocity)
        output_port.send(note_on_msg)
        # print(f"ON {note} ({velocity})")
    except Exception as e:
        print(f"Error sending note_on: {e}")


def note_off(note=60, velocity=64):
    output_port = get_output_port()
    if output_port is None:
        print("Cannot release note: No valid MIDI output port provided")
        return

    try:
        # Send note off message
        note_off_msg = mido.Message('note_off', note=note, velocity=velocity)
        output_port.send(note_off_msg)
        # print(f"OFF {note} ({velocity})")
    except Exception as e:
        print(f"Error sending note_off: {e}")


def play_note(note=60, velocity=64, duration=1.0):
    output_port = get_output_port()
    if output_port is None:
        print("Cannot play note: No valid MIDI output port provided")
        return

    try:
        note_on(note, velocity)

        # Hold for the specified duration
        time.sleep(duration)

        note_off(note, velocity)
    except Exception as e:
        print(f"Error playing note: {e}")




def midi_through_capture_off(message: Any) -> Union[int, bool]:
    if message.type == 'note_on':
        # When a note is pressed, play it on the output port
        if message.velocity > 0:
            # print(f"Received note: {message.note}, velocity: {message.velocity}")
            # Start a new thread to play the note asynchronously
            note_thread = threading.Thread(target=lambda: note_on(message.note, message.velocity))
            note_thread.daemon = True  # Thread will exit when main program exits
            note_thread.start()
            # return {'type': 'note_on', 'note': message.note}
    elif message.type == 'note_off':
        # When a note is released, send note off
        # print(f"Received note off: {message.note}")
        note_thread = threading.Thread(target=lambda: note_off(message.note, message.velocity))
        note_thread.daemon = True
        note_thread.start()
        # return {'type': 'note_off', 'note': message.note}
        return message.note

    return False

