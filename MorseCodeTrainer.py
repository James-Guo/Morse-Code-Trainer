import random
import pygame
import string
import sys
from pygame.locals import *

FPS = 60   # frames per second, the general speed of the program
WINDOWWIDTH = 640   # size of window's width in pixels
WINDOWHEIGHT = 480  # size of windows' height in pixels

# Colours used
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
YELLOW = (240, 196, 50)
GREEN = (0, 255, 0)
BLUE = (32, 78, 230)
PURPLE = (160, 32, 240)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

LETTERCOLOUR = BLUE
HIGHLIGHTCOLOUR = YELLOW
MENUCOLOUR = RED 

global FPSCLOCK, DISPLAYSURF

pygame.init()
FPSCLOCK = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Morse Code Trainer')


LARGETEXT = pygame.font.Font('freesansbold.ttf', 32)
SMALLTEXT = pygame.font.Font("freesansbold.ttf", 20)

MORSECODELARGETEXT = pygame.font.Font('MorseCode.ttf', 100)

BEEP = pygame.mixer.Sound('Beep.wav')


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
    drawMenu()


def drawMenu():
    DISPLAYSURF.fill(WHITE)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        button(
            "Guess Morse Code", 230, 200, 190, 50,
            WHITE, MENUCOLOUR, "guessMorseCode")

        button("Options", 230, 250, 190, 50, WHITE, MENUCOLOUR, "options")
        button("Quit", 230, 300, 190, 50, WHITE, MENUCOLOUR, "quit")
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def guessMorseCode():
    #  Intalisation
    press = pygame.key.get_pressed()
    currentLetter = generateLetter()

    while (True):
        DISPLAYSURF.fill(WHITE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if pygame.key.get_focused():
                #  Gets the current key pressed
                press = pygame.key.get_pressed()

        for i in range(0, len(press)):
            if press[i] == 1:
                #  gets the letter that was pressed
                letterInputted = pygame.key.name(i)
                drawLetter(letterInputted, 275, 250, 100, 100)
                if letterInputted == currentLetter:
                    playBeep()
                    currentLetter = generateLetter()

        # drawLetters()

        drawLetter(currentLetter, 275, 175, 100, 100, True)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawOptions():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exportSave()
                pygame.quit()
                sys.exit()

        button("Main Menu", 230, 350, 190, 50, WHITE, MENUCOLOUR, "menu")

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
                DISPLAYSURF.fill(WHITE)
                drawMenu()
            elif action == "options":
                DISPLAYSURF.fill(WHITE)
                drawOptions()
            elif action == "unpause":
                unpause()
            elif action == "quit":
                exportSave()
                pygame.quit()
                sys.exit()

    else:
        pygame.draw.rect(DISPLAYSURF, inactiveColour, (x, y, w, h))

    textSurf, textRect = textObjects(msg, SMALLTEXT)
    textRect.center = ((x + (w / 2), (y + (h / 2))))
    DISPLAYSURF.blit(textSurf, textRect)


def playBeep():
    BEEP.play()


def generateLetter():
    lowercaseLetters = string.ascii_lowercase
    letterChosen = random.choice(lowercaseLetters)

    return letterChosen


def drawLetter(letter, x, y, w, h, morseCode=False):

    #  drawLetterBorder(x, y, w, h)

    pygame.draw.rect(DISPLAYSURF, WHITE, (x, y, w, h))
    if morseCode:
        textSurf, textRect = textObjects(letter, MORSECODELARGETEXT)
    else:
        textSurf, textRect = textObjects(letter, LARGETEXT, RED)

    textRect.center = ((x + (w / 2), (y + (h / 2))))
    DISPLAYSURF.blit(textSurf, textRect)


def textObjects(text, font, textColour=BLACK):
    textSurface = font.render(text, True, textColour)
    return textSurface, textSurface.get_rect()


def drawLetterBorder(x, y, w, h):
    mouse = pygame.mouse.get_pos()
    # print(mouse)
    # if mouse is inside the box
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(
            DISPLAYSURF, HIGHLIGHTCOLOUR, (x - 5, y - 5, w + 10, h + 10), 4)
    else:
        pygame.draw.rect(DISPLAYSURF, WHITE, (x - 5, y - 5, w + 10, h + 10), 4)


"""
def drawLetters():
    alphabet = string.ascii_uppercase

    y = 150

    for letter, x in zip(alphabet, myRange(50, 675, 40)):
        if letter < "M":
            drawLetter(letter, x, y, 25, 25)
        else:
            drawLetter(letter, x - )


def myRange(start, end, step):
    while start <= end:
        yield start
        start += step
"""

if __name__ == '__main__':
    main()
