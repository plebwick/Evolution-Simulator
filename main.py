import pygame
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
    sim.create_graphs()

    #######temp

    previous_time = time()
    needed = 0 
    current_screen = "sim"
    draw = "sim"
    ##############

    while True:
    #for i in range(1000):
        start_time = time()
        sim.events = pygame.event.get()
        sim.keys = pygame.key.get_pressed()

        for event in sim.events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    
        #Key Presses

        if current_screen == "start":
            pass
        elif current_screen == "sim":
            for event in sim.events:
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

            sim.simulation_inputs()

            #Main simulation
            if sim.FPS:
                current_time = time()
                frame_time = current_time - previous_time
                previous_time = current_time

                needed += frame_time
                needed = min(needed,0.05)

                
                while needed >= 1/sim.FPS:
                    sim.update_simulation()
                    needed -= 1/sim.FPS

            if draw == "sim":
                sim.draw_simulation()
                sim.draw_simulation_ui()
            elif draw == "graph":
                sim.graph_inputs()
                sim.draw_graphs()
                sim.draw_graph_ui()

        timer = time()-start_time

        sim.draw_text(10, 20, round(1/timer), "FPS", place = "left")

        if round(1/timer,2) > 60:
            sim.FPS *= (1.005)
        elif round(1/timer,2) < 60:
            sim.FPS /= (1.005)

        pygame.display.update()
        clock.tick(60)

main()