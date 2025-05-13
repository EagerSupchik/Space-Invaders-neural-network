import pygame
import random
from game.models.bullet import EnemyBullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 120, 250))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.direction = 1
        self.shoot_cooldown = 0
        self.shoot_probability = 0.005

    def update(self):
        self.rect.x += self.speed * self.direction
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        if (self.shoot_cooldown == 0 and
            random.random() < self.shoot_probability):
            self.shoot_cooldown = 120
            return EnemyBullet(self.rect.centerx, self.rect.bottom)
        
        return None

    def set_shoot_probability(self, probability):
        self.shoot_probability = probability