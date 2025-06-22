from game.game_state import GameState
from game.music import note_val
import threading
import time
from game.midi.note_play import note_on, note_off, play_note
from game.play_sounds import play_failure_sound, play_note_list, play_success_sound


def print_note_prompt(game_state: GameState):
    # Create a visual representation of the sequence progress
    sequence_length = len(game_state.target_sequence)
    progress = []

    # Add completed notes in green
    for i in range(game_state.current_position):
        progress.append(f"\033[92m{game_state.target_sequence[i]}\033[0m")

    # Add current note indicator
    if game_state.current_position < sequence_length:
        progress.append("?")

    # Add greyed out question marks for remaining notes
    for i in range(game_state.current_position + 1, sequence_length):
        progress.append("\033[90m?\033[0m")  # Grey color in terminal

    # if(game_state.current_position == sequence_length):
    #     progress.append(" 🎉 🎉 🎉")
    # Print the progress on a single line
    print(' '.join(progress))


def notify_correct_note(game_state):
    note_name = game_state.current_target_note()
    # print(f"✅ {note_name}")

def notify_sequence_success(game_state):
    # print("\n🎉 CONGRATULATIONS! 🎉")
    print_note_prompt(game_state)

    # Play success sound in a separate thread
    sound_thread = threading.Thread(target=play_success_sound)
    sound_thread.daemon = True
    sound_thread.start()


def notify_failure(game_state):
    correct_note_name = game_state.current_target_note()
    print(f"\n❌ INCORRECT. That should have been {correct_note_name}.")

    correct_seq = game_state.target_sequence[:game_state.current_position]

    play_note_list(correct_seq)

    play_note(note_val(correct_note_name), 64, 1.5)
    time.sleep(0.4)


    # Play the failure sound in a separate thread to not block the game
    # sound_thread = threading.Thread(target=play_failure_sound)
    # sound_thread.daemon = True
    # sound_thread.start()

    play_failure_sound(1)
    time.sleep(0.4)
    play_failure_sound(0)
    time.sleep(0.5)

    # print("Let's try a new sequence.")
