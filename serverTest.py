import socket
port = 9999
host = ''
serverConnectionAcceptSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM)
serverConnectionAcceptSocket.bind((host,port))
serverConnectionAcceptSocket.listen(0)
while(True):
    conn,address = serverConnectionAcceptSocket.accept()
    print(address)