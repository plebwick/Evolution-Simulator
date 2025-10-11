import pygame

from people import Person, Genes
from simulation import Simulation

from random import uniform, randint
from math import pi
from time import time
clock = pygame.time.Clock()

pygame.init()

sim = Simulation()

screen = pygame.display.set_mode((sim.screen_x,sim.screen_y))
pygame.display.set_caption("Evolution Simulation")

people = [Person(x = randint(0,sim.world_x_size),
                 y = randint(0,sim.world_y_size),
                 direction = uniform(0,2*pi),
                 target = None,
                 genes = Genes(
                     uniform(0,100),
                     uniform(0,100),
                     uniform(0,100),
                     uniform(0,100),
                     uniform(0,100),
                     uniform(0,100),
                     uniform(0,100)),
                 age = 0,
                 postnatal_elapsed = None,
                 gestation_period = None,
                 satiety = 1000,
                 hydrated = 1000,
                 current_activity = None,
                 clock = 0)
                 for i in range(300)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    #Key Presses
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
        camera_y = screen_y / 2

    #Main simulation
    time = time.time()
    while time.time() - time < 1/FPS

    screen.fill("blue")

    for person in people: 
        person_size = 2
        person_x = ((person.x - camera_x) * zoom) + (sim.screen_x / 2)
        person_y = ((person.y - camera_y) * zoom) + (sim.screen_y / 2)
        pygame.draw.circle(screen, (255,255,255), (person_x, person_y), person_size*zoom)

    border_rect = pygame.Rect(((-camera_x * zoom) + sim.screen_x/2),((-camera_y * zoom) + sim.screen_y/2),round(sim.world_x_size*zoom),round(sim.world_y_size*zoom))
    pygame.draw.rect(screen, (255,255,255), border_rect, round(5*zoom))
    pygame.display.update()
    clock.tick()