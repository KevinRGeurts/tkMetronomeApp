# standard imports
import tkinter as tk
from tkinter import ttk
from multiprocessing import Process
import logging

# local imports
from tkApp import AppAboutInfo, tkApp
from tkMetronomeViewManager import tkMetronomeViewManager
from metronome import Metronome


class MetronomeApp(tkApp):
    """
    Class represent a Metronome application built using tkinter, leveraging tkApp framework.
    """
    def __init__(self, parent, log_level = logging.INFO) -> None:
        """
        :param log_level: The logging level to set for the logger, e.g., logging.DEBUG, logging.INFO, etc.
        """
        # TODO: Remove the File | Test menu item before production release.
        menu_dictionary = {'File':{'Open...':self.onFileOpen, 'Save':self.onFileSave, 'Save As...':self.onFileSaveAs, 'Exit':self.onFileExit, 'Test':self.onFileTest}, \
                           'Help':{'View Help...':self.onViewHelp,'About...':self.onHelpAbout}}
        info = AppAboutInfo(name='Metronome', version='0.1', copyright='2025', author='Kevin R. Geurts',
                            license='MIT License', source='https://github.com/KevinRGeurts/tkAppFramework',
                            help_file='.\\Help\\HelpFile.txt')
        super().__init__(parent, title="Metronome", menu_dict=menu_dictionary, app_info=info,
                         file_types=[('JSON file', '*.json')], log_level=log_level)

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

    def _setup_logging(self, log_level=logging.INFO):
        """
        This method extends tkApp._setup_logging to configure logging specifically for the metronome app.
        :param log_level: The logging level to set for the logger, e.g., logging.DEBUG, logging.INFO, etc.
        :return: None
        """
        super()._setup_logging(log_level)
        
        # Create a logger with name 'metronome_app_logger'. This is NOT the root logger, which is one level up from here, and has no name.
        logger = logging.getLogger('metronome_app_logger')
        # This is the threshold level for the logger itself, before it will pass to any handlers, which can have their own threshold.
        # Should be able to control here what the stream handler receives and thus what ends up going to stderr.
        # Use this key for now:
        #   DEBUG = debug messages sent to this logger will end up on stderr
        #   INFO = info messages sent to this logger will end up on stderr
        logger.setLevel(log_level)
        # Set up this highest level below root logger with a stream handler
        sh = logging.StreamHandler()
        # Set the threshold for the stream handler itself, which will come into play only after the logger threshold is met.
        sh.setLevel(log_level)
        # Add the stream handler to the logger
        logger.addHandler(sh)
            
        return None


if __name__ == '__main__':
    # Get Tcl interpreter up and running and get the root widget
    root = tk.Tk()
    # Create the metronome app
    app = MetronomeApp(root)
    # Start the metronome app's event loop running
    app.mainloop()


        
