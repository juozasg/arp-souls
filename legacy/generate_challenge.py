import random
import math
from enum import Enum

from game.music import note_val


def make_note_options(difficulty_tier: int) -> list[str]:
    notes_difficulty_tiers: list[list[str]] = [
        ['A3', 'B3', 'E4'], # 1, M2, P5
        ['Bb3'], # m2
        ['C4'], # m3
        ['Db4'], # M3
        ['D4'], # P4
        ['Eb4'], # TT
        ['F4'], # m6
        ['Gb4'], # M6
        ['G4'], # m7
        ['Ab4'], # M7
    ]

    # merge all previous tiers
    note_options = []
    for i in range(difficulty_tier + 1):
        note_options += notes_difficulty_tiers[i]

    # sort notes by note_val
    note_options.sort(key=lambda x: note_val(x))
    return note_options


class MelodyShape(Enum):
    UP = 0 # start at note_options[0]. each note is higher than the previous or the same
    DOWN = 1 # start at last note in note_options. each note is lower than the previous or the same
    UPDOWN = 2 # start at note_options[0]. each note is higher than the previous or the same until halfway, then each note is lower than the previous or the same
    RANDOM = 3 # random order of notes

def generate_challenge(sequence_length: int, note_options: list[str], shape: MelodyShape = MelodyShape.UP, leapiness: float = 0.2) -> list[str]:
    # print(f'Generating challenge with shape {shape} and leapiness {leapiness}. Notes = {note_options}. LEN = {sequence_length}')
    target_sequence: list[str] = []

    if shape == MelodyShape.UP:
        # leapiness = leapiness * 0.5
        idx = 0
        force_step = False
        for _ in range(sequence_length):
            leap = random.random() < leapiness
            leapiness = leapiness * 0.75 if leap == True else leapiness * 1.15

            if leap:
                idx = random.randint(idx, len(note_options) - 1)
                target_sequence.append(note_options[idx])
            else:
                # step or stay
                step = random.randint(0, 1)
                if step == 0:
                    if force_step == True:
                        idx = idx + 1
                        force_step = False
                    else:
                        force_step = True
                idx = idx + step
                if idx > len(note_options) - 1:
                    idx = len(note_options) - 1

                target_sequence.append(note_options[idx])

    elif shape == MelodyShape.DOWN:
        reversed_note_options = note_options[::-1]
        target_sequence = generate_challenge(sequence_length, reversed_note_options, MelodyShape.UP, leapiness)

    elif shape == MelodyShape.UPDOWN:
        half_length = sequence_length // 2
        up = generate_challenge(half_length, note_options, MelodyShape.UP, leapiness * half_length)
        # Get the last note from the up sequence and its index in note_options
        last_up_note = up[-1]
        max_idx = min(note_options.index(last_up_note) + 1, len(note_options) - 1)

        # slice note options to remove notes that are not in the up sequence
        down_note_options = list(reversed(note_options[:max_idx]))
        # remove note otions that are not in the up sequence and one more note
        down = generate_challenge(half_length, down_note_options, MelodyShape.UP, leapiness)
        target_sequence = up + [note_options[max_idx]] + down

    elif shape == MelodyShape.RANDOM:
        leapiness = leapiness * 1.5

        # Start with a random note
        target_sequence = [random.choice(note_options)]
        for _ in range(sequence_length - 1):
            current_index = note_options.index(target_sequence[-1])
            if random.random() < leapiness:  # Make a leap. 300% more likely to leap in random shape
                # For leaps, choose a note that's at least 2 steps away in either direction
                possible_indices = [i for i in range(len(note_options)) if abs(i - current_index) >= 2]
                if not possible_indices:  # If no leap is possible
                    next_index = random.randint(0, len(note_options) - 1)
                else:
                    next_index = random.choice(possible_indices)
            else:  # No leap, choose an adjacent note or stay the same
                # For non-leaps, choose a note that's at most 1 step away in either direction
                lower_bound = max(0, current_index - 1)
                upper_bound = min(len(note_options) - 1, current_index + 1)
                next_index = random.randint(lower_bound, upper_bound)
            target_sequence.append(note_options[next_index])

    return target_sequence



