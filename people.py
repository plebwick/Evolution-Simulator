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

    def draw(self, sim, screen):
        person_size = self.genes.size
        person_x = sim.normalise_coordinate(self.x, 0)
        person_y = sim.normalise_coordinate(self.y, 1)
        pygame.draw.circle(screen, (255,255,255), (person_x, person_y), max(1,person_size*sim.zoom))
        
        p0 = (person_x, person_y)
        angle1 = self.direction-self.genes.vision_angle/2
        x1 = (self.x + cos(angle1) * self.genes.vision_range)
        y1 = (self.y + sin(angle1) * self.genes.vision_range)

        angle2 = self.direction+self.genes.vision_angle/2
        x2 = (self.x + cos(angle2) * self.genes.vision_range)
        y2 = (self.y + sin(angle2) * self.genes.vision_range)

        pygame.draw.polygon(screen, (0,255,0), [p0,(sim.normalise_coordinate(x1, 0),sim.normalise_coordinate(y1, 1)),(sim.normalise_coordinate(x2, 0),sim.normalise_coordinate(y2, 1))], 1)


        #pygame.draw.polygon(screen, (0,255,0, 50), [x, y, vision_range*2, vision_range*2], lower_angle, higher_angle, 200)

    def step(self, sim):
        self.age += 1

        try:self.postnatal_elapsed += 1
        except:pass

        ##############temp
        self.satiety -= 70 * (self.genes.size**0.65) * (self.genes.speed**0.25) * 1/365 * 1/6
        self.hydrated -= 70 * (self.genes.size**0.65) * (self.genes.speed**0.25) * 1/365 * 1/6
        ##################

        #if self.satiety <= 0 or self.hydrated <=0: sim.people.remove(self)
        #elif uniform(0,1) < (0.2 + (0.00008*(self.age**2)))/29200: sim.people.remove(self)

    def decide_current_action(self, sim):
        if self.satiety > self.hydrated:
            self.current_activity = "water"
        else:
            self.current_activity = "food"

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
                    if distance < self.genes.vision_range**2:
                        target_direction = atan2(dy, dx)
                        if abs((target_direction - self.direction + pi) % (2*pi) - pi) < self.genes.vision_angle/2:
                            if distance < min_distance:
                                min_distance = distance
                                self.target = source
        """
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
        """
    
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
        if distance < self.genes.vision_range**2:
            try:
                sim.sources.remove(self.target)
                if self.current_activity == "food":
                    self.satiety += 1
                else:
                    self.hydrated += 1
                self.target = None
            except:
                self.target = None

    def angle_wander(self, sim):
        self.direction += uniform(-0.15,0.15)

    def move(self, sim):
        dx = cos(self.direction) * self.velocity
        dy = sin(self.direction) * self.velocity
        
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