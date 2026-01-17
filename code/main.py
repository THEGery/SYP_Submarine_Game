# -*- coding: utf-8 -*-
"""This is the main module where the game starts.

Other modules, classes and functions neccessary for the game are imported and
can not be run on their own -> start the game here.
"""

import pygame
import random
import time
import os
# Let's import the Submarine Class
from obstacle import Obstacle
from submarine import Submarine

BASE_PATH = os.path.dirname(__file__)

GREEN = (20, 255, 140)
GREY = (210, 210, 210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
BLUE = (100, 100, 255)

speed_factor = 5
speed_factor_max = 15
speed_factor_min = 3

color_list = (RED, GREEN, PURPLE, YELLOW, CYAN, BLUE)

SCREENWIDTH = 800
SCREENHEIGHT = 800
size = (SCREENWIDTH, SCREENHEIGHT)

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("The Adventures Of R.O.V.")

# Load bg images
# bg_01
SUB_PATH = r'..\art\assets\bg'
TILE = 'transition_01.png'
IMAGE_PATH = os.path.join(BASE_PATH, SUB_PATH, TILE)
bg_01 = pygame.image.load(IMAGE_PATH).convert()
# bg_02
SUB_PATH = r'..\art\assets\bg'
TILE = 'transition_02.png'
IMAGE_PATH = os.path.join(BASE_PATH, SUB_PATH, TILE)
bg_02 = pygame.image.load(IMAGE_PATH).convert()

# Load walls
SUB_PATH = r'..\art\assets\bg\cave'
TILE = 'cave_walls.png'
IMAGE_PATH = os.path.join(BASE_PATH, SUB_PATH, TILE)
wall_main = pygame.image.load(IMAGE_PATH)


rov = Submarine(BASE_PATH, size, 500, 150, 50)
# rov.rect.x = 460
# rov.rect.y = 100 # SCREENHEIGHT + 100

obstacle_1 = Obstacle(PURPLE, 60, 80, random.randint(60, 110), 80, 100)
# obstacle_1.rect.x = 60
# obstacle_1.rect.y = +100

obstacle_2 = Obstacle(YELLOW, 60, 80, random.randint(50, 100), 360, 600)
# obstacle_2.rect.x = 160
# obstacle_2.rect.y = +600

# obstacle_3 = Submarine(CYAN, 60, 80, random.randint(50, 100))
# obstacle_3.rect.x = 260
# obstacle_3.rect.y = +300

# obstacle_4 = Submarine(BLUE, 60, 80, random.randint(50, 100))
# obstacle_4.rect.x = 360
# obstacle_4.rect.y = +900

# A list containing all the sprites we intend to use in the game
all_sprites_list = pygame.sprite.Group()
# Add the rov to the list of objects
all_sprites_list.add(rov)
# all_sprites_list.add(obstacle_1)
# all_sprites_list.add(obstacle_2)
# all_sprites_list.add(obstacle_3)
# all_sprites_list.add(obstacle_4)

all_coming_obstacles = pygame.sprite.Group()
all_coming_obstacles.add(obstacle_1)
all_coming_obstacles.add(obstacle_2)
# all_coming_obstacles.add(obstacle_3)
# all_coming_obstacles.add(obstacle_4)


# Allowing the user to close the window...
carry_on = True
clock = pygame.time.Clock()
dt = 0

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
        if speed_factor < speed_factor_max:
            speed_factor += 0.2
        # else: speed_factor += 0.0
        
    if keys[pygame.K_DOWN]:
        if speed_factor > speed_factor_min:
            speed_factor -= 0.2
        # else: speed_factor -= 0.0
        
        
    print("Speed factor: ", speed_factor)

    # Game Logic
    for obstacle in all_coming_obstacles:
        obstacle.move_backward(speed_factor)
        if obstacle.rect.y < 0:
            obstacle.change_speed(random.randint(50, 100))
            obstacle.repaint(random.choice(color_list))
            # obstacle.rect.y = +900
            obstacle.rect.y = SCREENHEIGHT + random.randint(50, 200)

    # Check if there is a obstacle collision
    obstacle_collision_list = pygame.sprite.spritecollide(
        rov, all_coming_obstacles, False)
    for obstacle in obstacle_collision_list:
        print("obstacle crash!")
        # End Of Game
        carry_on = False


    all_sprites_list.update()
    all_coming_obstacles.update(dt)

    # Blit multiple images after one another
    screen.blits(((bg_01, [0, 0]), (bg_02, [0, 512])))
    # Draw wall
    screen.blit(wall_main)

    # Draw The Road
    # pygame.draw.rect(screen, GREY, [40, 0, 400, SCREENHEIGHT])
    # Draw Line painting on the road
    pygame.draw.line(screen, WHITE, [140, 0], [140, SCREENHEIGHT], 5)
    # Draw Line painting on the road
    pygame.draw.line(screen, WHITE, [240, 0], [240, SCREENHEIGHT], 5)
    # Draw Line painting on the road
    pygame.draw.line(screen, WHITE, [340, 0], [340, SCREENHEIGHT], 5)

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
