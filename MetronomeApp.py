# standard imports
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from multiprocessing import Process

# local imports
from tkApp import tkApp
from tkMetronomeViewManager import tkMetronomeViewManager
from metronome import Metronome
from exceptions import InvalidRhythmSpecificationError
from tkHelpApp import tkHelpApp


# TODO: This function probably should be served by the HelpApp or tkApp project, but place it here for now for
# testing the concept. Note that it cannot be a member of MetronomeApp, do to Process using pickle.
def _launch_help_app():
    """
    Launch tkinter app for displaying online help.
    """
    # Create and configure the app
    root = tk.Tk()
    myapp = tkHelpApp(root)

    # Start the app's event loop running
    myapp.mainloop()
    return None


class MetronomeApp(tkApp):
    """
    Class represent a Metronome application built using tkinter, leveraging tkApp framework.
    """
    def __init__(self, parent) -> None:
        
        # Create/initialize the metronome business logic object
        # Do this before calling super().__init__(...), because self._setup_child_widgets() requires it.
        self._metronome = Metronome()
        self._metronome.rhythm = 'WhhWhh'
        
        menu_dictionary = {'File':{'Exit':self.onFileExit},'Help':{'View Help':self.onViewHelp,'About...':self.onHelpAbout}}
        super().__init__(parent, title="Metronome", menu_dict=menu_dictionary)

        # Process running the HelpApp
        self._help_process = None
        
    def _setup_child_widgets(self):
        """
        Utility function to be called by __init__ to set up the child widgets of the app.
        """
        # TODO: Is there a way, perhaps by using a factory pattern, that the view manager can be specified when
        # the application is constructed? Challenge is that the parent of the view manager is the application,
        # so the application must exist before the view manager can be constructed.
        # Wonder if the solution is for tkApp to have a factory method that produces a tkViewManager child of the
        # right type?
        self._view_manager = tkMetronomeViewManager(self)
        self._view_manager.grid(column=0, row=0, sticky='NWES') # Grid-1
        self.columnconfigure(0, weight=1) # Grid-1
        self.rowconfigure(0, weight=1) # Grid-1
        return None

    def onFileExit(self):
        """
        Extend method from tkApp.
        """
        if self._help_process:
            print(f"Help Process {self._help_process.name} is alive={self._help_process.is_alive()}")
        super().onFileExit()
        return None
        
    def get_bpm(self):
        """
        Returns the number of beats per minute setting of the metronome.
        :return: The number of beats per minute setting of the metronome, int
        """
        return self._metronome.tempo

    def set_bpm(self, bpm):
        """
        Set the number of beats per minute setting of the metronome.
        :parameter bpm: The number of beats per minute, int
        """
        assert (bpm>0)
        self._metronome.tempo=bpm
    
    def get_rhythm(self):
        """
        Returns the string representation of the metronome's rhythm.
        :return: The string representation of the metronome's rhythm, string
        """
        return self._metronome.rhythm

    def set_rhythm(self, rhythm_str):
        """
        Set the rhythm of the metronome.
        :parameter rhythm_str: String representing the metronome rhythm, string
        """
        assert(type(rhythm_str) is str)
        self._metronome.rhythm=rhythm_str

    def get_next_beat(self):
        """
        Return the delay until the next beat of the metronome (or that length of the current beat),
        and whether or not the current beat is stressed.
        :return: (beat delay in seconds, stressed), as tuple
        """
        return self._metronome.next_beat()

    def onHelpAbout(self):
        """
        Method called when menu item Help | About is selected.
        """
        msg = 'Metronome\n'
        msg += 'version 0.1\n'
        msg += 'Copyright (c) 2025 by Kevin Geurts\n'
        msg += 'Licensed under the {some open source license}\n'
        msg += '{github link}\n'
        showinfo(title='About Metronome', message=msg, parent=self.master)
        return None
    
    # TODO: Consider refactoring and moving this functionality to tkApp project.
    def onViewHelp(self):
        """
        Method called when menu item Help | View Help is selected. Launch help app to view help.
        :return: None
        """
        self._help_process = Process(target=_launch_help_app, name='HelpApp Process')
        self._help_process.start()
        
        return None
        
