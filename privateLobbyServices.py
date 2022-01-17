from queue import Queue
from playerAndLobby import privateLobby
import responseMessages
import json
class lobbyCodeGeneratorService:
    waitingQueue = Queue()
    def __init__(self):
        self.lowerBound = 100000
        self.upperBound = self.lowerBound+lobbyCodeGeneratorService.waitingQueue.qsize()
    
    def generateLobbyCode(self):
        print("ran lobby code generator service")
        while(True):
            if(lobbyCodeGeneratorService.waitingQueue.qsize()>0):
                print("generating lobby code")
                player = lobbyCodeGeneratorService.waitingQueue.get()
                if(player.isLobbyCreater()=="True"):
                    player.setLobbyCode(self.lowerBound)
                    self.lowerBound += 1
                    self.upperBound = self.lowerBound+lobbyCodeGeneratorService.waitingQueue.qsize()
                    lobbyCodeGeneratorService.waitingQueue.task_done()
                    lobbyCreaterService.addPlayerToQueue(playerObject = player)
                else:
                    player.sendMessage(json.dumps(responseMessages.NOT_A_LOBBY_CREATER_RESPONSE, indent = 2))

    @classmethod
    def addPlayerToQueue(cls, lobbyCreaterPlayerObject):
        if(lobbyCreaterPlayerObject.isLobbyCreater()):
            cls.waitingQueue.put(lobbyCreaterPlayerObject)
            cls.waitingQueue.join()
    
class lobbyCreaterService:
    waitingQueue = Queue()
    def __init__(self, lobbyDictionary):
        self.lobbyDictionary = lobbyDictionary
    
    def createLobby(self):
        print("ran lobby creater service")
        while(True):
            if(lobbyCreaterService.waitingQueue.qsize()>0):
                player = lobbyCreaterService.waitingQueue.get()
                if(player.isLobbyCreater()=="True"):
                    lobby = privateLobby(roundTime = 0, noOfRounds = 0, lobbyCode = player.getLobbyCode(), lobbyCreaterPlayer = player)
                    lobby.addNewPlayer(player)
                    lobbyCreaterService.waitingQueue.task_done()
                    self.lobbyDictionary.addLobby(lobby)
                    responseMessages.PRIVATE_LOBBY_INFORMATION["lobbyCode"] = lobby.getLobbyCode()
                    player.sendMessage(json.dumps(responseMessages.PRIVATE_LOBBY_INFORMATION, indent = 2))
    
    @classmethod
    def addPlayerToQueue(cls, playerObject):
        if(playerObject.isLobbyCreater()):
            cls.waitingQueue.put(playerObject)
            cls.waitingQueue.join()

class privateLobbyJoiningService:
    waitingQueue = Queue()
    def __init__(self, lobbyDictionary):
        self.lobbyDictionary = lobbyDictionary
    
    def joinLobby(self):
        print("private lobby joining service")
        while(True):
            if(privateLobbyJoiningService.waitingQueue.qsize()>0):
                player = privateLobbyJoiningService.waitingQueue.get()
                lobby = self.lobbyDictionary.getLobby(player.getLobbyCode())
                lobby.addNewPlayer(player)
                privateLobbyJoiningService.waitingQueue.task_done()
                player.sendMessage(privateLobbyJoiningService.createResponseMessage(lobby))
    
    @staticmethod
    def createResponseMessage(lobbyObject):
        responseMessages.PRIVATE_LOBBY_INFORMATION["roundTime"] = lobbyObject.getRoundTime()
        responseMessages.PRIVATE_LOBBY_INFORMATION["noOfRounds"] = lobbyObject.getNoOfRounds()
        playersInfo = []
        infoDictionary = {
            "name" : "",
            "rank" : 0,
            "points" : 0,
            "avatar" : ""
        }
        listOfPlayers = lobbyObject.getListOfPlayers()
        for i in range(len(listOfPlayers)-1):
            infoDictionary["name"] = listOfPlayers[i].getName()
            infoDictionary["rank"] = listOfPlayers[i].getRank()
            infoDictionary["points"] = listOfPlayers[i].getPoints()
            infoDictionary["avatar"] = listOfPlayers[i].getAvatar()
            playersInfo.append(json.dumps(infoDictionary))
        responseMessages.PRIVATE_LOBBY_INFORMATION["listOfPlayers"] = playersInfo
        return json.dumps(responseMessages.PRIVATE_LOBBY_INFORMATION, indent = 2)

    @classmethod
    def addPlayerToQueue(cls, playerObject):
        cls.waitingQueue.put(playerObject)
        cls.waitingQueue.join()