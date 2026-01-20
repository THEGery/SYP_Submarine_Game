# -*- coding: utf-8 -*-
"""This is the main module where the game starts.

..module co-author:: Viktor Barath <viktor.barath7@gmail.com>
..module co-author:: Gerald Haueisen<>

Other modules, classes and functions neccessary for the game are imported and
can not be run on their own -> start the game here.
"""

import pygame
import random
import time
import os
import sys

from itertools import zip_longest

import tkinter as tk
from tkinter import messagebox

# Let's import the Submarine Class
from barrel import Barrel
from mine import Mine
# from obstacle import Obstacle
from submarine import Submarine
from background import Background

# BASE_PATH = os.path.dirname(__file__)
def resource_path(relative_path):
    """ Should find path, script or exe """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    # Wenn lokal: von /code/ eine Ebene hoch zum Hauptordner
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

BASE_PATH = resource_path("")




# game variables
scroll_speed = 1
speed_factor = 8 # old 5
speed_factor_max = 50 # old 15
speed_factor_min = 5 # old 3

# color_list = (RED, GREEN, PURPLE, YELLOW, CYAN, BLUE)


pygame.init()
#-------------------------------------
display_info = pygame.display.Info()
display_w = display_info.current_w
display_h = display_info.current_h
display_ratio = display_w / display_h

screen_width = display_w / 1.25
screen_height = display_h /1.25
screen_size = (screen_width, screen_height)
#-------------------------------------
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("The Adventures Of R.O.V.")


# instantiate background images and create bg list
background_layers_a = []
for image in range(1, 8):
    background = Background(screen_width, f'section_{image}.png', scroll_speed * 0.15)
    background_layers_a.append(background)

background_layers_b = []
for image in range(1, 7):
    background = Background(screen_width, f'transition_{image}.png', scroll_speed * 0.15)
    background_layers_b.append(background)

background_layers = []
for x, y in zip_longest(background_layers_a, background_layers_b):
    if x is not None:
        background_layers.append(x)
    if y is not None:
        background_layers.append(y)


# instantiate bottom images and create bg list
bottom_layers = []
for image in range(1, 4):
    background = Background(screen_width, f'cave_b_{image}.png', scroll_speed * 0.5, True)
    bottom_layers.append(background)

last_bg = background_layers[-1]


# instanciate background images and create midground list
midground_layers = [
    Background(screen_width, 'cave_1.png', scroll_speed * 0.5, True),
    Background(screen_width, 'cave_2.png', scroll_speed, True)
]


rov = Submarine(BASE_PATH, screen_size, 700, 150, 50)
# rov.rect.x = 460
# rov.rect.y = 100 # SCREENHEIGHT + 100

obstacle_1 = Barrel(BASE_PATH, screen_size, screen_width * 0.1,
                  screen_height * 0.9, random.randint(50, 100))
# obstacle_1.rect.x = 60
# obstacle_1.rect.y = +100

obstacle_2 = Barrel(BASE_PATH, screen_size, screen_width * 0.7,
                  screen_height * 0.7, random.randint(50, 100))
# obstacle_2.rect.x = 160
# obstacle_2.rect.y = +600
obstacle_3 = Mine(BASE_PATH, screen_size, screen_width * 0.4,
                  screen_height * 0.8, random.randint(50, 100))

# A list containing all the sprites we intend to use in the game
all_sprites_list = pygame.sprite.Group()
# Add the rov to the list of objects
all_sprites_list.add(rov)

all_coming_obstacles = pygame.sprite.Group()
all_coming_obstacles.add(obstacle_1)
all_coming_obstacles.add(obstacle_2)
all_coming_obstacles.add(obstacle_3)
# all_coming_obstacles.add(obstacle_4)


# Allowing the user to close the window...
carry_on = True
clock = pygame.time.Clock()
dt = 0

root = tk.Tk()
root.withdraw()

while carry_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carry_on = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                carry_on = False

    # polling vs event-triggered
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rov.move_left(7)
    if keys[pygame.K_RIGHT]:
        rov.move_right(7)
    if keys[pygame.K_UP]:
        if speed_factor > speed_factor_min:
            speed_factor -= 0.2
        # else: speed_factor += 0.0

    if keys[pygame.K_DOWN]:
        if speed_factor < speed_factor_max:
            speed_factor += 0.2
        # else: speed_factor -= 0.0

    print("Speed factor: ", speed_factor)

    # Game Logic
    for obstacle in all_coming_obstacles:
        obstacle.move_backward(speed_factor)
        if obstacle.rect.y < 0:
            obstacle.change_speed(random.randint(50, 100))
            # obstacle.repaint(random.choice(color_list))
            # obstacle.rect.y = +900
            obstacle.rect.y = screen_height + random.randint(50, 200)

    # Check if there is a obstacle collision
    obstacle_collision_list = pygame.sprite.spritecollide(
        rov, all_coming_obstacles, False)
    for obstacle in obstacle_collision_list:
        messagebox.showinfo("Game Over", "Obstacle crash!")
        carry_on = False
        break


    all_sprites_list.update()
    all_coming_obstacles.update(dt)


    # draw bg images
    for layer in background_layers:
        layer.update_bg(speed_factor)

    for i, layer in enumerate(background_layers):
        y_offset = i * layer.height
        layer.draw_bg(screen, y_offset=y_offset)
        # MAKE SURE LAYERS DESPAWN AFTER LEAVING SCREEN!
        
        # Prüfen, ob dieser Layer gerade im sichtbaren Bereich ist
        # (vereinfachte Logik: wenn der y_offset + layer_position innerhalb der screen_height liegt)
        if -layer.height < (layer.y + y_offset) < screen_height:
            print(f"Aktuell im Bild: Hintergrund Nr. {i}")


    # draw midground images
    for layer in midground_layers:
        layer.update(speed_factor)

    for layer in midground_layers:
        layer.draw_mid(screen)


    # draw bottom images
    for layer in bottom_layers:
        layer.update_bg(speed_factor)

    # for layer in bottom_layers:
    #     layer.draw_bottom(screen)


    # Actually it's items in the list: player plus 4 others
    all_sprites_list.draw(screen)
    all_coming_obstacles.draw(screen)

    # Refresh Screen
    pygame.display.flip()

    # Number of frames per secong e.g. 60
    # 1sec -> 1000ms; 1000ms/60=16.6ms; next loop starts after 16.6ms
    dt = clock.tick(60) / 1000
    print(f"[{time.strftime('%H:%M:%S')}] Hindernis-Reset durchgeführt!")

pygame.quit()
