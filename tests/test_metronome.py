# Standard imports
import unittest

# Local imports
from metronome import BeatType, Metronome
from exceptions import InvalidRhythmSpecificationError


class Test_metronome(unittest.TestCase):
    def test_next_beat_W(self):
        met = Metronome(tempo=60, rhythm='W')
        (delay, stressed) = met.next_beat()
        exp_val = (1.0, BeatType.STRESSED)
        act_val = (delay, stressed)
        self.assertTupleEqual(exp_val, act_val)

    def test_next_beat_w(self):
        met = Metronome(tempo=60, rhythm='w')
        (delay, stressed) = met.next_beat()
        exp_val = (1.0, BeatType.NORMAL)
        act_val = (delay, stressed)
        self.assertTupleEqual(exp_val, act_val)

    def test_next_beat_H(self):
        met = Metronome(tempo=60, rhythm='H')
        (delay, stressed) = met.next_beat()
        exp_val = (0.5, BeatType.STRESSED)
        act_val = (delay, stressed)
        self.assertTupleEqual(exp_val, act_val)

    def test_next_beat_h(self):
        met = Metronome(tempo=60, rhythm='h')
        (delay, stressed) = met.next_beat()
        exp_val = (0.5, BeatType.NORMAL)
        act_val = (delay, stressed)
        self.assertTupleEqual(exp_val, act_val)

    def test_next_beat_Q(self):
        met = Metronome(tempo=60, rhythm='Q')
        (delay, stressed) = met.next_beat()
        exp_val = (0.25, BeatType.STRESSED)
        act_val = (delay, stressed)
        self.assertTupleEqual(exp_val, act_val)

    def test_next_beat_q(self):
        met = Metronome(tempo=60, rhythm='q')
        (delay, stressed) = met.next_beat()
        exp_val = (0.25, BeatType.NORMAL)
        act_val = (delay, stressed)
        self.assertTupleEqual(exp_val, act_val)

    def test_next_beat_r(self):
        met = Metronome(tempo=60, rhythm='r')
        (delay, stressed) = met.next_beat()
        exp_val = (1.0, BeatType.REST)
        act_val = (delay, stressed)
        self.assertTupleEqual(exp_val, act_val)

    def test_next_beat_twice(self):
        met = Metronome(tempo=60, rhythm='Ww')
        met.next_beat()
        (delay, stressed) = met.next_beat()
        exp_val = (1.0, BeatType.NORMAL)
        act_val = (delay, stressed)
        self.assertTupleEqual(exp_val, act_val)

    def test_next_beat_loop(self):
        met = Metronome(tempo=60, rhythm='Ww')
        met.next_beat()
        met.next_beat()
        (delay, stressed) = met.next_beat()
        exp_val = (1.0, BeatType.STRESSED)
        act_val = (delay, stressed)
        self.assertTupleEqual(exp_val, act_val)

    def test_validate_rhythm_good(self):
        met = Metronome()
        exp_val = None
        act_val = met._validate_rhythm('Ww')
        self.assertEqual(exp_val, act_val)
        
    def test_validate_rhythm_empty(self):
        self.assertRaises(InvalidRhythmSpecificationError, Metronome, rhythm='')

    def test_validate_rhythm_bad(self):
        self.assertRaises(InvalidRhythmSpecificationError, Metronome, rhythm='Wx')

if __name__ == '__main__':
    unittest.main()
