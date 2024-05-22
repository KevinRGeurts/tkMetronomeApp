# Standard imports
import tkinter as tk
from tkinter import ttk
import winsound
from time import sleep

# Local imports

class Observer:
    """
    Base class for all objects that will be an Object in an Observer design pattern.
    """
    def __init__(self):
        pass

    def update(self, subject):
        """
        Interface method called by Subject to notify observer of a change in state. Must be implemented by children. Will raise NotImplementedError
        if called.
        :parameter subject: Which Subject instance is notifying the Obsderver instance?
        """
        raise NotImplementedError
        return None


class tkMetronomeViewManager(ttk.Frame, Observer):
    """
    Class follows mediator design pattern. It handles the interactions between widgets in a tkinter based application. Also acts as an Observer.
    """
    def __init__(self, parent) -> None:
        """
        :parameter parent: The parent widget of this widget, The tkinter App
        """
        ttk.Frame.__init__(self, parent)
        Observer.__init__(self)

        self._beat_after_id = 0
        self._bpm = 120

        self.CreateWidgets()

    def detach_from_subjects(self):
        """
        Detach from all widgets.
        :return None:
        """
        self._bpm_widget.detach(self)
        self._beacon_widget.detach(self)
        self._start_stop_widget.detach(self)
        return None

    def reset_widgets(self):
        """
        Utility function called to put child widgets in appropriate state after ... or before ....
        """
        # self._crib_widget.reset_widgets_for_new_deal()
        
        return None

    def CreateWidgets(self):
        """
        Utility function to be called by __init__ to set up the child widgets of the tkMetronomeViewManager widget.
        :return None:
        """

        self._bpm_widget = MetronomeBpmWidget(self, self._bpm)
        self._bpm_widget.attach(self)
        self._bpm_widget.grid(column=0, row=0, rowspan=2, sticky='NWES') # Grid-2
        self.columnconfigure(0, weight=1) # Grid-2
        self.rowconfigure(0, weight=1) # Grid-2

        self._beacon_widget = MetronomeBeaconWidget(self)
        self._beacon_widget.attach(self)
        self._beacon_widget.grid(column=2, row=0, sticky='NWES') # Grid-2
        self.columnconfigure(2, weight=1) # Grid-2
        self.rowconfigure(0, weight=1) # Grid-2

        self._start_stop_widget = MetronomeStartStopWidget(self)
        self._start_stop_widget.attach(self)
        self._start_stop_widget.grid(column=2, row=1, sticky='NWES') # Grid-2
        self.columnconfigure(2, weight=1) # Grid-2
        self.rowconfigure(1, weight=1) # Grid-2

        return None

    def update(self, subject):
        """
        Implementation of Subject.update(). Acts as a switchboard based on which widget is notifying.
        :parameter subject: Which widget instance is notifying the mediator?
        :return None:
        """
        # Determine which widget is notifying us of an update.
        match subject:
            case self._start_stop_widget:
                self.handle_start_stop_widget_update()
            case self._bpm_widget:
                self.handle_bmp_widget_update()
        return None

    def handle_start_stop_widget_update(self):
        """
        Handle updates from the start_stop_widget:
        :return None:
        """
        if self._start_stop_widget.get_state():
            # Metronome should be started.

            # Calculate the delay between clicks from the bpm value

            # Convert to beats per second
            bps = self._bpm / 60.
            # Compute delay between clicks in milliseconds
            click_delay = 1000. / bps

            # Start the event loop calling beat(...)
            self.beat()

        else:
            # Metronome should be stopped.

            # Cancel the beat after callback
            self.master.after_cancel(self._beat_after_id)
            # Reset the after id
            self._beat_after_id = 0
            # Turn off beacon light
            self._beacon_widget.set_state(False)

        return None

    def handle_bmp_widget_update(self):
        """
        Handle updates from bpm widget.
        :return None:
        """
        self._bpm = self._bpm_widget.get_state()
        return None

    def beat(self):
        """
        This is the function that is called to actually "tick" the metronome. Note that the timing of the beat is managed by the
        tkinter event loop, so is not seen within this method, but rather is controlling how often this method gets called.
        :return None:
        """
        # Determine beat delay, the time between beats (clicks) of the metronome

        # Convert to beats per second
        bps = self._bpm / 60
        # Compute delay between clicks in milliseconds
        beat_delay = 1000. / bps
        
        # Turn off beacon, in case it was turned on by a previous beat
        self._beacon_widget.set_state(False)
            
        # Beep
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 50  # Set Duration To 100 ms == 0.1 second (must be < 125, since maximum bpm is 480)
        winsound.Beep(frequency, duration)

        # Turn on beacon, to "flash" it as part of the beat
        self._beacon_widget.set_state(True)

        self._beat_after_id = self.master.after(int(beat_delay), self.beat)

        # sleep for the appropriate delay time
        # sleep(beat_delay)

        return None


