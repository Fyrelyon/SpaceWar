# Imports
import pygame
import sys
import os
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 801
HEIGHT = 601
SIZE = (WIDTH, HEIGHT)
TITLE = "space doggo fite evil !1"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

# Stage
stage1 = True
stage2 = False
stage3win = False
stage3lose = False

# Timer
clock = pygame.time.Clock()
refresh_rate = 60
k = 0
s = 0
shots = 0

# Fonts
myfont = pygame.font.Font('assets/font/FOXJUMP.ttf', 50)

# Colors
RED = (255, 0, 0)
what = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)

# Images
ship_img = pygame.image.load('assets/images/player.png')
ship_img2 = pygame.image.load('assets/images/player_shield.png')
ship_img3_1 = pygame.image.load('assets/images/player_hurt1.png')
ship_img3_2 = pygame.image.load('assets/images/player_hurt2.png')
ship_img3_3 = pygame.image.load('assets/images/player_hurt3.png')
ship_img3_4 = pygame.image.load('assets/images/player_hurt4.png')

laser_img = pygame.image.load('assets/images/bork.png')
enemy_img = pygame.image.load('assets/images/cat.png')
bomb_img = pygame.image.load('assets/images/meow.png')
space = pygame.image.load('assets/images/space.png')
background = pygame.image.load('assets/images/untitled.png')
lose = pygame.image.load('assets/images/lose.png')
win = pygame.image.load('assets/images/win.png')

# Sounds
meow = pygame.mixer.Sound('assets/sounds/meow.wav')
bark = pygame.mixer.Sound('assets/sounds/bark.wav')
oof = pygame.mixer.Sound('assets/sounds/oof.wav')
oof2 = pygame.mixer.Sound('assets/sounds/oof2.wav')

# Music
pygame.mixer.music.load('assets/music/opening.wav')
pygame.mixer.music.play()

# Restart
def restart():
        os.execv(sys.executable, ['python'] + sys.argv)


# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.use = False
        self.sheild = False

        self.speed = 5
        self.health = 5
        self.time2 = 1

    def move_left(self):
        self.rect.x -= self.speed
        
    def move_right(self):
        self.rect.x += self.speed

    def shoot_left(self):
        las = Laser(laser_img)
        
        las.rect.centerx = self.rect.x + (1/8)*self.rect.x
        las.rect.centery = self.rect.top

        bark.play()
        
        lasers.add(las)

    def shoot_right(self):
        las = Laser(laser_img)
        
        las.rect.centerx = self.rect.x + self.rect.width
        las.rect.centery = self.rect.top

        bark.play()
        
        lasers.add(las)

    def shoot_middle(self):
        las = Laser(laser_img)
        
        las.rect.centerx = self.rect.centerx
        las.rect.centery = self.rect.top

        bark.play()
        
        lasers.add(las)

    def update(self, bombs, fleet, image):
        self.image = image

        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width
            
        hit_list = pygame.sprite.spritecollide(self, bombs, True)

        if pygame.sprite.spritecollide(self, fleet, True):
            self.health = 0

        for hit in hit_list:
            if self.sheild or player.score >= 10:
                pass
            else:
                oof.play()
                self.health -= 1

        if self.health == 4:
            self.image = ship_img3_1

        if self.health == 3:
            self.image = ship_img3_2

        if self.health == 2:
            self.image = ship_img3_3

        if self.health == 1:
            self.image = ship_img3_4

        if self.sheild == True:
            self.image = ship_img2

        if self.health <= 0:
            oof2.play()
            self.kill()
            pygame.mixer.music.stop()            
            pygame.mixer.music.load('assets/music/lose_theme.wav')
            pygame.mixer.music.play()
            
