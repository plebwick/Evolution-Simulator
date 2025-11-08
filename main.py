import pygame
from simulation import Simulation

from random import uniform, randint
from math import pi
import time

def main():
    pygame.init()

    clock = pygame.time.Clock()

    sim = Simulation()

    screen = pygame.display.set_mode((sim.screen_x,sim.screen_y))
    pygame.display.set_caption("Evolution Simulation")

    sim.create_people()
    sim.create_sources()
    sim.create_graphs()

    previous_time = time.perf_counter()
    needed = 0 
    current_screen = "sim"
    draw = "sim"

    while True:
        FPS_time = time.perf_counter()
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
                            previous_time = time.perf_counter()
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

            if sim.keys[pygame.K_LCTRL]:
                sim.FPS /= (1 + sim.zoom_speed)
                sim.FPS = max(60, min(60000, sim.FPS))
            if sim.keys[pygame.K_LSHIFT]:
                sim.FPS *= (1 + sim.zoom_speed)
                sim.FPS = max(60, min(60000, sim.FPS))

            #Main simulation
            if sim.FPS:
                current_time = time.perf_counter()
                frame_time = current_time - previous_time
                previous_time = current_time

                needed += frame_time
                needed = min(needed,1/60)

                while needed >= 1/sim.FPS:
                    sim.update_simulation()
                    needed -= 1/sim.FPS

            if draw == "sim":
                sim.simulation_inputs()

                sim.draw_simulation()
                sim.draw_simulation_ui()
            elif draw == "graph":
                sim.graph_inputs()

                sim.draw_graphs()
                sim.draw_graph_ui()

        FPS_time = time.perf_counter()-FPS_time

        sim.draw_text(10, 20, f"{round(1/FPS_time)} FPS", place = "left")

        if False:
            if round(1/FPS_time,2) > 60:
                sim.FPS *= (1.005)
            elif round(1/FPS_time,2) < 60:
                sim.FPS /= (1.005)

        pygame.display.update()
        clock.tick(60)

main()