# Standard
import unittest
import tkinter as tk

# Local
from MetronomeApp import MetronomeApp


class Test_test_MetronomeApp(unittest.TestCase):
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
        exp_val = (0.5, True)
        myapp.set_bpm(120)
        act_val = myapp.get_next_beat()
        self.assertTupleEqual(exp_val, act_val)


if __name__ == '__main__':
    unittest.main()
