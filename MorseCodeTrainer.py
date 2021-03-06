import random
import pygame
import string
import sys
import time
from pygame.locals import *

#  start pygame
pygame.init()
pygame.display.set_caption('Morse Code Trainer')

FPS = 60   # frames per second, the general speed of the program
WINDOWWIDTH = 640   # size of window's width in pixels
WINDOWHEIGHT = 480  # size of windows' height in pixels

global FPSCLOCK, DISPLAYSURF
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
global PAUSE
PAUSE = False

# Colours used
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
YELLOW = (240, 196, 50)
GREEN = (0, 255, 0)
BLUE = (32, 78, 230)
PURPLE = (160, 32, 240)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TEXTCOLOUR = BLACK
BACKGROUNDCOLOUR = WHITE
LETTERCOLOUR = BLUE
HIGHLIGHTCOLOUR = YELLOW
MENUCOLOUR = RED
REFERENCECOLOUR1 = PURPLE
REFERENCECOLOUR2 = BLACK

# fonts used
LARGETEXT = pygame.font.Font('freesansbold.ttf', 32)
SMALLTEXT = pygame.font.Font("freesansbold.ttf", 20)

MORSECODELARGETEXT = pygame.font.Font('MorseCode.ttf', 100)
MORSECODESMALLTEXT = pygame.font.Font('MorseCode.ttf', 55)


#  Not needed currently
MORSECODEDICTIONARY = {
    "a": ".-",
    "b": "-...",
    "c": "-.-.",
    "d": "-..",
    "e": ".",
    "f": "..-.",
    "g": "--.",
    "h": "....",
    "i": "..",
    "j": ".---",
    "k": "-.-",
    "l": ".-..",
    "m": "--",
    "n": "-.",
    "o": "---",
    "p": ".--.",
    "q": "--.-",
    "r": ".-.",
    "s": "...",
    "t": "-",
    "u": "..-",
    "v": "...-",
    "w": ".--",
    "x": "-..-",
    "y": "--.-",
    "z": "--.."
}


def main():
    DISPLAYSURF.fill(BACKGROUNDCOLOUR)
    drawMenu()


