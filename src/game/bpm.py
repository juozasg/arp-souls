class BPM:
    def __init__(self):
        self.bpm: float | None = None
        self.beat_dts: list[float] = []
        self.error: float | None = None

    def update_beat(self, dt: float):
        self.beat_dts.append(dt)

        if dt > 1.0:
            self.beat_dts.clear()

        if len(self.beat_dts) > 5:
            self.beat_dts.pop(0)
        if len(self.beat_dts) < 2:
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
