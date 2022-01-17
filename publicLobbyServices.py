from queue import Queue
from playerAndLobby import publicLobby
import json
class publicLobbyJoiningService:
    waitingQueue = Queue()
    def __init__(self, lobbyList):
        self.lobbyList = lobbyList
    
    def searchAndAddPlayerToLobby(self):
        print("ran public lobby joining service")
        while(True):
            if(len(self.lobbyList.getLobbyList())==0 and publicLobbyJoiningService.waitingQueue.qsize()>1):
                self.createNewLobby()
            elif(len(self.lobbyList.getLobbyList())>0 and publicLobbyJoiningService.waitingQueue.qsize()>0):
                if(self.lobbyList.getLobbyList()[0].getNoOfPlayers()<10):
                    player = publicLobbyJoiningService.waitingQueue.get()
                    self.lobbyList.getLobbyList()[0].addNewPlayer(player)
                    player.sendMessage(
                        json.dumps(publicLobbyJoiningService.createResponseMessage(lobbyObject = self.lobbyList.getLobbyList()[0]),indent = 2))
                    publicLobbyJoiningService.waitingQueue.task_done()
                    self.lobbyList.sortLobbyList()
                else:
                    self.createNewLobby()
    
    def createNewLobby(self):
        lobby = publicLobby(roundTime = 80, noOfRounds = 10)
        for _ in range(10):
            if(publicLobbyJoiningService.waitingQueue.qsize()>1):
                player = publicLobbyJoiningService.waitingQueue.get()
                lobby.addNewPlayer(player)
                player.sendMessage(
                    json.dumps(publicLobbyJoiningService.createResponseMessage(lobbyObject = lobby), indent = 2))
                publicLobbyJoiningService.waitingQueue.task_done()
            else:
                break
        self.lobbyList.addLobby(lobby)
    
    @staticmethod
    def createResponseMessage(lobbyObject):
        playersInfo = []
        playersList = lobbyObject.getListOfPlayers()
        for i in range(lobbyObject.getNoOfPlayers()-1):
            playersInfo.append(
                {
                    "name" : playersList[i].getName(),
                    "points" : playersList[i].getPoints(),
                    "rank" : playersList[i].getRank(),
                    "avatar" : playersList[i].getAvatar()
                }
            )
        return {
            "responseType" : "public lobby information",
            "roundTime" : 80,
            "noOfRounds" : 10,
            "noOfRoundsPlayed" : lobbyObject.getNoOfRoundsPlayed(),
            "listOfPlayers" : playersInfo
        }

    @classmethod
    def addPlayerToQueue(cls, playerObject):
        cls.waitingQueue.put(playerObject)
        cls.waitingQueue.join()