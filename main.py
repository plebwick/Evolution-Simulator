import pygame

from simulation import Simulation

from random import uniform, randint
from math import pi
from time import time

pygame.init()

clock = pygame.time.Clock()

sim = Simulation()

screen = pygame.display.set_mode((sim.screen_x,sim.screen_y))
pygame.display.set_caption("Evolution Simulation")

sim.create_people()
sim.create_sources()

#######temp

font = pygame.freetype.Font("font.otf", 24)

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
            sim.camera_x = sim.world_x_size/2
            sim.camera_y = sim.world_y_size/2
        if keys[pygame.K_LCTRL]:
            sim.FPS /= (1 + sim.zoom_speed)
            sim.FPS = max(60, min(3000, sim.FPS))
        if keys[pygame.K_LSHIFT]:
            sim.FPS *= (1 + sim.zoom_speed)
            sim.FPS = max(60, min(3000, sim.FPS))
        if keys[pygame.K_SPACE]:
            if sim.FPS == 0:
                previous_time = time()
                sim.FPS = previous_fps
            else:
                previous_fps = sim.FPS
                sim.FPS = 0
        
        sim.zoom = max(0.1, min(50, sim.zoom))

        #Main simulation
        if sim.FPS is not 0:
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
        sim.draw_ui(screen, font)
        #########temp
        
        ############

    pygame.display.update()
    clock.tick(60)