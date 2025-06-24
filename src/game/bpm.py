import arcade
from typing import Literal

class BPM:
    def __init__(self):
        self.bpm: float | None = None
        self.beat_dts: list[float] = []
        self.error: float | None = None
        self.beat_dt: float | None = None

    def tick(self, delta_time):
        if self.beat_dt is not None:
            self.beat_dt += delta_time

        # too slow, lost the beat
        if self.beat_dt is not None and self.beat_dt > 1.0:
            self.beat_dt = None
            self.bpm = None
            self.error = None
            self.beat_dts.clear()

    def key_on(self, key: int) -> Literal['first_beat', 'new_beat', 'chord_beat']:
        """ @return True if a beat was detected, False otherwise (not the first note of a chord)"""
        # key = key % 12

        if self.beat_dt is None:
            self.beat_dt = 0.0
            return 'first_beat'
        elif self.beat_dt > 0.12:  # about 400 BPM max to count chords as one hit
            self.update_beat()
            self.beat_dt = 0.0  # Reset for next beat
            return 'new_beat'

        return 'chord_beat'

    def update_beat(self):
        dt = self.beat_dt
        self.beat_dts.append(dt)

        # a pulse each 1.5 second is too slow aka no beat
        if dt > 1.5:
            self.beat_dts.clear()

        if len(self.beat_dts) > 5:
            self.beat_dts.pop(0)
        if (len(self.beat_dts) < 2 and self.bpm is not None) or len(self.beat_dts) < 1:
            self.bpm = None
            self.error = None
            return

        # Calculate the average time between beats
        avg_dt = sum(self.beat_dts) / len(self.beat_dts)
        if avg_dt > 0:
            self.bpm = 60.0 / avg_dt
        else:
            self.bpm = None

        # Calculate the standard deviation of the last beat intervals
        if len(self.beat_dts) > 1:
            mean = sum(self.beat_dts) / len(self.beat_dts)
            variance = sum((x - mean) ** 2 for x in self.beat_dts) / (len(self.beat_dts) - 1)
            self.error = variance ** 0.5

    def draw_debug(self):
        beat_dts_str = ", ".join(f"{dt:.3f}" for dt in self.beat_dts)

        arcade.draw_text(f"Beats: {beat_dts_str}", 5, 5, arcade.color.DARK_BLUE_GRAY, font_size=12, anchor_x="left",
                         anchor_y="bottom")
