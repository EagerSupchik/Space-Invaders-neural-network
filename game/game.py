import pygame
from pygame.locals import *

from game.models.player import Player
from game.models.enemy import Enemy
from game.models.bullet import EnemyBullet

class Game:
    def __init__(self, width=800, height=600):
        self.WIDTH = width
        self.HEIGHT = height
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.FPS = 60
        
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        
        self.score = 0
        self.game_over = False
        self.move_down_counter = 0
        
    def init_game(self):
        self.all_sprites.empty()
        self.enemies.empty()
        self.bullets.empty()
        self.enemy_bullets.empty()
        
        self.player = Player()
        self.all_sprites.add(self.player)
        
        for i in range(8):
            for j in range(4):
                enemy = Enemy(100 + i * 70, 50 + j * 50)
                enemy.set_shoot_probability(0.005)
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)
                
        return self.all_sprites, self.enemies, self.bullets, self.enemy_bullets, self.player
    
    def get_state(self):
        closest_enemy_x = self.WIDTH // 2
        closest_enemy_y = 0
        closest_bullet_x = self.WIDTH // 2
        closest_bullet_y = self.HEIGHT
        
        min_dist = float('inf')
        for enemy in self.enemies:
            dist = ((self.player.rect.centerx - enemy.rect.centerx) ** 2 + 
                    (self.player.rect.centery - enemy.rect.centery) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                closest_enemy_x = enemy.rect.centerx
                closest_enemy_y = enemy.rect.centery
                
        min_dist = float('inf')
        for bullet in self.enemy_bullets:
            dist = ((self.player.rect.centerx - bullet.rect.centerx) ** 2 + 
                    (self.player.rect.centery - bullet.rect.centery) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                closest_bullet_x = bullet.rect.centerx
                closest_bullet_y = bullet.rect.centery
                
        state = [
            self.player.rect.centerx / self.WIDTH,
            self.player.rect.centery / self.HEIGHT,
            closest_enemy_x / self.WIDTH,
            closest_enemy_y / self.HEIGHT,
            closest_bullet_x / self.WIDTH,
            closest_bullet_y / self.HEIGHT,
            len(self.enemies) / 32,
            len(self.enemy_bullets) / 10
        ]
        
        return state
    
    def update(self, action=None):
        if not self.game_over:
            if action is not None:
                if action == 0:
                    pass
                elif action == 1:
                    self.player.update(0)
                elif action == 2:
                    self.player.update(1)
            else:
                self.player.update()
            
            self.bullets.update()
            self.enemy_bullets.update()
            
            for enemy in self.enemies:
                result = enemy.update()
                if result is not None and isinstance(result, EnemyBullet):
                    self.all_sprites.add(result)
                    self.enemy_bullets.add(result)
            
            move_down = False
            for enemy in self.enemies:
                if enemy.rect.right >= self.WIDTH or enemy.rect.left <= 0:
                    move_down = True
                    break
            
            if move_down:
                self.move_down_counter += 1
                for enemy in self.enemies:
                    enemy.direction *= -1
                    enemy.rect.y += 20
                    
                    if enemy.rect.bottom >= self.player.rect.top:
                        self.game_over = True
                        return True
            
            hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
            for hit in hits:
                self.score += 10
            
            hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
            if hits:
                self.game_over = True
                return True
            
            if len(self.enemies) == 0:
                for i in range(8):
                    for j in range(4):
                        enemy = Enemy(100 + i * 70, 50 + j * 50)
                        self.all_sprites.add(enemy)
                        self.enemies.add(enemy)
        
        return False
    
    def draw(self, nn_playing=False, generation=1):
        self.screen.fill(self.BLACK)
        self.all_sprites.draw(self.screen)
        
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(text, (10, 10))
        
        if nn_playing:
            gen_text = font.render(f"Generation: {generation}", True, self.WHITE)
            self.screen.blit(gen_text, (10, 50))
        
        nn_text = font.render(f"NN: {'On' if nn_playing else 'Off'} (A to toggle)", True, self.WHITE)
        self.screen.blit(nn_text, (self.WIDTH - 300, 10))
        
        if self.game_over and not nn_playing:
            game_over_text = font.render("GAME OVER - R to restart", True, self.RED)
            self.screen.blit(game_over_text, (self.WIDTH//2 - 200, self.HEIGHT//2))
        
        pygame.display.flip()
        self.clock.tick(self.FPS) 