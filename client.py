class player:
    def __init__(self, name, avatar):
        self.name = name
        self.points = 0
        self.rank = 10
        self.avatar = avatar
        self.chat = ''
    
    def getName(self):
        return self.name
    
    def getPoints(self):
        return self.points
    
    def getRank(self):
        return self.rank

    def getAvatar(self):
        return self.avatar
    
    def getChatMessage(self):
        return self.chat
    
    def updateChat(self, newChat):
        self.chat = newChat
    
    def updatePoints(self, extras):
        self.points += extras
    
    def updateRank(self, newRank):
        self.rank = newRank

class privateLobbyPlayer(player):
    def __init__(self, name, avatar, isLobbyCreater, lobbyCode = None):
        super().__init__(name = name, avatar = avatar)
        self.isLobbyCreater = isLobbyCreater
        self.lobbyCode = lobbyCode
    
    def getLobbyCode(self):
        return self.lobbyCode
    
    def islobbyCreater(self):
        return self.isLobbyCreater
    
    def setLobbyCode(self, newLobbyCode):
        self.lobbyCode = newLobbyCode

class lobby:
    def __init__(self, roundTime, noOfRounds, listOfPlayers, noOfRoundsPlayed):
        self.roundTime = roundTime
        self.noOfRounds = noOfRounds
        self.listOfPlayers = listOfPlayers
        self.noOfRoundsPlayed = noOfRoundsPlayed
    
    def getRoundTime(self):
        return self.roundTime
    
    def getNoOfRounds(self):
        return self.noOfRounds
    
    def getListOfPlayers(self):
        return self.listOfPlayers
    
    def getNoOfRoundsPlayed(self):
        return self.noOfRoundsPlayed

    def addPlayer(self, newPlayer):
        self.listOfPlayers.append(newPlayer)
    
    def removePlayer(self, player):
        self.listOfPlayers.remove(player)
    
    def getNoOfPlayers(self):
        return len(self.listOfPlayers)
    
    def updateNoOfRoundsPlayed(self, newNoOfRounds):
        if(newNoOfRounds>0 and newNoOfRounds<=10):
            self.noOfRoundsPlayed = newNoOfRounds

class publicLobby(lobby):
    def __init__(self, roundTime, noOfRounds, listOfPlayers, noOfRoundsPlayed):
        super().__init__(
            roundTime = roundTime,
            noOfRounds = noOfRounds,
            listOfPlayers = listOfPlayers,
            noOfRoundsPlayed = noOfRoundsPlayed 
        )

class privateLobby(lobby):
    def __init__(self, roundTime, noOfRounds, listOfPlayers, noOfRoundsPlayed, lobbyCode):
        super().__init__(
            roundTime = roundTime,
            noOfRounds = noOfRounds,
            listOfPlayers = listOfPlayers,
            noOfRoundsPlayed = noOfRoundsPlayed
        )
        self.lobbyCode = lobbyCode
    
    def getLobbyCode(self):
        return self.lobbyCode
    
    def setRoundTime(self, newRoundTime):
        if(newRoundTime in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]):
            self.roundTime = newRoundTime
    
    def setNoOfRounds(self, newNoOfRounds):
        if(newNoOfRounds in [2, 3, 4, 5, 6, 7, 8, 9, 10]):
            self.noOfRounds = newNoOfRounds