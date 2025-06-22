from game.generate_challenge import MelodyShape, generate_challenge, make_note_options

import random

from game.play_sounds import play_note_list
# from enum import Enum

class GameState:
    def __init__(self):
        self.current_position = 0
        self.target_sequence = []
        # self.note_options = ['C4', 'D4']

        self.length_difficulty = 1
        self.note_difficulty: int = 0 # 0 to 9
        self.shape_difficulty: int = 0 # 0 to 3
        self.leapiness_difficulty: float = 0.1 # 0 to 1

        self.consecutive_successes = 0
        self.consecutive_failures = 0

        self.total_successes = 0
        self.total_failures = 0


    def update_difficulty(self):

        if(random.random() < 0.30 and self.consecutive_successes >  2 and self.length_difficulty < 9):
            self.length_difficulty += 1
            print("[+++] LENGTH:", (self.length_difficulty + 2) * '🎹 ')

        if(random.random() < 0.60 and self.consecutive_failures > 1 and self.length_difficulty > 1):
            self.length_difficulty -= 1
            print("[---] LENGTH:", (self.length_difficulty + 2) * '🎹 ')

        # if more wins than loses, roll 25% to increase note_difficulty. with more consecutive wins, increase chance
        correct_percentage = self.total_successes / (self.total_successes + self.total_failures)
        if(correct_percentage > 0.85):
            if(random.random() < 0.10 + (self.consecutive_successes * 0.05)):
                self.note_difficulty = min(9, self.note_difficulty + 1)
                print("[+++] NOTES:", ' '.join(make_note_options(self.note_difficulty)))

        # if too many loses, roll 50% to decrease note_difficulty
        else:
            if(random.random() < 0.50 and self.note_difficulty > 0):
                self.note_difficulty = self.note_difficulty - 1
                print("[---] NOTES:", ' '.join(make_note_options(self.note_difficulty)))

        # print(f'note_difficulty: {self.note_difficulty}')

       # every 3 successes or any failures roll 50% to increase or decrease shape_difficulty
        if(self.consecutive_successes > 0 and self.consecutive_successes % 2 == 0 and random.random() > 0.5 and self.shape_difficulty < 3):
            self.shape_difficulty = self.shape_difficulty + 1
            print("[+++] MELODIC SHAPE")
            self.print_melodic_shape(MelodyShape(self.shape_difficulty))

        elif(self.consecutive_failures > 0 and random.random() > 0.75 and self.shape_difficulty > 0):
            self.shape_difficulty = self.shape_difficulty - 1
            print("[---] MELODIC SHAPE")
            self.print_melodic_shape(MelodyShape(self.shape_difficulty))

        print(f"\nTotal: {self.total_successes}/{self.total_failures} ({correct_percentage} correct)    Consecutive: {self.consecutive_successes}/{self.consecutive_failures}")

    def print_melodic_shape(self, shape: MelodyShape):
        if shape == MelodyShape.UP:
            print(f"MELODIC SHAPE  📈  (leapiness: {self.leapiness_difficulty})")
        elif shape == MelodyShape.DOWN:
            print(f"MELODIC SHAPE  📉  (leapiness: {self.leapiness_difficulty})")
        elif shape == MelodyShape.UPDOWN:
            print(f"MELODIC SHAPE  📈📉 (leapiness: {self.leapiness_difficulty})")
        elif shape == MelodyShape.RANDOM:
            print(f"MELODIC SHAPE  🎲🎲🎲 (leapiness: {self.leapiness_difficulty})")


    def play_challenge(self):
        note_options = make_note_options(self.note_difficulty)
        shape = MelodyShape(self.shape_difficulty)
        self.print_melodic_shape(shape)

        print(f'{len(self.target_sequence)} notes from: {' '.join(note_options)}')
        play_note_list(self.target_sequence)


    def new_challenge(self):
        sequence_length = self.length_difficulty + 1

        note_options = make_note_options(self.note_difficulty)

        # Convert numeric shape_difficulty to MelodyShape enum
        shape = MelodyShape(self.shape_difficulty)
        leapiness = ((self.length_difficulty + self.note_difficulty)/10.0) * self.leapiness_difficulty

        self.target_sequence = [note_options[0]] + generate_challenge(sequence_length, note_options, shape, leapiness)
        self.current_position = 0

        print("\n=== NEW CHALLENGE ===")
        self.play_challenge()

    def replay_challenge(self):
        self.current_position = 0

        # Replay the sequence to remind the player
        print("\n=== REPLAYING CHALLENGE ===")
        self.play_challenge()

    def current_target_note(self):
        return self.target_sequence[self.current_position]

    def success(self):
        self.consecutive_successes += 1
        self.consecutive_failures = 0
        self.leapiness_difficulty = min(1, self.leapiness_difficulty + 0.15)

        self.total_successes += 1
        self.update_difficulty()


    def failure(self):
        self.consecutive_failures += 1
        self.consecutive_successes = 0
        self.leapiness_difficulty = max(0, self.leapiness_difficulty - 0.15)

        self.total_failures += 1
        self.update_difficulty()