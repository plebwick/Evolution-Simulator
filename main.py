from math import sqrt, atan2, sin, cos, pi, e
from people import Person
from random import uniform, randint
import pygame, inspect
from sys import exit
import pyautogui, time
import pygame.freetype, cProfile, pstats
from line_profiler import LineProfiler
from main import world_y_size

clock = pygame.time.Clock()

screen_x = 2560
screen_y = 1440

world_x_size = 2560
world_y_size = 1440
pygame.init()
screen = pygame.display.set_mode((screen_x,screen_y))
pygame.display.set_caption("main")

camera_x = screen_x/2
camera_y = screen_y/2
zoom = 1

people = [Person(x = randint(0,world_x_size)
                 y = randint(0,world_y_size))
                 for i in range(300)]

for i in range(500000):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    move_speed = 5/zoom
    zoom_speed = 0.005

    if keys[pygame.K_UP]:
        camera_y -= move_speed
    if keys[pygame.K_DOWN]:
        camera_y += move_speed
    if keys[pygame.K_LEFT]:
        camera_x -= move_speed
    if keys[pygame.K_RIGHT]:
        camera_x += move_speed
    if keys[pygame.K_EQUALS] or keys[pygame.K_PLUS]:
        zoom *= (1 + zoom_speed)
    if keys[pygame.K_MINUS]:
        zoom /= (1 + zoom_speed)
    if keys[pygame.K_r]:
        zoom = 1
        camera_x = screen_x / 2
        camera_y = screen_y /2

    screen.fill("blue")

    for person in people: 
        person_size = 2
        person_x = ((person.x - camera_x) * zoom) + (screen_x / 2)
        person_y = ((person.y - camera_y) * zoom) + (screen_y / 2)
        pygame.draw.circle(screen, (255,255,255), (person_x, person_y), person_size*zoom)

    border_rect = pygame.Rect(((-camera_x * zoom) + screen_x/2),((-camera_y * zoom) + screen_y/2),round(world_x_size*zoom),round(world_y_size*zoom))
    pygame.draw.rect(screen, (255,255,255), border_rect, round(5*zoom))
    pygame.display.update()
    clock.tick()