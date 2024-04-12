import pygame
import random
import copy
from menu_screen import MenuScreen
import numpy as np
import socket
import time


import sys
sys.path.append('othelloAI')

from othelloAI.OthelloPlayer import AlphaZeroPlayer

# def select_move(cur_state, player_to_move, remain_time):
#     return AlphaZeroPlayer().play(cur_state, player_to_move, remain_time)

# Utility functions
def directions(x, y, minX=0, minY=0, maxX=7, maxY=7):
    """Check to determine which directions are valid from current cell"""
    validdirections = []
    if x != minX: validdirections.append((x-1, y))
    if x != minX and y != minY: validdirections.append((x-1, y-1))
    if x != minX and y != maxY: validdirections.append((x-1, y+1))

    if x!= maxX: validdirections.append((x+1, y))
    if x != maxX and y != minY: validdirections.append((x+1, y-1))
    if x != maxX and y != maxY: validdirections.append((x+1, y+1))

    if y != minY: validdirections.append((x, y-1))
    if y != maxY: validdirections.append((x, y+1))

    return validdirections

def loadImages(path, size):
    """Load image into game and scale it"""
    img = pygame.image.load(f"{path}").convert_alpha()
    img = pygame.transform.scale(img, size)
    return img

def loadSpriteSheet(sheet, row, col, newSize, size):
    """creates an empty surface, loads a portion of the spritesheet onto the surface, then return that surface as img"""
    image = pygame.Surface((32, 32)).convert_alpha()
    image.blit(sheet, (0, 0), (row * size[0], col * size[1], size[0], size[1]))
    image = pygame.transform.scale(image, newSize)
    image.set_colorkey("Black")
    return image

def evaluateBoard(grid, player):
    score = 0
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            # Ở đây PC đóng vai player2 = -1 nên điểm sẽ trừ tức ngược lại thành cộng
            score -= col
    return score

class Network:

    def __init__(self):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # self.server = str(input('Server Address : '))
        # if self.server == '':
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
            

