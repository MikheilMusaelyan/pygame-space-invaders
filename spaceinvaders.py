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

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel
    
    def off_screen(self, height):
        return self.y < height and self.y >= 0
    
    def collision(self, obj):
        return collide(self, obj)


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

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACESHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACESHIP, RED_LASER),
        "blue": (BLUE_SPACESHIP, BLUE_LASER),
        "green": (GREEN_SPACESHIP, GREEN_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

# mask is important for hitting an object on its pixels, the object isn't a square
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 60 # how fast the game gors
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 5 # how many enemies each wave
    enemy_vel = 1 # move speed

    player_vel = 5 # on each keypress move howmany pixels

    player = Player(300, 650)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0)) # draw image
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
           lost_label = lost_font.render("You Lost!!", 1, (255, 255, 255))
           WIN.blit(lost_label, ((WIDTH / 2) - lost_label.get_width(), 350))

        pygame.display.update() # render

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        
        if lost:
            if lost_count > FPS * 3: # 3 seconds
                run = False
            else:
                continue
        
        # when beat the current wave of enemies
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(['red', 'blue', 'green']))
                enemies.append(enemy)

        for event in pygame.event.get(): # pressing
            if event.type == pygame.QUIT: # x in corner
                run = False

        keys = pygame.key.get_pressed() # keys that are pressed
        if keys[pygame.K_a]: # left
            player.x = max(player.x - player_vel, 0)
        if keys[pygame.K_d]: # right
            player.x = min(player.x + player_vel, 750 - player.get_width())
        if keys[pygame.K_w]: # up
            player.y = max(player.y - player_vel, 0)
        if keys[pygame.K_s]: # down
            player.y = min(player.y + player_vel, 750 - player.get_height())

        # for enemy this just comes down
        for enemy in enemies[:]: # make a copy so when u remove an enemy from the actual list no errors occur
            enemy.move(enemy_vel)

            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1 # our lives
                enemies.remove(enemy)
        
main()