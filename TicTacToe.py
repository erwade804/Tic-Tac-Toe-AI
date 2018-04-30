import math  # imports used in this game
import random
import pygame

WINFRAME = 60  # used for graphics
winFrameCount = 60


class Point:  # used in the AI class
    board = 0  # a board to calculate the distance between another board
    label = 0  # to show what move the point was made on
    moveNum = 0

    def __init__(self, board_, label_, moveNum_):  # sets board and label
        self.board = board_
        self.label = label_
        self.moveNum = moveNum_

    def getInvertedPoint(self):  # invert the board from x's to o's and o's to x's
        if self.board.board[self.label] == "o":
            self.board.board[self.label] = "x"
        else:
            self.board.board[self.label] = "o"
        return self

    def getDist(self, newPoint):  # gets the distance between two boards
        dist = 0
        newBoard = newPoint.getBoard()
        if type(newBoard) == Board:
            newBoard = newBoard.getBoard()
        for i in range(len(newBoard)):  # sets the value of the board for the AI's to see
            if self.board[i] == " ":
                a = 0
            elif self.board[i] == "x":
                a = 1
            else:
                a = -1
            if newBoard[i] == " ":
                b = 0
            elif newBoard[i] == "x":
                b = 1
            else:
                b = -1
            dist += (a - b)**2
        dist += (self.moveNum - newPoint.moveNum)**2
        if self.moveNum < newPoint.moveNum:
            dist += 3
        dist = abs(dist)
        dist = math.sqrt(dist)
        return dist

    def getLabel(self):  # returns the label associated with the board
        return self.label

    def getBoard(self):  # returns the array of the board
        return self.board

    def setOption(self, option):
        newBoard = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
        for i in range(9):
            if type(self.board) == Board:
                if self.board.getBoard()[i] == option:
                    newBoard[i] = option
            else:
                if self.board[i] == option:
                    newBoard[i] = option
        newPoint = Point(newBoard, self.label, self.moveNum)
        return newPoint

    def getRotation(self, degree):  # used to have more info on each board
        if degree == 0:
            return self
        if degree == 1:  # rotates 90 degrees
            pointA = Point([self.board[2], self.board[5], self.board[8], self.board[1], self.board[4], self.board[7], self.board[0], self.board[3], self.board[6]], self.getLabel(), self.moveNum)
            return pointA
        elif degree == 2:  # rotates 180 degrees
            pointA = Point([self.board[8], self.board[7], self.board[6], self.board[5], self.board[4], self.board[3], self.board[2], self.board[1], self.board[0]], self.getLabel(), self.moveNum)
            return pointA
        elif degree == 3:  # reflected across the Y axis
            pointA = Point([self.board[2], self.board[1], self.board[0], self.board[5], self.board[4], self.board[3], self.board[8], self.board[7], self.board[6]], self.getLabel(), self.moveNum)
            return pointA
        elif degree == 4:  # reflected across the X axis
            pointA = Point([self.board[6], self.board[7], self.board[8], self.board[3], self.board[4], self.board[5], self.board[0], self.board[1], self.board[2]], self.getLabel(), self.moveNum)
            return pointA
        else:  # rotates 270 degrees
            pointA = Point([self.board[6], self.board[3], self.board[0], self.board[7], self.board[4], self.board[1], self.board[8], self.board[5], self.board[2]], self.getLabel(), self.moveNum)
            return pointA


