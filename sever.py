import socket
from _thread import *

# return array of cells available around the current cell
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

class Grid:
    # Số row, column, size là kích thước của mỗi ô cờ
    def __init__(self, rows = 8, columns = 8, size = (80, 80), main = 0):
        # self.GAME = main
        self.rows = rows
        self.columns = columns
        # self.size = size

        # self.whitetoken = loadImages("assets/WhiteToken.png", size)
        # self.blacktoken = loadImages("assets/BlackToken.png", size)
        # self.transitionWhiteToBlack = [loadImages(f"assets/WhiteToBlack{i}.png", size) for i in range(1, 4)]
        # self.transitionBlackToWhite = [loadImages(f"assets/BlackToWhite{i}.png", size) for i in range(1, 4)]

        # self.bg = self.loadBackGroundImages()
        # self.gridBg = self.createbgimg()

        # self.player1Score = 0
        # self.player2Score = 0

        # List các quân cờ đang nằm trên bàn
        # self.tokens = {}

        # self.font = pygame.font.SysFont('Arial', 20, True, False)

        self.gridLogic = self.regenLogic(self.rows, self.columns)

    def newGame(self):
        # self.tokens.clear()
        self.gridLogic = self.regenLogic(self.columns, self.rows)

    # def loadBackGroundImages(self):
    #     alpha = "ABCDEFGHI"
    #     spriteSheet = pygame.image.load("assets/wood.png").convert_alpha()
    #     imageDict = {}
    #     for i in range(3):
    #         for j in range(7):
    #             imageDict[alpha[j] + str(i)] = loadSpriteSheet(spriteSheet, j, i, (self.size), (32, 32))
    #     return imageDict

    # def createbgimg(self):
    #     """Tạo background image cho bàn cờ"""
    #     gridBg = [
    #         ['C0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'E0'],
    #         ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
    #         ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
    #         ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
    #         ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
    #         ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
    #         ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
    #         ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
    #         ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
    #         ['C2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'E2'],
    #     ]
    #     image = pygame.Surface((960, 960))
    #     for j, row in enumerate(gridBg):
    #         for i, img in enumerate(row):
    #             image.blit(self.bg[img], (i * self.size[0], j * self.size[1]))
    #     return image

    def regenLogic(self, rows, columns):
        """Generate an empty grid for logic use"""
        grid = []
        for y in range(rows):
            line = []
            for x in range(columns):
                line.append(0)
            grid.append(line)
        grid[3][3] = 1
        grid[4][4] = 1
        grid[3][4] = -1
        grid[4][3] = -1
        # self.insertToken(grid, 1, 3, 3)
        # self.insertToken(grid, -1, 3, 4)
        # self.insertToken(grid, 1, 4, 4)
        # self.insertToken(grid, -1, 4, 3)

        return grid

    # def printGameLogicBoard(self):
    #     print(" | A | B | C | D | E | F | G | H |")
    #     for i, row in enumerate(self.gridLogic):
    #         line = f"{i} |".ljust(3, " ")
    #         for item in row:
    #             line += f"{item}".center(3, " ") + "|"
    #         print(line)
    #     print()

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

    # Return a list of all tiles that can be swapped
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

    #Return a list of all available moves for the current player
    def findAvailMoves(self, grid, currentPlayer):
        """Takes the list of validCells and checks each to see if playable"""
        validCells = self.findValidCells(grid, currentPlayer)
        playableCells = []

        for cell in validCells:
            x, y = cell
            if cell in playableCells:
                continue
            swapTiles = self.swappableTiles(x, y, grid, currentPlayer)

            # Nếu nước đi đó có thể lật đc quân đối phương
            if len(swapTiles) > 0:
                playableCells.append(cell)

        return playableCells


    # def insertToken(self, grid, curplayer, y, x):
    #     tokenImage = self.whitetoken if curplayer == 1 else self.blacktoken
    #     self.tokens[(y, x)] = Token(curplayer, y, x, tokenImage, self.GAME)
    #     grid[y][x] = self.tokens[(y, x)].player

    # def animateTransitions(self, cell, player):
    #     if player == 1:
    #         self.tokens[(cell[0], cell[1])].transition(self.transitionWhiteToBlack, self.whitetoken)
    #     else:
    #         self.tokens[(cell[0], cell[1])].transition(self.transitionBlackToWhite, self.blacktoken)

    def calculatePlayerScore(self, player):
        score = 0
        for row in self.gridLogic:
            for col in row:
                if col == player:
                    score += 1
        return score

    # def drawScore(self, player, score):
    #     textImg = self.font.render(f'{player} : {score}', 1, 'White')
    #     return textImg

    # def endScreen(self):
    #     if self.GAME.gameOver:
    #         endScreenImg = pygame.Surface((320, 320))
    #         endText = self.font.render(f'{"Congratulations, You Won!!" if self.player1Score > self.player2Score else "Bad Luck, You Lost"}', 1, 'White')
    #         endScreenImg.blit(endText, (0, 0))
    #         newGame = pygame.draw.rect(endScreenImg, 'White', (80, 160, 160, 80))
    #         newGameText = self.font.render('Play Again', 1, 'Black')
    #         endScreenImg.blit(newGameText, (120, 190))
    #     return endScreenImg

    # def drawGrid(self, window):
    #     window.blit(self.gridBg, (0, 0))

    #     window.blit(self.drawScore('White', self.player1Score), (900, 100))
    #     window.blit(self.drawScore('Black', self.player2Score), (900, 200))

    #     for token in self.tokens.values():
    #         token.draw(window)

    #     # Vẽ những bước đi khả thi trên bàn cờ
    #     availMoves = self.findAvailMoves(self.gridLogic, self.GAME.currentPlayer)
    #     if self.GAME.currentPlayer == 1:
    #         for move in availMoves:
    #             pygame.draw.rect(window, 'White', (80 + (move[1] * 80) + 30, 80 + (move[0] * 80) + 30, 20, 20))

    #     if self.GAME.gameOver:
    #         window.blit(self.endScreen(), (240, 240))

