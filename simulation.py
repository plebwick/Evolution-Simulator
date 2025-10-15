import pygame, pyautogui
from random import randint, uniform
from math import pi
from sources import Source
from people import Person
from people import Genes
from collections import defaultdict
from time import time, perf_counter

class Simulation:
    def __init__(self):    
        self.people = []
        self.sources = []
        self.graphs = []

        self.FPS = 500
        self.screen_x = 2560
        self.screen_y = 1440
        self.world_x_size = 2560*4
        self.world_y_size = 1440*4
        self.camera_x = self.world_x_size/2
        self.camera_y = self.world_y_size/2
        self.zoom = 0.25
        self.move_speed = 20/(self.zoom)
        self.zoom_speed = 0.05

        self.grid = defaultdict(list)
        self.grid_size = 1

        self.day = 0
        self.year_length = 365
        self.mutation_rate = 1

        self.starting_population = 400

        total = 1000
        self.food_max = total/2
        self.water_max = total/2
        self.food_water_chance = 0.5

    def create_people(self):
        self.people = [Person(x = randint(0,self.world_x_size),
                 y = randint(0,self.world_y_size),
                 direction = uniform(0,2*pi),
                 target = None,
                 genes = Genes(
                     uniform(4,6),
                     uniform(0.25,1),
                     uniform(0.1,0.2),
                     uniform(0,100),
                     uniform(0,100),
                     uniform(0,100),
                     uniform(0,100),
                     uniform(0,100),
                     uniform(0,100)),
                 age = randint(0,100),
                 postnatal_elapsed = None,
                 gestation_period = None,
                 satiety = 1000,
                 hydrated = 1000,
                 current_activity = None
                 )
                 for i in range(self.starting_population)]
    
    def create_sources(self):
        self.sources = [Source(randint(0,self.world_x_size),
                      randint(0,self.world_y_size),
                      "food" if uniform(0,1) > self.food_water_chance else "water")
                      for i in range(100)]
        
    def update_simulation(self):
        t0 = perf_counter()
        Source.respawn(self)
        t1 = perf_counter()
        for person in self.people:
            person.step(self)
            person.decide_current_action(self)
            person.scan(self)
            person.wander(self)
        t2 = perf_counter()
        self.update_grid(self.sources + self.people)
        t3 = perf_counter()

        print(f"respawn={t1-t0:.4f}s | people={t2-t1:.4f}s | grid={t3-t2:.4f}s | total={t3-t0:.4f}s")

    def update_grid(self, objects):
        for grid_object in self.grid.values():
            grid_object.clear()
        #self.grid.clear()

        grid_size = self.grid_size
        grid = self.grid

        for object in objects:
            location = (int(object.x // grid_size), int(object.y // grid_size))
            grid[location].append(object)

    def check_grid(self, x, y):
        person_location = (int(x // self.grid_size), int(y // self.grid_size))
        return [object for object in self.grid[person_location] if object.x != x and object.y != y and isinstance(object, Source)]
    
    def display_grid(self, screen):
        for i in range(self.world_x_size//self.grid_size + 1):
            x = (i*self.grid_size - self.camera_x) * self.zoom + self.screen_x/2
            y1 = - self.camera_y * self.zoom + self.screen_y/2
            y2 = (self.world_y_size - self.camera_y) * self.zoom + self.screen_y/2
            pygame.draw.line(screen, (255,255,255), (x,y1), (x, y2), 1)

        for i in range(self.world_y_size//self.grid_size + 1):
            y = (i*self.grid_size - self.camera_y) * self.zoom + self.screen_y/2
            x1 = - self.camera_x * self.zoom + self.screen_x/2
            x2 = (self.world_x_size - self.camera_x) * self.zoom + self.screen_x/2
            pygame.draw.line(screen, (255,255,255), (x1,y), (x2, y), 1)

    def draw_simulation(self, screen):

        screen.fill("#5473ff")

        for person in self.people:
            person.draw(self, screen)

        for source in self.sources:
            source.draw(self, screen)

        border_rect = pygame.Rect(((-self.camera_x * self.zoom) + self.screen_x/2),((-self.camera_y * self.zoom) + self.screen_y/2),round(self.world_x_size*self.zoom),round(self.world_y_size*self.zoom))
        pygame.draw.rect(screen, (255,255,255), border_rect, max(1,round(5*self.zoom)))

    def draw_ui(self, screen, font):
        #self.display_grid(screen)
        text_1, rect = font.render(f"Speed: {self.FPS/60}",  (0, 0, 0))
        text_2, rect = font.render(f"Zoom:  {self.zoom}",  (0, 0, 0))
        mouse_pos = pyautogui.position()
        for person in self.people:
            person_x = ((person.x - self.camera_x) * self.zoom) + (self.screen_x / 2)
            person_y = ((person.y - self.camera_y) * self.zoom) + (self.screen_y / 2)
            if abs(mouse_pos[0] - person_x) < person.genes.size*self.zoom and abs(mouse_pos[1] - person_y) < person.genes.size*self.zoom:
                stat, rect = font.render(f"Current activity: {person.current_activity}",  (0, 0, 0))
                screen.blit(stat, (mouse_pos[0] + 10, mouse_pos[1] + 10))

                stat, rect = font.render(f"Direction: {person.direction}",  (0, 0, 0))
                screen.blit(stat, (mouse_pos[0] + 10, mouse_pos[1] + 30))

                stat, rect = font.render(f"Direction: {person.target.type}",  (0, 0, 0))
                screen.blit(stat, (mouse_pos[0] + 10, mouse_pos[1] + 50))
        
        screen.blit(text_1, (50, 50))
        screen.blit(text_2, (50, 100))