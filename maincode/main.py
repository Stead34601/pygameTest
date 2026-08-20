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
cameray = 0
camerax = 0


#create a character class
class player:
    def __init__(self,pos):
        self.pos = pos
        self.speed = 3.0
        self.health = 100
        self.surf = pygame.image.load("maincode/trooper.svg").convert_alpha()
        self.rect = self.surf.get_rect(center = pos)

    def __str__(self):
        message = ("The player has "+ str(self.health)+ "health, and is at "+ str(self.pos))
        return message

    def move(self,cam,direction):
        if direction == "up":
            self.rect.centery -= self.speed
        elif direction == "down":
            self.rect.centery += self.speed
        elif direction == "left":
            self.rect.centerx -= self.speed
        elif direction == "right":
            self.rect.centerx += self.speed
        cam.x = self.rect.centerx - (cam.width / 2)
        cam.y = self.rect.centery - (cam.height / 2)
        cam.updatePos()
        self.updatePos()

    def faceMouse(self):
        pos = self.rect.center
        bearing = getMouseBearing(pos)
        self.rotated = pygame.transform.rotate(self.surf, bearing)
        self.rect = self.rotated.get_rect(center=self.rect.center)

    def updatePos(self):
        self.pos = (self.rect.centerx,self.rect.centery)

#create a camera class
class Camera:
    def __init__(self,width, height, player):
        self.width = width
        self.height = height
        self.x = player.rect.centerx - (width / 2)
        self.y = player.rect.centery - (height / 2)
        self.pos = (self.x, self.y)

    def __str__(self):
        message = ("The cam is: " + str(self.width) + "x" + str(self.height) + " and is at pos" + str(self.pos))
        return message

    def updatePos(self):
        self.pos = (self.x, self.y)

#functions
def getMouseBearing(pos):
    mousePos = pygame.mouse.get_pos()
    dx = mousePos[0] - pos[0]
    dy = mousePos[1] - pos[1]
    return math.degrees(math.atan2(-dy, dx)) - 90

def doInputs(cam):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        character.move(cam,"up")
    if keys[pygame.K_s]:
        character.move(cam,"down")
    if keys[pygame.K_a]:
        character.move(cam,"left")
    if keys[pygame.K_d]:
        character.move(cam,"right")


#create a character with a camera
character = player((50,50))
camera = Camera(40,30, character)



#main game loop
while True:
    #Allow for exiting the loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


    #cam stuff

    #Player stuff

    #keys
    doInputs(camera)
    character.faceMouse()
    print(str(camera))
    print(str(character))


    #blit everything
    #screen.blit(background,(0,0))
    screen.blit(background, (camera.pos))
    screen.blit(character.rotated, character.rect)


    #needed stuff for pygame to refresh
    pygame.display.update()
    clock.tick(30)
    