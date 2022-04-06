# 22.02.22 
# Doodle Gaming
# Marshmallow RPG Game

# Import required libraries
import pygame
import random

# Initialize pygame library
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((1024, 600))
pygame.display.set_caption("Marshmallow Mania")

# Create player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.state = "Front"
        self.image = pygame.image.load("assets/hero" + self.state + ".png")
        self.rect = self.image.get_rect(topleft = (100, 200))

        self.speedX = 3
        self.speedY = 3
        self.directionX = 0
        self.directionY = 0

        self.poking = False

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.directionX = -1
            self.state = "Left"
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.directionX = 1
            self.state = "Right"
        else:
            self.directionX = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.directionY = -1
            self.state = "Back"
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.directionY = 1
            self.state = "Front"
        else:
            self.directionY = 0

    def poke(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.poking = True
        else:
            self.poking = False


    def update(self):
        self.move()
        self.poke()
        self.image = pygame.image.load("assets/hero" + self.state + ".png")

# Create an obstacle sprite
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([64, 64])
        self.image.fill((100, 100, 255))
        self.rect = self.image.get_rect(topleft = (x, y))

    def update(self, velX, velY):
        self.rect.x += velX
        self.rect.y += velY
        
# Create an enemy sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([64, 64])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft = (x, y))

    def update(self, velX, velY):
        self.rect.x += velX
        self.rect.y += velY

# Create Game class
class Game():
    def __init__(self):
        self.gameState = "play"
        self.velX = 0
        self.velY = 0

    def setUp(self):
        # Instantiate player
        self.player_group = pygame.sprite.GroupSingle()
        self.obstacle_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        player = Player()
        self.player_group.add(player)

        # Intsantiate obstacle
        for i in range(1, 11):
            obstacle = Obstacle(random.randint(1, 1000), random.randint(-500, 500))
            self.obstacle_group.add(obstacle)

        # Instantiate enemies
        for i in range(1, 11):
            enemy = Enemy(random.randint(1, 1000), random.randint(-500, 500))
            self.enemy_group.add(enemy)

    def scroll(self):
        player = self.player_group.sprite

        if player.rect.x > 896 and player.directionX > 0:
            self.velX = -3
            player.speedX = 0
        elif player.rect.x < 64 and player.directionX < 0:
            self.velX = 3
            player.speedX = 0
        else:
            player.speedX = 3
            self.velX = 0

        if player.rect.y > 472 and player.directionY > 0:
            self.velY = -3
            player.speedY = 0
        elif player.rect.y < 64 and player.directionY < 0:
            self.velY = 3
            player.speedY = 0
        else:
            player.speedY = 3
            self.velY = 0

    def v_collision(self):
        player = self.player_group.sprite

        player.rect.y += player.speedY * player.directionY
        for sprite in self.obstacle_group.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.directionY<0:
                    player.rect.top = sprite.rect.bottom
                elif player.directionY>0:
                    player.rect.bottom = sprite.rect.top

    def h_collision(self):
        player = self.player_group.sprite
        
        player.rect.x += player.speedX * player.directionX
        for sprite in self.obstacle_group.sprites():
                if sprite.rect.colliderect(player.rect):
                    if player.directionX<0:
                        player.rect.left = sprite.rect.right
                    elif player.directionX>0:
                        player.rect.right = sprite.rect.left
    
    def kill(self):
        player = self.player_group.sprite

        for sprite in self.enemy_group.sprites():
                if sprite.rect.colliderect(player.rect) and player.poking:
                    sprite.kill()

    def play(self):

        self.player_group.draw(screen)
        self.player_group.update()
        self.v_collision()
        self.h_collision()
        self.kill()

        self.obstacle_group.draw(screen)
        self.obstacle_group.update(self.velX, self.velY)

        self.enemy_group.draw(screen)
        self.enemy_group.update(self.velX, self.velY)

        self.scroll()

run = True

game = Game()
game.setUp()

while run:

    game.play()

    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    screen.fill((255, 200, 200))

pygame.quit()
