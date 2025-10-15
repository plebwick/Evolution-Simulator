from math import sin, cos, pi, sqrt
from random import uniform, randint
import pygame

class Person:
    def __init__(self,
                 x,
                 y,
                 direction,
                 target,
                 genes,
                 age,
                 postnatal_elapsed,
                 gestation_period,
                 satiety,
                 hydrated,
                 current_activity
                 ):
        
        self.x,self.y = (x,y)
        self.direction = direction
        self.velocity = genes.speed
        self.target = target

        self.genes = genes

        self.age = age
        self.postnatal_elapsed = postnatal_elapsed
        self.gestation_period = gestation_period

        self.satiety = satiety
        self.hydrated = hydrated

        self.current_activity = current_activity

    def draw(self, sim, screen):
        person_size = self.genes.size
        person_x = ((self.x - sim.camera_x) * sim.zoom) + (sim.screen_x / 2)
        person_y = ((self.y - sim.camera_y) * sim.zoom) + (sim.screen_y / 2)
        pygame.draw.circle(screen, (255,255,255), (person_x, person_y), max(1,person_size*sim.zoom))

    def step(self, sim):
        self.age += 1

        try:self.postnatal_elapsed += 1
        except:pass

        ##############temp
        self.satiety -= 70 * (self.genes.size**0.65) * (self.genes.speed**0.25) * 1/365 * 1/6
        ##################

        #if self.satiety <= 0 or self.hydrated <=0: sim.people.remove(self)
        #elif uniform(0,1) < (0.2 + (0.00008*(self.age**2)))/29200: sim.people.remove(self)

    def decide_current_action(self, sim):
        if self.satiety > self.hydrated:
            self.current_activity = "find_water"
        else:
            self.current_activity = "find_food"

    def scan(self, sim):
        if self.age % 60 == 0:
            min_distance = float("inf")
            possible_sources = [source for source in sim.sources if source.type not in self.current_activity]
            for source in possible_sources:
                dx = self.x - source.x
                dy = self.y - source.y
                distance = dx**2 + dy**2
                if distance < min_distance:
                    min_distance = distance
                    self.target = source
    
    def move_towards_target(self):
        pass

    def wander(self, sim):
        dx = cos(self.direction) * self.velocity
        dy = sin(self.direction) * self.velocity

        self.direction += uniform(-self.genes.agility,self.genes.agility)
        self.x += dx
        self.y += dy

        if self.x > sim.world_x_size:
            self.x = sim.world_x_size
            self.direction *= -1
            self.direction -= pi
        if self.x < 0:
            self.x = 0
            self.direction *= -1
            self.direction -= pi
        if self.y > sim.world_y_size:
            self.y = sim.world_y_size
            self.direction *= -1
        if self.y < 0:
            self.y = 0
            self.direction *= -1

class Genes:
    def __init__(self,
                 size,
                 speed,
                 agility,
                 vision_range,
                 vision_angle,
                 fertility,
                 virility,
                 male_chance,
                 gestation_period):
        self.size = size
        self.speed = speed
        self.agility = agility
        self.vision_range = vision_range
        self.vision_angle = vision_angle
        self.fertility = fertility
        self.virility = virility
        self.male_chance = male_chance
        self.gestation_period = gestation_period