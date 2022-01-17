from queue import Queue
import socket
from threading import Thread
import commonServices
from publicLobbyServices import publicLobbyJoiningService
from playerAndLobby import player, privateLobbyPlayer
from privateLobbyServices import lobbyCodeGeneratorService, lobbyCreaterService, privateLobbyJoiningService
import json

NUMBER_OF_THREADS = 6
JOB_NUMBER = [1, 2, 3, 4, 5, 6]
queue = Queue()
privateLobbyDictionary = commonServices.privateLobbyDictionary()

class request:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
    
    def getConnection(self):
        return self.connection

    def getAddress(self):
        return self.address

class routingService:
    waitingQueue = Queue()

    @classmethod
    def parseAndRouteRequest(cls):
        print("ran routing service")
        while(True):
            if(cls.waitingQueue.qsize()>0):
                r = cls.waitingQueue.get()
                message = str(r.getConnection().recv(4096).decode("utf-8"))
                message = json.loads(message)
                if(message["requestType"] == "join public lobby"):
                    publicLobbyJoiningService.addPlayerToQueue(
                        playerObject = player(
                        name = message["name"], 
                        avatar = message["avatar"], 
                        connectionSocket = r.getConnection(), 
                        address = r.getAddress()
                    ))
                elif(message["requestType"] == "create a private lobby"):
                    print("yes request parsed")
                    lobbyCodeGeneratorService.addPlayerToQueue(
                        lobbyCreaterPlayerObject = privateLobbyPlayer(
                            name = message["name"],
                            avatar = message["avatar"],
                            isLobbyCreater = message["isLobbyCreater"],
                            lobbyCode = 0,
                            connectionSocket = r.getConnection(),
                            address = r.getAddress()
                        ))
                elif(message["requestType"] == "join a private lobby"):
                    privateLobbyJoiningService.addPlayerToQueue(
                        playerObject = privateLobbyPlayer(
                            name = message["name"],
                            avatar = message["avatar"],
                            isLobbyCreater = message["isLobbyCreater"],
                            lobbyCode = message["lobbyCode"],
                            connectionSocket = r.getConnection(),
                            address = r.getAddress()
                        ))
                cls.waitingQueue.task_done()

    
    @classmethod
    def addRequestToQueue(cls, requestObject):
        print("in add request to queue of routing service")
        cls.waitingQueue.put(requestObject)
        cls.waitingQueue.join()

class server:
    def __init__(self):
        self.port = 9999
        self.host = ''
        self.sct = None
    
    def createSocket(self):
        self.sct = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM)
    
    def bindSocket(self):
        self.sct.bind((self.host,self.port))
        self.sct.listen(5)

    def acceptConnections(self):
        while(True):
            conn, addrs = self.sct.accept()
            print("connected to : ",addrs)
            if(conn is not None and addrs is not None):
                routingService.addRequestToQueue(requestObject = request(connection = conn, address = addrs))

def createWorkerThreads():
    for _ in range(NUMBER_OF_THREADS):
        t = Thread(target = work)
        t.deamon = True
        t.start()

def work():
    for _ in range(6):
        x = queue.get()
        if(x==1):
            print("ran server class")
            serverObject = server()
            serverObject.createSocket()
            serverObject.bindSocket()
            serverObject.acceptConnections()    
        elif(x==2):
            publicLobbyList = commonServices.publicLobbyList()
            publicLobbyJoiningService(lobbyList = publicLobbyList).searchAndAddPlayerToLobby()
        elif(x==3):
            lobbyCodeGeneratorService().generateLobbyCode()
        elif(x==4):
            lobbyCreaterService(privateLobbyDictionary).createLobby()
        elif(x==5):
            routingService.parseAndRouteRequest()
        elif(x==6):
            privateLobbyJoiningService(privateLobbyDictionary).joinLobby()
        queue.task_done()

def createJobs():
    for job in JOB_NUMBER:
        queue.put(job)
    queue.join()

createWorkerThreads()
createJobs()