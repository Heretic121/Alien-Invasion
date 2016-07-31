import pygame, sys, random
from pygame.locals import *
from spriteclass import *

pygame.init()
DS = pygame.display.set_mode((640,480))
pygame.display.set_caption('Alien Invasion!')
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
LIME = (0,255,0)
GREEN = (0,127,0)
RED = (255,0,0)

Blocks = pygame.sprite.Group()
Aliens = pygame.sprite.Group()
AlienDB = {}
ABullets = pygame.sprite.Group()
EBullets = pygame.sprite.Group()
Players = pygame.sprite.Group()

Blocks.add(block_create(BLACK,(85,360),(100,40)))
Blocks.add(block_create(BLACK,(270,360),(100,40)))
Blocks.add(block_create(BLACK,(455,360),(100,40)))

for y in range(0,4):
    AlienDB[y] = {}
    for x in range(0,16):
        ali = Alien(BLUE,20,20)
        ali.rect.x = 85 + ((20*x)+(10*x))
        ali.rect.y = 50 + ((20*y)+(30*y))
        ali.offsetx = x
        ali.offsety = y
        Aliens.add(ali)
        AlienDB[y][x] = ali

PlayerChar = Player(RED,80,20)
PlayerChar.rect.y = 430
PlayerChar.rect.x = 280
Players.add(PlayerChar)

clock = pygame.time.Clock()
score = 0
movePlayer = (0,None)

start = 0

while start == 0:
    DS.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            start = 1
    Blocks.draw(DS)
    Players.draw(DS)
    Aliens.draw(DS)
    clock.tick(20)
    pygame.display.flip()

try:
    while True:
        DS.fill(WHITE)
        Aliens.update()
        ABullets.update()
        EBullets.update()
        for y in range(0,4):
            if y in AlienDB and len(AlienDB[y]) <= 0:
                del(AlienDB[y])
        if len(AlienDB) == 0:
            print("You won!")
            pygame.event.post(pygame.event.Event(QUIT))
        AlreadyFired = {}
        y = 3
        while y >= 0 :
            if y in AlienDB:
                for x in range(0,16):
                    if x in AlienDB[y]:
                        if x not in AlreadyFired:
                            if random.randrange(200) == 1:
                                bullet = Bullet(GREEN,10,10,1)
                                bullet.rect.x = (AlienDB[y][x].rect.x + 5)
                                bullet.rect.y = (AlienDB[y][x].rect.y + 21)
                                EBullets.add(bullet)
                            AlreadyFired[x] = x
            y -= 1
        del(AlreadyFired)
        pygame.sprite.groupcollide(ABullets, Blocks, True, False)
        pygame.sprite.groupcollide(EBullets, Blocks, True, False)
        Kills = pygame.sprite.groupcollide(Aliens, ABullets, True, True)
        for kill in Kills:
            del(AlienDB[kill.offsety][kill.offsetx])
            score += 1
        Death = pygame.sprite.groupcollide(Players, EBullets, True, True)
        if Death:
            print("You died!")
            pygame.event.post(pygame.event.Event(QUIT))
        for bullet in EBullets:
            if bullet.rect.y > 480:
                EBullets.remove(bullet)
        for bullet in ABullets:
            if bullet.rect.y < -10:
                ABullets.remove(bullet)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    movePlayer = (1,0)
                elif event.key == pygame.K_RIGHT:
                    movePlayer = (1,1)
                elif event.key == pygame.K_SPACE:
                    bullet = Bullet(LIME,10,10,0)
                    bullet.rect.x = (PlayerChar.rect.x + 35)
                    bullet.rect.y = 420
                    ABullets.add(bullet)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and movePlayer[1] == 0:
                    movePlayer = (0,None)
                elif event.key == pygame.K_RIGHT and movePlayer[1] == 1:
                    movePlayer = (0,None)
            if event.type == QUIT or ( event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                print("Game exit.")
                pygame.quit()
                sys.exit()
        if movePlayer[0] == 1:
            PlayerChar.update(movePlayer[1])
        Blocks.draw(DS)
        Players.draw(DS)
        Aliens.draw(DS)
        ABullets.draw(DS)
        EBullets.draw(DS)
        clock.tick(30)
        pygame.display.flip()
except KeyboardInterrupt:
    print("Error.")
finally:
    print("Score: %d" % score)
    pygame.quit()
