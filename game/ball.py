import pygame
import random
import os
import math
import array

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

        # Initialize sound effects with simple beeps
        try:
            pygame.mixer.init(44100, -16, 2, 512)
            # Create different pitched beep sounds
            self.paddle_sound = self._create_beep(1000, 20)  # Higher pitch, short duration
            self.wall_sound = self._create_beep(800, 20)     # Medium pitch, short duration
            self.score_sound = self._create_beep(600, 40)    # Lower pitch, longer duration
            
            # Set sound volumes
            self.paddle_sound.set_volume(0.3)
            self.wall_sound.set_volume(0.2)
            self.score_sound.set_volume(0.4)
        except:
            print("Warning: Could not initialize sounds")
            self.paddle_sound = self.wall_sound = self.score_sound = None

    def _create_beep(self, frequency, duration):
        """Create a simple beep sound"""
        sample_rate = 44100
        period = int(sample_rate / frequency)
        amplitude = 32767
        samples = array.array('h')

        # Generate a simple square wave
        for i in range(int(sample_rate * duration / 1000.0)):
            if (i % period) < period/2:
                samples.append(int(amplitude))
            else:
                samples.append(int(-amplitude))

        return pygame.mixer.Sound(buffer=samples)

    def move(self):
        # Store previous position for collision check
        prev_x = self.x
        prev_y = self.y
        
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wall collision
        if self.y <= 0:
            self.y = 0
            self.velocity_y *= -1
            self.wall_sound.play()
        elif self.y + self.height >= self.screen_height:
            self.y = self.screen_height - self.height
            self.velocity_y *= -1
            self.wall_sound.play()

    def check_collision(self, player, ai):
        # Create slightly larger collision rectangles for paddles
        player_extended = pygame.Rect(player.x - abs(self.velocity_x), 
                                    player.y, 
                                    player.width + abs(self.velocity_x) * 2, 
                                    player.height)
        
        ai_extended = pygame.Rect(ai.x - abs(self.velocity_x), 
                                ai.y, 
                                ai.width + abs(self.velocity_x) * 2, 
                                ai.height)
        
        ball_rect = self.rect()
        
        # Check collision with extended paddle areas
        if ball_rect.colliderect(player_extended) or ball_rect.colliderect(ai_extended):
            # Play paddle hit sound
            self.paddle_sound.play()
            
            # Reverse x velocity and add a small speed increase
            self.velocity_x *= -1.1  # Increases difficulty as game progresses
            
            # Adjust y velocity based on where the ball hits the paddle
            if ball_rect.colliderect(player_extended):
                relative_intersect_y = (player.y + (player.height/2)) - (self.y + (self.height/2))
                normalized_intersect = relative_intersect_y / (player.height/2)
                bounce_angle = normalized_intersect * 0.75  # Max 45-degree angle
                self.velocity_y = -bounce_angle * abs(self.velocity_x)

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
