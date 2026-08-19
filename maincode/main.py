import pygame
import time
import math
from sys import exit

#initial variables
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("TestGame")
background = pygame.image.load("maincode/background.svg").convert()

clock = pygame.time.Clock()


#main game loop
while True:
    #Allow for exiting the loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


    #blit everything
    screen.blit(background,(0,0))
    pygame.display.update()
    clock.tick(30)
    