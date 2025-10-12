from math import sin, cos, pi
from random import uniform, randint

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
                 current_activity,
                 clock):
        
        self.x,self.y = (x,y)
        self.direction = direction
        self.target = target

        self.genes = genes

        self.age = age
        self.postnatal_elapsed = postnatal_elapsed
        self.gestation_period = gestation_period

        self.satiety = satiety
        self.hydrated = hydrated

        self.current_activity = current_activity

        self.clock = clock

    def move(self, sim):
        dx = cos(self.direction) * self.genes.speed
        dy = sin(self.direction) * self.genes.speed

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
                 fertility,
                 virility,
                 male_chance,
                 gestation_period):
        self.size = size
        self.speed = speed
        self.agility = agility
        self.vision_range = vision_range
        self.fertility = fertility
        self.virility = virility
        self.male_chance = male_chance
        self.gestation_period = gestation_period