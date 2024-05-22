# standard imports
import tkinter as tk
from tkinter import ttk

# local imports
from tkMetronomeViewManager import tkMetronomeViewManager


class MetronomeApp(ttk.Frame):
    """
    Class represent a Metronome application built using tkinter.
    """
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.grid(column=0, row=0, sticky='NWES') # Grid-0
        # Weights control the relative "stretch" of each column and row as the frame is resized
        parent.columnconfigure(0, weight=1) # Grid-0
        parent.rowconfigure(0, weight=1) # Grid-0
        parent.option_add('*tearOff', False) # Prevent menus from tearing off

        # Create and setup a menubar for the app
        self.setup_menubar()
        
        # Create and setup the child widgets of the app
        self.setup_child_widgets()

        # If the user X's the main window, make sure we clean up 
        parent.protocol("WM_DELETE_WINDOW", self.onExit)

    def setup_menubar(self):
        """
        Utility function to be called by __init__ to set up the menu bar of the app.
        """
        self._menubar = tk.Menu(self.master)
        self.master['menu'] = self._menubar
        self._menu_file = tk.Menu(self._menubar)
        self._menubar.add_cascade(menu=self._menu_file, label='File')
        self._menu_file.add_command(label='Exit', command=self.onExit)
        return None
        
    def setup_child_widgets(self):
        """
        Utility function to be called by __init__ to set up the child widgets of the app.
        """
        self._view_manager = tkMetronomeViewManager(self)
        self._view_manager.grid(column=0, row=0, sticky='NWES') # Grid-1
        self.columnconfigure(0, weight=1) # Grid-1
        self.rowconfigure(0, weight=1) # Grid-1
        
        return None
        
    def onExit(self):
        """
        Method called when menu item File | Exit is selected.
        """
        self._view_manager.detach_from_subjects()
        self.master.destroy()
        return None
        
        
