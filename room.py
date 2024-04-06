class Room:
    def __init__(self, roomId, currentPlayersNumber):
        self.roomId = roomId
        self.currentPlayersNumber = currentPlayersNumber
        
    def setCurrentPlayersNumber(self, newCurrentPlayersNumber):
        self.currentPlayersNumber = newCurrentPlayersNumber
    
    