class Othello:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1100, 800))
        pygame.display.set_caption("Othello")
  
        self.showMenu = True
        self.time = 0

        self.rows = 8
        self.columns = 8

        self.player1 = 1
        self.player2 = -1

        self.currentPlayerTurn = 1
        self.currentPlayer = 1
        

        self.grid = Grid(self.rows, self.columns, (80, 80), self)
        self.font = pygame.font.SysFont('Arial', 20, True, False)

        self.computerPlayer = ComputerPlayer(self.grid)

        self.AlphaZeroPlayer = None
        self.gameOver = False
        
        self.RUN = True
        self.menuFont = pygame.font.SysFont('Arial', 42, True, False)
        self.menuScreen = MenuScreen(self.screen, self.menuFont)
        
        self.is_pvp = False
        self.network = None
        self.clicked_x = -1
        self.clicked_y = -1
        self.disconnected = False
        

    def run(self):
        while self.RUN == True:
            if self.showMenu:
                drawMenuReturn = self.menuScreen.drawMenu()
                if drawMenuReturn == "notShowMenu":
                    self.showMenu = False
                continue

            if self.menuScreen.menuType =="hard" and self.AlphaZeroPlayer == None:
                self.AlphaZeroPlayer = AlphaZeroPlayer()
            
            if self.menuScreen.menuType == "chooseRoom" and self.is_pvp == False:
                self.is_pvp = True
                self.network = Network()
                if int(self.network.player) == 1:
                    self.currentPlayer = 1
                elif int(self.network.player) == 2:
                    self.currentPlayer = -1
                

            self.input()
            self.update()
            self.draw()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUN = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:	# Right click
                    self.grid.printGameLogicBoard()

                if event.button == 1:	# Left click
                    if self.currentPlayerTurn == self.currentPlayer and not self.gameOver:
                        x, y = pygame.mouse.get_pos()
                        x, y = (x - 80) // 80, (y - 80) // 80
                        validCells = self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayerTurn)
                        if not validCells:
                            pass
                        else:
                            if (y, x) in validCells:
                                self.grid.insertToken(self.grid.gridLogic, self.currentPlayerTurn, y, x)
                                swappableTiles = self.grid.swappableTiles(y, x, self.grid.gridLogic, self.currentPlayerTurn)
                                for tile in swappableTiles:
                                    self.grid.animateTransitions(tile, self.currentPlayerTurn)
                                    self.grid.gridLogic[tile[0]][tile[1]] *= -1
                                self.currentPlayerTurn *= -1
                                self.time = pygame.time.get_ticks()
                                
                                self.clicked_y = y
                                self.clicked_x = x

                    if self.gameOver:
                        x, y = pygame.mouse.get_pos()
                        if x >= 320 and x <= 480 and y >= 400 and y <= 480:
                            self.grid.newGame()
                            self.gameOver = False

    def update(self):
        if self.currentPlayerTurn == -1*self.currentPlayer:
            if self.is_pvp: # new code PvP
                playerTurn , grid, move = self.getData(self.network.send(self.makeData()))
                # print( playerTurn , move)
                if playerTurn == 404:
                    self.gameOver = True
                    self.disconnected = True
                    return
                
                if move != [-1,-1] and -1*playerTurn != self.currentPlayer :
                    # print( playerTurn , move)
                    
                    print('----------------')
                    print(self.currentPlayerTurn)
                    print(move)
                    self.grid.insertToken(self.grid.gridLogic, self.currentPlayerTurn, move[0], move[1])
                    swappableTiles = self.grid.swappableTiles(move[0], move[1], self.grid.gridLogic, self.currentPlayerTurn)
                    for tile in swappableTiles:
                        self.grid.animateTransitions(tile, self.currentPlayerTurn)
                        self.grid.gridLogic[tile[0]][tile[1]] *= -1
                    self.currentPlayerTurn *= -1
            
            else:
               # PvE old code     
                new_time = pygame.time.get_ticks()
                #cell = None
                if new_time - self.time >= 100:	# Delay 1s
                    if not self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayerTurn):
                        self.gameOver = True
                        return
                    if self.menuScreen.difficulty =="easy":
                        cell, score = self.computerPlayer.computerHard(self.grid.gridLogic, 5, -64, 64, self.currentPlayerTurn)
                    elif self.menuScreen.difficulty =="hard" :
                        # cell, score = self.computerPlayer.computerHard(self.grid.gridLogic, 5, -64, 64, -1)
                        # print('Dumb Move: ', cell)
                        cell = self.AlphaZeroPlayer.play(np.array(self.grid.gridLogic), self.currentPlayerTurn, 0)
                        # print('AlphaZero Move: ', move)

                    self.grid.insertToken(self.grid.gridLogic, self.currentPlayerTurn, cell[0], cell[1])
                    swappableTiles = self.grid.swappableTiles(cell[0], cell[1], self.grid.gridLogic, self.currentPlayerTurn)
                    for tile in swappableTiles:
                        self.grid.animateTransitions(tile, self.currentPlayerTurn)
                        self.grid.gridLogic[tile[0]][tile[1]] *= -1
                    self.currentPlayerTurn *= -1

        self.grid.player1Score = self.grid.calculatePlayerScore(self.player1)
        self.grid.player2Score = self.grid.calculatePlayerScore(self.player2)
        if not self.grid.findAvailMoves(self.grid.gridLogic, self.currentPlayerTurn):
            self.gameOver = True
            return
    
    def getData(self, data):
        tmp = eval(data)
        playerTurn = tmp[0]
        grid = tmp[1]
        move = tmp[2]
        return playerTurn , grid, move


    def makeData(self):
        clicked = [self.clicked_y, self.clicked_x]
        data = str([clicked, self.currentPlayer])
        if (clicked != [-1, -1]):
            print("Sent: ", data)
        return data

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.grid.drawGrid(self.screen)

        pygame.display.update()

