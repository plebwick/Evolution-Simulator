from random import randint, uniform
import pygame

class Source:
    def __init__(self,
                 x,
                 y,
                 type):
        
        self.x,self.y = (x,y)
        self.type = type

    def respawn(sim):
        if len(sim.sources) < (sim.food_max + sim.water_max):
            random_source = sim.sources[randint(0,len(sim.sources)-1)]
            x = random_source.x + randint(-50,50)
            y = random_source.y + randint(-50,50)
            sim.sources.append(Source(x,
                                      y,
                                      "food" if uniform(0,1) > sim.food_water_chance else "water"))
            
    def draw(self, sim, screen):
        source_size = 5
        source_x = ((self.x - sim.camera_x) * sim.zoom) + (sim.screen_x / 2)
        source_y = ((self.y - sim.camera_y) * sim.zoom) + (sim.screen_y / 2)
        r = 255 if self.type == "food" else 0
        g = 0
        b = 255 if self.type == "water" else 0
        pygame.draw.circle(screen, (r,g,b), (source_x, source_y), max(1,source_size*sim.zoom))
