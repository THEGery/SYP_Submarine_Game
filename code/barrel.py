# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 17:26:12 2026

@author: gerald
"""

# -*- coding: utf-8 -*-
"""This module represents the main submarine - the R.O.V.

So far it mainly consists of the Submarine class but everything
related to the main subject, the R.O.V., will be added here.
"""

import pygame
import os
import math

# BASE_PATH = os.path.dirname(__file__)
SUB_PATH = r'art\assets\obsticles'
TILE = 'barrel_obsticle.png'
# IMAGE_PATH = os.path.join(BASE_PATH, SUB_PATH, TILE)

SCALE_FACTOR = 25 # 2.5


class Barrel(pygame.sprite.Sprite):
    """Submarine class; derives from the Sprite class."""
    def __init__(self, basepath: str, screen_size: tuple[int, int],
                 start_x: int, start_y: int, speed: int, alpha_val: int=255):
        """Call the parent class (Sprite) constructor."""
        super().__init__()
        
        # self.screen_size = screen_size
        self.screen_w = screen_size[0]
        self.screen_h = screen_size[1]
        
        image_path = os.path.join(basepath, SUB_PATH, TILE)
        self.image_og = pygame.image.load(image_path).convert_alpha()
        size_tuple = self.image_og.get_size()
        image_og_width = size_tuple[0]
        image_og_height = size_tuple[1]
        display_area = self.screen_w * self.screen_h
        image_area = image_og_width * image_og_height
        image_conversion_ratio = display_area / (image_area * SCALE_FACTOR)
        # print('display factor:', self.screen_w, self.screen_h)
        # print('image size:', image_og_width, image_og_height)
        self.image = pygame.transform.scale(
            self.image_og,
            (image_og_width/image_conversion_ratio,
             image_og_height/image_conversion_ratio)
        )

        # # Initialise attributes of the submarine.
        # self.width = width
        # self.height = height
        # self.color = color
        self.speed = speed
        
        # --- Oszillations-Parameter ---
        # self.dt = delta_time # delta_time, 
        # Der feste Mittelpunkt, um den das Objekt oszilliert
        self.start_x = start_x
        
        # Maximale Auslenkung vom Mittelpunkt in Pixeln
        self.amplitude = 55
        
        # Set frequency (speed of movement)
        # higher frequency means more speed
        self.frequency = 3.0 # Hier als 3.0 (Radians pro Sekunde) gewählt
        
        # Akkumulator für die verstrichene Gesamtzeit
        self.time_elapsed = 0.0 

        # Draw the submarine (a rectangle!)
        # pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Fetch rectangle object which has the dimensions of the image
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.alpha_val = alpha_val
        
        pygame.Surface.set_alpha(self.image, self.alpha_val)

    def move_right(self, pixels):
        """Move character to the right."""
        self.rect.x += pixels
        # move while oscilating; looks weird
        # self.start_x += pixels

    def move_left(self, pixels):
        """Move character to the left."""
        self.rect.x -= pixels
        # move while oscilating; looks weird
        # self.start_x -= pixels

    def move_forward(self, speed_factor):
        """Move character forward."""
        self.rect.y += self.speed * speed_factor / 100

    def move_backward(self, speed_factor): 
        """Move character backwards."""
        move_factor = int(self.speed * speed_factor / 100)
        print(move_factor)
        self.rect.y -= move_factor

    def change_speed(self, speed):
        """Change the speed of the player character."""
        self.speed = speed

    def repaint(self, color):
        """Define color of the player character."""
        self.color = color
        pygame.draw.rect(self.image, self.color,
                         [0, 0, self.width, self.height])
        
    def oscillating_movement(self, dt):
        """
        Aktualisiert die X-Position basierend auf einer Sinuswelle.
        
        Args:
            dt (float): Die seit dem letzten Frame vergangene Zeit in Sekunden.
        """
        
        # 1. Zeit akkumulieren (time_elapsed ist jetzt die Zeit in Sekunden)
        self.time_elapsed += dt
        
        # 2. Den Sinuswert berechnen
        # math.sin(time * frequency) steuert die Welle
        sinus_value = math.sin(self.time_elapsed * self.frequency)
        
        # 3. Die Verschiebung berechnen
        verschiebung = self.amplitude * sinus_value
        
        # 4. Position setzen
        self.rect.x = self.start_x + verschiebung
        
    # Die Standard-Pygame-Update-Methode würde diese Logik aufrufen
    def update(self, dt):
        # ... (andere Update-Logik, z.B. Kollisions-Check)
        self.oscillating_movement(dt)
