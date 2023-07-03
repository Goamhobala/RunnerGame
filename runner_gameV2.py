# runner_gameV2.py
import sys
from random import randint
import pygame


class Asset(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, path=None, paths=None):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos

        if path:
            # if only one image
            self.image = path

        else:
            self.images = paths
            self.images_index = 0
            # self.image = pygame.image.load(
            #     self.images[self.images_index]).convert_alpha()
            self.image = self.images[self.images_index]

        self.rect = self.image.get_rect(midbottom=(x_pos, y_pos))

    def animation(self, speed):
        self.images_index += speed
        if int(self.images_index) >= len(self.images):
            self.images_index = 0
        else:
            self.image = self.images[int(self.images_index)]

# 'Images/graphics/Player/player_walk_2.png'


class Player(Asset):

    def __init__(self, x_pos, y_pos):
        walking = [pygame.image.load('Images/graphics/Player/player_walk_1.png').convert_alpha(),
                   pygame.image.load('Images/graphics/Player/player_walk_2.png').convert_alpha()]
        super().__init__(x_pos=x_pos, y_pos=y_pos, paths=walking)
        self.vert_speed = 0
        self.jumping_image = pygame.image.load(
            'Images/graphics/Player/player_jump.png')
        self.time_in_air = 0
        self.ground = y_pos

    def jump(self, height):
        '''
        This method sets the player's vert speed to the height arg
        and set the time in air to 1 for the calculation of gravity
        '''
        keys = pygame.key.get_pressed()
        if self.rect.bottom == self.ground and keys[pygame.K_SPACE]:
            self.vert_speed = -height
            self.time_in_air = 1

    def gravity(self, strength):
        '''
        This method calculates the vert accleration and updates the vert speed.
        '''
        if self.rect.bottom < self.ground:
            self.vert_speed += (self.time_in_air * strength)
            self.time_in_air += 0.1
        else:
            self.time_in_air = 0
            self.vert_speed = 0
            self.rect.bottom = self.ground

    def animation(self, speed):
        '''
        This method first check if the player is on the ground.
        If the player's on the ground then this method will increase the walking images index by 1
        and change the current image to the index
        If the player's above the ground, then this method will change the current image to
        jump
        '''
        if self.rect.bottom != self.ground:
            self.image = self.jumping_image
        else:
            super().animation(speed)

    def update(self):
        self.jump(30)
        self.rect.y += int(self.vert_speed)
        self.gravity(1.15)
        self.animation(0.1)


class Enemy(Asset):
    def __init__(self, x_pos, y_pos, ani_speed, move_speed=int):
        self.ground = 300
        if y_pos != self.ground:
            # then it's a flying enemy
            super().__init__(x_pos, y_pos, paths=[
                pygame.image.load('Images/graphics/Fly/Fly1.png').convert_alpha(), pygame.image.load('Images/graphics/Fly/Fly2.png').convert_alpha()])

        else:
            super().__init__(x_pos, y_pos, paths=[
                pygame.image.load('Images/graphics/snail/snail2.png').convert_alpha(), pygame.image.load('Images/graphics/snail/snail1.png').convert_alpha()])

        self.ani_speed = ani_speed
        self.move_speed = move_speed

    def move_hori(self):
        self.rect.x += self.move_speed

    def destroy(self):
        if self.rect.right < -50:
            self.kill()

    def update(self):
        self.destroy()
        self.move_hori()
        self.animation(self.ani_speed)

    # def animation(self, speed):
    #     super().animation(speed)


def enemy_spawn(lowest_freq, highest_freq):

    if randint(0, 1):  # True or False
        # Spawn a snail
        y_pos = 300
        move_speed = -8

    else:
        # Spawn a fly
        y_pos = 100
        move_speed = -10
    x_pos = randint(lowest_freq, highest_freq)
    enemy = Enemy(x_pos=x_pos, y_pos=y_pos,
                  ani_speed=0.1, move_speed=move_speed)
    enemy_group.add(enemy)


# class Text(pygame.sprite.Sprite):
#     def __init__(self, x_pos, y_pos, size):
#         super().__init__()
#         self.font = pygame.font.Font("font/Pixeltype.ttf", size)
#         self.x_pos = x_pos
#         self.y_pos = y_pos

# class Score(Text):
#     de

def draw_assets():
    win.blit(bg, (0, 0))
    player_group.update()
    player_group.draw(win)
    enemy_group.update()
    enemy_group.draw(win)


def collision():
    if pygame.sprite.spritecollide(player_group.sprite, enemy_group, False):
        game_active = False


def score_draw(screen, score):
    score_font = pygame.font.Font("font/Pixeltype.ttf", 36)
    score_surface = score_font.render(
        f"Score: {score} ", False, "black")
    score_rect = score_surface.get_rect(topright=(790, 25))
    screen.blit(score_surface, score_rect)


def score_calc():
    score = pygame.time.get_ticks() / 60
    score_show = int(score//1)
    return score_show


# Game
pygame.init()

win = pygame.display.set_mode((800, 400))

fps = pygame.time.Clock()

# Background
bg = pygame.image.load('Images/ina_in_a_background.png')


# Player
player_test = Player(100, 300)
player_group = pygame.sprite.GroupSingle()
player_group.add(player_test)

# Enemy
snail_test = Enemy(750, 300, 0.25, -5)
enemy_group = pygame.sprite.Group()
enemy_group.add(snail_test)
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 900)

game_active = True
# Game loop
while True:

    # When game is active
    if game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_test.jump(25)

            if event.type == enemy_timer:
                enemy_spawn(900, 1100)
        draw_assets()
        collision()

    pygame.display.update()
    fps.tick(60)
