from math import sin, cos, pi, sqrt, atan2
import math
from random import uniform, randint
import pygame

class Person:
    def __init__(self,
                 x,
                 y,
                 grid,
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
        self.grid = grid
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

    def draw(self, sim):
        person_size = self.genes.size
        person_x = sim.normalise_coordinate(self.x, 0)
        person_y = sim.normalise_coordinate(self.y, 1)
        colour = (255,255,255)
        
        if self.target: colour = (0,0,255) if self.target.type == "water" else (255,0,0)
        else: colour = (255,128,128) if self.current_activity == "food" else (128,128,255)
        pygame.draw.circle(sim.screen, colour, (person_x, person_y), max(1,person_size*sim.zoom))

    def draw_vision_radius(self,sim):
        person_x = sim.normalise_coordinate(self.x, 0)
        person_y = sim.normalise_coordinate(self.y, 1)

        accuracy = 30
        points = []
        points.append((person_x, person_y))
        for i in range(-accuracy,accuracy+1):
            if i == 0:
                angle = self.direction
            else:
                angle = self.direction-self.genes.vision_angle/accuracy * i
            x = (self.x + cos(angle) * self.genes.vision_range)
            y = (self.y + sin(angle) * self.genes.vision_range)
            points.append((sim.normalise_coordinate(x, 0),sim.normalise_coordinate(y, 1)))

        pygame.draw.polygon(sim.screen, (0,255,0), points, 1)

    def step(self, sim):
        self.age += 1
        try:self.postnatal_elapsed += 1
        except:pass

        if self.target:
            if self.target not in sim.sources:
                self.target = None

        ##############temp
        self.satiety -= 70 * self.genes.size * self.genes.speed * 1/365 * 1/20
        self.hydrated -= 70 * self.genes.size * self.genes.speed * 1/365 * 1/20
        ##################

        if self.satiety <= 0 or self.hydrated <=0: 
            sim.people.remove(self)
            if sim.selected_person == self:
                sim.selected_person = None

        #elif uniform(0,1) < (0.2 + (0.00008*(self.age**2)))/29200: sim.people.remove(self)

    def decide_current_action(self, sim):
        if self.age % 120 == 0 or self.current_activity == None:
            food_water_chance = self.hydrated/(self.satiety+self.hydrated)

            if uniform(0,1) < food_water_chance: self.current_activity = "food"
            else: self.current_activity = "water"
            #if self.satiety > self.hydrated: self.current_activity = "water"
            #else: self.current_activity = "food"

    def scan(self, sim):
        if self.age % 60 == 0:
            sources = sim.check_grid(self)
            if sources:
                min_distance = float("inf")
                possible_sources = [source for source in sources if source.type == self.current_activity]
                #possible_sources = sources
                for source in possible_sources:
                    dx = source.x - self.x
                    dy = source.y - self.y
                    distance = dx**2 + dy**2
                    distance = sqrt(distance)
                    if distance < self.genes.vision_range:
                        target_direction = atan2(dy, dx)
                        if abs((target_direction - self.direction + pi) % (2*pi) - pi) < self.genes.vision_angle/2:
                            if distance < min_distance:
                                min_distance = distance
                                self.target = source
                                #return
    
    def angle_towards_target(self, sim):
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        target_direction = atan2(dy, dx)
        
        angle_diff = (target_direction - self.direction + pi) % (2*pi) - pi

        if angle_diff > self.genes.agility:
            self.direction += self.genes.agility
        elif angle_diff < -self.genes.agility:
            self.direction -= self.genes.agility
        else:self.direction = target_direction
    
    def check_distance(self,sim):
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = dx**2 + dy**2
        if distance < self.genes.size:
            try:sim.sources.remove(self.target)
            except:pass
            try:sim.grid[self.target.grid].remove(self.target)
            except:pass

            if self.current_activity == "food": self.satiety += 1000
            else: self.hydrated += 1000
            self.target = None
            self.current_activity = None

    def angle_wander(self, sim):
        self.direction += uniform(-0.1,0.10)

    def move(self, sim):
        dx = cos(self.direction) * self.velocity
        dy = sin(self.direction) * self.velocity
        
        self.x += dx
        self.y += dy

        if self.x > sim.world_x_size:
            self.x = sim.world_x_size
            self.direction *= -1
            self.direction -= pi
        elif self.x < 0:
            self.x = 0
            self.direction *= -1
            self.direction -= pi
        if self.y > sim.world_y_size:
            self.y = sim.world_y_size
            self.direction *= -1
        elif self.y < 0:
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