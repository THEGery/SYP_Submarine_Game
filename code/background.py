#!/usr/bin/env python3
"""
Module for the backgroun images.

..module author:: Viktor Barath <viktor.barath7@gmail.com>
"""

import pygame
import os

BASE_PATH = os.path.dirname(__file__)
SUB_PATH = r'..\art\assets\bg'


class Background(pygame.surface.Surface):
    def __init__(self, screen_width: int, image: str, speed: float, alpha: bool=False):
        self.screen_width = screen_width
        self.image = image
        self.speed = speed
        self.y = 0

        # import image with or without alpha
        image_path = os.path.join(BASE_PATH, SUB_PATH, self.image)
        if alpha:
            bg_image = pygame.image.load(image_path).convert_alpha()
        else:
            bg_image = pygame.image.load(image_path).convert()
        # loaded background image with or without alpha
        self.bg_image = bg_image

        bg_image_width, bg_image_height = self.bg_image.get_size()
        scale_factor = screen_width / bg_image_width
        new_height = int(bg_image_height * scale_factor)

        # bg_image scaled to the window width
        self.scaled_image = pygame.transform.scale(self.bg_image, (screen_width, new_height))
        self._height = self.scaled_image.get_height()
        self._rect = self.scaled_image.get_rect().bottom


    @property
    def height(self):
        return self._height


    @property
    def rect_bottom(self):
        return self._rect


    def update_bg(self, speed_factor: float):
        """Scroll background images."""
        self.y -= self.speed * speed_factor


    def update(self, speed_factor: float):
        """Scroll background  and reset image after it leaves screen."""
        self.update_bg(speed_factor)

        if self.y <= -self.height:
            self.y += self.height


    def draw_bg(self, screen, y_offset):
        screen.blit(self.scaled_image, (0, self.y + y_offset))
        # screen.blit(self.scaled_image, (0, self.y - self.height + y_offset))


    def draw_mid(self, screen):
        screen.blit(self.scaled_image, (0, self.y))
        screen.blit(self.scaled_image, (0, (self.y + self.height)))
        screen.blit(self.scaled_image, (0, (self.y + self.height * 2)))


    def draw_bottom(self, screen):
        screen.blit(self.scaled_image, (0, self.y))