class AI:

    def __init__(self):  # sets a standard board with 1 filled in, with a label for the move
        self.winningPoints = []
        self.point = Point([0, 0, 0, 0, 0, 0, 0, 0, 0], -1, 0)  # show where the board is at
        self.lastPoint = 0
        self.allPoints = []
        self.allPoints.append(Point([1, 0, 0, 0, 0, 0, 0, 0, 0], 0, 1))  # nine starting positions for the ai to chose from
        self.allPoints.append(Point([0, 1, 0, 0, 0, 0, 0, 0, 0], 1, 1))
        self.allPoints.append(Point([0, 0, 1, 0, 0, 0, 0, 0, 0], 2, 1))
        self.allPoints.append(Point([0, 0, 0, 1, 0, 0, 0, 0, 0], 3, 1))
        self.allPoints.append(Point([0, 0, 0, 0, 1, 0, 0, 0, 0], 4, 1))
        self.allPoints.append(Point([0, 0, 0, 0, 0, 1, 0, 0, 0], 5, 1))
        self.allPoints.append(Point([0, 0, 0, 0, 0, 0, 1, 0, 0], 6, 1))
        self.allPoints.append(Point([0, 0, 0, 0, 0, 0, 0, 1, 0], 7, 1))
        self.allPoints.append(Point([0, 0, 0, 0, 0, 0, 0, 0, 1], 8, 1))

    def getMoveNum(self, noMove):  # gets a move from the games it has won, or one of the default
        if noMove == [0, 1, 2, 3, 4, 5, 6, 7, 8]:  # returns that the board is full
            return -1
        closestDist = 9999999999999  # farther than all possible points
        lis = [self.allPoints[0]]  # to show all closest points
        for i in range(len(self.allPoints)):
            for j in range(0, 6):
                validPoint = self.allPoints[i].getRotation(j)
                if not (validPoint.getLabel() in noMove):  # if it is not on the board
                    a = random.random()  # for use later
                    if a > 0:  # has a chance to fail and not use the point
                        if closestDist > self.point.getDist(validPoint):
                            closestDist = self.point.getDist(validPoint)
                            lis = [validPoint]
                        elif self.point.getDist(validPoint) == closestDist:
                            lis.append(validPoint)
        a = random.choice(lis)  # make a random move based off of winning and distance
        self.lastPoint = a  # set the last point to the move
        return self.lastPoint.getLabel()  # return the "best" (not necessarily the best move) position

    def setPoint(self, board, label):  # used for class functionality, not user functionality
        self.point = Point(board, label)

    def addPoint(self, point):  # adds a point for the AI to use later
        if points is Point:
            self.allPoints.append(point)

    def getLastPoint(self):  # gets the last point that the board had
        return self.lastPoint

    def addWinPoint(self, point):
        self.winningPoints.append(point)

    def getRandomMove(self, noMove):
        if noMove == [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            return -1
        possibleMove = []
        print(noMove)
        for i in range(9):
            if i not in noMove:
                possibleMove.append(i)
        return random.choice(possibleMove)


class Board:
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    player = "o"

    def __init__(self):  # board and player setup
        self.board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
        self.player = "x"

    def move(self, k):  # moves on a board if you can
        if self.board[k] == " ":
            self.board[k] = self.player
            self.swapPlayer()

    def getMoveNum(self):
        total = 0
        for i in self.board:
            if i != 0:
                total += 1
        return total

    def getBoard(self, option=""):  # returns the board array
        if option == "":
            return self.board
        else:
            newboard = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
            for i in range(len(self.board)):
                if self.board[i] == option:
                    newboard[i] = option
            return newboard

    def getInvertBoard(self):  # gets an inverted board
        newBoard = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(len(self.board)):
            if self.board[i] == "o":
                newBoard[i] = "x"
            elif self.board[i] == "x":
                newBoard[i] = "o"
            else:
                newBoard[i] = " "
        return newBoard

    def swapPlayer(self):  # swaps who is playing
        if self.player == "x":
            self.player = "o"
        else:
            self.player = "x"

    def boardWin(self):  # tests to see if the board has a winning position
        # true means there is a winner, false means there is not a winner
        if self.getWin(0, 1, 2):
            return True, self.board[0]
        if self.getWin(3, 4, 5):
            return True, self.board[3]
        if self.getWin(6, 7, 8):
            return True, self.board[8]
        if self.getWin(0, 4, 8):
            return True, self.board[4]
        if self.getWin(2, 4, 6):
            return True, self.board[2]
        if self.getWin(0, 3, 6):
            return True, self.board[3]
        if self.getWin(1, 4, 7):
            return True, self.board[1]
        if self.getWin(2, 5, 8):
            return True, self.board[2]
        for i in range(len(self.board)):  # checks if the board is full or not
            if self.board[i] == " ":
                break
            elif i == len(self.board)-1:
                return True, " "
        return False, " "

    def getWin(self, a, b, c):  # if these points are the same and not blank return true
        if self.board[a] == self.board[b] and self.board[b] == self.board[c]:
            if self.board[a] != " ":
                return True
        return False

    def getNotMove(self):  # returns the spots in the board that are used
        lis = []
        for i in range(len(self.board)):
            if self.board[i] != " ":
                lis.append(i)
        return lis

SCREEN_WIDTH = 1366  # the size of this screen
SCREEN_HEIGHT = 768

pygame.init()  # initiates the pygame class and allows use of displays
width = SCREEN_WIDTH/2  # half of the screen's value
height = width  # half of the screen's value
gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN, 32)
pygame.display.set_caption('Tic Tac Toe')  # sets what the top bar of the application says
clock = pygame.time.Clock()  # clock for in-game timing
myfont = pygame.font.SysFont('Times New Roman', 30)  # used to show different text

