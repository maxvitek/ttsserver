# -*- coding: utf-8 -*-
import cgi
import time

from Queue import Empty

# Load the Soco classes
from soco.snapshot import Snapshot
#from soco.event_structures import LastChangeEvent
from soco.events import event_listener


#########################################################################
# Sonos Speech class to get a device to talk
#########################################################################
class Speech():

    def __init__(self, device):
        # The device that the speech will be sent to
        self.device = device

    def say(self, message):
        # Need to subscribe to transport events, this is so that we know
        # when a given track has finished, and so we can stop it, if
        # we do not stop it, then it will repeat the text for a second time
        sub = self.device.avTransport.subscribe()

        # fade out
        prefade_volume = self.device.volume
        for v in range(prefade_volume):
            self.device.volume -= 1
            time.sleep(0.25)

        # Take a snapshot of the current sonos device state, we will want
        # to roll back to this when we are done
        snap = Snapshot(self.device)
        snap.snapshot()

        msg = cgi.escape(message)
        trans_URL = "x-rincon-mp3radio://translate.google.com/translate_tts?tl=en&q=%s" % msg
        self.device.play_uri(trans_URL, title="Speech")
        
        self.device.volume = prefade_volume

        impatience = time.time()
        patience = time.time() + 20
        while patience > impatience:
            try:
                event = sub.events.get(timeout=0.5)
                if 'restart_pending' not in event.variables:
                    continue
                restart_pending = event.variables['restart_pending']
                # About to try and restart, so stop looping and stop the
                # track before it starts again
                if restart_pending == '1':
                    break
            except Empty:
                pass
            # Wait another second for the speech to stop playing
            time.sleep(1)
            impatience = time.time()

        time.sleep(0)
        # Stop the stream playing
        self.device.stop()
        # Restore the sonos device back to it's previous state
        snap.restore()
        
        # fade back in
        for v in range(prefade_volume):
            self.device.volume += 1
            time.sleep(0.25)
        
        # We no longer want to  receive messages
        sub.unsubscribe()
        event_listener.stop()
