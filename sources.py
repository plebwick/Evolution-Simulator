from random import randint, uniform
import pygame

class Source:
    def __init__(self,
                 x,
                 y,
                 grid,
                 type):
        
        self.x,self.y = (x,y)
        self.grid = grid
        self.type = type

    def respawn(sim):
        if len(sim.sources) < (sim.food_max + sim.water_max):
            food = [source for source in sim.sources if source.type == "food"]

            try:food_chance = len(food)/len(sim.sources)
            except:food_chance = 0.5
            if uniform(0,1) > food_chance: type = "food"
            else: type = "water"

            random_source = sim.permanent_sources[randint(0,len(sim.permanent_sources)-1)]
            x = min(max(random_source[0] + randint(-100,100),0),sim.world_x_size)
            y = min(max(random_source[1] + randint(-100,100),0),sim.world_y_size)
            type = random_source[2]

            grid_location = int(x // sim.grid_size), int(y // sim.grid_size)
            new_source = Source(x,
                                y,
                                grid_location,
                                type)
            sim.sources.append(new_source)
            sim.grid[grid_location].append(new_source)

    def draw(self, sim):
        source_size = 3
        source_x = ((self.x - sim.camera_x) * sim.zoom) + (sim.screen_x / 2)
        source_y = ((self.y - sim.camera_y) * sim.zoom) + (sim.screen_y / 2)
        r = 255 if self.type == "food" else 0
        g = 0
        b = 255 if self.type == "water" else 0
        pygame.draw.circle(sim.screen, (r,g,b), (source_x, source_y), max(1,source_size*sim.zoom))