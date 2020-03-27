import pygame
from pygame.event import Event

import xbox360_controller

WINDOW_X = 100
WINDOW_Y = 100

pygame.init()

windowSize = [WINDOW_X, WINDOW_Y]
screen = pygame.display.set_mode(windowSize)

controller = xbox360_controller.Controller()

buttons = {
    0: "A",
    1: "B",
    2: "X",
    3: "Y",
    4: "LEFT_BUMP",
    5: "RIGHT_BUMP",
    6: "BACK",
    7: "START",
    8: "LEFT_STICK_BTN",
    9: "RIGHT_STICK_BTN"
}

hats = {
    (-1, 0): "LEFT",
    (0, -1): "DOWN",
    (1, 0): "RIGHT",
    (0, 1): "UP"
}


def matchToButton(input: int):
    return buttons.get(input)


def matchToHat(input: int):
    return hats.get(input)


def handleButton(event: Event):
        print(matchToButton(event.button))


def handleHat(event: Event):
        value = matchToHat(event.value)
        if value != None:
            print(value)


while True:
    for event in pygame.event.get():

        if event.type == pygame.JOYBUTTONDOWN:
            handleButton(event)

        if event.type == pygame.JOYHATMOTION:
            handleHat(event)

        if event.type == pygame.QUIT:
            pygame.quit()
