# ******** Libraries ************
import threading 
import time

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.values = []
        self.is_running = False
        self.next_call = time.time()
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.values.append(self.function(*self.args, **self.kwargs))

    def start(self):
        if not self.is_running:
            self.next_call += self.interval
            self._timer = threading.Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

# ********************Example ********************#
def hello(name):
    print ("Hello %s!" % name)
    return 2
 
print ("starting...")
rt = RepeatedTimer(0.02, hello, 1) # it auto-starts, no need of rt.start()
try:
    time.sleep(0.09) # your long-running job goes here...
finally:
    rt.stop() # better in a try/finally block to make sure the program ends!
    print(rt.values)
