import pygame
import os
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space shooter')

# load images
WIZARD = pygame.image.load(os.path.join("assets", "wizard.png"))
WIZARD = pygame.transform.scale(WIZARD, (80, 80))
SNIPER = pygame.image.load(os.path.join("assets", "sniper.png"))
SNIPER = pygame.transform.scale(SNIPER, (80, 80))
GOLEM = pygame.image.load(os.path.join("assets", "goliath.png"))
GOLEM = pygame.transform.scale(GOLEM, (80, 80))
FINAL_BOSS = pygame.image.load(os.path.join("assets", "finalboss.png"))
FINAL_BOSS = pygame.transform.scale(FINAL_BOSS, (130, 130))

# player character
PLAYER = pygame.image.load(os.path.join("assets", "player.png"))
PLAYER = pygame.transform.scale(PLAYER, (140, 80))

# bullets
WIZARD_BULLET = pygame.image.load(os.path.join("assets", "wizard_bullet.png"))
SNIPER_BULLET = pygame.image.load(os.path.join("assets", "sniper_bullet.png"))
GOLEM_BULLET = pygame.image.load(os.path.join("assets", "goliath_bullet.png"))
PLAYER_BULLET = pygame.image.load(os.path.join("assets", "player_bullet.png"))

# background
BG = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "background-black.png")),
    (WIDTH, HEIGHT)
)


class Bullet:
    def __init__(self, x, y, img, damage):
        self.x = x
        self.y = y
        self.img = img
        self.damage = damage
        # bullet speed maybe
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.x += vel

    def off_screen(self, width):
        return not (self.x < width and self.x >= 0)

    def collision(self, obj):
        return collide(self, obj)


# abstract class, health=optional
class Character:
    def __init__(self, x, y, health=10, cool_down=30):
        self.x = x
        self.y = y
        self.image = None
        self.bullet_img = None
        self.bullets = []
        self.poisons_recieved = 0
        self.health = health
        self.max_health = health
        self.cooldown_timer = 0
        self.cool_down = cool_down

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(window)

    def move_bullets(self, vel, obj):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.off_screen(WIDTH):
                self.bullets.remove(bullet)
            elif bullet.collision(obj):
                obj.health -= bullet.damage
                obj.add_poison(10)
                self.bullets.remove(bullet)

    def cooldown(self):
        if self.cooldown_timer >= self.cool_down:
            self.cooldown_timer = 0
        elif self.cooldown_timer > 0:
            self.cooldown_timer += 1

    def shoot(self):
        if self.cooldown_timer == 0:
            bullet = Bullet(self.x, self.y, self.bullet_img, 10)
            self.bullets.append(bullet)
            self.cooldown_timer = 1

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()

    def collision(self, obj):
        return collide(self, obj)


class Player(Character):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.image = PLAYER
        self.bullet_img = PLAYER_BULLET
        self.mask = pygame.mask.from_surface(self.image)

    def move_bullets(self, vel, objs):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.off_screen(WIDTH):
                self.bullets.remove(bullet)
            else:
                for obj in objs:
                    if bullet.collision(obj):
                        obj.health -= 10
                        if(obj.health <= 0):
                            objs.remove(obj)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),(self.x, self.y + self.image.get_height() + 10, self.image.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.image.get_height() + 10, self.image.get_width() * (self.health / self.max_health),10))
    
    def apply_poison(self):
        rate = 5/60 # 5 each second
        if(self.poisons_recieved > 0):
            self.poisons_recieved -= rate
            self.health -= rate

    def add_poison(self, posion):
        self.poisons_recieved += posion

class FinalBoss(Character):
    def __init__(self, x, y, health=200):
        super().__init__(x, y, health=health)
        self.speed = .45
        self.damage = 20
        self.poision_damage = 15
        self.image = FINAL_BOSS
        self.bullet_img = WIZARD_BULLET
        self.health = 200
        
        self.mask = pygame.mask.from_surface(self.image)
        self.nextY = 0
        self.spawnCooldown = 0
        self.cooldownCounter = 0
        self.cool_down = 40

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),(self.x, self.y + self.image.get_height() + 10, self.image.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.image.get_height() + 10, self.image.get_width() * (self.health / self.max_health),10))

    def move(self):
        # print(f"counter ${self.cooldownCounter} cooldown: ${self.spawnCooldown}")
        self.x -= self.speed
        if self.cooldownCounter < self.spawnCooldown:
            self.cooldownCounter += 1
        else:
            self.spawnCooldown = random.randrange(120, 240)
            self.cooldownCounter = 0
            self.y = random.randrange(self.image.get_height(), HEIGHT - self.image.get_height())
    