class Laser(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        
        self.speed = 1

    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0-self.rect.height:
            self.kill()

    
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit = False

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
        
    def update(self, lasers):
        hit_list = pygame.sprite.spritecollide(self, lasers, True)

        if len(hit_list) > 0:
            meow.play()
            player.score += 1
            self.hit = True
            
        if self.rect.y <= 0-self.rect.height:
            self.kill()


class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        
        self.speed = 3

    def update(self):
        self.rect.y += self.speed

        if self.rect.y > HEIGHT:
            self.kill()


class Fleet:

    def __init__(self, mobs):
        self.mobs = mobs
        self.bomb_rate = 5
        self.speed = 5
        self.moving_right = True

    def move(self):
        reverse = False

        if self.moving_right:
            for m in mobs:
                if m.hit == False:
                    m.rect.x += self.speed
                    if m.rect.right >= WIDTH:
                        reverse = True
                else:
                    m.rect.y -= self.speed*2
        else:
            for m in mobs:
                if m.hit == False:
                    m.rect.x -= self.speed
                    if m.rect.left <= 0:
                        reverse = True
                else:
                    m.rect.y -= self.speed*2
                    

        if reverse:
            self.moving_right = not self.moving_right

            for m in mobs:
                m.rect.y += 32


    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()
        
        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None


    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()

    
# Make game objects
ship = Ship(100, 475, ship_img)
mob1 = Mob(100, 64, enemy_img)
mob2 = Mob(200, 64, enemy_img)
mob3 = Mob(300, 64, enemy_img)
mob4 = Mob(400, 64, enemy_img)
mob5 = Mob(500, 64, enemy_img)
mob6 = Mob(100, 184, enemy_img)
mob7 = Mob(200, 184, enemy_img)
mob8 = Mob(300, 184, enemy_img)
mob9 = Mob(400, 184, enemy_img)
mob10 = Mob(500, 184, enemy_img)

# Make sprite groups
player = pygame.sprite.Group()
player.add(ship)
player.score = 0

lasers = pygame.sprite.Group()

mobs = pygame.sprite.Group()
mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8, mob9, mob10)

bombs = pygame.sprite.Group()

# Make fleet
fleet = Fleet(mobs)

# Game loop
done = False

# Game helper functions
def show_stats(player, ship):
    if player.score < 10:
        score_text = myfont.render("youre score; " + str(player.score) + "/10", 1, what)
        screen.blit(score_text, [32, 10])
    else:
        score_text = myfont.render("youre winner !", 1, what)
        screen.blit(score_text, [32, 10])

    healths = myfont.render("youre sheild; " + str(ship.health), 1, what)
    screen.blit(healths, [32, 45])

def win_music():
    pygame.mixer.music.stop()
    pygame.mixer.music.load('assets/music/win_theme.wav')
    pygame.mixer.music.play()

while not done:
    what = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    # time based functions
    if ship.sheild == True:
        k += 1
        if k == 120:
            ship.sheild = False

    if player.score >= 10:
        s += 1
        if s == 120:
            win_music()
            stage2 = False
            stage3win = True
            score = 0

    if player.score == 9.9999999999:
        s += 1
        if s == 300:
            ship.health = 0

    if len(player) == 0 and player.score < 10:
        stage2 = False
        stage3lose = True
        
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN and stage2:
            if event.key == pygame.K_a and len(player) > 0:
                ship.shoot_left()
                shots += 1
            if event.key == pygame.K_d and len(player) > 0:
                ship.shoot_right()
                shots += 1
            if event.key == pygame.K_s and len(player) > 0:
                ship.shoot_middle()
                shots += 1

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_k] and stage1:
        stage1 = False
        stage2 = True
        pygame.mixer.music.stop()
        pygame.mixer.music.load('assets/music/battle.wav')
        pygame.mixer.music.play()


    if pressed[pygame.K_p] and stage2:
        for m in mobs:
            meow.play()
            m.kill()
            player.score = 9.9999999999

    if pressed[pygame.K_q]:
        if ship.use == False and stage2 == True:
            ship.sheild = True
            ship.use = True
            ship.health = 5


    if pressed[pygame.K_LEFT] and stage2:
        ship.move_left()


    elif pressed[pygame.K_RIGHT] and stage2:
        ship.move_right()
        
    
    # Game logic (Check for collisions, update points, etc.)
    if stage1 == True:
        pass

    if stage2 == True:
        player.update(bombs, mobs, ship_img)
        lasers.update()
        bombs.update()
        mobs.update(lasers)
        fleet.update()

    if stage3win == True:
        if pressed[pygame.K_r]:
            restart()

    if stage3lose == True:
        if pressed[pygame.K_r]:
            restart()

    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    if stage1 == True:
        screen.blit(background, (0,0))

    if stage2 == True:
        screen.blit(space, (0,0))
        lasers.draw(screen)
        bombs.draw(screen)
        player.draw(screen)
        mobs.draw(screen)
        show_stats(player, ship)

    if stage3win == True:
        screen.blit(win, (0,0))

        if shots < 10:
            shots = 10

        score_text = myfont.render("acurracie: " + str(round((10/shots)*100)) + "%", 1, what)
        screen.blit(score_text, [32, 10])

    if stage3lose == True:
        screen.blit(lose, (0,0))
    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
