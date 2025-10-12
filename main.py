import pygame

from simulation import Simulation
from people import Person, Genes
from sources import Source

from random import uniform, randint
from math import pi
from time import time

pygame.init()

clock = pygame.time.Clock()

sim = Simulation()

screen = pygame.display.set_mode((sim.screen_x,sim.screen_y))
pygame.display.set_caption("Evolution Simulation")

sim.people = [Person(x = randint(0,sim.world_x_size),
                 y = randint(0,sim.world_y_size),
                 direction = uniform(0,2*pi),
                 target = None,
                 genes = Genes(
                     uniform(2,8),
                     uniform(1,3),
                     uniform(0.1,0.2),
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

sim.sources = [Source(randint(0,sim.world_x_size),
                      randint(0,sim.world_y_size),
                      "food")
                      for i in range(100)]
#######temp

font1 = pygame.freetype.Font("font.otf", 24)

previous_time = time()
needed = 0
previous_needed = 0
graph_screen = 0
##############

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #Key Presses
    keys = pygame.key.get_pressed()

    if graph_screen != True:

        #Speed and zoom
        sim.move_speed = 20/(sim.zoom)

        if keys[pygame.K_w]:
            sim.camera_y -= sim.move_speed
        if keys[pygame.K_s]:
            sim.camera_y += sim.move_speed
        if keys[pygame.K_a]:
            sim.camera_x -= sim.move_speed
        if keys[pygame.K_d]:
            sim.camera_x += sim.move_speed
        if keys[pygame.K_e]:
            sim.zoom *= (1 + sim.zoom_speed)
        if keys[pygame.K_q]:
            sim.zoom /= (1 + sim.zoom_speed)
        if keys[pygame.K_r]:
            sim.zoom = 1
            sim.camera_x = sim.screen_x / 2
            sim.camera_y = sim.screen_y / 2
        if keys[pygame.K_LCTRL]:
            sim.FPS /= (1 + sim.zoom_speed)
        if keys[pygame.K_LSHIFT]:
            sim.FPS *= (1 + sim.zoom_speed)
        
        sim.FPS = max(30, min(10000, sim.FPS))
        sim.zoom = max(0.1, min(100, sim.zoom))
        
        #Main simulation

        current_time = time()
        frame_time = current_time - previous_time
        previous_time = current_time

        needed += frame_time
        if needed > 0.5:
            sim.FPS /= (1 + sim.zoom_speed)
        previous_needed = needed

        while needed >= 1/sim.FPS:
            sim.update_simulation()
            needed -= 1/sim.FPS

        sim.draw_simulation(screen)
        sim.draw_ui
        #########temp

        text_1, rect = font1.render(f"Speed: {sim.FPS}",  (0, 0, 0))
        text_2, rect = font1.render(f"Zoom:  {sim.zoom}",  (0, 0, 0))

        screen.blit(text_1, (50, 50))
        screen.blit(text_2, (50, 100))
        
        ############

    pygame.display.update()
    clock.tick(60)