class Subject:
    """
    Base class for all objects that will a Subject in an Observer design pattern.
    """
    def __init__(self) -> None:
        """
        """
        self._observers = []

    def attach(self, observer=None):
        """
        Attach an observer to the subject.
        :parameter observer: Observer object, instance of Observer class 
        :return None:
        """
        if observer:
            assert(isinstance(observer, Observer))
            self._observers.append(observer)
        return None

    def detach(self, observer=None):
        """
        Detach an observer from the subject.
        :parameter observer: Observer object, instance of Observer class 
        :return None:
        """
        if observer:
            self._observers.remove(observer)
        return None

    def notify(self):
        """
        Call update(...) on all observers.
        :return None:
        """
        for o in self._observers:
            o.update(self)
        return None


class MetronomeBpmWidget(ttk.Labelframe, Subject):
    """
    Class represents a tkinter label frame, the widget contents of which allow the beats per minute of the metronome to be set.
    """
    def __init__(self, parent, bpm=0) -> None:
        """
        :parameter parent: tkinter widget that is the parent of this widget
        """
        ttk.Labelframe.__init__(self, parent, text=f"Beats Per Minute")
        Subject.__init__(self)

        self._scale_bpm = tk.Scale(self, orient=tk.VERTICAL, length='2i', from_=30, to=240, command=self.OnBpmChanged,
                                   tickinterval=30)
        self._scale_bpm.grid(column=0, row=0) # Grid-2
        self.columnconfigure(0, weight=1) # Grid-2
        self.rowconfigure(0, weight=1) # Grid-2
        self._value_bpm=tk.IntVar()
        self._value_bpm.set(bpm)
        self._scale_bpm['variable']=self._value_bpm

    def OnBpmChanged(self, value):
        """
        Event handler for changes to bpm scale.
        """
        # Inform the mediator object of the change in beats per minute of the metronome
        self.notify()
        pass

    def get_state(self):
        """
        Return the bpm value from the widget.
        """
        return self._value_bpm.get()


class MetronomeStartStopWidget(ttk.Labelframe, Subject):
    """
    Class represents a tkinter label frame, the widget contents of which will allow the metronome to be started and stopped.
    """
    def __init__(self, parent) -> None:
        ttk.Labelframe.__init__(self, parent, text='Start/Stop')
        Subject.__init__(self)
        
        self._btn_start_stop = ttk.Button(self, command=self.OnStartStopButtonClicked)
        self._btn_start_stop.grid(column=0, row=0) # Grid-2
        self.columnconfigure(0, weight=1) # Grid-2
        self.rowconfigure(0, weight=1) # Grid-2
        self._lbl_start_stop=tk.StringVar()
        self._lbl_start_stop.set('Start')
        self._btn_start_stop['textvariable']=self._lbl_start_stop
        self._is_started = False

    def get_state(self):
        """
        Return whether the widget's state is started or stopped. Returns this as a bool which is True if started,
        and False if NOT started (that is, stopped).
        :return isStarted: True of started, False if stopped, bool
        """
        return self._is_started

    
    def OnStartStopButtonClicked(self):
        """
        Event handler for start/stop button click.
        """
        # Flip the started state
        if self._is_started:
            # Metronome state is currently started, so change state to stopped
            self._is_started = False
            # Change button text to 'Start'
            self._lbl_start_stop.set('Start')
        else:
            # Metronome state is currently stopped, so change it's state to started
            self._is_started = True
            # Change button text to 'Stop'
            self._lbl_start_stop.set('Stop')

        # Notify observers
        self.notify()

        return None


class MetronomeBeaconWidget(ttk.Labelframe, Subject):
    """
    Class represents a tkinter label frame, the widget contents of which will be a visual indicator of the metronome's timing tick.
    """
    def __init__(self, parent) -> None:
        ttk.Labelframe.__init__(self, parent, text='Beacon')
        Subject.__init__(self)
        
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

    def set_state(self, light=False):
        """
        Sets whether the beacon is lit or not.
        :parameter light: If True, then beacon state should be set to lit, boolean
        :return None:
        """
        if light:
            self._btn_beacon['background']='green'
        else:
            self._btn_beacon['background']='black'
        self.master.update_idletasks()

        return None