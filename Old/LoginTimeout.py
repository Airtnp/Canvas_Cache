import threading

class TimeLimitExpired(Exception): 
    pass

def TimeoutThread(timeout, func, params, args=(), kwargs={}):
    """ Run func with the given timeout. If func didn't finish running
        within the timeout, raise TimeLimitExpired
    """

    class FuncThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None

        def run(self):
            self.result = func(params, *args, **kwargs)

        def _stop(self):
            if self.isAlive():
                threading.Thread._Thread__stop(self)

    it = FuncThread()
    it.start()
    it.join(timeout)
    if it.isAlive():
        it._stop()
        raise TimeLimitExpired()
    else:
        return it.result