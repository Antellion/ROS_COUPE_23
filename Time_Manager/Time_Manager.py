import time
from threading import Thread


class Time:

    def __init__(self):
        self._running = True
        self.counter_time = 100 #timer of ... seconds
        self.seuil_time_left = 3

    def __counter(self):
        while self._running and self.counter_time > 0:
            self.counter_time -= 1
            time.sleep(1)

    def launch_counter(self): #start counter
        self._running = True
        tcounter = Thread(target=self.__counter, daemon=True)
        tcounter.start()
        pass

    def stop_counter(self):
        self._running = False
        pass

    def get_time(self):
        return self.counter_time #return time 
        
    def seuil_time(self):
        return self.seuil_time_left