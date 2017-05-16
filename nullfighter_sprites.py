import pygame

class Ship(pygame.sprite.Sprite):

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.rect.x+= (self.x - self.rect.x) * .3
        self.rect.y+= (self.y - self.rect.y) * .3

    def move(self, x, y):
        self.x = x
        self.y = y
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.transform.scale(pygame.image.load("ship.png"), (80, 80))
        self.rect = self.image.get_rect()
        self.move(x, y)
        self.rect.x = self.x
        self.rect.y = self.y

class Bullet(pygame.sprite.Sprite):

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.rect.y-= 20

    def check_bounds(self, screen):
        return -self.rect.height > self.rect.y

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.transform.scale(pygame.image.load("ship_bullet.png"), (80, 80))
        self.rect = self.image.get_rect()
        self.move(x, y)

class Enemy(pygame.sprite.Sprite):

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.rect.x+= (self.x - self.rect.x) * .3
        self.rect.y+= (self.y - self.rect.y) * .3

    def move(self, x, y):
        self.x = x
        self.y = y

    def hit(self, bullet):
        return bullet.rect.colliderect(self.rect)
    
    def __init__(self, x, y, enemy_type):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load("enemy_" + str(enemy_type) + ".png"), (80, 80))
        self.rect = self.image.get_rect()
        self.move(x, y)
        self.rect.x = self.x
        self.rect.y = self.y

class Star(pygame.sprite.Sprite):

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.rect.y+= self.speed

    def check_bounds(self, screen):
        return self.rect.y > screen.get_height()

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def __init__(self, x, speed, size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load("star.png"), (size, size))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.move(x, 0)

class BasicParticle(pygame.sprite.Sprite):

    def draw(self, screen):
        screen.fill(self.color, self.rect)
        self.rect.x+= self.x_vel
        self.rect.y+= self.y_vel
        self.draw_count+= 1

    def check_bounds(self, screen):
        return self.draw_count > self.lifetime

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def __init__(self, x, y, x_vel, y_vel, lifetime, color):
        pygame.sprite.Sprite.__init__(self)

        self.color = color
        self.draw_count = 0
        self.rect = pygame.Rect(x, y, 3, 3)
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.lifetime = lifetime