text = myfont.render('Player Match', False, (0, 0, 0))  # to show which side the player is on
text2 = myfont.render('AI Match', False, (0, 0, 0))  # used to show the game number of the AI

# sets the colors for reference later in the code.
green = (30, 180, 20)
black = (0, 0, 0)
blue = (50, 150, 200)
red = (200, 50, 40)
white = (255, 255, 255)


def getInput():  # gets user input from the graphical interface
    lastFrame = pygame.mouse.get_pressed()  # gets if the mouse was pressed in the last frame
    pygame.event.get()  # updates events
    newFrame = pygame.mouse.get_pressed()  # gets if the mouse is pressed in the current frame
    if lastFrame[0] != newFrame[0] and newFrame[0] != 0:  # if the mouse was actaully pressed
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseX /= width/3  # puts these values between 0 and 3
        mouseY /= height/3
        if mouseX < 1:  # if mouse is on the left third
            if mouseY < 1:  # if mouse is on the top third
                playerBoard.move(0)
            elif mouseY < 2:  # middle third
                playerBoard.move(3)
            else:  # bottom third
                playerBoard.move(6)
        elif mouseX < 2:  # if mouse is in the middle third
            if mouseY < 1:
                playerBoard.move(1)
            elif mouseY < 2:
                playerBoard.move(4)
            else:
                playerBoard.move(7)
        else:  # if mouse is in the right third
            if mouseY < 1:
                playerBoard.move(2)
            elif mouseY < 2:
                playerBoard.move(5)
            else:
                playerBoard.move(8)


def drawO(x, y):  # draws an "o" to the board at a specified location
    if x == 0:  # x cord of O
        x = width/6
    elif x == 1:
        x = width/2
    elif x == 2:
        x = 5*width/6
    elif x == 3:
        x = width + width/6
    elif x == 4:
        x = width + width/2
    elif x == 5:
        x = width + 5 * width /6
    if y == 0:  # y cord of O
        y = height/6
    elif y == 1:
        y = height/2
    elif y == 2:
        y = 5*height/6
    elif y == 3:
        y = height + height/6
    elif y == 4:
        y = height + height/2
    elif y == 5:
        y = height + 5*height/6
    x = int(x)  # used because the PyGame circle function requires integers
    y = int(y)
    pygame.draw.circle(gameDisplay, red, (x, y), int(width/7), 12)  # actually draws the "o"


def drawX(x, y):  # same as drawO, but with an "x" instead
    if x == 0:  # x cord of X
        x = width/6
    elif x == 1:
        x = width/2
    elif x == 2:
        x = 5*width/6
    elif x == 3:
        x = width + width/6
    elif x == 4:
        x = width + width/2
    elif x == 5:
        x = width + 5 * width /6
    if y == 0:  # y cord of X
        y = height/6
    elif y == 1:
        y = height/2
    elif y == 2:
        y = 5*height/6
    elif y == 3:
        y = height + height/6
    elif y == 4:
        y = height + height/2
    elif y == 5:
        y = height + 5*height/6
    pygame.draw.line(gameDisplay, blue, (x-width/7, y-height/7), (x+width/7, y+height/7), 17)
    pygame.draw.line(gameDisplay, blue, (x-width/7, y+height/7), (x+width/7, y-height/7), 17)


