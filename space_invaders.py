#!/usr/bin/env python3
"""
Vintage Space Invaders Game
A classic arcade-style space invader game built with pygame.
"""

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (vintage green-on-black aesthetic)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Player settings
PLAYER_SPEED = 5
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 30

# Bullet settings
BULLET_SPEED = 7
BULLET_WIDTH = 3
BULLET_HEIGHT = 10

# Enemy settings
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 30
ENEMY_SPEED = 2
ENEMY_DROP = 30

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        
    def move_left(self):
        self.x = max(0, self.x - self.speed)
        
    def move_right(self):
        self.x = min(SCREEN_WIDTH - self.width, self.x + self.speed)
        
    def draw(self, screen):
        # Draw a simple triangle ship
        points = [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ]
        pygame.draw.polygon(screen, GREEN, points)
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Bullet:
    def __init__(self, x, y, direction=1):
        self.x = x
        self.y = y
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.speed = BULLET_SPEED * direction
        
    def update(self):
        self.y -= self.speed
        
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def is_off_screen(self):
        return self.y < 0 or self.y > SCREEN_HEIGHT

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.speed = ENEMY_SPEED
        self.direction = 1
        
    def update(self):
        self.x += self.speed * self.direction
        
    def drop_down(self):
        self.y += ENEMY_DROP
        self.direction *= -1
        
    def draw(self, screen):
        # Draw a simple invader shape
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
        # Add some details
        pygame.draw.rect(screen, GREEN, (self.x + 5, self.y + 5, 10, 10))
        pygame.draw.rect(screen, GREEN, (self.x + self.width - 15, self.y + 5, 10, 10))
        pygame.draw.rect(screen, GREEN, (self.x + self.width // 2 - 5, self.y + self.height - 10, 10, 5))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
    def can_shoot(self):
        return random.random() < 0.0005  # Small chance each frame

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.reset_game()
        
    def reset_game(self):
        self.player = Player(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.score = 0
        self.game_over = False
        self.won = False
        
        # Create enemy grid
        for row in range(5):
            for col in range(10):
                x = 50 + col * (ENEMY_WIDTH + 10)
                y = 50 + row * (ENEMY_HEIGHT + 10)
                self.enemies.append(Enemy(x, y))
                
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    # Shoot bullet
                    bullet_x = self.player.x + self.player.width // 2 - BULLET_WIDTH // 2
                    bullet_y = self.player.y
                    self.bullets.append(Bullet(bullet_x, bullet_y, 1))
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
        return True
        
    def update(self):
        if self.game_over:
            return
            
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
            
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
                
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.enemy_bullets.remove(bullet)
                
        # Check bullet-enemy collisions
        for bullet in self.bullets[:]:
            bullet_rect = bullet.get_rect()
            for enemy in self.enemies[:]:
                if bullet_rect.colliderect(enemy.get_rect()):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    break
                    
        # Check bullet-player collisions
        player_rect = self.player.get_rect()
        for bullet in self.enemy_bullets[:]:
            if bullet.get_rect().colliderect(player_rect):
                self.game_over = True
                break
                
        # Update enemies
        should_drop = False
        for enemy in self.enemies:
            enemy.update()
            # Check if enemy hits side
            if enemy.x <= 0 or enemy.x >= SCREEN_WIDTH - enemy.width:
                should_drop = True
                
            # Enemy shooting
            if enemy.can_shoot():
                bullet_x = enemy.x + enemy.width // 2 - BULLET_WIDTH // 2
                bullet_y = enemy.y + enemy.height
                self.enemy_bullets.append(Bullet(bullet_x, bullet_y, -1))
                
        if should_drop:
            for enemy in self.enemies:
                enemy.drop_down()
                
        # Check if enemy reached player
        for enemy in self.enemies:
            if enemy.y + enemy.height >= self.player.y:
                self.game_over = True
                break
                
        # Check win condition
        if len(self.enemies) == 0:
            self.won = True
            self.game_over = True
            
    def draw(self):
        self.screen.fill(BLACK)
        
        if not self.game_over:
            # Draw game elements
            self.player.draw(self.screen)
            
            for bullet in self.bullets:
                bullet.draw(self.screen)
                
            for bullet in self.enemy_bullets:
                bullet.draw(self.screen)
                
            for enemy in self.enemies:
                enemy.draw(self.screen)
                
            # Draw score
            score_text = self.small_font.render(f"Score: {self.score}", True, GREEN)
            self.screen.blit(score_text, (10, 10))
        else:
            # Draw game over screen
            if self.won:
                game_over_text = self.font.render("YOU WIN!", True, GREEN)
                score_text = self.font.render(f"Final Score: {self.score}", True, GREEN)
            else:
                game_over_text = self.font.render("GAME OVER", True, RED)
                score_text = self.font.render(f"Final Score: {self.score}", True, GREEN)
                
            restart_text = self.small_font.render("Press R to Restart", True, WHITE)
            
            # Center the text
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(restart_text, restart_rect)
            
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
