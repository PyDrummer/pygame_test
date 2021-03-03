import pygame
import time
pygame.init()

screenWidth = 500
screenHeight = 300

win = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption('First Game')

# Global variables:
# Character imgs:
walkRight = [pygame.image.load('wr1.png'), pygame.image.load('wr2.png'), pygame.image.load('stand.png')]
walkLeft = [pygame.image.load('wl1.png'), pygame.image.load('wl2.png')]
bg = pygame.image.load('bb2.png')
charR = pygame.image.load('stand.png')
charL = pygame.image.load('standleft.png')

#clock speed:
clock = pygame.time.Clock()

# player class
class Player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True

    def draw(self, win):
         # our character:
        if self.walkCount + 1 >= 4:
            self.walkCount = 0

        if not (self.standing):
            # walking left
            if self.left:
                win.blit(walkLeft[self.walkCount//2], (self.x, self.y))
                self.walkCount += 1
            # walking right
            elif self.right:
                win.blit(walkRight[self.walkCount//2], (self.x, self.y))
                self.walkCount += 1

        else:
            if self.right:
                win.blit(charR, (self.x, self.y))
            else:
                win.blit(charL, (self.x,self.y))

class Projectile():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 15 * facing

    # draws the projectile
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x +15, self.y), self.radius)


class Enemy():
    walkRight = [pygame.image.load('estand.png'), pygame.image.load('ewr.png'), pygame.image.load('epr.png')]
    walkLeft = [pygame.image.load('estandleft.png'), pygame.image.load('ewl.png'), pygame.image.load('epl.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        # x is where we start, end is where we end.
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3


    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 4:
            self.walkCount = 0
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount // 2], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount // 2], (self.x, self.y))
            self.walkCount += 1

    # moves our enemy
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                # flip direction
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0


# creating the boundries of the window function and the drawings/animations:
def gamewindow():
    # this is the background
    win.blit(bg, (0,0))
    dino.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

# the main loop
dino = Player(0, 225, 64, 64)
goblin = Enemy(0, 210, 64, 64, 425)
bullets = []
run = True
number = 0

while run:
    # Frame rate:
    clock.tick(25)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                number += 1
            

    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    # movement list
    keys = pygame.key.get_pressed()

    if (keys[pygame.K_LEFT] or keys[ord('a')]) and dino.x > dino.vel:
        dino.x -= dino.vel
        dino.left = True
        dino.right = False
        dino.standing = False
    elif (keys[pygame.K_RIGHT] or keys[ord('d')]) and dino.x < screenWidth - dino.width - dino.vel:
        dino.x += dino.vel
        dino.left = False
        dino.right = True
        dino.standing = False
    else:
        dino.standing = True
        dino.walkCount = 0

    if not(dino.isJump):
        if keys[pygame.K_SPACE]:
            dino.isJump = True
            dino.right = False
            dino.left = False
            dino.walkCount = 0
    else:
        if dino.jumpCount >= -10:
            # to make your character move down, change the down to change how long the character stays in the air
            down = 1
            if dino.jumpCount < 0:
                down = -1
            # makes the character go up:
            dino.y -= (dino.jumpCount ** 2) * .8 * down
            dino.jumpCount -= 2
        else:
            dino.isJump = False
            dino.jumpCount = 10

    # shooting mechanics
    # if keys[ord('f')]:
    if number > 0:
        # Direction to decide which way the bullet goes
        if dino.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(Projectile(dino.x + dino.width // 2, round(dino.y + dino.height //2), 6, (255, 0, 0), facing))
        number = 0
        
    gamewindow()


pygame.quit()