from random import randint, uniform
import pygame
from math import sin

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
        #if sim.season == "Spring": season_frequency = 100
        #if sim.season == "Summer": season_frequency = 75
        #if sim.season == "Autumn": season_frequency = 100
        #if sim.season == "Winter": season_frequency = 150
        #season_frequency = abs(sin(sim.day))
        chance = 1/7 * sin((1/50000) * sim.day) + 1
        if uniform(0,1) < chance/100:
            if len(sim.sources) < (sim.food_max + sim.water_max):
                food = [source for source in sim.sources if source.type == "food"]
                water = [source for source in sim.sources if source.type == "water"]

                if len(food) > sim.food_max:
                    type = "water"
                elif len(water) > sim.water_max:
                    type = "food"
                else:
                    if len(food):
                        food_chance = len(food)/len(sim.sources)
                    else:
                        food_chance = 0.5
                    if uniform(0,1) > food_chance: type = "food"
                    else: type = "water"

                random_source = sim.permanent_sources[randint(0,len(sim.permanent_sources)-1)]
                x = min(max(random_source[0] + randint(-100,100),0),sim.world_x_size)
                y = min(max(random_source[1] + randint(-100,100),0),sim.world_y_size)
                type = random_source[2]

                x = randint(0, sim.world_x_size)
                y = randint(0, sim.world_y_size)

                if len(food):
                    type = "water" if len(food)/len(sim.sources) > 0.5 else "food"
                else:
                    type = "food"

                grid_location = int(x // sim.grid_size), int(y // sim.grid_size)
                new_source = Source(x,
                                    y,
                                    grid_location,
                                    type)
                sim.sources.append(new_source)
                sim.grid[grid_location].append(new_source)

    def draw(self, sim):
        source_size = 1
        source_x = sim.normalise_coordinate(self.x, 0)
        source_y = sim.normalise_coordinate(self.y, 1)
        if 0 < source_x < sim.screen_x and 0 < source_y < sim.screen_y:
            source_size = 1
            colour = "#8F2323" if self.type == "food" else "#30B3FF"
            pygame.draw.circle(sim.screen, colour, (source_x, source_y), max(1,source_size*sim.zoom))