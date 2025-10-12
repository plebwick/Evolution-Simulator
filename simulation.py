import pygame
from sources import Source
from people import Person

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
        self.zoom = 1
        self.move_speed = 20/(self.zoom*self.zoom)
        self.zoom_speed = 0.05

        self.day = 0
        self.year_length = 365
        self.mutation_rate = 1

        self.food_max = 100
        self.water_max = 100
        self.food_water_chance = 0.5
        self.source_respawn_chance = 1

    def update_simulation(self):
        Source.respawn(self)
        for person in self.people:
            person.clock += 1
            person.death(self)
            person.move(self)
    
    def draw_simulation(self, screen):

        screen.fill("#5473ff")

        for person in self.people:
            person.draw(self, screen)

        for source in self.sources:
            source.draw(self, screen)

        border_rect = pygame.Rect(((-self.camera_x * self.zoom) + self.screen_x/2),((-self.camera_y * self.zoom) + self.screen_y/2),round(self.world_x_size*self.zoom),round(self.world_y_size*self.zoom))
        pygame.draw.rect(screen, (255,255,255), border_rect, max(1,round(5*self.zoom)))

    def draw_ui():
        pass