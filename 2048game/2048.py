import pygame, sys, time, random
from pygame.locals import *

TOTAL_POINTS = 0
default_score = 2
BOARD_SIZE = 4

# colors
white = (255, 255, 255)
black = (0, 0, 0)
brown = (165, 42, 42)
yellow = (255, 255, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (128, 128, 128)
goldenrod = (218, 165, 32)
hotpink = (255, 105, 180)
midnightblue = (25, 25, 112)
crimson = (220, 20, 60)
sienna = (160, 82, 45)
violetred = (199, 21, 133)
purple = (128, 0, 128)

color_dict = {0: white, 2: black, 4: brown, 8: sienna, 16: red, 32: violetred, 64: blue, 128: gray, 256: purple,
              512: hotpink, 1024: midnightblue, 2048: crimson}

pygame.init()

SURFACE = pygame.display.set_mode((400, 500), 0, 32)
pygame.display.set_caption('2048')

myfont = pygame.font.SysFont("monospace", 25)
scorefont = pygame.font.SysFont("monospace", 50)

tileMatrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
undoMat = []


def main(fromLoaded=False):
    if not fromLoaded:
        placeRandomTile()
        placeRandomTile()
    printMatrix()
    while True:
        global BOARD_SIZE
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if checkIfCanGo():
                if event.type == KEYDOWN and isArrow(event.key):
                    rotations = getRotations(event.key)
                    addToUndo()
                    for i in range(0, rotations):
                        rotateMatrixClockwise()
                    if canMove():
                        moveTiles()
                        mergeTiles()
                        placeRandomTile()
                    for j in range(0, (4 - rotations) % 4):
                        rotateMatrixClockwise()
                    printMatrix()
                highestval = 0
                for i in range(0, BOARD_SIZE):
                    for j in range(0, BOARD_SIZE):
                        if tileMatrix[i][j] > highestval:
                            highestval = tileMatrix[i][j]
                if highestval == 2048:
                    gameOverWon()
            else:
                printGameOver()
            if event.type == KEYDOWN:

                if event.key == pygame.K_r:
                    reset()
                if 50 < event.key and 56 > event.key:
                    BOARD_SIZE = event.key - 48
                    reset()
                if event.key == pygame.K_s:
                    saveGameState()
                elif event.key == pygame.K_l:
                    loadGameState()
                elif event.key == pygame.K_u:
                    undo()
        pygame.display.update()


def getcolor(i):
    return color_dict[i]


def printMatrix():
    SURFACE.fill(getcolor(2))
    global BOARD_SIZE
    global TOTAL_POINTS
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            pygame.draw.rect(SURFACE, getcolor(tileMatrix[i][j]), (
            i * (400 / BOARD_SIZE), ((j * (400 / BOARD_SIZE)) + 100), (400 / BOARD_SIZE), (400 / BOARD_SIZE)))
            label1 = myfont.render(str(tileMatrix[i][j]), 1, (255, 255, 255))
            label2 = scorefont.render("Score:" + str(TOTAL_POINTS), 1, (255, 255, 255))
            SURFACE.blit(label1, (i * (400 / BOARD_SIZE) + 30, j * (400 / BOARD_SIZE) + 130))
            SURFACE.blit(label2, (10, 20))


def printGameOver():
    global TOTAL_POINTS
    SURFACE.fill(getcolor(0))
    label1 = scorefont.render("Game Over", 1, black)
    label2 = scorefont.render("Score " + str(TOTAL_POINTS), 1, black)
    label3 = scorefont.render("press r ", 1, black)
    label4 = scorefont.render("to restart", 1, black)

    SURFACE.blit(label1, (50, 100))
    SURFACE.blit(label2, (50, 200))
    SURFACE.blit(label3, (50, 300))
    SURFACE.blit(label4, (50, 400))


def placeRandomTile():
    count = 0
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            if tileMatrix[i][j] == 0:
                count += 1

    k = random.randrange(0, 4, 1)
    p = random.randrange(0, 4, 1)
    while tileMatrix[k][p] != 0:
        k = random.randrange(0, 4, 1)
        p = random.randrange(0, 4, 1)
    tileMatrix[k][p] = 2


def floor(n):
    return int(n - (n % 1))


def moveTiles():
    # We want to work column by column shifting up each element in turn.
    for i in range(0, BOARD_SIZE):  # Work through our 4 columns.
        for j in range(0, BOARD_SIZE - 1):  # Now consider shifting up each element by checking top 3 elements if 0.
            while tileMatrix[i][j] == 0 and sum(tileMatrix[i][
                                                j:]) > 0:  # If any element is 0 and there is a number to shift we want to shift up elements below.
                for k in range(j, BOARD_SIZE - 1):  # Move up elements below.
                    tileMatrix[i][k] = tileMatrix[i][k + 1]  # Move up each element one.
                tileMatrix[i][BOARD_SIZE - 1] = 0


def mergeTiles():
    global TOTAL_POINTS
    for i in range(0, BOARD_SIZE):
        for k in range(0, BOARD_SIZE - 1):
            if tileMatrix[i][k] == tileMatrix[i][k + 1] and tileMatrix[i][k] != 0:
                tileMatrix[i][k] = tileMatrix[i][k] * 2
                tileMatrix[i][k + 1] = 0
                TOTAL_POINTS += tileMatrix[i][k]
                moveTiles()


def checkIfCanGo():
    for i in range(0, BOARD_SIZE ** 2):
        if tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE] == 0:
            return True
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE - 1):
            if tileMatrix[i][j] == tileMatrix[i][j + 1]:
                return True
            elif tileMatrix[j][i] == tileMatrix[j + 1][i]:
                return True
    return False


