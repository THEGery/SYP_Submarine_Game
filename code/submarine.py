#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module represents the main submarine - the R.O.V.

What it does so far:
    Load an image and scale it; controll the movement of the R.O.V.
    A new method for the movement is planned...
"""

import pygame
import os

BASE_PATH = os.path.dirname(__file__)
SUB_PATH = r'..\art\assets\player'
TILE = 'player.png'
IMAGE_PATH = os.path.join(BASE_PATH, SUB_PATH, TILE)
print(IMAGE_PATH)

SCALE_FACTOR = 23 # 23


class Submarine(pygame.sprite.Sprite):
    """Submarine class; derives from the Sprite class."""

    def __init__(self, basepath: str, screen_size: tuple[int, int],
                 start_x: int, start_y: int, speed: int):
        """Call the parent class (Sprite) constructor."""
        super().__init__()
        
        # self.screen_size = screen_size
        self.screen_w = screen_size[0]
        self.screen_h = screen_size[1]
        self.speed = speed
        
        image_path = os.path.join(basepath, SUB_PATH, TILE)
        self.image_og = pygame.image.load(image_path).convert_alpha()
        size_tuple = self.image_og.get_size()
        image_og_width = size_tuple[0]
        image_og_height = size_tuple[1]
        display_area = self.screen_w * self.screen_h
        image_area = image_og_width * image_og_height
        image_conversion_ratio = display_area / (image_area * SCALE_FACTOR)
        print('display factor:', self.screen_w, self.screen_h)
        print('image size:', image_og_width, image_og_height)
        self.image = pygame.transform.scale(
            self.image_og,
            (image_og_width/image_conversion_ratio,
            image_og_height/image_conversion_ratio)
        )
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        print('rect:', self.rect.width, self.rect.height)


    def move_right(self, pixels):
        """Move character to the right."""
        self.rect.x += pixels

    def move_left(self, pixels):
        """Move character to the left."""
        self.rect.x -= pixels

    def move_forward(self, pixels):
        """Move character forward."""
        # self.rect.y += self.speed * speed / 20
        self.rect.y -= pixels

    def move_backward(self, pixels):
        """Move character backwards."""
        # self.rect.y -= self.speed * speed / 20
        self.rect.y += pixels

    def change_speed(self, speed):
        """Change the speed of the player character."""
        self.speed = speed
        
    def update(self):
        pass
