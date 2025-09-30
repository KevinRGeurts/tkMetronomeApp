# standard imports
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from multiprocessing import Process

# local imports
from tkApp import AppAboutInfo, tkApp
from tkMetronomeViewManager import tkMetronomeViewManager
from metronome import Metronome
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
        
        # TODO: Remove the File | Test menu item before production release.
        menu_dictionary = {'File':{'Open...':self.onFileOpen, 'Save':self.onFileSave, 'Save As...':self.onFileSaveAs, 'Exit':self.onFileExit, 'Test':self.onFileTest}, \
                           'Help':{'View Help':self.onViewHelp,'About...':self.onHelpAbout}}
        info = AppAboutInfo(name='Metronome', version='0.1', copyright='2025', author='Kevin R. Geurts',
                            license='MIT License', source='https://github.com/KevinRGeurts/tkAppFramework')
        super().__init__(parent, title="Metronome", menu_dict=menu_dictionary, app_info=info,
                         file_types=[('JSON file', '*.json')])

        # Process running the HelpApp
        self._help_process = None

    def _createViewManager(self):
        """
        Factory method to create the view manager for the app.
        :return: The view manager for the app, tkMetronomeViewManager
        """
        return tkMetronomeViewManager(self)

    def _createModel(self):
        """
        Factory method to create the model for the app.
        :return: The model for the app, Metronome
        """
        # return Metronome(rhythm='WhhWhh')
        return Metronome()

    def onFileExit(self):
        """
        Extend method from tkApp.
        """
        if self._help_process:
            print(f"Help Process {self._help_process.name} is alive={self._help_process.is_alive()}")
        super().onFileExit()
        return None

    # TODO: Remove this temporary test method before production release.
    def onFileTest(self):
        """
        Method called when menu item File | Test is selected. This is temporary for testing purposes.
        """
        # Test notification process when model changes.
        self.getModel().tempo = 120
        self.getModel().rhythm = 'wH'
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


if __name__ == '__main__':
    # Get Tcl interpreter up and running and get the root widget
    root = tk.Tk()
    # Create the metronome app
    app = MetronomeApp(root)
    # Start the metronome app's event loop running
    app.mainloop()


        
