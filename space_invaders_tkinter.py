 #!/usr/bin/env python3
"""
Vintage Space Invaders Game (Tkinter Version)
A classic arcade-style space invader game built with tkinter.
No external dependencies required - works with standard Python!
"""

import tkinter as tk
import random
import math
import subprocess
import platform
import wave
import struct
import io
import threading

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
FRAME_DELAY = 1000 // FPS

# Colors (vintage green-on-black aesthetic)
BLACK = "#000000"
GREEN = "#00FF00"
WHITE = "#FFFFFF"
RED = "#FF0000"

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

# Barrier settings
BARRIER_WIDTH = 80
BARRIER_HEIGHT = 60
BARRIER_BLOCK_SIZE = 4  # Size of each pixel block
BARRIER_DAMAGE_RADIUS = 8  # Radius of damage when hit

# Sound settings
SOUND_ENABLED = True

class Player:
    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        self.canvas = canvas
        self.shape = None
        
    def move_left(self):
        self.x = max(0, self.x - self.speed)
        
    def move_right(self):
        self.x = min(SCREEN_WIDTH - self.width, self.x + self.speed)
        
    def draw(self):
        if self.shape:
            self.canvas.delete(self.shape)
        # Draw a simple triangle ship
        points = [
            self.x + self.width // 2, self.y,
            self.x, self.y + self.height,
            self.x + self.width, self.y + self.height
        ]
        self.shape = self.canvas.create_polygon(points, fill=GREEN, outline=GREEN)
        
    def get_rect(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)

class Bullet:
    def __init__(self, x, y, direction, canvas):
        self.x = x
        self.y = y
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.speed = BULLET_SPEED * direction
        self.canvas = canvas
        self.shape = None
        
    def update(self):
        self.y -= self.speed
        
    def draw(self):
        if self.shape:
            self.canvas.delete(self.shape)
        self.shape = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill=GREEN, outline=GREEN
        )
        
    def get_rect(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)
        
    def is_off_screen(self):
        return self.y < 0 or self.y > SCREEN_HEIGHT
        
    def cleanup(self):
        if self.shape:
            self.canvas.delete(self.shape)

class Enemy:
    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.speed = ENEMY_SPEED
        self.direction = 1
        self.canvas = canvas
        self.shapes = []
        
    def update(self):
        self.x += self.speed * self.direction
        
    def drop_down(self):
        self.y += ENEMY_DROP
        self.direction *= -1
        
    def draw(self):
        # Clean up old shapes
        for shape in self.shapes:
            self.canvas.delete(shape)
        self.shapes = []
        
        # Draw a simple invader shape
        self.shapes.append(self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill=GREEN, outline=GREEN
        ))
        # Add some details
        self.shapes.append(self.canvas.create_rectangle(
            self.x + 5, self.y + 5, self.x + 15, self.y + 15,
            fill=GREEN, outline=GREEN
        ))
        self.shapes.append(self.canvas.create_rectangle(
            self.x + self.width - 15, self.y + 5, self.x + self.width - 5, self.y + 15,
            fill=GREEN, outline=GREEN
        ))
        self.shapes.append(self.canvas.create_rectangle(
            self.x + self.width // 2 - 5, self.y + self.height - 10,
            self.x + self.width // 2 + 5, self.y + self.height - 5,
            fill=GREEN, outline=GREEN
        ))
        
    def get_rect(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)
        
    def can_shoot(self):
        return random.random() < 0.0005  # Small chance each frame
        
    def cleanup(self):
        for shape in self.shapes:
            self.canvas.delete(shape)