# Class grid biểu diễn bàn cờ
class Grid:
    # Số row, column, size là kích thước của mỗi ô cờ
    def __init__(self, rows, columns, size, main):
        self.GAME = main
        self.x = rows
        self.y = columns
        self.size = size

        self.whitetoken = loadImages("assets/WhiteToken.png", size)
        self.blacktoken = loadImages("assets/BlackToken.png", size)
        self.transitionWhiteToBlack = [loadImages(f"assets/WhiteToBlack{i}.png", size) for i in range(1, 4)]
        self.transitionBlackToWhite = [loadImages(f"assets/BlackToWhite{i}.png", size) for i in range(1, 4)]

        self.bg = self.loadBackGroundImages()
        self.gridBg = self.createbgimg()

        self.player1Score = 0
        self.player2Score = 0

        # List các quân cờ đang nằm trên bàn
        self.tokens = {}

        self.font = pygame.font.SysFont('Arial', 20, True, False)

        self.gridLogic = self.regenLogic(self.x, self.y)

    def newGame(self):
        self.tokens.clear()
        self.gridLogic = self.regenLogic(self.y, self.x)

    def loadBackGroundImages(self):
        alpha = "ABCDEFGHI"
        spriteSheet = pygame.image.load("assets/wood.png").convert_alpha()
        imageDict = {}
        for i in range(3):
            for j in range(7):
                imageDict[alpha[j] + str(i)] = loadSpriteSheet(spriteSheet, j, i, (self.size), (32, 32))
        return imageDict

    def createbgimg(self):
        """Tạo background image cho bàn cờ"""
        gridBg = [
            ['C0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'E0'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'E2'],
        ]
        image = pygame.Surface((960, 960))
        for j, row in enumerate(gridBg):
            for i, img in enumerate(row):
                image.blit(self.bg[img], (i * self.size[0], j * self.size[1]))
        return image

    def regenLogic(self, rows, columns):
        """Generate an empty grid for logic use"""
        grid = []
        for y in range(rows):
            line = []
            for x in range(columns):
                line.append(0)
            grid.append(line)
        self.insertToken(grid, 1, 3, 3)
        self.insertToken(grid, -1, 3, 4)
        self.insertToken(grid, 1, 4, 4)
        self.insertToken(grid, -1, 4, 3)

        return grid

    def printGameLogicBoard(self):
        print(" | A | B | C | D | E | F | G | H |")
        for i, row in enumerate(self.gridLogic):
            line = f"{i} |".ljust(3, " ")
            for item in row:
                line += f"{item}".center(3, " ") + "|"
            print(line)
        print()

    def findValidCells(self, grid, curPlayer):
        """Performs a check to find all empty cells that are adjacent to opposing player"""
        validCellToClick = []
        for gridX, row in enumerate(grid):
            for gridY, col in enumerate(row):
                if grid[gridX][gridY] != 0:
                    continue
                # Kiểm tra các hướng từ các ô trống
                DIRECTIONS = directions(gridX, gridY)

                for direction in DIRECTIONS:
                    dirX, dirY = direction
                    checkedCell = grid[dirX][dirY]

                    if checkedCell == 0 or checkedCell == curPlayer:
                        continue

                    if (gridX, gridY) in validCellToClick:
                        continue

                    # Chỉ chọn ô trống có giao nhau với ô của địch
                    validCellToClick.append((gridX, gridY))

        return validCellToClick

    def swappableTiles(self, x, y, grid, player):
        surroundCells = directions(x, y)
        if len(surroundCells) == 0:
            return []

        swappableTiles = []
        for checkCell in surroundCells:
            checkX, checkY = checkCell
            difX, difY = checkX - x, checkY - y
            currentLine = []

            RUN = True
            while RUN:
                # Nếu giao với quan đối phương, tức hàng đó có tiềm năng tạo thành 1 bộ, thêm vào curentLine
                if grid[checkX][checkY] == player * -1:
                    currentLine.append((checkX, checkY))
                # Giáp với quân mình, vẫn có thể tạo thành bộ ở phía sau nên break ra check ô tiếp theo
                elif grid[checkX][checkY] == player:
                    RUN = False
                    break
                # Giao với ô trống thì chắc chắn hàng đó không tạo thành bộ, clear currentLine và break
                elif grid[checkX][checkY] == 0:
                    currentLine.clear()
                    RUN = False
                # Check tiếp ở các ô liền kề
                checkX += difX
                checkY += difY

                # Tương tự giao ô trống, ra ngoài biên cũng clear
                if checkX < 0 or checkX > 7 or checkY < 0 or checkY > 7:
                    currentLine.clear()
                    RUN = False

            if len(currentLine) > 0:
                swappableTiles.extend(currentLine)

        return swappableTiles

    def findAvailMoves(self, grid, currentPlayerTurn):
        """Takes the list of validCells and checks each to see if playable"""
        validCells = self.findValidCells(grid, currentPlayerTurn)
        playableCells = []

        for cell in validCells:
            x, y = cell
            if cell in playableCells:
                continue
            swapTiles = self.swappableTiles(x, y, grid, currentPlayerTurn)

            # Nếu nước đi đó có thể lật đc quân đối phương
            if len(swapTiles) > 0:
                playableCells.append(cell)

        return playableCells


    def insertToken(self, grid, curplayer, y, x):
        tokenImage = self.whitetoken if curplayer == 1 else self.blacktoken
        self.tokens[(y, x)] = Token(curplayer, y, x, tokenImage, self.GAME)
        grid[y][x] = self.tokens[(y, x)].player

    def animateTransitions(self, cell, player):
        if player == 1:
            self.tokens[(cell[0], cell[1])].transition(self.transitionWhiteToBlack, self.whitetoken)
        else:
            self.tokens[(cell[0], cell[1])].transition(self.transitionBlackToWhite, self.blacktoken)

    def calculatePlayerScore(self, player):
        score = 0
        for row in self.gridLogic:
            for col in row:
                if col == player:
                    score += 1
        return score

    def drawScore(self, player, score):
        textImg = self.font.render(f'{player} : {score}', 1, 'White')
        return textImg

    def endScreen(self):
        if self.GAME.gameOver:
            endScreenImg = pygame.Surface((320, 320))
            if (self.player1Score > self.player2Score) and  (self.GAME.currentPlayer == 1):
                txt = "Congratulations, You Won!!"
            elif (self.player1Score < self.player2Score) and  (self.GAME.currentPlayer == -1):
                txt = "Congratulations, You Won!!"
            else:
                txt = "Bad Luck, You Lost"
            
            if self.GAME.disconnected == True:
                txt = "Opponent disconnected. You Won!!"
                
            endText = self.font.render(txt, 1, 'White')
            endScreenImg.blit(endText, (0, 0))
            newGame = pygame.draw.rect(endScreenImg, 'White', (80, 160, 160, 80))
            newGameText = self.font.render('Play Again', 1, 'Black')
            endScreenImg.blit(newGameText, (120, 190))
        return endScreenImg

    def drawGrid(self, window):
        window.blit(self.gridBg, (0, 0))

        window.blit(self.drawScore('White', self.player1Score), (900, 100))
        window.blit(self.drawScore('Black', self.player2Score), (900, 200))

        for token in self.tokens.values():
            token.draw(window)

        # Vẽ những bước đi khả thi trên bàn cờ
        availMoves = self.findAvailMoves(self.gridLogic, self.GAME.currentPlayerTurn)
        if self.GAME.currentPlayerTurn == self.GAME.currentPlayer:
            for move in availMoves:
                pygame.draw.rect(window, 'White', (80 + (move[1] * 80) + 30, 80 + (move[0] * 80) + 30, 20, 20))

        if self.GAME.gameOver:
            window.blit(self.endScreen(), (240, 240))

# Class đại diện cho mỗi quân cờ
class Token:
    def __init__(self, player, gridX, gridY, image, main):
        self.player = player
        # Tọa độ ô trên bàn cờ
        self.gridX = gridX
        self.gridY = gridY
        # Tọa độ pixel trên màn hình
        self.posX = 80 + (gridY * 80)
        self.posY = 80 + (gridX * 80)

        self.GAME = main

        self.image = image

    def draw(self, window):
        window.blit(self.image, (self.posX, self.posY))

    def transition(self, transitionImages, tokenImage):
        for i in range(30):
            self.image = transitionImages[i // 10]
            self.GAME.draw()
        self.image = tokenImage

class ComputerPlayer:
    def __init__(self, gridObject):
        self.grid = gridObject

    def computerHard(self, grid, depth, alpha, beta, player):
        # Tạo 1 bản copy của grid hiện tại
        newGrid = copy.deepcopy(grid)
        availMoves = self.grid.findAvailMoves(newGrid, player)

        # Nếu độ sâu AI = 0 hoặc không còn nước nào để đi
        if depth == 0 or len(availMoves) == 0:
            bestMove, Score = None, evaluateBoard(grid, player)
            return bestMove, Score

        if player < 0:	# Quân đen đi sau
            bestScore = -64
            bestMove = None

            for move in availMoves:
                x, y = move
                swappableTiles = self.grid.swappableTiles(x, y, newGrid, player)
                newGrid[x][y] = player
                for tile in swappableTiles:
                    newGrid[tile[0]][tile[1]] = player

                bMove, value = self.computerHard(newGrid, depth-1, alpha, beta, player *-1)
                if value > bestScore:
                    bestScore = value
                    bestMove = move
                alpha = max(alpha, bestScore)
                if beta <= alpha:
                    break

                newGrid = copy.deepcopy(grid)

            return bestMove, bestScore

        if player > 0:	# Quân trắng đi trước
            bestScore = 64
            bestMove = None

            for move in availMoves:
                x, y = move
                swappableTiles = self.grid.swappableTiles(x, y, newGrid, player)
                newGrid[x][y] = player
                for tile in swappableTiles:
                    newGrid[tile[0]][tile[1]] = player

                bMove, value = self.computerHard(newGrid, depth-1, alpha, beta, player)

                if value < bestScore:
                    bestScore = value
                    bestMove = move
                beta = min(beta, bestScore)
                if beta <= alpha:
                    break

            newGrid = copy.deepcopy(grid)
        return bestMove, bestScore


# Main program to run game
if __name__ == "__main__":
    game = Othello()
    game.run()
    pygame.quit()