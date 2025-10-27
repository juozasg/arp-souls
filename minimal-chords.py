import random
import sys
from time import sleep


chords = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
flat_chords = ['Db', 'Eb', 'Gb', 'Ab', 'Bb']
sharp_chords = ['C#', 'D#', 'F#', 'G#', 'A#']


sleep_time = 1
# get sleep time from first arg if available
if len(sys.argv) > 1:
    sleep_time = float(sys.argv[1])

while True:
    flat_or_sharp = random.choice([flat_chords, sharp_chords])
    all_chords = chords + flat_or_sharp
    # choose 4 chords randomly
    random_chords = random.sample(all_chords, 4)
    print(' '.join(random_chords))

    # sleep until any key is pressed
    input("")
    # sleep(sleep_time)