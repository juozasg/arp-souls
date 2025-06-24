import arcade
import tinysoundfont

SYNTH = tinysoundfont.Synth()

def load_soundfound():
    sf2_path = arcade.resources.resolve(':assets:piano.sf2')
    print("Loading soundfont:")
    sfid = SYNTH.sfload(str(sf2_path))
    SYNTH.program_select(0, sfid, 0, 0)
    SYNTH.start(128)
    print("Loaded", sf2_path)
    # SYNTH.sfload('avc')

class PianoSampler:
    def __init__(self):
        self.sound = arcade.load_sound(":resources:sounds/hurt1.wav")

    def play_sound(self):
        arcade.play_sound(self.sound)

    @staticmethod
    def note_on(note: int, velocity: int = 100):
        # print("note on", note)
        SYNTH.noteon(0, note, 100)

    @staticmethod
    def note_off(note: int):
        # print("note off", note)
        SYNTH.noteoff(0, note)