def drawMenu():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        button(
            "Guess Morse Code", 230, 200, 190, 50,
            BACKGROUNDCOLOUR, MENUCOLOUR, "guessMorseCode")
        button("Reference", 230, 250, 190, 50, BACKGROUNDCOLOUR, MENUCOLOUR, "reference")
        button("Options", 230, 300, 190, 50, BACKGROUNDCOLOUR, MENUCOLOUR, "options")
        button("Quit", 230, 400, 190, 50, BACKGROUNDCOLOUR, MENUCOLOUR, "quit")
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def guessMorseCode():
    #  Intalisation
    global PAUSE
    press = pygame.key.get_pressed()
    currentLetter = generateLetter()
    chances = 3
    letterPressed = ""
    letterTime = FPS
    while (True):
        DISPLAYSURF.fill(BACKGROUNDCOLOUR)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # if pygame.key.get_pressed():
                #  Gets the current key pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    PAUSE = True
                    pause()
                if event.key < 127:
                    letterPressed = str(chr(event.key))
                    if letterPressed == currentLetter:
                        playCorrectAnswer()
                        currentLetter = generateLetter()
                    else:
                        playWrongAnswer()
                        chances -= 1
                        if chances == 0:
                            drawGameOver()


        drawLetter(letterPressed, 275, 250, 100, 100, LARGETEXT, RED)
        drawLetter(currentLetter, 275, 175, 100, 100, MORSECODELARGETEXT, BLACK)
        drawText(WINDOWWIDTH - 100, WINDOWHEIGHT - 50, LARGETEXT, str(chances), TEXTCOLOUR)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawReference():
    global REFERENCECOLOUR1, REFERENCECOLOUR2
    DISPLAYSURF.fill(BACKGROUNDCOLOUR)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        lowercaseLetters = string.ascii_lowercase

        firstpart, secondpart = lowercaseLetters[
        :len(lowercaseLetters) // 2], lowercaseLetters[len(lowercaseLetters) // 2:]

        for letter, y in zip(firstpart, myRange(30, 420, 30)):
            drawLetter(letter, 100, y, 8, 8, SMALLTEXT, REFERENCECOLOUR1)
            drawLetter(letter, 150, y + 10, 8, 8, MORSECODESMALLTEXT, REFERENCECOLOUR2)

        for letter, y in zip(secondpart, myRange(30, 420, 30)):
            drawLetter(letter, 500, y, 8, 8, SMALLTEXT, REFERENCECOLOUR1)
            drawLetter(letter, 550, y + 10, 8, 8, MORSECODESMALLTEXT, REFERENCECOLOUR2)

        button("Main Menu", 230, 350, 190, 50, BACKGROUNDCOLOUR, MENUCOLOUR, "menu")

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def unpause():
    global PAUSE
    PAUSE = False


def pause():
    while PAUSE:
        for event in pygame.event.get():
            if event.type == QUIT:
                exportSave()
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill(BACKGROUNDCOLOUR)

        drawText(WINDOWWIDTH/2 + 30, 150, LARGETEXT, "Game paused!", TEXTCOLOUR)

        button("Continue", 230, 300, 190, 50, BACKGROUNDCOLOUR, MENUCOLOUR, "unpause")
        button("Main Menu", 230, 350, 190, 50, BACKGROUNDCOLOUR, MENUCOLOUR, "menu")
        button("Quit", 230, 400, 190, 50, BACKGROUNDCOLOUR, MENUCOLOUR, "quit")

        pygame.display.update()
        FPSCLOCK.tick(FPS)

    DISPLAYSURF.fill(BACKGROUNDCOLOUR)
    #  drawScore(WINDOWWIDTH - 100, WINDOWHEIGHT - 50, LARGETEXT, 'Score: ', SCORE, CIRCLECOLOUR)


def drawGameOver():
    global SCORE
    DISPLAYSURF.fill(BACKGROUNDCOLOUR)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exportSave()
                pygame.quit()
                sys.exit()

        #  draw game over text
        drawText(WINDOWWIDTH / 2, WINDOWHEIGHT / 2 - 25, LARGETEXT, "Game over!", TEXTCOLOUR)

        button("Main Menu", 230, 350, 190, 50, BACKGROUNDCOLOUR, MENUCOLOUR, "menu")

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawOptions():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        button("Main Menu", 230, 350, 190, 50, BACKGROUNDCOLOUR, MENUCOLOUR, "menu")

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def button(msg, x, y, w, h, inactiveColour, activeColour, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        # if mouse is inside the box
        pygame.draw.rect(DISPLAYSURF, activeColour, (x, y, w, h))

        if click[0] == 1 and action is not None:
            if action == "guessMorseCode":
                guessMorseCode()
            elif action == "menu":
                DISPLAYSURF.fill(BACKGROUNDCOLOUR)
                drawMenu()
            elif action == "reference":
                DISPLAYSURF.fill(BACKGROUNDCOLOUR)
                drawReference()
            elif action == "options":
                DISPLAYSURF.fill(BACKGROUNDCOLOUR)
                drawOptions()
            elif action == "unpause":
                unpause()
            elif action == "quit":
                pygame.quit()
                sys.exit()
    else:
        pygame.draw.rect(DISPLAYSURF, inactiveColour, (x, y, w, h))

    textSurf, textRect = textObjects(msg, SMALLTEXT)
    textRect.center = ((x + (w / 2), (y + (h / 2))))
    DISPLAYSURF.blit(textSurf, textRect)


def generateLetter():
    lowercaseLetters = string.ascii_lowercase
    letterChosen = random.choice(lowercaseLetters)
    return letterChosen


def drawText(x, y, textSize, text, colour):
    textSurfaceObj = textSize.render(str(text), True, colour, BACKGROUNDCOLOUR)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (x, y)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)


def drawLetter(letter, x, y, w, h, font, colour):
    pygame.draw.rect(DISPLAYSURF, BACKGROUNDCOLOUR, (x, y, w, h))
    textSurf, textRect = textObjects(letter, font, colour)
    textRect.center = ((x + (w / 2), (y + (h / 2))))
    DISPLAYSURF.blit(textSurf, textRect)


def drawLetterBorder(x, y, w, h):
    mouse = pygame.mouse.get_pos()
    # print(mouse)
    # if mousei s inside the box
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(
            DISPLAYSURF, HIGHLIGHTCOLOUR, (x - 5, y - 5, w + 10, h + 10), 4)
    else:
        pygame.draw.rect(DISPLAYSURF, BACKGROUNDCOLOUR, (x - 5, y - 5, w + 10, h + 10), 4)


def textObjects(text, font, textColour=BLACK):
    textSurface = font.render(text, True, textColour)
    return textSurface, textSurface.get_rect()


def playCorrectAnswer():
    correctAnswer = pygame.mixer.Sound('CorrectAnswer.wav')
    correctAnswer.play()


def playWrongAnswer():
    incorrectAnswer = pygame.mixer.Sound("IncorrectAnswer.wav")
    incorrectAnswer.play()

"""
def drawLetters():
    alphabet = string.ascii_uppercase

    y = 150

    for letter, x in zip(alphabet, myRange(50, 675, 40)):
        if letter < "M":
            drawLetter(letter, x, y, 25, 25)
        else:
            drawLetter(letter, x - )

"""
def myRange(start, end, step):
    while start <= end:
        yield start
        start += step


if __name__ == '__main__':
    main()
