import pygame

from people import Person, Genes
from simulation import Simulation

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

#######temp

font1 = pygame.freetype.Font("font.otf", 24)

previous_time = time()
needed = 0
previous_needed = 0
##############

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    #Key Presses
    keys = pygame.key.get_pressed()

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
        for person in sim.people:
            person.move(sim)
        needed -= 1/sim.FPS

    screen.fill("blue")

    #########temp

    text_1, rect = font1.render(f"Speed: {sim.FPS}",  (0, 0, 0))
    text_2, rect = font1.render(f"Zoom:  {sim.zoom}",  (0, 0, 0))

    screen.blit(text_1, (50, 50))
    screen.blit(text_2, (50, 100))
    
    ############

    for person in sim.people: 
        person_size = person.genes.size
        person_x = ((person.x - sim.camera_x) * sim.zoom) + (sim.screen_x / 2)
        person_y = ((person.y - sim.camera_y) * sim.zoom) + (sim.screen_y / 2)
        pygame.draw.circle(screen, (255,255,255), (person_x, person_y), max(1,person_size*sim.zoom))

    border_rect = pygame.Rect(((-sim.camera_x * sim.zoom) + sim.screen_x/2),((-sim.camera_y * sim.zoom) + sim.screen_y/2),round(sim.world_x_size*sim.zoom),round(sim.world_y_size*sim.zoom))
    pygame.draw.rect(screen, (255,255,255), border_rect, max(1,round(5*sim.zoom)))

    pygame.display.update()
    clock.tick(60)