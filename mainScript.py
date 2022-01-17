from threading import Thread
from clientConnection import connectToServer
from loginWindowFrontend import loginWindow
class main:
    @classmethod
    def launchBackgroundThreads(cls):
        sendRequestThread = Thread(target = connectToServer.sendRequestToServer)
        sendRequestThread.daemon = True
        recieveResponseThread = Thread(target=connectToServer.recieveServerResponse)
        recieveResponseThread.daemon = True
        sendRequestThread.start()
        recieveResponseThread.start()
    
    @classmethod
    def launchLoginWindow(cls):
        ui1 = loginWindow(width=1000, height=600, background="#e9f2f5")
        print("yes")
        loopVariable = True
        while (loopVariable):
            if (ui1.isGettingDestroyed()):
                loopVariable = False
                while (True):
                    if (len(connectToServer.serverResponse) > 0):
                        pass

main.launchBackgroundThreads()
main.launchLoginWindow()