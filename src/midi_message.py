from dataclasses import dataclass
from typing import Literal

@dataclass
class MidiMessage:
    type: Literal['note_on', 'note_off']
    note: int
    velocity: int