# Class đại diện cho mỗi quân cờ
class Token:
    def __init__(self, player: int, gridX: int, gridY: int, image = 0, main = 0):
        self.player = player
        # Tọa độ ô trên bàn cờ
        self.gridX = gridX
        self.gridY = gridY
        # Tọa độ pixel trên màn hình
        # self.posX = 80 + (gridY * 80)
        # self.posY = 80 + (gridX * 80)

        # self.GAME = main

        # self.image = image

    # def draw(self, window):
    #     window.blit(self.image, (self.posX, self.posY))

    # def transition(self, transitionImages, tokenImage):
    #     for i in range(30):
    #         self.image = transitionImages[i // 10]
    #         self.GAME.draw()
    #     self.image = tokenImage


class Server:

    def __init__(self):
        
        self.ip = str(input("Ip (default: 127.0.0.1): "))
        if self.ip == "":
            self.ip = "127.0.0.1"

        self.port = str(input("Port (default: 8080): "))
        if self.port == "":
            self.port = 8080
        self.port = int(self.port)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind((self.ip, self.port))
        except socket.error as e:
            print(e)

        self.server.listen(2)
        print(f"Server started at {self.ip}:{self.port}")

        self.playercount = 0

        # self.grid = [
        #     ['', '', '', '', '', '', '', ''],
        #     ['', '', '', '', '', '', '', ''],
        #     ['', '', '', '', '', '', '', ''],
        #     ['', '', '', 'w', 'b', '', '', ''],
        #     ['', '', '', 'b', 'w', '', '', ''],
        #     ['', '', '', '', '', '', '', ''],
        #     ['', '', '', '', '', '', '', ''],
        #     ['', '', '', '', '', '', '', ''],
        # ]
        self.grid = Grid()
        self.playerTurn = 1
        self.whiteCount = 0,
        self.blackCount = 0,
        self.win = 0


    def clientConn(self, conn, addr):
        self.playercount += 1
        playerNB = str(self.playercount)
        conn.send(str.encode(playerNB))
        reply = ""

        while True:
            try:
                recvData = conn.recv(2048).decode()
                if not recvData:
                    print("Client", addr, ": Disconnected")
                else:
                    
                    self.getData(recvData)
                    self.win = self.checkWin()
                    sendData = str(self.makeData(self.playerTurn, self.grid.gridLogic, (self.win)))
                    reply = str.encode(sendData)

                conn.sendall(reply)

            except:
                print("Lost Connection")
                break
        
        self.playercount -= 1


    def getData(self, data):
        if self.win == 0:
            tmp = eval(data)
            if tmp[0] == [-1, -1]:
                pass
            else:
                playerNB = tmp[1]
                pos = tmp[0]
                if self.grid.gridLogic[pos[0]][pos[1]] == 0:
                    availMoves = self.grid.findAvailMoves(self.grid.gridLogic, playerNB)
                    print('availbleMove: ', availMoves)
                    flag = False
                    for move in availMoves:
                        if pos[0] == move[0] and pos[1] == move[1]:
                            flag = True
                            break
                    if not flag:
                        return
                    self.grid.gridLogic[pos[0]][pos[1]] = playerNB
                    cells = self.grid.swappableTiles(pos[0], pos[1], self.grid.gridLogic, playerNB)
                    for cell in cells:
                        self.grid.gridLogic[cell[0]][cell[1]] = playerNB
                        print(self.grid.gridLogic[0])
                        print(self.grid.gridLogic[1])
                        print(self.grid.gridLogic[2])
                        print(self.grid.gridLogic[3])
                        print(self.grid.gridLogic[4])
                        print(self.grid.gridLogic[5])
                        print(self.grid.gridLogic[6])
                        print(self.grid.gridLogic[7])
                    self.playerTurn *= -1


    def makeData(self, playerTurn, grid, win):
        data = [playerTurn, grid, win]
        return data
        

    def checkWinOld(self):
        for player in range(1, 3):
            #check rows
            p = str(player)
            for r in range(3):
                win = p
                for c in range(3):
                    if self.grid[r][c] != p:
                        win = ''
                if win:
                    return win
            #check columns
            for c in range(3):
                win = p
                for r in range(3):
                    if self.grid[r][c] != p:
                        win = ''
                if win:
                    return win
            
            #check diagonals
            win = p
            for i in range(3):
                if self.grid[i][i] != p:
                    win = ''
            if win:
                return win
            
            win = p
            for i in range(3):
                if self.grid[i][2-i] != p:
                    win = ''
            if win:
                return win

        win = 't'
        for c in range(3):
            for r in range(3):
                if self.grid[c][r] == '':
                    win = ''
        if win:
            return win

        return ''

    def checkWin(self):
        if len(self.grid.findAvailMoves(self.grid.gridLogic, self.playerTurn)) == 0:
            self.blackCount, self.whiteCount = self.countBlackWhite()
            if self.blackCount < self.whiteCount:
              return 1
            elif self.whiteCount > self.blackCount:
                return -1
            else:
                return 2
        return 0
        
    
    def countBlackWhite(self):
        blackCount = 0
        whiteCount = 0
        for c in range(8):
            for r in range(8):
                if self.grid.gridLogic[c][r] == -1:
                    blackCount += 1
                elif self.grid.gridLogic[c][r] == 1:
                    whiteCount += 1
        return blackCount, whiteCount

    def run(self):

        while True:
            #wait until a connection is etablished
            conn, addr = self.server.accept()
            print("Client Connected:", addr)

            if self.playercount == 0:
                self.grid = Grid()
                self.playerTurn = 1
                self.win = 0

            #start async connection for client
            start_new_thread(self.clientConn, (conn, addr))


server = Server()
server.run()