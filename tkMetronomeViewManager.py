# Standard imports
import tkinter as tk
from tkinter import ttk
import winsound
from time import sleep

# Local imports

class tkMetronomeViewManager(ttk.Frame):
    """
    Class follows mediator design pattern. It handles the interactions between widgets in a tkinter based application.
    """
    def __init__(self, parent) -> None:
        """
        :parameter parent: The parent widget of this widget, The tkinter App
        """
        super().__init__(parent)

        self.CreateWidgets()

    def reset_widgets(self):
        """
        Utility function called to put child widgets in appropriate state after ... or before ....
        """
        # self._crib_widget.reset_widgets_for_new_deal()
        
        return None

    def handle_X_event(self, info):
        """
        Called to handle  event.
        """
        # assert(info.event_type == CribbageGameOutputEvents.START_GAME)
        # self._board_widget._player1_track['text']=f"{info.name_player1}"
        # self._board_widget._player2_track['text']=f"{info.name_player1}"
        
        # self.reset_widgets_for_new_deal()

        # self._board_widget.set_pegs_player1()
        # self._board_widget.set_pegs_player2()
        
        return None

    def CreateWidgets(self):
        """
        Utility function to be called by __init__ to set up the child widgets of the tkMetronomeViewManager widget.
        :return None:
        """

        self._bpm_widget = MetronomeBpmWidget(self)
        self._bpm_widget.grid(column=0, row=0, rowspan=2, sticky='NWES') # Grid-2
        self.columnconfigure(0, weight=1) # Grid-2
        self.rowconfigure(0, weight=1) # Grid-2

        self._beacon_widget = MetronomeBeaconWidget(self)
        self._beacon_widget.grid(column=2, row=0, sticky='NWES') # Grid-2
        self.columnconfigure(2, weight=1) # Grid-2
        self.rowconfigure(0, weight=1) # Grid-2

        self._start_stop_widget = MetronomeStartStopWidget(self)
        self._start_stop_widget.grid(column=2, row=1, sticky='NWES') # Grid-2
        self.columnconfigure(1, weight=1) # Grid-2
        self.rowconfigure(0, weight=1) # Grid-2
        
        return None


class MetronomeBpmWidget(ttk.Labelframe):
    """
    Class represents a tkinter label frame, the wdiget contents of which allow the beats per minute of the metronome to be set.
    """
    def __init__(self, parent) -> None:
        """
        :parameter parent: tkinter widget that is the parent of this widget
        """
        super().__init__(parent, text=f"Beats Per Minute")

        self._scale_bpm = tk.Scale(self, orient=tk.VERTICAL, length='2i', from_=60, to=480, command=self.OnBpmChanged,
                                    tickinterval=60)
        self._scale_bpm.grid(column=0, row=0) # Grid-2
        self.columnconfigure(0, weight=1) # Grid-2
        self.rowconfigure(0, weight=1) # Grid-2
        self._value_bpm=tk.IntVar()
        self._value_bpm.set(120)
        self._scale_bpm['variable']=self._value_bpm

    def OnBpmChanged(self, value):
        # Inform the mediator object of the change in beats per minute of the metronome
        pass


class MetronomeStartStopWidget(ttk.Labelframe):
    """
    Class represents a tkinter label frame, the wdiget contents of which will allow the metronome to be started and stopped.
    """
    def __init__(self, parent) -> None:
        super().__init__(parent, text='Start/Stop')
        
        self._btn_start_stop = ttk.Button(self, command=self.OnStartStopButtonClicked)
        self._btn_start_stop.grid(column=0, row=0) # Grid-2
        self.columnconfigure(0, weight=1) # Grid-2
        self.rowconfigure(0, weight=1) # Grid-2
        self._lbl_start_stop=tk.StringVar()
        self._lbl_start_stop.set('Start')
        self._btn_start_stop['textvariable']=self._lbl_start_stop
        self._beat_after_id = 0
    
    def OnStartStopButtonClicked(self):
        # Inform the mediator object that the start/stop button has been clicked
        # TODO: Move this out of the widget, and to the view manager, but okay for now for POC

        # TODO: Using the button text to determine "state" feels kind of klugey. Do something more elegant, like maybe a class attribute.

        if self._beat_after_id:
            # Metronome is currently beating, so stop it.

            # Cancel the beat after callback
            self.master.after_cancel(self._beat_after_id)

            # Resest the after id
            self._beat_after_id = 0

            # Change button text to 'Stop'
            self._lbl_start_stop.set('Start')

            # Restore beacon to black
            self.master._beacon_widget._btn_beacon['background']='black'
            self.master.update_idletasks()

        else:
            # Metronome is NOT currently beating, so start it

            # Change button text to 'Stop'
            self._lbl_start_stop.set('Stop')

            # Calculate the delay between clicks from the bpm value
            bpm=self.master._bpm_widget._value_bpm.get()
            # Convert to beats per second
            bps = bpm / 60.
            # Compute delay between clicks in milliseconds
            click_delay = 1000. / bps

            # Start the event loop calling beat(...)
            self.beat(int(click_delay))
        
        return None

    def beat(self, beat_delay):
        """
        This is the function that is called to actually "tick" the metronome. Note that the timing of the beat is managed by the
        tkinter event loop, so is not seen within this method, but rather is controlling how often this method gets called.
        :parameter beat_delay: The time in milliseconds between beats, int
        :return None:
        """
        # Restore beacon to black, in case it was set to green by a previous beat
        # self.master._beacon_widget._btn_beacon['background']='black'
        # self.master.update_idletasks()
            
        # Beep
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 50  # Set Duration To 100 ms == 0.1 second (must be < 125, since maximum bpm is 480)
        winsound.Beep(frequency, duration)

        # "Flash" beacon by turning it green
        # self.master._beacon_widget._btn_beacon['background']='green'
        # self.master.update_idletasks()

        self._beat_after_id = self.master.after(int(beat_delay), self.beat, int(beat_delay))

        # sleep for the appropriate delay time
        # sleep(click_delay)

        return None


class MetronomeBeaconWidget(ttk.Labelframe):
    """
    Class represents a tkinter label frame, the wdiget contents of which will be a visual indicator of the metronome's timing tick.
    """
    def __init__(self, parent) -> None:
        super().__init__(parent, text='Beacon')
        
        self._btn_beacon=tk.Button(self)
        self._btn_beacon.grid(column=0, row=0) # Grid-2
        self.columnconfigure(0, weight=1) # Grid-2
        self.rowconfigure(0, weight=1) # Grid-2
        self._lbl_beacon=tk.StringVar()
        self._lbl_beacon.set('--')
        self._btn_beacon['textvariable']=self._lbl_beacon
        self._btn_beacon['height']=8
        self._btn_beacon['width']=10
        self._btn_beacon['background']='black'
        self._btn_beacon['state']=tk.DISABLED