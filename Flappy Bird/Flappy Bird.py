from random import *
from time import *
import pygame
import math
import random
from pygame import mixer
# mixer.init()
# mixer.music.load('music.ogg')
# mixer.music.play()

pygame.init()

screen = pygame.display.set_mode((600,600))


pygame.display.set_caption("Flappy Bird")

start = True
close = True
bg = pygame.image.load("bg.jpg")
screenCONT = 0
k = pygame.draw.circle(screen, (255, 255, 255), (pygame.mouse.get_pos()), 9)
k2 = pygame.draw.circle(screen, (0, 0, 0), (pygame.mouse.get_pos()), 7)

while start:
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
    screenCONT += 1
    if screenCONT % 100 == 0:
        screen.fill((randint(0,20),randint(0,20),randint(0,20)))
    sFont = pygame.font.SysFont("courier", 60)
    font3 = (sFont.render("Flappy Bird", True, "White"))
    screen.blit(font3, (90, 200))
    fontRECT = pygame.draw.rect(screen, (255, 255, 255), [225, 300, 120, 40])
    sFont = pygame.font.SysFont("courier", 40)
    font3 = (sFont.render("Start", True, "Black"))
    screen.blit(font3, (225, 300))
    font2RECT = pygame.draw.rect(screen, (255, 255, 255), [225, 350, 120, 40])
    sFont = pygame.font.SysFont("courier", 40)
    font3 = (sFont.render("Close", True, "Black"))
    screen.blit(font3, (225, 350))
    k = pygame.draw.circle(screen, (255, 255, 255), (pygame.mouse.get_pos()), 9)
    k2 = pygame.draw.circle(screen, (0, 0, 0), (pygame.mouse.get_pos()), 7)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            k = pygame.draw.circle(screen, (255, 255, 255), (pygame.mouse.get_pos()), 9)
            k2 = pygame.draw.circle(screen, (0, 0, 0), (pygame.mouse.get_pos()), 7)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if k.colliderect(fontRECT):
                start = False
            if k.colliderect(font2RECT):
                start = False
                close = False

    pygame.display.update()

# Images


floor = pygame.image.load("floor.png")
birdy = pygame.image.load("bird.png")
pipe = pygame.image.load("pipe.png")
pipeh = pygame.image.load("pipe.png")
pipeh = pygame.transform.rotate(pipeh,180)
pipeCAP = pygame.image.load("pipeCAP.png")

# Pre-Vars 1

xground = -100
groundS = 1

counter = 90
pairDIFFERENCE = [[30,30]]
upPipes = [[80,9000]]
downPipes = [[80,9000]]

class Bird:
    def __init__(self):
        self.x = 225
        self.y = 30
        self.i = 0
        self.delta_y = 2
        self.jump = 0

    def space(self, ja):
        self.i = 0
        self.jump = ja
        self.delta_y = -2

# Pre-Vars 2

birdL = Bird()
score = 0

holdC = 0
lokk = False
clock = pygame.time.Clock()

