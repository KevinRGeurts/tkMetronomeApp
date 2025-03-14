# Standard
import unittest
import tkinter as tk

# Local
from MetronomeApp import MetronomeApp
from metronome import BeatType


class Test_MetronomeApp(unittest.TestCase):
    def test_set_bpm_get_bpm(self):
        root = tk.Tk()
        myapp = MetronomeApp(root)
        myapp.set_bpm(120)
        exp_val = 120
        act_val = myapp.get_bpm()
        self.assertEqual(exp_val, act_val)

    def test_get_next_beat(self):
        root = tk.Tk()
        myapp = MetronomeApp(root)
        exp_val = (0.5, BeatType.STRESSED)
        myapp.set_bpm(120)
        act_val = myapp.get_next_beat()
        self.assertTupleEqual(exp_val, act_val)

    def test_set_rhythm_get_rhythm(self):
        root = tk.Tk()
        myapp = MetronomeApp(root)
        myapp.set_rhythm('WrWw')
        exp_val = 'WrWw'
        act_val = myapp.get_rhythm()
        self.assertEqual(exp_val, act_val)

if __name__ == '__main__':
    unittest.main()