def checkPlayerBoard():  # updates the player board
    global playerBoard, winFrameCount, playerPoints
    if not playerBoard.boardWin()[0]:  # if there is not a winner yet
        if playerBoard.player == "x":  # if it is the AI's turn to move
            tempnum = ai1.getMoveNum(playerBoard.getNotMove())  # grab the move number the AI plays
            playerPoints.append([Point(playerBoard, tempnum, playerBoard.getMoveNum()), "x"])  # adds to points to be given to AI if the AI wins
            playerBoard.move(tempnum)  # AI makes a move on the board
            if playerBoard.boardWin()[0]:  # if there is a winner
                if playerBoard.boardWin()[1] == "x":  # if the AI won             AI HAS WON
                    for i in range(len(playerPoints)):  # add the points to the AI
                        if playerPoints[i] not in ai1.allPoints:
                            ai1.addPoint(playerPoints[i])
                        if playerPoints[i][0].setOption("x") not in ai1.winningPoints:
                            ai1.addWinPoint([playerPoints[i][0].setOption("x"), playerPoints[i][1]])
                    playerPoints = []  # clear the points from this round
                elif playerBoard.boardWin()[1] == "o":  # if you won             YOU HAVE WON
                    for i in range(len(playerPoints)):
                        if i != len(playerPoints) -1:
                            pointa = Point(playerPoints[i].getBoard().getInvertBoard(), playerPoints[i][0].getLabel(), playerPoints[i][0].moveNum)
                            if pointa not in ai1.allPoints:
                                ai1.addPoint(pointa)  # adds the points you've played to the ai
                        else:
                            if playerPoints[i].getInvertedPoint() not in ai1.allPoints:
                                ai1.addPoint(playerPoints[i].getInvertedPoint())
                        tempPoint = playerPoints[i].getInvertedPoint().setOption("x")
                        if tempPoint not in ai1.winningPoints:
                            ai1.addWinPoint(tempPoint)
                    playerPoints = []  # clears points from this round
                else:
                    for i in range(len(playerPoints)):  # add the points to the AI
                        if playerPoints[i] not in ai1.allPoints:
                            ai1.addPoint(playerPoints[i])
                    for i in range(len(playerPoints)):
                        pointa = Point(playerPoints[i][0].getBoard().getInvertBoard(), playerPoints[i][0].getLabel(), playerPoints[i][0].moveNum)
                        if pointa not in ai1.allPoints:
                            ai1.addPoint(Point(playerPoints[i][0].getBoard().getInvertBoard(), playerPoints[i][0].getLabel(), playerPoints[i][0].moveNum))  # adds the points you've played to the ai
                    playerPoints = []  # clears points from this round
                winFrameCount -= 1  # used to see the final board in the game
    else:
        playerPoints = []
        winFrameCount -= 1  # used to see the final board in the game


def drawAITiles(board):  # draws the tiles of the AI board onto the screen
    for i in range(0, 3):  # a simple nested for-loop to draw the tiles to the screen
        for j in range(0, 3):
            if board[i*3 + j] == "x":
                drawX(j+3, i)
            elif board[i*3 + j] == "o":
                drawO(j+3, i)


def drawTiles(board):  # draws the tiles to the board
    for i in range(0, 3):  # a simple nested for-loop to draw the tiles to the screen
        for j in range(0, 3):
            if board[i*3 + j] == "x":
                drawX(j, i)
            elif board[i*3 + j] == "o":
                drawO(j, i)


def drawBoard():  # makes the total board with everything that is needed, but does not show until a different time.
    clock.tick(60)  # caps the frame rate
    gameDisplay.fill(white)  # makes a white background
    pygame.draw.line(gameDisplay, black, (width/3, 0), (width/3, height), 4)  # the actual Tic Tac Toe board
    pygame.draw.line(gameDisplay, black, (2*width/3, 0), (2*width/3, height), 4)
    pygame.draw.line(gameDisplay, black, (0, height/3), (width, height/3), 4)
    pygame.draw.line(gameDisplay, black, (0, 2*height/3), (width, 2*height/3), 4)
    pygame.draw.line(gameDisplay, black, (width, height/3), (2*width, height/3), 4)  # the AI's Tic Tac Toe board
    pygame.draw.line(gameDisplay, black, (width, 2*height/3), (2*width, 2*height/3), 4)
    pygame.draw.line(gameDisplay, black, (width + width/3, 0), (width + width/3, height), 4)
    pygame.draw.line(gameDisplay, black, (width + 2*width / 3, 0), (width + 2*width / 3, height), 4)
    pygame.draw.line(gameDisplay, green, (width, 0), (width, SCREEN_HEIGHT), 10)  # a boarder between the two games
    drawTiles(playerBoard.getBoard())  # draws all the tiles
    drawAITiles(AIboard.getBoard())
    pygame.draw.rect(gameDisplay, green, (0, height, SCREEN_WIDTH, SCREEN_HEIGHT))  # a boarder between the bottom of the screen and the games
    gameDisplay.blit(text, (width/2 - 60, height + 30))
    gameDisplay.blit(text2, (width + width/2 - 60, height+30))

