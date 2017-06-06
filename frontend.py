from appJar import gui
from backend import *
from threading import Thread

# UI WINDOW
class Window:
    def __init__(self, game):
        self.game = game
        self.app = None
        self.turn = 'R'
        self.UI()

    # HORRIBLE UI, IDC
    def UI(self):
        self.app = gui("NIM", "800x600")
        self.board()

        self.app.addButton("Start", self.makeMove)
        self.app.addLabel("winner")
        self.app.go()

    # ACTUAL GAMEPLAY
    def Play(self):
        # TO DO: make this work
        board = self.game.board.boxes
        turn = 'R'
        winner = self.game.checkWinLose(board, turn)

        while winner == 'Continue':
            if self.makeMove("Start") is False:
                return 'Blue Win'
            if turn == 'R':
                turn = 'B'
            else:
                turn = 'R'
            winner = self.game.checkWinLose(self.game.board.boxes, turn)
        print(winner)
        return winner

    # FROM OLD IDEA, COULD BE USEFULL TO NOT GIVE INPUT VIA TERMINAL
    def getPlayerBoxes(self):
        possibilites = self.game.getPlayerPossbilities(self.game.board.boxes)
        self.app.addListBox("Player Boxes: ")
        for i in possibilites:
            self.app.addListItem("Player Boxes: ", i)

    # BOARD WITH BOXES
    def board(self):
        self.app.setBg("lightGrey")

        j = 0
        for i in self.game.board.boxes:
            if i == 'w':
                self.app.addLabel("label" + str(j), 'w', 0, j)
                self.app.setLabelBg("label" + str(j), 'White')
                self.app.setLabelWidth("label" + str(j), 0)
            elif i == 'R':
                self.app.addLabel("label" + str(j), 'R', 0, j)
                self.app.setLabelBg("label" + str(j), 'Red')
                self.app.setLabelWidth("label" + str(j), 0)
            else:
                self.app.addLabel("label" + str(j), 'B', 0, j)
                self.app.setLabelBg("label" + str(j), 'Blue')
                self.app.setLabelWidth("label" + str(j), 0)
            j += 1

    # UPDATE BOARD WITH EVERY MOVE
    def newBoard(self):
        j = 0
        for i in self.game.board.boxes:
            if i == 'w':
                self.app.setLabel("label" + str(j), 'w')
                self.app.setLabelBg("label" + str(j), 'White')
                self.app.setLabelWidth("label" + str(j), 0)
            elif i == 'R':
                self.app.setLabel("label" + str(j), 'R')
                self.app.setLabelBg("label" + str(j), 'Red')
                self.app.setLabelWidth("label" + str(j), 0)
            else:
                self.app.setLabel("label" + str(j), 'B')
                self.app.setLabelBg("label" + str(j), 'Blue')
                self.app.setLabelWidth("label" + str(j), 0)
            j += 1

    # MAKE PLAYER (BLUE) MOVE
    def makeMove(self, name):

        board = self.game.board.boxes
        j = 0
        thread = Thread(target=self.game.StrategicTurn, args=[board, self.turn])
        t = thread.run()
        if t == False:
            return 'Blue Win'
        if self.turn == 'R':
            self.turn = 'B'
        else:
            self.turn = 'R'
        winner = self.game.checkWinLose(self.game.board.boxes, self.turn)
        self.newBoard()
        j+= 1
        self.app.setLabel("winner", winner)

    # CREATE BUTTON TO START GAME; NOTE: BAD FUNCTION NAME
    def playerMove(self):
        self.app.addButton("Start", self.makeMove)

b = Board(3, 11)
g = Game(b)
w = Window(g)