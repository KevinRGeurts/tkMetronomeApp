# Standard
import tkinter as tk
import winsound
from time import sleep

# Local
from MetronomeApp import MetronomeApp


if __name__ == '__main__':
    
    """
    Launch tkinter-based Metronome App.
    """
    
    # for i in range(1,20):
    #     # Beep
    #     frequency = 2500  # Set Frequency To 2500 Hertz
    #     duration = 50  # Set Duration To 100 ms == 0.1 second (must be < 125, since maximum bpm is 480)
    #     winsound.Beep(frequency, duration)

    #     # sleep for the appropriate delay time
    #     bpm = 480
    #     sleep(60 / bpm)

    # Create and configure the app
    root = tk.Tk()
    myapp = MetronomeApp(root)
    myapp.master.title("Metronome Application")

    # Start the app's event loop running
    myapp.mainloop()

