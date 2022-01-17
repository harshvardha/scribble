import json
import socket
class connectToServer:
    requestMessage = {}
    coordinatesMessage = {
        "requestType": "canvas drawing coordinates",
        "name": "",
        "avatar": "",
        "x-coordinate": 0,
        "y-coordinate": 0 
    }
    chatMessage = {
        "requestType": "user chat",
        "name": "",
        "avatar": "",
        "chat": ""
    }
    host = 'localhost'
    port = 9999
    sct = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM)
    serverResponse = ''
    requestSended = False
    
    @classmethod
    def createRequestMessage(cls, messageType, messageDictionary):
        if(messageType=="join a public lobby"):
            cls.requestMessage["requestType"] = "join a public lobby"
            cls.requestMessage["name"] = messageDictionary["name"]
            cls.requestMessage["avatar"] = messageDictionary["avatar"]
        elif(messageType=="create a private lobby"):
            cls.requestMessage["requestType"] = "create a private lobby"
            cls.requestMessage["name"] = messageDictionary["name"]
            cls.requestMessage["avatar"] = messageDictionary["avatar"]
            cls.requestMessage["isLobbyCreater"] = "True"
        elif(messageType=="join a private lobby"):
            cls.requestMessage["requestType"] = "join a private lobby"
            cls.requestMessage["name"] = messageDictionary["name"]
            cls.requestMessage["avatar"] = messageDictionary["avatar"]
            cls.requestMessage["isLobbyCreater"] = "False"
            cls.requestMessage["lobbyCode"] = messageDictionary["lobbyCode"]
        elif(messageType == "send lobby configuration"):
            cls.requestMessage["requestType"] = "lobby configurations"
            cls.requestMessage["isLobbyCreater"] = "False"
            cls.requestMessage["roundTime"] = messageDictionary["roundTime"]
            cls.requestMessage["noOfRounds"] = messageDictionary["noOfRounds"]
        elif(messageType == "send canvas coordinates"):
            cls.coordinatesMessage["name"] = messageDictionary["name"]
            cls.coordinatesMessage["avatar"] = messageDictionary["avatar"]
            cls.coordinatesMessage["x-coordinate"] = messageDictionary["x-coordinate"]
            cls.coordinatesMessage["y-coordinate"] = messageDictionary["y-coordinate"]
        elif (messageType == "send chat"):
            cls.chatMessage["name"] = messageDictionary["name"]
            cls.chatMessage["avatar"] = messageDictionary["avatar"]
            cls.chatMessage["chat"] = messageDictionary["chat"]
    
    @classmethod
    def updateCanvasCoordinatesMessage(cls, xCoordinate, yCoordinate):
        cls.coordinatesMessage["x-coordinate"] = xCoordinate
        cls.coordinatesMessage["y-coordinate"] = yCoordinate

    @classmethod
    def updateChatMessage(cls, newChat):
        cls.chatMessage["chat"] = newChat

    @classmethod    
    def connectToServer(cls):
        try:
            cls.sct.connect((cls.host,cls.port))
        except:
            print("error connecting to server from connectToServer")

    @classmethod
    def sendRequestToServer(cls):
        try:
            while (True):
                requestMessageKeys = list(cls.requestMessage.keys())
                if(len(requestMessageKeys)>0):
                    cls.sct.send(str.encode(json.dumps(cls.requestMessage, indent=2)))
                    cls.requestSended = True
                    cls.requestMessage = {}
                elif (cls.coordinatesMessage["name"] != "" and cls.coordinatesMessage["avatar"] != ""):
                    cls.sct.send(str.encode(json.dumps(cls.coordinatesMessage, indent=2)))
                    cls.requestSended = True
                elif (cls.chatMessage["name"] != "" and cls.chatMessage["avatar"] != "" and cls.chatMessage["chat"] != ""):
                    cls.sct.send(str.encode(json.dumps(cls.chatMessage, indent=2)))
                    cls.requestSended = True
        except:
            print("error connecting to server from sendRequestToServer")
    
    @classmethod
    def recieveServerResponse(cls):
        try:
            while (True):
                if (cls.requestSended):
                    cls.requestSended = False
                    response = str(cls.sct.recv(4096).decode("utf-8"))
                    if (len(response) > 0):
                        cls.serverResponse = response
        except:
            print("error connecting to server from recieveServerResponse")