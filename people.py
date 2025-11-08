from math import sin, cos, pi, sqrt, atan2, e
import math
from random import uniform, randint
import pygame

class Genes:
    def __init__(self,
                 size,
                 speed,
                 agility,
                 wander_agility,
                 vision_range,
                 vision_angle,
                 fertility,
                 virility,
                 male_chance,
                 gestation):
        self.size = size
        self.speed = speed
        self.agility = agility
        self.wander_agility = wander_agility
        self.vision_range = vision_range
        self.vision_angle = vision_angle
        self.fertility = fertility
        self.virility = virility
        self.male_chance = male_chance
        self.gestation = gestation

class Person:
    def __init__(self,
                 x,
                 y,
                 grid,
                 direction,
                 target,
                 mate,
                 alive,
                 sex,
                 genes,
                 age,
                 postnatal,
                 gestational,
                 satiety,
                 hydrated,
                 activity,
                 colour
                 ):
        
        self.x = x
        self.y = y
        self.grid = grid
        self.dir = direction
        self.vel = genes.speed
        self.target = target
        self.mate = mate
        self.alive = alive
        self.sex = sex
        self.genes = genes
        self.age = age
        self.postnatal = postnatal
        self.gestational = gestational
        self.activity = activity
        self.colour = colour

        size = self.genes.size
        speed = self.vel
        self.metabolic_rate = 0.00005 #((size/5)**2 * (speed/5)**2 + 0.1) / 432 / 5
        self.stomach_size = size*5
        self.bladder_size = size*5

        self.satiety = self.stomach_size/2
        self.hydrated = self.bladder_size/2

    def draw(self, sim):
        x = sim.normalise_coordinate(self.x, 0)
        y = sim.normalise_coordinate(self.y, 1)
        size = self.genes.size

        colour = (255,255,255)
        if self.activity == "mate": 
            if self.target: colour = (255,255,255)
            else: colour = (128,128,128)
        elif self.target: colour = (0,0,255) if self.target.type == "water" else (255,0,0)
        else: colour = (255,128,128) if self.activity == "food" else (128,128,255)
        colour = (255,255,255)

        pygame.draw.circle(sim.screen, self.colour, (x, y), max(1,size*sim.zoom))

    def draw_vision_radius(self,sim):
        x = sim.normalise_coordinate(self.x, 0)
        y = sim.normalise_coordinate(self.y, 1)
        points = [(x,y)]
        accuracy = 30
        for i in range(-accuracy,accuracy+1):
            if i == 0:
                angle = self.dir
            else:
                angle = self.dir-(self.genes.vision_angle/accuracy * i)/2
            angle = self.dir + self.genes.vision_angle/2 * i/accuracy
            x = (self.x + cos(angle) * self.genes.vision_range)
            y = (self.y + sin(angle) * self.genes.vision_range)
            points.append((sim.normalise_coordinate(x, 0),sim.normalise_coordinate(y, 1)))
        pygame.draw.polygon(sim.screen, (0,255,0), points, 1)

    def step(self, sim):
        self.age += 1
        if self.postnatal: self.postnatal += 1

        if self.target:
            if (self.activity == "food" or self.activity == "water") and self.target not in sim.sources: self.target = None
            elif self.activity == "mate" and self.target.activity != "mate": self.target = None

        self.satiety -= self.metabolic_rate
        self.hydrated -= (self.metabolic_rate*3)

        if self.gestation:
            self.satiety -= self.metabolic_rate * 0.25
            self.hydrated -= self.metabolic_rate * 0.25
        
        if self.satiety < 0 or self.hydrated < 0: 
            self.alive = False
            return #ends the step for dead people
        #elif uniform(0,1) < (0.2 + (0.00008*(self.age**2)))/29200: sim.people.remove(self)
        
        self.scan(sim)
        
        if self.target:
            self.angle_towards_target(sim)
            self.check_distance(sim)

        else:
            self.decide_current_action(sim)
            self.angle_wander(sim)

        if self.gestational: self.gestation(sim)

        self.move(sim)

    def decide_current_action(self, sim):
        if self.age % 120 != 0:
            return

        s = self.satiety/self.stomach_size
        h = self.hydrated/self.bladder_size

        if self.gestational: chance_to_mate = 0
        elif self.postnatal: 
            if self.postnatal < 10000: 
                chance_to_mate = 0
            else:
                chance_to_mate = (s/2 + h/2 + self.genes.virility)**8
        else:chance_to_mate = (s/2 + h/2 + self.genes.virility)**8

        if chance_to_mate > uniform(0,1): self.activity = "mate"
        else:
            food_water_chance = self.hydrated/(self.satiety+self.hydrated)
            if food_water_chance > uniform(0,1): self.activity = "food"
            else: self.activity = "water"

            if self.satiety > self.hydrated:
                self.activity = "water"
            else:
                self.activity = "food"

    def scan(self, sim):
        if self.age % 60 != 0 and self.target != "mate": return
        
        targets = sim.check_grid(self)

        if not targets: return

        min_distance = float("inf")

        if self.activity == "food" or self.activity == "water":
            possible_targets = [source for source in targets if source.type == self.activity]
        elif self.activity == "mate":
            possible_targets = [target for target in targets if target.sex != self.sex and target.activity == "mate"]

        for target in possible_targets:
            dx = target.x - self.x
            dy = target.y - self.y
            distance = dx**2 + dy**2
            if distance < self.genes.vision_range**2:
                target_direction = atan2(dy, dx)
                if abs((target_direction - self.dir + pi) % (2*pi) - pi) < self.genes.vision_angle/2:
                    if distance < min_distance:
                        min_distance = distance
                        self.target = target
                        if self.activity == "mate": self.mate = target
    
    def angle_towards_target(self, sim):
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        target_direction = atan2(dy, dx)
        angle_diff = (target_direction - self.dir + pi) % (2*pi) - pi
        if angle_diff > self.genes.agility: self.dir += self.genes.agility
        elif angle_diff < -self.genes.agility: self.dir -= self.genes.agility
        else:self.dir = target_direction
    
    def check_distance(self,sim):
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = dx**2 + dy**2
        if distance < self.genes.size:
            if self.activity == "food" or self.activity == "water":
                sim.sources.remove(self.target)
                sim.grid[self.target.grid].remove(self.target)

                if self.activity == "food": 
                    self.satiety += sim.food_water_size
                    self.satiety = min(self.satiety, self.stomach_size)
                else: 
                    self.hydrated += sim.food_water_size
                    self.hydrated = min(self.hydrated, self.bladder_size)
            elif self.activity == "mate":
                #self.satiety -= self.stomach_size*0.1
                #self.hydrated -= self.bladder_size*0.1
                self.satiety -= 1
                self.hydrated -= 1
                if self.sex == "female":
                    self.gestational = 1
            self.target = None
            self.activity = None

    def gestation(self,sim):
        if self.gestational > self.genes.gestation:
            self.reproduce(sim)
        else:
            self.gestational += 1

    def reproduce(self,sim):
        self.gestational = None
        self.postnatal = 1

        new_size = self.genes.size + uniform(-self.genes.size*0.1,self.genes.size*0.1)
        new_speed = self.genes.speed + uniform(-self.genes.speed*0.1,self.genes.speed*0.1)
        new_agility = self.genes.agility + uniform(-self.genes.agility*0.1,self.genes.agility*0.1)
        new_wander_agility = self.genes.wander_agility + uniform(-self.genes.wander_agility*0.1,self.genes.wander_agility*0.1)
        new_vision_range = self.genes.vision_range + uniform(-self.genes.vision_range*0.1,self.genes.vision_range*0.1)
        new_vision_angle = self.genes.vision_angle + uniform(-self.genes.vision_angle*0.1,self.genes.vision_angle*0.1)
        new_fertility = self.genes.fertility + uniform(-self.genes.fertility*0.1,self.genes.fertility*0.1)
        new_virility = self.genes.virility + uniform(-self.genes.virility*0.1,self.genes.virility*0.1)
        new_male_chance = self.genes.male_chance + uniform(-self.genes.male_chance*0.1,self.genes.male_chance*0.1)
        new_gestation = self.genes.gestation + uniform(-self.genes.gestation*0.1,self.genes.gestation*0.1)

        male_chance = (self.genes.male_chance + self.mate.genes.male_chance)
        satiety = self.satiety*0.25
        hydration = self.hydrated*0.25

        sim.people.append(Person(x = self.x,
                 y = self.y,
                 grid = None,
                 direction = uniform(0,2*pi),
                 target = None,
                 mate = None,
                 alive = True,
                 sex = "male" if uniform(0,1) > male_chance else "female",
                 genes = Genes(
                     new_size,
                     new_speed,
                     new_agility,
                     new_wander_agility,
                     new_vision_range,
                     new_vision_angle,
                     new_fertility,
                     new_virility,
                     new_male_chance,
                     new_gestation
                 ),
                 age = randint(0,100),
                 postnatal = None,
                 gestational = None,
                 satiety = satiety,
                 hydrated = hydration,
                 activity = None,
                 colour = self.colour
                 )
        )

        self.satiety *= 0.70
        self.hydrated *= 0.70

    def angle_wander(self, sim):
        self.dir += uniform(-self.genes.wander_agility,self.genes.wander_agility)

    def move(self, sim):
        dx = cos(self.dir) * self.vel
        dy = sin(self.dir) * self.vel
        
        self.x += dx
        self.y += dy

        if self.x > sim.world_x_size:
            self.x = sim.world_x_size
            self.dir *= -1
            self.dir -= pi
        elif self.x < 0:
            self.x = 0
            self.dir *= -1
            self.dir -= pi
        if self.y > sim.world_y_size:
            self.y = sim.world_y_size
            self.dir *= -1
        elif self.y < 0:
            self.y = 0
            self.dir *= -1