ai1 = AI()  # starts the ai's
ai2 = AI()

AIboard = Board()  # starts the AI versus AI board
playerBoard = Board()  # starts the player versus AI board (AI always goes first)

playerPoints = []  # points that the AI can learn from if it wins
ai1Wins = 0  # a simple counter for how many games each AI has won
ai2Wins = 0
while True:  # the main game loop
    points = []  # to add data to the ai
    while not AIboard.boardWin()[0] and ai1.getMoveNum(
            AIboard.getNotMove()) > -1:  # while the game is still going in the background
        tempNum = ai1.getRandomMove(AIboard.getNotMove())
        points.append([Point(AIboard, tempNum, AIboard.getMoveNum()), "x"])  # appends the move and who played it #change second board to tempNum
        AIboard.move(tempNum)  # make the move
        if winFrameCount == WINFRAME:
            drawBoard()  # draw to the screen
        elif winFrameCount == 0:
            winFrameCount = WINFRAME
        else:  # stops all games until winFrameCount == 0
            if winFrameCount == WINFRAME - 1:
                drawBoard()
                playerBoard = Board()
            winFrameCount -= 1
        pygame.display.update()  # show the updated screen
        if AIboard.boardWin()[0] or ai2.getMoveNum(AIboard.getNotMove()) < 0:  # if there's a winner or no moves, stop the game
            if AIboard.boardWin()[1] == " ":  # if there is not a winner, add all points to the AI's
                print()
                # for i in range(len(points)):
                #     if points[i] not in ai1.allPoints:
                #         ai1.addPoint(points[i])
                #     if points[i] not in ai2.allPoints:
                #         ai2.addPoint(points[i])
            elif AIboard.boardWin()[1] == "x":  # if AI1 wins the game, add points to both AI's
                for i in range(len(points)):
                    if points[i] not in ai1.allPoints:
                        ai1.addPoint(points[i])
                    # if i != len(points) - 1:
                    #     pointa = [Point(points[i][0].getBoard().getInvertBoard(), points[i][0].getLabel(), points[i][0].moveNum),points[i][1]]
                    #     if pointa not in ai2.allPoints:
                    #         ai2.addPoint(pointa)
                    # else:
                    #     pointa = [points[i][0].getInvertedPoint(), points[i][1]]
                    #     if pointa not in ai2.allPoints:
                    #         ai2.addPoint(pointa)
            else:  # if AI2 wins the game, add points to both AI's
                for i in range(len(points)):
                    if points[i] not in ai2.allPoints:
                        ai2.addPoint(points[i])
                    if i != len(points) - 1:
                        pointa = [Point(points[i][0].getBoard().getInvertBoard(), points[i][0].getLabel(), points[i][0].moveNum),
                                  points[i][1]]
                        if pointa not in ai1.allPoints:
                            ai1.addPoint(pointa)
                    else:
                        pointa = [points[i][0].getInvertedPoint(), points[i][1]]
                        if pointa not in ai1.allPoints:
                            ai1.addPoint(pointa)
            break  # after two plays of the AI game
        getInput()  # gets user input from the graphical screen
        checkPlayerBoard()  # does the following loop, but altered for a player versus AI game
        tempNum = ai2.getMoveNum(AIboard.getNotMove())
        points.append([Point(AIboard, tempNum, AIboard.getMoveNum()), "o"])  # appends move and who played it
        AIboard.move(tempNum)  # make the move
        if winFrameCount == WINFRAME:  # this next part makes a small delay on both games between each Player-AI game
            drawBoard()  # draw to the screen
        elif winFrameCount == 0:
            winFrameCount = WINFRAME
        else:
            if winFrameCount == WINFRAME-1:
                drawBoard()
                playerBoard = Board()
            winFrameCount -= 1
    pygame.display.update()  # show the updated screen
    AIboard = Board()  # reset board
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:  # if the escape key is pressed, quit the program
        pygame.quit()