ENEMY_MAP = {
    "Wizard": {
        "speed": 1.5,
        "damage": 10,
        "poision_damage": 10, # 5 damage is delivered every second
        "image": WIZARD,
        "bullet_image": WIZARD_BULLET
    },
    "Goliath": {
        "speed": 1,
        "damage": 25,
        "poision_damage": 0,
        "image": GOLEM,  
        "bullet_image": GOLEM_BULLET  
    },
    "Sniper": {
        "speed": 2,
        "damage": 15,
        "poision_damage": 5,
        "image": SNIPER,
        "bullet_image": SNIPER_BULLET 
    },
    # "FinalBoss": {
    #     "health": 300,
    #     "speed": 0.5,
    #     "damage": 30,
    #     "poision_damage": 15,
    #     "image": FINAL_BOSS_IMAGE,  # Replace FINAL_BOSS_IMAGE with the actual image path
    #     "bullet_image": FINAL_BOSS_BULLET_IMAGE  # Replace FINAL_BOSS_BULLET_IMAGE with the actual image path
    # }
}


class Villain(Character):
    def __init__(self, x, y, type):
        super().__init__(x, y)
        self.speed = ENEMY_MAP[type]['speed']
        self.damage = ENEMY_MAP[type]['damage']
        self.poision_damage = ENEMY_MAP[type]['poision_damage']
        self.image = ENEMY_MAP[type]['image']
        self.bullet_img = ENEMY_MAP[type]['bullet_image']
        
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.x -= self.speed

    def collision(self, obj):
        return collide(self, obj)

    def shoot(self):
        if self.cooldown_timer == 0:
            bullet = Bullet(self.x, self.y, self.bullet_img, self.damage)
            self.bullets.append(bullet)
            self.cooldown_timer = 1


# mask is important for hitting an object on its pixels, the object isn't a square
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    FPS = 60  # how fast the game gors
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    won_font = pygame.font.SysFont("comicsans", 60)

    villains = []
    wave_length = 5  # how many villains each wave
    villain_speed = 1  # move speed, running 60 times a second so 1 unit per second

    player_vel = 5  # on each keypress move howmany pixels
    bullet_vel = 5 # bullet speed

    player = Player(300, 630, 100)

    clock = pygame.time.Clock()

    lost = False
    won = False
    lost_count = 0
    won_count = 0

    finalBossReleased = False
    randomShootingRange = 120 # 2 seconds (60FPS)

    def redraw_window():
        WIN.blit(BG, (0, 0))  # draw image
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for villain in villains:
            villain.draw(WIN)

        # each Character class draws its bullets and itself
        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!", 1, (255, 255, 255))
            WIN.blit(lost_label, ((WIDTH / 2) - lost_label.get_width(), 350))
        if won:
            won_label = won_font.render("You Won!", 1, (255, 255, 255))
            WIN.blit(won_label, ((WIDTH / 2) - won_label.get_width(), 350))

        pygame.display.update()  # render

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
            
        if lost:
            if lost_count > FPS * 3:  # 3 seconds
                run = False
        
        if won_count > FPS * 3:
            run = False
        

        # when beat the current wave of villains
        if level == 3:
            if finalBossReleased == False:
                finalBossReleased = True
                randomShootingRange = 80 # make shooting more often
                finalboss = FinalBoss(
                    random.randrange(850, 1500),
                    random.randrange(50, HEIGHT - 100),
                )
                villains.append(finalboss)
            elif len(villains) == 0:
                won_count += 1
                won = True
                
        elif len(villains) == 0:
            level += 1
            if level < 3:
                wave_length += 4
                for i in range(wave_length):
                    villain = Villain(
                        random.randrange(850, 1500),
                        random.randrange(50, HEIGHT - 100),
                        random.choice(['Wizard', 'Sniper', 'Goliath']) # chooses a random one
                    )
                    villains.append(villain)

        for event in pygame.event.get():  # pressing
            if event.type == pygame.QUIT:  # x in corner
                quit()  # quit the whole program

        keys = pygame.key.get_pressed()  # keys that are pressed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # left
            player.x = max(player.x - player_vel, 0)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # right
            player.x = min(player.x + player_vel, 750 - player.get_width())
        if keys[pygame.K_w] or keys[pygame.K_UP]:  # up
            player.y = max(player.y - player_vel, 0)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  # down
            player.y = min(player.y + player_vel, 750 - player.get_height() - 15)
        if keys[pygame.K_SPACE]:
            player.shoot()

        # for villain this just comes down
        for villain in villains[:]:  # make a copy so when u remove an villain from the actual list no errors occur
            villain.move_bullets(-bullet_vel, player)
            villain.move()

            # they shoot ab twice a second
            if random.randrange(0, randomShootingRange) == 1:
                villain.shoot()

            if collide(villain, player) and level != 3:
                villains.remove(villain)
                player.health -= 10
            elif villain.x < 0:
                if level == 3:
                    lost = True
                    lost_count += 1
                else:
                    lives -= 1  # our lives
                    villains.remove(villain)

        player.move_bullets(bullet_vel, villains)
        player.apply_poison()


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press the mouse to begin", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()