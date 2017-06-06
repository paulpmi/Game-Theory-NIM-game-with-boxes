from random import randint
from copy import deepcopy
from operator import xor

# BOARD FOR THE GAME
class Board:
    def __init__(self, n, k):
        self.k = k
        self.n = n
        self.boxes = ['w' for _ in range(k)]
        self.createState()
        # tests
        #self.boxes = ['R', 'B', 'R', 'B', 'w', 'w', 'w', 'R', 'B', 'R', 'B', 'w', 'w', 'w', 'w']
        #self.boxes = ['R', 'B', 'R', 'B', 'w', 'w', 'w', 'R', 'w', 'w', 'B'] best used for testing
        #self.boxes = ['R', 'B', 'w', 'R', 'w', 'B', 'w']
        #self.boxes = ['R', 'B', 'w', 'R', 'B']

    # CREATE A RANDOM STATE WITH BOXES; BOXES ARE ALWAYS ARRANGED ACCORDING TO THE RULES
    def createState(self):
        # TO DO: make creation consistent
        last =0
        lastPos = 0
        for i in range(0, self.n*2):
            newPos = randint(lastPos + 1, lastPos + 2)
            while newPos > self.k:
                newPos = randint(lastPos+1, lastPos+2)
            if last == 0:
                self.boxes[newPos] = 'R'
                last = 1
                lastPos = newPos
            else:
                self.boxes[newPos] = 'B'
                last = 0
                lastPos = newPos
        print(self.boxes)
    # NOTE: SOMETIMES THE INDEX GOES OUT OF THE BOARD JUST RETRYING WORKS


# OLD IMPLEMENTATION PRESERVED BECAUSE I WANT TO
class LegacyGame:
    def findPlayerSolutions(self, board):
        # TO DO: Check for different solution using the formula of NIM found in course (pg 33)
        possibles, TUP = self.getPossibleMoves(board, 'R')
        bestBoard = None
        min = 999
        for boardStates in possibles:
            fitness = 0
            for i in range(len(boardStates)-1):
                j = i + 1
                while j < len(boardStates) and boardStates[j] != 'R':
                    j += 1
                fitness += j - i
            if fitness < min:
                bestBoard = boardStates

        return bestBoard

    def checkPossibleMove(self, initial, board):
        l = []
        i = initial+1
        rightPossibilites = 0
        while i < len(board) and board[i] != 'B' and board[i] != 'R':
            #print(i)
            rightPossibilites += 1
            l.append(initial + rightPossibilites)
            i += 1

        i = initial-1
        leftPossibilites = 0
        while board[i] != 'B' and board[i] != 'R' and i > -1:
            leftPossibilites -= 1
            l.append(initial + leftPossibilites)
            i -= 1

        return l

    # OLD WAY USING PARITY STRATEGY; LEAD TO BAD MOVES AND NO STRATEGIC THOUGHT
    def makeBestMove(self, board):
        positions = []
        length = []
        lastPosition = -1
        for i in range(len(self.board.boxes)):
            if self.board.boxes[i] == 'R':
                positions.append(i)
                length.append(i-lastPosition-1)
                lastPosition = i
            if self.board.boxes[i] == 'B':
                length.append(i - lastPosition-1)
                lastPosition = i

        nimSum = length[0] + length[1]
        for i in range(2, len(length)-1):
            nimSum = xor(nimSum, length[i]+length[i+1])
        intNimSum = int(nimSum)

        change = None
        for i in range(0, len(length), 2):
            if length[i] != 0 or length[i+1] != 0:
                if length[i] > length[i +1]:
                    print(length[i]+length[i+1], ' sum vs xor ', xor(length[i]+length[i+1], intNimSum))
                    if (length[i]+length[i+1]) <= xor(length[i]+length[i+1], intNimSum):
                        change = i
                else:
                    if (length[i]+length[i+1]) >= xor(length[i]+length[i+1], intNimSum):
                        change = i
        if change == None:
            for i in range(0, len(length)):
                if length[i] != 0:
                    change = i
                    break
        print(change, ' ', length)
        self.board.boxes[positions[int(change/2)]] = 'w'
        if length[change] < length[change+1]:
            self.board.boxes[positions[int(change/2)] + length[change+1]] = 'R'
        else:
            self.board.boxes[positions[int(change/2)] - length[change]] = 'R'

        return self.board.boxes

    def getPossibleMoves(self, board, turn):

        if turn =='R':
            l = self.getComputerPossibilites(board)

            phases = []

            for i in l:
                possibles = self.checkPossibleMove(i, board)
                for j in possibles:
                    possibleBoard = deepcopy(board)
                    possibleBoard[i] = 'w'
                    possibleBoard[j] = 'R'
                    phases.append(possibleBoard)

            turn = 'B'
            return phases, turn

    def checkMove(self, initial, final, board):

        if board[final] == 'B' or board[final] == 'R':
            return False

        if initial < final:
            for i in range(initial+1, final):
                if board[i] == 'R' or board[i] == 'B':
                    return False
            return True
        else:
            for i in range(final, initial):
                if board[i] == 'R' or board[i] == 'B':
                    return False
            return True

    def Turn(self, board, turn):
        board = self.board.boxes
        if turn == 'R':
            print("RED TURN")
            initial = deepcopy(self.board.boxes)
            print(initial, " Initial")
            best = self.makeBestMove(board)
            print(self.board.boxes, ' Final')
            self.moves.append(self.board.boxes)

            if initial == self.board.boxes:
                return False
        else:
            print("BLUE TURN")
            self.playerMove()
            self.moves.append(self.board.boxes)

    def Play(self):
        board = self.board.boxes
        turn = 'R'
        winner = self.checkWinLose(board, turn)

        while winner == 'Continue':
            t = self.Turn(self.board.boxes, turn)
            if t == False:
                return 'Blue Win'
            if turn == 'R':
                turn = 'B'
            else:
                turn = 'R'
            winner = self.checkWinLose(self.board.boxes, turn)
        print(winner)
        return winner


