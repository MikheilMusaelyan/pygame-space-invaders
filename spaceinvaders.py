import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space shooter')

# load images
RED_SPACESHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACESHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACESHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# player ship
YELLOW_SPACESHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# background
BG = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "background-black.png")),
    (WIDTH, HEIGHT)
)

# abstract class, health=optional
class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
    
    def draw(self, window):
        window.blit(self.ship_img (self.x, self.y))

        

def main():
    run = True
    FPS = 60 # how fast the game gors
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)

    player_vel = 5 # on each keypress move howmany pixels

    ship = Ship(300, 650)

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0, 0)) # draw image
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level, (WIDTH - level_label.get_width() - 10, 10))

        ship.draw(WIN)

        pygame.display.update() # render

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get(): # pressing
            if event.type == pygame.QUIT: # x in corner
                run = False

        keys = pygame.key.get_pressed() # keys that are pressed
        if keys[pygame.K_a]: # left
            ship.x = max(ship.x - player_vel, 0)
        if keys[pygame.K_d]: # right
            ship.x = min(ship.x + player_vel, 700) # -50
        if keys[pygame.K_w]: # up
            ship.y = max(ship.y - player_vel, 0)
        if keys[pygame.K_s]: # down
            ship.y = min(ship.y + player_vel, 700) # -50
main()