while close:
    # Setup

    counter+=1
    clock.tick(100)

    # Game Over

    def Game_Over():
        global close
        screen.fill((0,0,0))
        sFont = pygame.font.SysFont("courier", 80)
        font3 = (sFont.render("GAME OVER", True, "White"))
        screen.blit(font3, (90, 200))
        sFont = pygame.font.SysFont("courier", 40)
        font3 = (sFont.render("Score: " + str(score), True, "White"))
        screen.blit(font3, (225, 300))
        sFont = pygame.font.SysFont("courier", 40)
        font3 = (sFont.render("Time: " + str(int(counter/100)) + "s", True, "White"))
        screen.blit(font3, (225, 350))
        pygame.display.update()
        sleep(100)
        close = False

    # Hitboxes + collision

    if birdL.i < 4.0 * 5:
        bird_hitbox = pygame.draw.rect(screen, (255, 255, 255), [birdL.x+15, birdL.y, 90, 60])
    else:
        bird_hitbox = pygame.draw.rect(screen, (255, 255, 255), [birdL.x+15, birdL.y+40, 90, 60])
    for b in upPipes:
        pipeHIT = pygame.draw.rect(screen, (0, 255, 0), [b[0], b[1]+20, 120, 10000])
        collide = bird_hitbox.colliderect(pipeHIT)
        pipeHIT2 = pygame.draw.rect(screen, (255, 255, 0), [b[0], b[1]-1000135, 120, 1000000])
        collide2 = bird_hitbox.colliderect(pipeHIT2)
        if bird_hitbox.left == b[0]-60 and bird_hitbox.top<0:
            Game_Over()
        if bird_hitbox.left == b[0] and bird_hitbox.top<0:
            Game_Over()
        if bird_hitbox.left == b[0]+60 and bird_hitbox.top<0:
            Game_Over()
        if collide == True or collide2 == True:
            Game_Over()

    # Events

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            close = False
        if e.type == pygame.KEYDOWN:
            birdL.space(holdC)
            holdC = 0
            lokk = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            birdL.space(holdC)
            holdC = 0
            lokk = False
    if lokk:
        holdC += 1

    # Background

    background = pygame.transform.scale(bg, (600,600))
    yAT = background.get_rect()
    yAT = yAT.move((0, 0))
    screen.blit(background, yAT)

    # Base

    xground-=groundS
    if xground < -200:
        xground = -100
    base = pygame.transform.scale(floor, (800,200))
    yAT2 = base.get_rect()
    yAT2 = yAT2.move((xground, 500))
    screen.blit(base, yAT2)

    # Pipes UP

    if counter % 20 == 0:
        newPIPEx = upPipes[len(upPipes)-1][0]+500
        upPipes.append([newPIPEx, randint(140,500)]) # (140, 500)
    for p in upPipes:
        p[0] = p[0] - 1
        if p[0] < 600:
            pipe = pygame.transform.scale(pipe, (120,460))
            yATz = pipe.get_rect()
            yATz = yATz.move((p[0], p[1]))
            screen.blit(pipe, yATz)

    # Pipes DOWN

    if counter % 20 == 0:
        newPIPEDx = downPipes[len(downPipes)-1][0]+500
        downPipes.append([newPIPEDx, randint(50,80)])
    for d in downPipes:
        d[0] = d[0] - 1
        if d[0] < 600:
            pipeh = pygame.transform.scale(pipeh, (120,460))
            yATzf = pipeh.get_rect()
            yATzf = yATzf.move((d[0], upPipes[downPipes.index(d)][1]-575))
            screen.blit(pipeh, yATzf)

    # Pipe Cleanup

    for l in downPipes:
        if l[0] < -120:
            downPipes.remove(l)
    for j in upPipes:
        if j[0] < -120:
            upPipes.remove(j)
            score += 1

    # Bird

    birdL.i += 1
    birdL.y += birdL.delta_y
    if birdL.i > 1.0*5:
        birdL.delta_y = -2
    if birdL.i > 3*5:
        birdL.delta_y = -0.833
    if birdL.i > 4*5:
        birdL.delta_y = 2

    if birdL.y > 430:
        birdL.delta_y = 0
        Game_Over()
    if birdL.i < 4.0*5:
        bird = pygame.transform.scale(birdy, (120, 60))
        b = bird.get_rect()
        b = b.move((birdL.x, birdL.y))
        screen.blit(bird, b)
    else:
        bird = pygame.transform.scale(birdy, (120,60))
        bird = pygame.transform.rotate(bird,310)
        b = bird.get_rect()
        b = b.move((birdL.x, birdL.y))
        screen.blit(bird, b)

    # Score and Time

    if counter <= 91:
        score -= 1
    if counter > 290:
        sFont = pygame.font.SysFont("courier", 40)
        font3 = (sFont.render("Score: " + str(score), True, "Black"))
        screen.blit(font3, (190, 510))
        sFont = pygame.font.SysFont("courier", 40)
        font3 = (sFont.render("Time: " + str(int(counter/100)) + "s", True, "Black"))
        screen.blit(font3, (190, 550))
    pygame.display.update()

