import socket
import pygame

class Network:

    def __init__(self):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server = str(input('Server Address : '))
        if self.server == '':
            self.server = "127.0.0.1:8080"
        self.ip = str(self.server.split(":")[0])
        self.port = int(self.server.split(":")[1])
        print(self.ip, "/", self.port)
        self.addr = (self.ip, self.port)

        self.player = self.connect()


    def connect(self):
        try:
            self.client.connect(self.addr)
            print("Connected !")
            return self.client.recv(2048).decode()
        except:
            pass


    def send(self, data):
        try:
            self.client.send(str.encode(data))
            temp =  self.client.recv(2048).decode()
            return temp
        except socket.error as e:
            print(e)




class Cursor:
    def __init__(self, screen):
        self.x = 1
        self.y = 1
        self.width = 49
        self.height = 49
        self.surface = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.color = pygame.Color(150, 150, 150, 50)
        self.screen = screen

    def draw(self):
        self.rect = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.surface, self.color, self.rect)
        self.screen.blit(self.surface, self.rect)

    def update(self, pos):
        self.x = 50*pos[0]+1
        self.y = 50*pos[1]+1
        self.draw()




class Game:

    def __init__(self):

        pygame.font.init()
        self.font = pygame.font.SysFont('arial', 20)

        self.n = Network()
        if self.n.player == '1':
            self.playerNB = 1
        elif self.n.player == '2':
            self.playerNB = -1
        else:
            self.playerNB = 0
        self.playerTurn = 1

        self.grid = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, -1, 0, 0, 0],
            [0, 0, 0, -1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.clicked = [-1, -1]

        self.win = 0
        
        self.screen = pygame.display.set_mode((400, 450), pygame.SRCALPHA)
        pygame.display.set_caption("TicTacToe")

        self.cursor = Cursor(self.screen)


    def msg(self):
        txt = ''
        if self.playerNB == 1 or self.playerNB == -1:
            if self.win == 0:
                if self.playerTurn == self.playerNB:
                    txt = "Your Turn"
                else:
                    txt = "Your Opponent Turn"
            elif self.win == 2:
                txt = "Tie!"
            elif self.win == self.playerNB:
                txt = "You won the game, GG!"
            else:
                txt = "You lost..."
        else:
            txt = "Spectating"

        text = self.font.render(txt, False, (255, 255, 255), (0, 0, 0))
        self.screen.blit(text, (200-(10*len(txt)/2), 425))


    def render(self):

        self.screen.fill((0, 0, 0))
        
        for x in range(1, 8):
            pygame.draw.line(self.screen, (255, 255, 255), (0, 50*x), (400, 50*x))
        for y in range(1, 8):
            pygame.draw.line(self.screen, (255, 255, 255), (50*y, 0), (50*y, 400))

        for row in range(0, 8):
            for column in range(0, 8):
                pos = [row, column]
                element = self.grid[row][column]

                if element == 0:
                    None
                elif element == 1:
                    pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(50*pos[0]+10, 50*pos[1]+10, 30, 30))
                elif element == -1:
                    pygame.draw.circle(self.screen, (255, 255, 255), (50*pos[0]+25, 50*pos[1]+25), 15)


    def input(self):
        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0]<=100/2:
            mouseX = 0
        elif mouse_pos[0]<=200/2:
            mouseX = 1
        elif mouse_pos[0]<=300/2:
            mouseX = 2
        elif mouse_pos[0]<=400/2:
            mouseX = 3
        elif mouse_pos[0]<=500/2:
            mouseX = 4
        elif mouse_pos[0]<=600/2:
            mouseX = 5
        elif mouse_pos[0]<=700/2:
            mouseX = 6
        else:
            mouseX = 7

        if mouse_pos[1]<=100/2:
            mouseY = 0
        elif mouse_pos[1]<=200/2:
            mouseY = 1
        elif mouse_pos[1]<=300/2:
            mouseY = 2
        elif mouse_pos[1]<=400/2:
            mouseY = 3
        elif mouse_pos[1]<=500/2:
            mouseY = 4
        elif mouse_pos[1]<=600/2:
            mouseY = 5
        elif mouse_pos[1]<=700/2:
            mouseY = 6
        else:
            mouseY = 7

        self.clicked = [-1, -1]
        if self.grid[mouseX][mouseY] == 0:
            self.cursor.update([mouseX, mouseY])
            if pygame.mouse.get_pressed()[0]:
                self.clicked = [mouseX, mouseY]


    def getData(self, data):
        tmp = eval(data)
        self.playerTurn = tmp[0]
        self.grid = tmp[1]
        self.win = tmp[2]


    def makeData(self):
        data = str([self.clicked, self.playerNB])
        if (self.clicked != [-1, -1]):
            print("Sent: ", data)
        return data

    
    def run(self):

        clock = pygame.time.Clock()
        run = True

        while run:

            self.render()

            if self.playerTurn == self.playerNB:
                self.input()
                self.cursor.draw()

            self.msg()
            pygame.display.update()

            self.getData(self.n.send(self.makeData()))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            clock.tick(30)
        
        pygame.quit


game = Game()
game.run()