def reset():
    global TOTAL_POINTS
    global tileMatrix
    TOTAL_POINTS = 0
    SURFACE.fill(black)
    tileMatrix = [[0 for i in range(0, BOARD_SIZE)] for j in range(0, BOARD_SIZE)]
    main()


def canMove():
    for i in range(0, BOARD_SIZE):
        for j in range(1, BOARD_SIZE):
            if tileMatrix[i][j - 1] == 0 and tileMatrix[i][j] > 0:
                return True
            elif (tileMatrix[i][j - 1] == tileMatrix[i][j]) and tileMatrix[i][j - 1] != 0:
                return True
    return False


def rotateMatrixClockwise():
    for i in range(0, int(BOARD_SIZE / 2)):
        for k in range(i, BOARD_SIZE - i - 1):
            temp1 = tileMatrix[i][k]
            temp2 = tileMatrix[BOARD_SIZE - 1 - k][i]
            temp3 = tileMatrix[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k]
            temp4 = tileMatrix[k][BOARD_SIZE - 1 - i]
            tileMatrix[BOARD_SIZE - 1 - k][i] = temp1
            tileMatrix[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k] = temp2
            tileMatrix[k][BOARD_SIZE - 1 - i] = temp3
            tileMatrix[i][k] = temp4


def isArrow(k):
    return (k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT)


def getRotations(k):
    if k == pygame.K_UP:
        return 0
    elif k == pygame.K_DOWN:
        return 2
    elif k == pygame.K_LEFT:
        return 1
    elif k == pygame.K_RIGHT:
        return 3


def convertToLinearMatrix():
    mat = []
    for i in range(0, BOARD_SIZE ** 2):
        mat.append(tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE])
    mat.append(TOTAL_POINTS)
    return mat


def addToUndo():
    undoMat.append(convertToLinearMatrix())


def undo():
    if len(undoMat) > 0:
        mat = undoMat.pop()
        for i in range(0, BOARD_SIZE ** 2):
            tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE] = mat[i]
        global TOTAL_POINTS
        TOTAL_POINTS = mat[BOARD_SIZE ** 2]
        printMatrix()


def gameOverWon():
    global TOTAL_POINTS
    SURFACE.fill(getcolor(0))
    label1 = scorefont.render("You Win!", 1, black)
    label2 = scorefont.render("Score " + str(TOTAL_POINTS), 1, black)
    label3 = scorefont.render("press r ", 1, black)
    label4 = scorefont.render("to restart", 1, black)

    SURFACE.blit(label1, (50, 100))
    SURFACE.blit(label2, (50, 200))
    SURFACE.blit(label3, (50, 300))
    SURFACE.blit(label4, (50, 400))


if __name__ == '__main__':
    main()


