import socket
from _thread import *

class Server:

    def __init__(self):
        self.ip = str(input("IP (default: 127.0.0.1): "))
        if self.ip == "":
            self.ip = "127.0.0.1"

        self.port = str(input("Port (default: 5757): "))
        if self.port == "":
            self.port = 5757
        self.port = int(self.port)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind((self.ip, self.port))
        except socket.error as e:
            print(e)

        self.server.listen(2)
        print(f"Server started at {self.ip}:{self.port}")

        self.playercount = 0
        self.currentPlayer = 0
        self.pos = [-100,-100]

    def clientConn(self, conn, addr):
        self.playercount += 1
        playerType = 1 if self.playercount == 1 else -1
        playerType = str(playerType)
        print(playerType)
        conn.send(str.encode(playerType))
        # conn.send(str.encode(playerType))

        reply = ""

        while True:
            try:
                recvData = conn.recv(2048).decode()
                if not recvData:
                    print("Client", addr, ": Disconnected")
                else:
                    self.getData(recvData)
                    sendData = str(self.makeData(self.currentPlayer, self.pos))
                    reply = str.encode(sendData)

                conn.send(reply)

            except:
                print("Lost Connection")
                break
        
        self.playercount -= 1

    def makeData(self, player, pos):
        data = [player, pos]
        return data
    
    def getData(self, data):
        player, pos = eval(data)  # Extract player and position
        self.currentPlayer = player
        self.pos = pos

    def run(self):
        while True:
            conn, addr = self.server.accept()
            print("Client Connected:", addr)

            if self.playercount == 0:
                self.playerTurn = 1

            start_new_thread(self.clientConn, (conn, addr))

server = Server()
server.run()
