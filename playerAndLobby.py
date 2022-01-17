import json
from threading import Thread
class player:
    def __init__(self, name, avatar, connectionSocket, address):
        self.name = name
        self.points = 0
        self.rank = 10
        self.avatar = avatar
        self.address = address
        self.connectionSocket = connectionSocket
    
    def getName(self):
        return self.name

    def getPoints(self):
        return self.points
    
    def getRank(self):
        return self.rank
    
    def getAvatar(self):
        return self.avatar
    
    def getIPAddress(self):
        return self.address[0]
    
    def getConnection(self):
        return self.connectionSocket
    
    def sendMessage(self, message):
        self.connectionSocket.send(str.encode(message))
    
    def updatePoints(self, extras):
        self.points += extras

    def updateRank(self, newRank):
        self.rank = newRank

class privateLobbyPlayer(player):
    def __init__(self, name, avatar, isLobbyCreater, lobbyCode, connectionSocket, address):
        super().__init__(name = name, avatar = avatar, connectionSocket = connectionSocket, address = address)
        self.lobbyCreater = isLobbyCreater
        self.lobbyCode = lobbyCode
    
    def isLobbyCreater(self):
        return self.lobbyCreater
    
    def setLobbyCode(self, newLobbyCode):
        self.lobbyCode = newLobbyCode
    
    def getLobbyCode(self):
        return self.lobbyCode

class lobby:
    def __init__(self, roundTime, noOfRounds):
        self.roundTime = roundTime
        self.noOfRounds = noOfRounds
        self.listOfPlayers = []
        self.noOfRoundsPlayed = 0
    
    def getRoundTime(self):
        return self.roundTime

    def getNoOfRounds(self):
        return self.noOfRounds

    def getListOfPlayers(self):
        return self.listOfPlayers
    
    def getNoOfRoundsPlayed(self):
        return self.noOfRoundsPlayed
    
    def getNoOfPlayers(self):
        return len(self.listOfPlayers)
    
    def updateNoOfRoundsPlayed(self, newRoundNumber):
        if(newRoundNumber>0 and newRoundNumber<=10):
            self.noOfRoundsPlayed = newRoundNumber
    
    def addNewPlayer(self, playerObject):
        self.listOfPlayers.append(playerObject)
    
    def removePlayer(self, playerObjectToRemove):
        self.listOfPlayers.remove(playerObjectToRemove)

class publicLobby(lobby):
    def __init__(self, roundTime, noOfRounds):
        super().__init__(roundTime = roundTime, noOfRounds = noOfRounds)

class privateLobby(lobby):
    def __init__(self, roundTime, noOfRounds, lobbyCode, lobbyCreaterPlayer):
        super().__init__(roundTime = roundTime, noOfRounds = noOfRounds)
        self.lobbyCode = lobbyCode
        self.lobbyCreaterPlayer = lobbyCreaterPlayer
        self.waitingThread = Thread(target = self.waitForLobbyConfigs)
        self.waitingThread.daemon = True
        self.waitingThread.start()
    
    def waitForLobbyConfigs(self):
        response = json.dumps({
            "messageType" : "confirmation for starting game",
            "message" : "game starting"
        }, indent = 2)
        while(True):
            lobbyConfigs = str(self.lobbyCreaterPlayer.getConnection().recv(1024).decode("utf-8"))
            print(len(lobbyConfigs))
            if(len(lobbyConfigs)>0):
                lobbyConfigs = json.loads(lobbyConfigs)
                print(lobbyConfigs)
                self.lobbyCreaterPlayer.getConnection().send(str.encode(response))
                break
        #self.waitingThread.join()
    
    def getLobbyCode(self):
        return self.lobbyCode
    
    def setRoundTime(self, newRoundTime):
        if(newRoundTime in [10,20,30,40,50,60,70,80,90,100,110]):
            self.roundTime = newRoundTime
    
    def setNoOfRounds(self, newNoOfRounds):
        if(newNoOfRounds in [2,3,4,5,6,7,8,9,10]):
            self.noOfRounds = newNoOfRounds