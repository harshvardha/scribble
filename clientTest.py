import socket
import json
serverAddress = 'localhost'
port = 9999
requestMessage = {
    "requestType" : "join private lobby",
    "name" : "Drasiel",
    "avatar" : "male",
    "isLobbyCreater" : "False",
    "lobbyCode" : 100001
}
data = json.dumps(requestMessage, indent = 2)
clientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM)
clientSocket.connect((serverAddress,port))
while(True):
    clientSocket.send(str.encode(data))
    recievedData = clientSocket.recv(1024).decode("utf-8")
    recievedData = json.loads(recievedData)
    print(recievedData)
    # listOfPlayers = recievedData["listOfPlayers"]
    # player = json.loads(listOfPlayers[0])
    # print(player["name"])