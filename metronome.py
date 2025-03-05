"""
This module provides the metronome class, which represents the "business logic" of a metronome.
"""

# standard imports
from dataclasses import dataclass
from enum import Enum

# local imports


class BeatType(Enum):
    """
    An enumeration that represents the type of the metronome beat.
    """
    REST = 1
    NORMAL = 2
    STRESSED = 3


@dataclass
class Metronome:
    """
    This class represents the "business logic" of a metronome.
        tempo: The tempo of the metronome, in bpm (beats per minute), int
        rhythm: A string representing the rhythm of the metronome beats, string
        _current_beat: Current location in the rhythm string, int
    """
    tempo: int = 60
    rhythm: str = 'Wwww' 

    """
    This member function is called automatically by the auto-generated __init__(). Here we use it
    to create/initialize a hidden member variable.
    """
    def __post_init__(self):
        self._current_beat = 0

    def next_beat(self):
        """
        Returns information about the next metronome beat, and advances _current beat.
        :return: (beat delay in seconds, stressed? (NORMAL/STRESSED)), as (float, BeatType Enum)
        Note: The beat delay is really the delay until the next beat, or the duration of the current beat.
              stressed is whether or not the current beat is a stressed beat.
        """
        beat_delay = 0
        beat_factor = 1
        stressed = BeatType.NORMAL
        beat_code = self.rhythm[self._current_beat]
        match beat_code:
            case 'W':
                stressed = BeatType.STRESSED
                beat_factor = 1 
            case 'w':
                stressed = BeatType.NORMAL
                beat_factor = 1.0
            case 'r':
                stressed = BeatType.REST
                beat_factor = 2.0 
            case 'H':
                stressed = BeatType.STRESSED
                beat_factor = 0.5 
            case 'h':
                stressed = BeatType.NORMAL
                beat_factor = 0.5
            case 'Q':
                stressed = BeatType.STRESSED
                beat_factor = 0.25 
            case 'q':
                stressed = BeatType.NORMAL
                beat_factor = 0.25
        beat_delay = beat_factor / (self.tempo / 60.)

        # Advance current beat
        self._current_beat += 1
        
        # Loop current beat back to beginning of rhythm string when necessary
        if self._current_beat >= len(self.rhythm):
            self._current_beat = 0

        return (beat_delay, stressed)




