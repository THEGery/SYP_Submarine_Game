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
    def __init__(self, screen_size: tuple, image: str, speed: float, alpha: bool=False):
        self.screen_size = screen_size
        self.image = image
        self.speed = speed
        (screen_width, screen_height) = self.screen_size

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
        self.rect = self.scaled_image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self._height = self.scaled_image.get_height()
        self._rect = self.scaled_image.get_rect().bottom
        self.scrolling = True


    @property
    def height(self):
        return self._height

    def scroll_slow_down():
        # pixels befor scroll stop, deceleration start
        SLOWDOWN_DISTANCE = 200

        # if distance > 0:
        #     if distance < SLOWDOWN_DISTANCE:


    def update(self, screen, last_image, last_img_height, y_offset, speed_factor: float, bg: bool=True):
        """
        Scroll background  and reset image after it leaves screen.
        
        Stops the scrolling when reached the last image, with a slow down.
        """

        # if already stopped, scrolling do nothing
        if not self.scrolling:
            return

        SLOWDOWN_DISTANCE = 300
        STOP_TRASHOLD = 60
        base_speed = self.speed * speed_factor
        stop_point = screen.get_height() - last_img_height
        distance = last_image.rect.y + y_offset + stop_point 

        if distance > STOP_TRASHOLD:
            if distance < SLOWDOWN_DISTANCE:
                factor = distance / SLOWDOWN_DISTANCE
                move_amount = base_speed * factor
            else:
                move_amount = base_speed

            move_amount = min(move_amount, distance)

            self.rect.y -= move_amount

            if not bg:
                if self.rect.y <= -self.rect.height:
                    self.rect.y += self.rect.height
        else:
            self.rect.y -= distance
            self.scrolling = False


    def draw_bg(self, screen, y_offset):
        screen.blit(self.scaled_image, (self.rect.x, self.rect.y + y_offset))


    def draw_mid(self, screen):
        screen.blit(self.scaled_image, (self.rect.x, self.rect.y))
        screen.blit(self.scaled_image, (self.rect.x, (self.rect.y + self.rect.height)))
        screen.blit(self.scaled_image, (self.rect.x, (self.rect.y + self.rect.height * 2)))


    def draw_bottom(self, screen, last_image, y_offset):
        screen.blit(self.scaled_image, (self.rect.x, self.rect.y + y_offset))
