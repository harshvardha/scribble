class publicLobbyList:
    def __init__(self):
        print("ran public lobby list")
        self.lobbyList = []
    
    def addLobby(self, lobbyObject):
        self.lobbyList.append(lobbyObject)
    
    def removeLobby(self, lobbyObject):
        self.lobbyList.remove(lobbyObject)
    
    def sortLobbyList(self):
        for j in range(len(self.lobbyList)-1):
            if(self.lobbyList[j].getNoOfPlayers()>self.lobbyList[j+1].getNoOfPlayers()):
                temp = self.lobbyList[j+1]
                self.lobbyList[j+1] = self.lobbyList[j]
                self.lobbyList[j] = temp
            else:
                break

    def getLobbyList(self):
        return self.lobbyList

class privateLobbyDictionary:
    def __init__(self):
        print("ran private lobby dictionary")
        self.lobbyDictionary = {}
    
    def addLobby(self, lobbyObject):
        self.lobbyDictionary[lobbyObject.getLobbyCode()] = lobbyObject

    def removeLobby(self, lobbyCode):
        del(self.lobbyDictionary[lobbyCode])
    
    def getLobby(self, lobbyCode):
        return self.lobbyDictionary.get(lobbyCode)