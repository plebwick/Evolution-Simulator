import pygame
from line_profiler import LineProfiler
from simulation import Simulation

from random import uniform, randint
from math import pi
from time import time

def main():
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
    current_screen = "sim"
    draw = "sim"
    ##############

    while True:
    #for i in range(1000):
        start_time = time()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    
        #Key Presses
        keys = pygame.key.get_pressed()

        if current_screen == "start":
            pass
        elif current_screen == "sim":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    #toggle pause
                    if event.key == pygame.K_SPACE:
                        if sim.FPS == 0:
                            previous_time = time()
                            sim.FPS = previous_fps
                        else:
                            previous_fps = sim.FPS
                            sim.FPS = 0

                    #toggle graph
                    if event.key == pygame.K_h:
                        if draw == "sim": 
                            draw = "graph"
                        elif draw == "graph": 
                            draw = "sim"

                    #toggle grid
                    if event.key == pygame.K_g:
                        if sim.toggle_grid: sim.toggle_grid = False
                        else: sim.toggle_grid = True

                    #toggle vision radius
                    if event.key == pygame.K_v:
                        if sim.toggle_vision_radius: sim.toggle_vision_radius = False
                        else: sim.toggle_vision_radius = True

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
                sim.FPS = max(60, min(6000, sim.FPS))
            if keys[pygame.K_LSHIFT]:
                sim.FPS *= (1 + sim.zoom_speed)
                sim.FPS = max(60, min(6000, sim.FPS))
            
            sim.zoom = max(0.1, min(50, sim.zoom))

            #Main simulation
            if sim.FPS:
                current_time = time()
                frame_time = current_time - previous_time
                previous_time = current_time

                needed += frame_time
                needed = min(needed,0.01)

                
                while needed >= 1/sim.FPS:
                    sim.update_simulation()
                    needed -= 1/sim.FPS

            if draw == "sim":
                sim.draw_simulation()
                sim.draw_ui(font)
            elif draw == "graph":
                sim.screen.fill("#843723")

        timer = time()-start_time
        stat, rect = font.render(f"{round(1/timer)}FPS",  (0, 0, 0))
        screen.blit(stat, (10, 10))

        if round(1/timer,2) > 60:
            sim.FPS *= (1.005)
        elif round(1/timer,2) < 60:
            sim.FPS /= (1.005)

        pygame.display.update()
        clock.tick(60)

main()