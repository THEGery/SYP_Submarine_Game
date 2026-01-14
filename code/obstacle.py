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

WHITE = (255, 255, 255)


class Obstacle(pygame.sprite.Sprite):
    """Submarine class; derives from the Sprite class."""

    def __init__(self, color, width, height, speed, start_x, start_y):
        """Call the parent class (Sprite) constructor."""
        super().__init__()

        # Instead we could load a proper pciture of a submarine...
        # self.image = pygame.image.load("submarine.png").convert_alpha()
        # BASE_PATH = os.path.dirname(__file__)
        # image_path = os.path.join(BASE_PATH, "..",
        #                           "art", "assets", "player", "player.png")
        # self.image = pygame.image.load(image_path)

        # Pass in color, x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        # Initialise attributes of the submarine.
        self.width = width
        self.height = height
        self.color = color
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
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Fetch rectangle object which has the dimensions of the image
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

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