class Barrier:
    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y
        self.width = BARRIER_WIDTH
        self.height = BARRIER_HEIGHT
        self.canvas = canvas
        self.blocks = {}  # Dictionary of (bx, by) -> shape_id for active blocks
        self.shapes = []  # All canvas shapes for this barrier
        
        # Initialize barrier with a classic bunker shape
        self._create_barrier_shape()
        
    def _create_barrier_shape(self):
        """Create the initial barrier shape (classic arcade bunker)"""
        # Create a pixel-based barrier with a curved top
        # Calculate dimensions in blocks
        blocks_wide = self.width // BARRIER_BLOCK_SIZE
        blocks_high = self.height // BARRIER_BLOCK_SIZE
        center_x = blocks_wide // 2
        
        for by in range(blocks_high):
            for bx in range(blocks_wide):
                # Create curved top (parabolic arc)
                if by < blocks_high // 2:
                    # Arc shape - more blocks at edges, fewer in middle
                    dist_from_center = abs(bx - center_x)
                    # Create a smooth arc
                    arc_max = blocks_high // 2
                    if center_x > 0:
                        arc_height = int(arc_max - (dist_from_center ** 2) / (center_x * 1.5))
                    else:
                        arc_height = arc_max
                    if by < arc_height:
                        continue  # Skip blocks above the arc
                
                # Create sides with gaps (classic look)
                if bx < 3 or bx >= blocks_wide - 3:
                    if by > blocks_high * 0.6:
                        continue  # Open bottom sides
                
                # Add the block
                self.blocks[(bx, by)] = None
                
    def draw(self):
        # Clean up old shapes
        for shape in self.shapes:
            self.canvas.delete(shape)
        self.shapes = []
        
        # Draw all active blocks
        for (bx, by), _ in self.blocks.items():
            x1 = self.x + bx * BARRIER_BLOCK_SIZE
            y1 = self.y + by * BARRIER_BLOCK_SIZE
            x2 = x1 + BARRIER_BLOCK_SIZE
            y2 = y1 + BARRIER_BLOCK_SIZE
            
            shape = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=GREEN, outline=GREEN
            )
            self.blocks[(bx, by)] = shape
            self.shapes.append(shape)
            
    def check_collision(self, bullet_rect):
        """Check if bullet collides with barrier and damage it"""
        bx1, by1, bx2, by2 = bullet_rect
        
        # Check if bullet is in barrier's general area first
        if bx2 < self.x or bx1 > self.x + self.width or by2 < self.y or by1 > self.y + self.height:
            return False
        
        # Convert bullet rect to barrier block coordinates
        barrier_x1 = max(0, (bx1 - self.x) // BARRIER_BLOCK_SIZE)
        barrier_y1 = max(0, (by1 - self.y) // BARRIER_BLOCK_SIZE)
        barrier_x2 = min(self.width // BARRIER_BLOCK_SIZE - 1, (bx2 - self.x) // BARRIER_BLOCK_SIZE)
        barrier_y2 = min(self.height // BARRIER_BLOCK_SIZE - 1, (by2 - self.y) // BARRIER_BLOCK_SIZE)
        
        # Check all blocks in the bullet's area
        hit = False
        blocks_to_remove = set()  # Use set to avoid duplicates
        
        for bx in range(barrier_x1, barrier_x2 + 1):
            for by in range(barrier_y1, barrier_y2 + 1):
                if (bx, by) in self.blocks:
                    hit = True
                    # Remove blocks in a radius around the hit
                    for dx in range(-BARRIER_DAMAGE_RADIUS, BARRIER_DAMAGE_RADIUS + 1):
                        for dy in range(-BARRIER_DAMAGE_RADIUS, BARRIER_DAMAGE_RADIUS + 1):
                            if dx*dx + dy*dy <= BARRIER_DAMAGE_RADIUS * BARRIER_DAMAGE_RADIUS:
                                remove_x = bx + dx
                                remove_y = by + dy
                                if (remove_x, remove_y) in self.blocks:
                                    blocks_to_remove.add((remove_x, remove_y))
        
        # Remove damaged blocks
        for block_pos in blocks_to_remove:
            if block_pos in self.blocks:
                shape = self.blocks[block_pos]
                if shape:
                    self.canvas.delete(shape)
                    if shape in self.shapes:
                        self.shapes.remove(shape)
                del self.blocks[block_pos]
        
        return hit
        
    def get_rect(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)
        
    def cleanup(self):
        for shape in self.shapes:
            self.canvas.delete(shape)
        self.blocks.clear()
        self.shapes.clear()

def rects_collide(rect1, rect2):
    """Check if two rectangles collide"""
    x1, y1, x2, y2 = rect1
    x3, y3, x4, y4 = rect2
    return not (x2 < x3 or x4 < x1 or y2 < y3 or y4 < y1)

class SoundManager:
    """Manages sound effects for the game using system commands"""
    
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.system = platform.system()
        self.enemy_step_counter = 0
        
    def _generate_tone(self, frequency, duration, sample_rate=44100):
        """Generate a simple tone as WAV data"""
        num_samples = int(duration * sample_rate)
        samples = []
        for i in range(num_samples):
            # Generate sine wave
            value = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * i / sample_rate))
            samples.append(struct.pack('<h', value))
        return b''.join(samples)
    
    def _generate_laser_sound(self, duration=0.08, sample_rate=44100):
        """Generate a realistic laser/shooting sound with frequency sweep"""
        num_samples = int(duration * sample_rate)
        samples = []
        
        for i in range(num_samples):
            t = i / sample_rate
            progress = t / duration
            
            # Frequency sweep: start high, drop quickly (laser "pew" effect)
            start_freq = 1200
            end_freq = 400
            current_freq = start_freq - (start_freq - end_freq) * (progress ** 0.5)
            
            # Amplitude envelope: quick attack, exponential decay
            if progress < 0.1:
                amplitude = progress * 10  # Quick attack
            else:
                amplitude = math.exp(-(progress - 0.1) * 8)  # Exponential decay
            
            # Generate tone with harmonics for richer sound
            value = 0
            # Fundamental
            value += math.sin(2 * math.pi * current_freq * t)
            # Add some harmonics
            value += 0.3 * math.sin(2 * math.pi * current_freq * 2 * t)
            value += 0.15 * math.sin(2 * math.pi * current_freq * 3 * t)
            
            # Apply envelope
            value *= amplitude * 0.25
            
            # Convert to 16-bit
            samples.append(struct.pack('<h', int(32767 * value)))
        
        return b''.join(samples)
    
    def _generate_impact_sound(self, duration=0.12, sample_rate=44100):
        """Generate a realistic impact/thud sound for barrier hits"""
        num_samples = int(duration * sample_rate)
        samples = []
        
        for i in range(num_samples):
            t = i / sample_rate
            progress = t / duration
            
            # Low frequency thud with noise component
            base_freq = 150 - (progress * 50)  # Frequency drops
            
            # Amplitude envelope: very quick attack, fast decay
            if progress < 0.05:
                amplitude = progress * 20  # Very quick attack
            else:
                amplitude = math.exp(-(progress - 0.05) * 12)  # Fast decay
            
            # Generate low thud tone
            value = math.sin(2 * math.pi * base_freq * t)
            # Add lower harmonic for depth
            value += 0.4 * math.sin(2 * math.pi * base_freq * 0.5 * t)
            
            # Add some noise for impact texture (high frequency component)
            noise = (random.random() - 0.5) * 0.3
            noise *= math.exp(-progress * 15)  # Noise decays quickly
            value += noise
            
            # Apply envelope
            value *= amplitude * 0.3
            
            # Convert to 16-bit
            samples.append(struct.pack('<h', int(32767 * value)))
        
        return b''.join(samples)
    
    def _play_wav_data(self, wav_data):
        """Play WAV data using system commands"""
        if not self.enabled:
            return
            
        try:
            # Create a temporary WAV file in memory
            wav_file = io.BytesIO()
            with wave.open(wav_file, 'wb') as wf:
                wf.setnchannels(1)  # Mono
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(44100)
                wf.writeframes(wav_data)
            
            wav_file.seek(0)
            
            # Play using system command
            if self.system == 'Darwin':  # macOS
                # Write to temp file and play
                import tempfile
                import os
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                    tmp.write(wav_file.read())
                    tmp_path = tmp.name
                subprocess.Popen(['afplay', tmp_path], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
                # Clean up after a delay
                def cleanup():
                    try:
                        os.remove(tmp_path)
                    except:
                        pass
                threading.Timer(1.0, cleanup).start()
            elif self.system == 'Linux':
                subprocess.Popen(['aplay', '-q', '-'], 
                               input=wav_file.read(),
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
            elif self.system == 'Windows':
                import tempfile
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                    tmp.write(wav_file.read())
                    tmp_path = tmp.name
                subprocess.Popen(['powershell', '-c', f'(New-Object Media.SoundPlayer "{tmp_path}").PlaySync(); Remove-Item "{tmp_path}"'],
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
        except Exception:
            # Silently fail if sound can't be played
            pass
    
    def play_shoot(self):
        """Play realistic laser/shooting sound"""
        if not self.enabled:
            return
        # Realistic laser sound with frequency sweep
        sound = self._generate_laser_sound(0.08)
        threading.Thread(target=self._play_wav_data, args=(sound,), daemon=True).start()
    
    def play_barrier_hit(self):
        """Play realistic impact/thud sound for barrier hits"""
        if not self.enabled:
            return
        # Realistic impact sound with low frequency thud and noise
        sound = self._generate_impact_sound(0.12)
        threading.Thread(target=self._play_wav_data, args=(sound,), daemon=True).start()
    
    def play_enemy_move(self):
        """Play enemy movement sound - classic space invader marching sound"""
        if not self.enabled:
            return
        self.enemy_step_counter += 1
        # Classic space invader sound: alternating between two tones
        if self.enemy_step_counter % 2 == 0:
            frequency = 200
        else:
            frequency = 150
        # Very short beep for marching effect
        tone = self._generate_tone(frequency, 0.05)
        threading.Thread(target=self._play_wav_data, args=(tone,), daemon=True).start()

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Space Invaders")
        self.root.resizable(False, False)
        
        self.canvas = tk.Canvas(
            self.root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT,
            bg=BLACK, highlightthickness=0
        )
        self.canvas.pack()
        
        self.score_text = None
        self.keys_pressed = set()
        self.sound_manager = SoundManager(SOUND_ENABLED)
        self.enemy_move_counter = 0
        self.reset_game()
        
        # Bind events
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.root.focus_set()
        
    def reset_game(self):
        # Clean up old game objects
        if hasattr(self, 'barriers'):
            for barrier in self.barriers:
                barrier.cleanup()
        self.canvas.delete("all")
        
        self.player = Player(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, SCREEN_HEIGHT - 50, self.canvas)
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.barriers = []
        self.score = 0
        self.game_over = False
        self.won = False
        
        # Create enemy grid
        for row in range(5):
            for col in range(10):
                x = 50 + col * (ENEMY_WIDTH + 10)
                y = 50 + row * (ENEMY_HEIGHT + 10)
                self.enemies.append(Enemy(x, y, self.canvas))
        
        # Create 3 barriers in front of player
        barrier_y = SCREEN_HEIGHT - 150
        barrier_spacing = SCREEN_WIDTH // 4
        for i in range(3):
            barrier_x = barrier_spacing + i * barrier_spacing - BARRIER_WIDTH // 2
            self.barriers.append(Barrier(barrier_x, barrier_y, self.canvas))
        
        self.score_text = self.canvas.create_text(
            10, 10, anchor="nw", text=f"Score: {self.score}",
            fill=GREEN, font=("Courier", 16)
        )
        
    def on_key_press(self, event):
        self.keys_pressed.add(event.keysym)
        if event.keysym == "space" and not self.game_over:
            # Shoot bullet
            bullet_x = self.player.x + self.player.width // 2 - BULLET_WIDTH // 2
            bullet_y = self.player.y
            self.bullets.append(Bullet(bullet_x, bullet_y, 1, self.canvas))
            self.sound_manager.play_shoot()
        elif event.keysym.lower() == "r" and self.game_over:
            self.reset_game()
            
    def on_key_release(self, event):
        self.keys_pressed.discard(event.keysym)
        
    def quit(self):
        self.root.quit()
        self.root.destroy()
        
    def update(self):
        if self.game_over:
            return
            
        # Handle player movement
        if "Left" in self.keys_pressed or "a" in self.keys_pressed:
            self.player.move_left()
        if "Right" in self.keys_pressed or "d" in self.keys_pressed:
            self.player.move_right()
            
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                bullet.cleanup()
                self.bullets.remove(bullet)
            else:
                bullet.draw()
                
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                bullet.cleanup()
                self.enemy_bullets.remove(bullet)
            else:
                bullet.draw()
                
        # Check bullet-barrier collisions (player bullets)
        for bullet in self.bullets[:]:
            bullet_rect = bullet.get_rect()
            for barrier in self.barriers:
                if barrier.check_collision(bullet_rect):
                    bullet.cleanup()
                    self.bullets.remove(bullet)
                    barrier.draw()  # Redraw barrier with damage
                    self.sound_manager.play_barrier_hit()
                    break
            else:
                continue
            break  # Bullet was destroyed, move to next bullet
            
        # Check bullet-barrier collisions (enemy bullets)
        for bullet in self.enemy_bullets[:]:
            bullet_rect = bullet.get_rect()
            for barrier in self.barriers:
                if barrier.check_collision(bullet_rect):
                    bullet.cleanup()
                    self.enemy_bullets.remove(bullet)
                    barrier.draw()  # Redraw barrier with damage
                    self.sound_manager.play_barrier_hit()
                    break
            else:
                continue
            break  # Bullet was destroyed, move to next bullet
        
        # Check bullet-enemy collisions
        for bullet in self.bullets[:]:
            bullet_rect = bullet.get_rect()
            for enemy in self.enemies[:]:
                if rects_collide(bullet_rect, enemy.get_rect()):
                    bullet.cleanup()
                    enemy.cleanup()
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 10
                    self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
                    break
                    
        # Check bullet-player collisions
        player_rect = self.player.get_rect()
        for bullet in self.enemy_bullets[:]:
            if rects_collide(bullet.get_rect(), player_rect):
                self.game_over = True
                break
                
        # Update enemies
        should_drop = False
        enemies_moved = False
        for enemy in self.enemies:
            enemy.update()
            enemies_moved = True
            # Check if enemy hits side
            if enemy.x <= 0 or enemy.x >= SCREEN_WIDTH - enemy.width:
                should_drop = True
                
            # Enemy shooting
            if enemy.can_shoot():
                bullet_x = enemy.x + enemy.width // 2 - BULLET_WIDTH // 2
                bullet_y = enemy.y + enemy.height
                self.enemy_bullets.append(Bullet(bullet_x, bullet_y, -1, self.canvas))
        
        # Play enemy movement sound (classic marching sound)
        # Play sound every few frames to create the marching rhythm
        if enemies_moved:
            self.enemy_move_counter += 1
            # Play sound every 8 frames (adjust for desired rhythm)
            if self.enemy_move_counter % 8 == 0:
                self.sound_manager.play_enemy_move()
                
        if should_drop:
            for enemy in self.enemies:
                enemy.drop_down()
            # Play sound when enemies drop down
            self.sound_manager.play_enemy_move()
                
        # Check if enemy reached player
        for enemy in self.enemies:
            if enemy.y + enemy.height >= self.player.y:
                self.game_over = True
                break
                
        # Check win condition
        if len(self.enemies) == 0:
            self.won = True
            self.game_over = True
            
        # Draw barriers
        for barrier in self.barriers:
            barrier.draw()
        
        # Draw player
        self.player.draw()
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw()
            
    def draw_game_over(self):
        self.canvas.delete("all")
        if self.won:
            text_color = GREEN
            message = "YOU WIN!"
        else:
            text_color = RED
            message = "GAME OVER"
            
        self.canvas.create_text(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
            text=message, fill=text_color, font=("Courier", 36)
        )
        self.canvas.create_text(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
            text=f"Final Score: {self.score}", fill=GREEN, font=("Courier", 24)
        )
        self.canvas.create_text(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
            text="Press R to Restart", fill=WHITE, font=("Courier", 16)
        )
        
    def game_loop(self):
        if self.game_over:
            self.draw_game_over()
        else:
            self.update()
            
        self.root.after(FRAME_DELAY, self.game_loop)
        
    def run(self):
        self.game_loop()
        self.root.mainloop()

if __name__ == "__main__":
    game = Game()
    game.run()
