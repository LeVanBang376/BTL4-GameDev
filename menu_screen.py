import pygame
from room import Room

class MenuScreen:
    def __init__(self, window, font, rooms = [Room(1201, 1), Room(1202, 1) , Room(1203, 2)]):
        self.window = window
        self.font = font
        self.background = pygame.image.load("assets/ReversiImage.jpg")
        self.logo = pygame.image.load("assets/ReversiLogo.png")
        self.menuType = "chooseEnemy"
        self.rooms = rooms
        self.roomButtons = []
        
    def drawEnemyMenu(self):
        self.window.blit(self.background, (0, 0))
        self.window.blit(self.logo, (390, 70))
        
        vs_computuer_button = pygame.Rect((270, 360, 560, 80))  
        pygame.draw.rect(self.window, (159,191,223), vs_computuer_button)
        vs_computuer_text = self.font.render("Vs computer", True, (0, 0, 0))
        vs_computuer_text_center = vs_computuer_text.get_rect(center=(550, 400))
        self.window.blit(vs_computuer_text, vs_computuer_text_center) 
        
        vs_player_button = pygame.Rect((270, 480, 560, 80))  
        pygame.draw.rect(self.window, (159,191,223), vs_player_button)
        vs_player_text = self.font.render("Vs player", True, (0, 0, 0))
        vs_player_text_center = vs_player_text.get_rect(center=(550, 520))
        self.window.blit(vs_player_text, vs_player_text_center) 
        
        # setting_button = pygame.Rect((270, 600, 560, 80))  
        # pygame.draw.rect(self.window, (255, 255, 255), setting_button)
        # setting_text = self.font.render("Setting", True, (0, 0, 0))
        # setting_text_center = setting_text.get_rect(center=(550, 515))
        # self.window.blit(setting_text, setting_text_center) 
        
        exit_button = pygame.Rect((270, 600, 560, 80))  
        pygame.draw.rect(self.window, (159,191,223), exit_button)
        exit_text = self.font.render("Exit", True, (0, 0, 0))
        exit_text_center = exit_text.get_rect(center=(550, 640))
        self.window.blit(exit_text, exit_text_center) 

        pygame.display.flip()
            
        # Wait for a key press to exit
        waiting_for_input = True
        while waiting_for_input:
            # draw border of buttons
            mousePos = pygame.mouse.get_pos()
            if vs_computuer_button.collidepoint(mousePos):
                vs_computuer_btn_border = pygame.Rect((270, 360, 560, 80))  
                pygame.draw.rect(self.window, (0, 0, 0), vs_computuer_btn_border, 3)
            elif vs_player_button.collidepoint(mousePos):
                vs_player_button = pygame.Rect((270, 480, 560, 80))  
                pygame.draw.rect(self.window, (0, 0, 0), vs_player_button, 3)
            elif exit_button.collidepoint(mousePos):
                exit_btn_border = pygame.Rect((270, 600, 560, 80))  
                pygame.draw.rect(self.window, (0, 0, 0), exit_btn_border, 3) 
            else:
                # remove border of buttons by changing border color to (159,191,223)
                vs_computuer_btn_border = pygame.Rect((270, 360, 560, 80))  
                pygame.draw.rect(self.window, (159,191,223), vs_computuer_btn_border, 3)
                
                vs_player_button = pygame.Rect((270, 480, 560, 80))  
                pygame.draw.rect(self.window, (159,191,223), vs_player_button, 3)
                
                exit_btn_border = pygame.Rect((270, 600, 560, 80))  
                pygame.draw.rect(self.window, (159,191,223), exit_btn_border, 3)
            pygame.display.flip()
            
            # get events
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    waiting_for_input = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    print(mouse_pos)
                    if vs_computuer_button.collidepoint(mouse_pos):
                        return "Vs computer"
                    if vs_player_button.collidepoint(mouse_pos):
                        return "Vs player"
                    if exit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        exit()
        return False
    
    def drawDifficultMenu(self):
    # Display the final score
        self.window.blit(self.background, (0, 0))
        self.window.blit(self.logo, (390, 70))
        
        easy_button = pygame.Rect((270, 360, 560, 80))  
        pygame.draw.rect(self.window, (159,191,223), easy_button)
        easy_text = self.font.render("Easy", True, (0, 0, 0))
        easy_text_center = easy_text.get_rect(center=(550, 400))
        self.window.blit(easy_text, easy_text_center) 
        
        hard_button = pygame.Rect((270, 480, 560, 80))  
        pygame.draw.rect(self.window, (159,191,223), hard_button)
        hard_text = self.font.render("Hard", True, (0, 0, 0))
        hard_text_center = hard_text.get_rect(center=(550, 520))
        self.window.blit(hard_text, hard_text_center) 
        
        back_button = pygame.Rect((270, 600, 560, 80))  
        pygame.draw.rect(self.window, (159,191,223), back_button)
        back_text = self.font.render("Back to menu", True, (0, 0, 0))
        back_text_center = back_text.get_rect(center=(550, 640))
        self.window.blit(back_text, back_text_center) 
        

        pygame.display.flip()
            
        # Wait for a key press to exit
        waiting_for_input = True
        while waiting_for_input:
            # draw border of buttons
            mousePos = pygame.mouse.get_pos()
            if easy_button.collidepoint(mousePos):
                easy_btn_border = pygame.Rect((270, 360, 560, 80))  
                pygame.draw.rect(self.window, (0, 0, 0), easy_btn_border, 3)
            elif hard_button.collidepoint(mousePos):
                hard_btn_button = pygame.Rect((270, 480, 560, 80))  
                pygame.draw.rect(self.window, (0, 0, 0), hard_btn_button, 3)
            elif back_button.collidepoint(mousePos):
                back_button_border = pygame.Rect((270, 600, 560, 80))  
                pygame.draw.rect(self.window, (0, 0, 0), back_button_border, 3) 
            else:
                # remove border of buttons by changing border color to (159,191,223)
                easy_btn_border = pygame.Rect((270, 360, 560, 80))  
                pygame.draw.rect(self.window, (159,191,223), easy_btn_border, 3)
                
                hard_btn_button = pygame.Rect((270, 480, 560, 80))  
                pygame.draw.rect(self.window, (159,191,223), hard_btn_button, 3)
                
                back_button_border = pygame.Rect((270, 600, 560, 80))  
                pygame.draw.rect(self.window, (159,191,223), back_button_border, 3)
            pygame.display.flip()
            
            # Get events
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    waiting_for_input = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    if easy_button.collidepoint(mouse_pos):
                        return "Easy"
                    if hard_button.collidepoint(mouse_pos):
                        return "Hard"
                    if back_button.collidepoint(mouse_pos):
                        return "ChooseEnemy"
        return False

    def drawRoom(self, roomId, x, y):
        room_button = pygame.Rect((x, y, 560, 80))  
        pygame.draw.rect(self.window, (159,191,223), room_button)
        room_text = self.font.render(f"Room {roomId}", True, (0, 0, 0))
        room_text_center = room_text.get_rect(center=(550, y + 40))
        self.window.blit(room_text, room_text_center) 
        
        pygame.display.flip()
        
        return room_button
    
    def drawRoomMenu(self):
    # Display the final score
        self.window.blit(self.background, (0, 0))
        
        rooms_container = pygame.Rect((270, 50, 560, 500))  
        pygame.draw.rect(self.window, (255,255,255), rooms_container)
        
        if (len(self.roomButtons) == len(self.rooms)):
            self.roomButtons = []
        startY = 50
        for i in range(0, len(self.rooms)):
            self.roomButtons.append(self.drawRoom(self.rooms[i].roomId, 270, startY + i*90)) 
            
        
        back_button = pygame.Rect((270, 600, 560, 80))  
        pygame.draw.rect(self.window, (159,191,223), back_button)
        back_text = self.font.render("Back to menu", True, (0, 0, 0))
        back_text_center = back_text.get_rect(center=(550, 640))
        self.window.blit(back_text, back_text_center) 
        

        pygame.display.flip()
            
        # Wait for a key press to exit
        waiting_for_input = True
        while waiting_for_input:
            # draw border of buttons
            mousePos = pygame.mouse.get_pos()
            startY = 50
            for i in range(0, len(self.roomButtons)):
                if self.roomButtons[i].collidepoint(mousePos):
                    room_btn_border = pygame.Rect((270, startY + i*90, 560, 80))  
                    pygame.draw.rect(self.window, (0, 0, 0), room_btn_border, 3)
                else:
                    # remove border of buttons by changing border color to (159,191,223)
                    room_btn_border = pygame.Rect((270, startY + i*90, 560, 80))  
                    pygame.draw.rect(self.window, (159,191,223), room_btn_border, 3)
                    
            if back_button.collidepoint(mousePos):
                back_button_border = pygame.Rect((270, 600, 560, 80))  
                pygame.draw.rect(self.window, (0, 0, 0), back_button_border, 3) 
            else:
                # remove border of buttons by changing border color to (159,191,223)         
                back_button_border = pygame.Rect((270, 600, 560, 80))  
                pygame.draw.rect(self.window, (159,191,223), back_button_border, 3)
                
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    waiting_for_input = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    if back_button.collidepoint(mouse_pos):
                        return "ChooseEnemy"
        return False
    
    def drawMenu(self):
        if self.menuType == "chooseEnemy":
            drawEnemyReturn = self.drawEnemyMenu()
            if drawEnemyReturn == "Vs computer":
                self.menuType = "chooseDifficult"
            if drawEnemyReturn == "Vs player":
                self.menuType = "chooseRoom"
            return "showMenu"
        if self.menuType == "chooseDifficult":
            drawDifficultReturn = self.drawDifficultMenu()
            if drawDifficultReturn == "Easy":
                self.menuType = "easy"
                self.difficulty = "easy"
            if drawDifficultReturn == "Hard":
                self.menuType = "hard"
                self.difficulty = "hard"
                
            if drawDifficultReturn == "ChooseEnemy":
                self.menuType = "chooseEnemy"
                return "showMenu"
            return "notShowMenu"
        if self.menuType == "chooseRoom":
            # drawRoomReturn = self.drawRoomMenu()
            # # if drawDifficultReturn == "Easy":
            # #     self.menuType = "chooseDifficult"
            # if drawRoomReturn == "ChooseEnemy":
            #     self.menuType = "chooseEnemy"
            #     return "showMenu"
            return "notShowMenu"