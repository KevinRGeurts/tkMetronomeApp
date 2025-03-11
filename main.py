# Standard
import tkinter as tk

# Local
from MetronomeApp import MetronomeApp


if __name__ == '__main__':
    
    """
    Create and launch tkinter-based Metronome App.
    """
    
    # Create and configure the app
    root = tk.Tk()
    myapp = MetronomeApp(root)

    # Start the app's event loop running
    myapp.mainloop()

     