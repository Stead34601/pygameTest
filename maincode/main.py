import pygame
import time
import math
from sys import exit
import random

#initial variables
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("TestGame")
background = pygame.image.load("maincode/background.svg").convert()
backgroundRect = background.get_rect(topleft = (0,0))

clock = pygame.time.Clock()


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

    def move(self,world,direction):
        y = 0
        x = 0
        if direction == "up":
            y += self.speed
        elif direction == "down":
            y -= self.speed
        elif direction == "left":
            x += self.speed
        elif direction == "right":
            x -= self.speed
        world.move(x,y)
        self.updatePos()

    def faceMouse(self):
        pos = self.rect.center
        bearing = getMouseBearing(pos)
        self.rotated = pygame.transform.rotate(self.surf, bearing)
        self.rect = self.rotated.get_rect(center=self.rect.center)
        self.mouseBearing = bearing % 360

    def updatePos(self):
        self.pos = (self.rect.centerx,self.rect.centery)

    def spawnBullet(self):
        Bullet(world,self.pos,self.mouseBearing,100)

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

class World:
    def __init__(self,player,cam):
        self.player = player
        self.cam = cam
        self.enemies = []
        self.bullets = []
        self.pos = (0,0)
        self.y = self.cam.x
        self.x = self.cam.y
        self.updatePos
        self.background = backgroundRect

    def updatePos(self):
        print('worldUpdated: ' + str(self.x) + " " + str(self.y))
        self.pos = (self.x,self.y)

    def move(self,x,y):
        self.lockAtEdges(2400,1800)
        #remember to world.updatePos()
        self.x += x
        self.y += y

        #cam
        self.cam.x += x
        self.cam.y += y
        self.cam.updatePos()

        
        if not(self.lockAtEdges(2400,1800)):
            #bullets
            for bullet in self.bullets:
                bullet.rect.centerx += x
                bullet.rect.centery += y

            #enemies
            for enemy in self.enemies:
                enemy.rect.centerx += x
                enemy.rect.centery += y
                enemy.updatePos()


        self.updatePos()

    def lockAtEdges(self, width, height):
        locked = False
        print(str(width) + "wdith")
        print (str(-height))
        if self.cam.y < (-height):
            self.cam.y = (-height)
            print("Height Locked max")
            locked = True
        elif self.cam.y > 0:
            self.cam.y = 0
            print("Height Locked Min")
            locked = True


        

        print(self.cam.pos)


        if self.cam.x > 0:
            self.cam.x = 0
            locked = True
            print("Width Locked max")
        elif self.cam.x < -width:
            self.cam.x = -width
            locked = True
            print("Width Locked min")
        self.cam.updatePos()
        return locked

        
class Enemy:
    def __init__(self,pos, world):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.surf = pygame.image.load("maincode/enemy.svg").convert_alpha()
        self.rect = self.surf.get_rect(center = pos)

        world.enemies.append(self)

    def updatePos(self):
        self.pos = self.x + self.y




    
class Bullet:
    def __init__(self,world,pos,bearing,damage):
        self.pos = pos
        self.bearing = bearing + 90
        self.damage = damage
        self.speed = 0.2
        self.surf = pygame.Surface((2,2))
        self.surf.fill('Yellow')
        self.rect = self.surf.get_rect(center=pos)

        #add it to the bullets
        world.bullets.append(self)

    def move(self):
        self.rect.centerx += self.speed * math.degrees(math.cos(math.radians(self.bearing)))
        self.rect.centery -= self.speed * math.degrees(math.sin(math.radians(self.bearing)))

    def __str__(self):
        message = "Bullet: \n Position: " + str(self.pos) + "\nBearing: " + str(self.bearing)
        return message


#functions
def getMouseBearing(pos):
    mousePos = pygame.mouse.get_pos()
    dx = mousePos[0] - pos[0]
    dy = mousePos[1] - pos[1]
    return math.degrees(math.atan2(-dy, dx)) - 90

def doInputs(world):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        character.move(world,"up")
    if keys[pygame.K_s]:
        character.move(world,"down")
    if keys[pygame.K_a]:
        character.move(world,"left")
    if keys[pygame.K_d]:
        character.move(world,"right")
    if keys[pygame.K_v]:
        world.player.spawnBullet()


#create a character with a camera
character = player((400,300))
camera = Camera(400,300, character)
world = World(character,camera)

for i in range(5):
    x = random.randint(0,2400)
    y = random.randint(0,1800)
    x = x
    y = y
    Enemy((x,y), world)



#main game loop
while True:
    #Allow for exiting the loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


    #cam stuff

    #Player stuff

    #check for bullet contacts
    for enemy in world.enemies:
        for bullet in world.bullets:
            if enemy.rect.colliderect(bullet.rect):
                world.enemies.remove(enemy)
                print("Yay you killed them")
                world.bullets.remove(bullet)


    #keys
    doInputs(world)
    character.faceMouse()

    #tick



    #blit background
    screen.blit(background, (world.cam.pos))
    #blit everything
    for bullet in world.bullets:
        bullet.move()
        screen.blit(bullet.surf,bullet.rect)

    for enemy in world.enemies:
        screen.blit(enemy.surf, enemy.rect)
    screen.blit(character.rotated, character.rect)


    #needed stuff for pygame to refresh
    pygame.display.update()
    clock.tick(30)
    