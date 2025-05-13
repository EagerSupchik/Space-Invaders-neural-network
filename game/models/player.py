import pygame
from pygame.locals import *
from game.models.bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = 800 // 2
        self.rect.bottom = 600 - 10
        self.speed = 8
        self.shoot_cooldown = 0

    def update(self, action=None):
        if action is None:
            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                self.rect.x -= self.speed
            if keys[K_RIGHT]:
                self.rect.x += self.speed
        else:
            if action == 0:
                self.rect.x -= self.speed
            elif action == 1:
                self.rect.x += self.speed
            
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
            
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 30
            return Bullet(self.rect.centerx, self.rect.top)
        return None