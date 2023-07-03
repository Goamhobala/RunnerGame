# runner_game.py
# link to the tutorial https://www.youtube.com/watch?v=AY9MnQ4x3zk
from sys import exit
from random import randint
import pygame
import character as ch

# class Movables(pygame.sprite.Sprite):

#     def __init__(self, path=str, paths=list):
#         super().__init__()
#         if paths:
#             #if there are mu


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.imgaes = {'walk1': 'Images/graphics/Player/player_walk_1.png',
                       'walk2': 'Images/graphics/Player/player_walk_2.png',
                       'jump': 'Images/graphics/Player/player_jump.png',
                       'stand': 'Images/graphics/Player/player_stand.png'}
        self.walking = [self.imgaes['walk1'], self.imgaes['walk2']]
        self.walking_index = 0
        self.image = self.walking[self.walking_index]
        self.rect = self.image.get_rect(bottomleft=(50, 300))
        self.vert_speed = 0

    def accelerate(self, time,  acceleration):
        speed = time * acceleration
        return speed

    def jump(self, height):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.vert_speed = self.accelerate(1, -height)

    def update_jump(self, time):
        if self.rect.bottom < 300:
            self.rect.y += (self.vert_speed -
                            self.accelerate(time, ))

        else:
            self.rect.bottom = 300

    def animation(self):
        if randint(0, 2):
            self.walking_index = 0
        else:
            self.walking_index = 1

    def update(self):
        self.jump(15)
        self.update_jump()

        # def jump(self, height):
        #     keys = pygame.key
        #     for k in keys:
        #         if pygame.get_pressed() == pygame.K_SPACE:
        #             self.rect.y += self.accelerate()


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


def main():

    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption('Nishino Nanase my waifu')
    clock = pygame.time.Clock()

    background_surface = pygame.image.load('Images/graphics/Sky.png').convert()
    floor_surface = pygame.image.load('Images/graphics/ground.png').convert()
    title_font = pygame.font.Font("font/Pixeltype.ttf", 72)
    smaller_font = pygame.font.Font("font/Pixeltype.ttf", 36)
    title_surface = title_font.render(
        "Nishino Nanase My Waifu", False, 'black')

    snail_surface = pygame.image.load(
        "Images/graphics/snail/snail1.png").convert_alpha()
    snail_rect = snail_surface.get_rect(midbottom=(800, 300))

    player_stand_surface = pygame.image.load(
        "Images/graphics/Player/player_stand.png").convert_alpha()
    player_stand_surface = pygame.transform.rotozoom(
        player_stand_surface, 0, 2)
    player_stand_rect = player_stand_surface.get_rect(
        center=(400, 200))

    player = ch.Player(50, 300, "Images/graphics/Player/player_walk_1.png")
    ground = 300

    player_surface = pygame.image.load(player.get_path()).convert_alpha()
    player_rect = player_surface.get_rect(bottomleft=player.get_pos())

    player_surface = pygame.image.load(
        "Images/graphics/Player/player_walk_1.png").convert_alpha()
    player_rect = player_surface.get_rect(bottomleft=(50, 300))
    restart_text_surface = title_font.render(
        "Pressed ESC to start!", False, 'black')

    start_time = 0
    ground = 300
    vert_speed = 0
    game_active = False
    score = 0

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # if event.type == pygame.MOUSEMOTION:
            #     if player_rect.collidepoint(event.pos):
            #         print("Fuck, it hurts!" + str(i))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(player_rect.bottom)
                    if player_rect.bottom == ground:
                        vert_speed += -15

                if event.key == pygame.K_ESCAPE and not game_active:
                    start_time = pygame.time.get_ticks() // 60
                    score_draw(screen, 0)
                    snail_rect.left = 800
                    vert_speed = 0
                    player_rect.bottom = ground
                    game_active = True

        if game_active:

            score = score_calc() - start_time

            if player_rect.midbottom[1] < ground:
                vert_speed += 0.6

            elif vert_speed > 0 and player_rect.midbottom[1] > ground:
                player_rect.bottom = 300
                vert_speed = 0

            player_rect.y += vert_speed

            screen.blit(background_surface, (0, 0))
            screen.blit(floor_surface, (0, 300))
            screen.blit(title_surface, (150, 100))
            screen.blit(player_surface, player_rect)
            score_draw(screen, score)
            if snail_rect.x < -100:
                snail_rect.left = 800

            else:
                snail_rect.left -= 4

            screen.blit(snail_surface, snail_rect)

            if snail_rect.colliderect(player_rect):
                game_active = False

        else:

            screen.fill((94, 129, 164))
            if score != 0:
                result_text_surface = title_font.render(
                    "Game Over!", False, 'black')

                score_summary_surface = title_font.render(
                    f"Score: {score}", False, "black")
                score_rect = score_summary_surface.get_rect(center=(400, 325))
                screen.blit(score_summary_surface, score_rect)

                restart_text_surface = smaller_font.render(
                    "Pressed ESC to restart!", False, 'black')

                restart_text_rect = restart_text_surface.get_rect(
                    center=(400, 375))

            else:
                result_text_surface = title_font.render(
                    "Welcome! ", False, 'black')

                restart_text_surface = title_font.render(
                    "Pressed ESC to start!", False, 'black')

                restart_text_rect = restart_text_surface.get_rect(
                    center=(400, 350))

            result_text_rect = result_text_surface.get_rect(
                center=(400, 50))

            screen.blit(restart_text_surface, restart_text_rect)
            screen.blit(player_stand_surface, player_stand_rect)
            screen.blit(result_text_surface, result_text_rect)

        clock.tick(60)
        pygame.display.update()


if __name__ == '__main__':
    main()
