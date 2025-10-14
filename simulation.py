import pygame, pyautogui
from random import randint, uniform
from math import pi
from sources import Source
from people import Person
from people import Genes

class Simulation:
    def __init__(self):    
        self.people = []
        self.sources = []
        self.graphs = []

        self.FPS = 60
        self.screen_x = 2560
        self.screen_y = 1440
        self.world_x_size = 10240
        self.world_y_size = 5760
        self.camera_x = self.world_x_size/2
        self.camera_y = self.world_y_size/2
        self.zoom = 0.25
        self.move_speed = 20/(self.zoom)
        self.zoom_speed = 0.05

        self.day = 0
        self.year_length = 365
        self.mutation_rate = 1

        self.food_max = 500
        self.water_max = 500
        self.food_water_chance = 0.5
        self.source_respawn_chance = 1

    def create_people(self):
        self.people = [Person(x = randint(0,self.world_x_size),
                 y = randint(0,self.world_y_size),
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
                     uniform(0,100),
                     uniform(0,100)),
                 age = 0,
                 postnatal_elapsed = None,
                 gestation_period = None,
                 satiety = 1000,
                 hydrated = 1000,
                 current_activity = None
                 )
                 for i in range(300)]
    
    def create_sources(self):
        self.sources = [Source(randint(0,self.world_x_size),
                      randint(0,self.world_y_size),
                      "food" if uniform(0,1) > self.food_water_chance else "water")
                      for i in range(100)]
        
    def update_simulation(self):
        Source.respawn(self)
        for person in self.people:
            person.step(self)
            person.decide_current_action(self)
            person.wander(self)
    
    def draw_simulation(self, screen):

        screen.fill("#5473ff")

        for person in self.people:
            person.draw(self, screen)

        for source in self.sources:
            source.draw(self, screen)

        border_rect = pygame.Rect(((-self.camera_x * self.zoom) + self.screen_x/2),((-self.camera_y * self.zoom) + self.screen_y/2),round(self.world_x_size*self.zoom),round(self.world_y_size*self.zoom))
        pygame.draw.rect(screen, (255,255,255), border_rect, max(1,round(5*self.zoom)))

    def draw_ui(self, screen, font):
        text_1, rect = font.render(f"Speed: {self.FPS}",  (0, 0, 0))
        text_2, rect = font.render(f"Zoom:  {self.zoom}",  (0, 0, 0))
        mouse_pos = pyautogui.position()
        for person in self.people:
            if abs(mouse_pos[0] - person.x) < 100 and abs(mouse_pos[1] - person.y) < 100:
                stat, rect = font.render(f"Current activity: {person.current_activity}",  (0, 0, 0))
                screen.blit(stat, (mouse_pos[0] + 10, mouse_pos[1] + 10))

                stat, rect = font.render(f"Direction: {person.direction}",  (0, 0, 0))
                screen.blit(stat, (mouse_pos[0] + 10, mouse_pos[1] + 10))
        
        screen.blit(text_1, (50, 50))
        screen.blit(text_2, (50, 100))