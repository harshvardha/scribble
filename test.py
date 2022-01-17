from threading import Thread
class functions:
    @classmethod
    def thread1(cls):
        while (True):
            print("thread1")
    
    @classmethod
    def thread2(cls):
        while (True):
            print("thread2")

class xyz:
    @classmethod
    def launchThreads(cls):
        thread1 = Thread(target=functions.thread1)
        thread1.deamon = True
        thread2 = Thread(target=functions.thread2)
        thread2.deamon = True
        thread1.start()
        thread2.start()

xyz.launchThreads()