# ACTUAL IMPLEMENTATION
class Game:
    def __init__(self, b):
        self.board = b
        self.moves = deepcopy(b.boxes)

    # GET WHERE RED BOXES ARE
    def getComputerPossibilites(self, board):
        l = []
        for i in range(len(board)):
            if board[i] == 'R':
                l.append(i)
        return l

    # GET WHERE BLUE BOXES ARE
    def getPlayerPossbilities(self, board):
        l = []
        for i in range(len(board)):
            if board[i] == 'B':
              l.append(i)
        return l

    # CHECK IF SOMEONE WON THE GAME
    def checkWinLose(self, board, turn):
        playerPos = self.getPlayerPossbilities(board)
        computerPos = self.getComputerPossibilites(board)

        print(turn, 'Turn')
        if turn == 'R':
            lost = True
            for i in range(len(self.board.boxes)-1):
                if i != 0:
                    if self.board.boxes[i] == 'R' and (self.board.boxes[i-1] != 'B' or self.board.boxes[i+1] != 'B'):
                        lost = False
                else:
                    if self.board.boxes[0] == 'R' and self.board.boxes[1] != 'B':
                        lost = False
            if lost == True:
                return 'Blue Wins'
        if turn == 'B':
            lost = True
            for i in range(len(self.board.boxes)):
                if i != len(self.board.boxes)-1:
                    if self.board.boxes[i] == 'B' and (self.board.boxes[i-1] != 'R' or self.board.boxes[i+1] != 'R'):
                        lost = False
                else:
                    if self.board.boxes[i] == 'B' and self.board.boxes[i - 1] != 'R':
                        lost = False
            if lost == True:
                return 'Red Wins'
        return 'Continue'

    # CHECKS IF BLUEs BOX MOVEMENT IS CORRECT
    def checkMove(self, initial, final, board):

        if board[final] == 'B' or board[final] == 'R':
            return False

        if initial < final:
            for i in range(initial+1, final):
                if board[i] == 'R' or board[i] == 'B':
                    return False
            return True
        else:
            for i in range(final, initial):
                if board[i] == 'R' or board[i] == 'B':
                    return False
            return True

    # GET ALL MOVEMENT FROM THE KEYBOARD
    def starter(self):
        possibleMoves = self.getPlayerPossbilities(self.board.boxes)
        print(possibleMoves)


        print("Choose your stone: ", end=' ')
        chosenStone = int(input())

        while chosenStone not in possibleMoves:
            print("Unacceptable TARGET")
            print(possibleMoves)
            print("Choose your stone: ", end=' ')
            chosenStone = int(input())

        print("Make your move: ", end=' ')
        chosenPosition = int(input())

        while chosenPosition > len(self.board.boxes) or chosenPosition < 0 or chosenPosition == chosenStone:
            print("Impossible MOVE")
            print(self.board.boxes)
            print("Make your move: ", end=' ')
            chosenPosition = int(input())

        validity = self.checkMove(chosenStone, chosenPosition, self.board.boxes)
        return validity, chosenStone, chosenPosition

    # IF EVERYTHING IS OK MAKE THE MOVE
    def playerMove(self):

        validity, chosenStone, chosenPosition = self.starter()
        while validity != True:
            print("UNACCEPTABLE MOVE")
            validity, chosenStone, chosenPosition = self.starter()

        self.board.boxes[chosenStone] = 'w'
        self.board.boxes[chosenPosition] = 'B'
        print(self.board.boxes)

    # GET ALL THE MOVES OF A POSITION LEFT AND RIGHT
    def getMoves(self, position, board):
        j = position - 1
        i = position + 1

        right = []
        while i < len(board):
            if board[i] == 'w':
                right.append(i)
            else:
                break
            i+=1

        left = []
        while 0 <= j:
            if board[j] == 'w':
                left.append(j)
            else:
                break
            j-=1
        return left, right

    # CHECK IF WE LEAVE THE BOARD IN A STABLE STATE
    def checkStability(self, board, left, right, position):
        if right == []:
            board[position-1] = 'R'
            board[position] = 'w'
        else:
            board[max(right)] = 'R'
            board[position] = 'w'
        return board

    # CHECK OF WE LEAVE THE BOARD IN AN UNSTABLE STATE
    def checkStabilityBlue(self, board, left, right, position):
        if right == []:
            board[max(left)] = 'B'
            board[position] = 'w'
        else:
            board[position-1] = 'B'
            board[position] = 'w'
        return board

    # THIS IS THE ACTUAL FUNCTION WE USE TO PLAY; IT USES THE MINMAX WITH PARITY STRATEGY TO FIND THE BEST POSSIBLE SOLUTION
    def minMaxStrategy(self, board, turn, winLose, win, route):
        if win == 1:
            print(route, win)
            return route, win

        if turn == 'R':
            redpossibleBoards = []
            for j in board:
                positionRed = self.getComputerPossibilites(j)
                for i in positionRed:
                    left, right = self.getMoves(i, j)
                    if left == right == []:
                        winLose = True
                    else:
                        redpossibleBoards.append(self.checkStability(j, left,right,i))
                        route.append(self.getComputerPossibilites(j))
                        winLose = False
            if redpossibleBoards == []:
                return self.minMaxStrategy(redpossibleBoards, 'B', winLose, -1, route)
            else:
                return self.minMaxStrategy(redpossibleBoards, 'B', winLose, -1, route)
        else:
            bluepossibleBoards = []
            for j in board:
                positionBlue = self.getPlayerPossbilities(j)
                for i in positionBlue:
                    left, right = self.getMoves(i, j)
                    if left == right == []:
                        winLose = False
                    else:
                        bluepossibleBoards.append(self.checkStabilityBlue(j, left, right, i))
                        winLose = True
            if bluepossibleBoards == []:
                return self.minMaxStrategy(bluepossibleBoards, 'R', winLose, 1, route)
            else:
                return self.minMaxStrategy(bluepossibleBoards, 'R', winLose, -1, route)
    # NOTE: THIS DOES NOT OPTIMIZE BETWEEN BEST MOVES AND MAY LEAD TO EXTENSIVE GAMES DUE TO THAT

    # MAKE ONE SINGLE PLANNED MOVE
    def makeStrategicMove(self, turn):
        board = deepcopy(self.board.boxes)
        howToWin, win = self.minMaxStrategy([board], turn, True, 0, [self.getComputerPossibilites(self.board.boxes)])
        for i in range(len(howToWin)-1):
            for j in range(len(howToWin[0])):
                if howToWin[i][j] != howToWin[i+1][j]:
                    print("eere")
                    initialPos, finalPos = howToWin[i][j], howToWin[i+1][j]
                    self.board.boxes[initialPos] = 'w'
                    self.board.boxes[finalPos] = 'R'
                    return True
        return False

    # TURN
    def StrategicTurn(self, board, turn):
        board = self.board.boxes
        if turn == 'R':
            print("RED TURN")
            initial = deepcopy(self.board.boxes)
            print(initial, " Initial")
            best = self.makeStrategicMove(turn)
            print(self.board.boxes, ' Final')
            self.moves.append(self.board.boxes)

            if initial == self.board.boxes:
                return False
        else:
            print("BLUE TURN")
            self.playerMove()
            self.moves.append(self.board.boxes)

    # ACTUAL GAMEPLAY
    def StrategicPlay(self):
        board = self.board.boxes
        turn = 'R'
        winner = self.checkWinLose(board, turn)

        while winner == 'Continue':
            t = self.StrategicTurn(self.board.boxes, turn)
            if t == False:
                return 'Blue Win'
            if turn == 'R':
                turn = 'B'
            else:
                turn = 'R'
            winner = self.checkWinLose(self.board.boxes, turn)
        print(winner)
        return winner
