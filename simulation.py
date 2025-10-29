import pygame, inspect
from random import randint, uniform
from math import pi, ceil
from sources import Source
from graph import Graph
from people import Person
from people import Genes
from collections import defaultdict
from time import time, perf_counter

class Simulation:
    def __init__(self):
        self.people = []
        self.sources = []
        self.permanent_sources = []

        self.gene_dict = {
            "size": "blue",
            "speed": "red",
            "agility": "yellow",
            "wander_agility":"indigo",
            "vision_range": "green",
            "vision_angle": "lightgreen",
            "fertility":"#FFD900",
            "virility":"#8C00FF",
            "male_chance":"#FF00AA",
            "gestation":"#FFAE51",
            "Population":"#6DFFFF",
            "Sources":"#FFFFFF"
        }

        self.gene_method = Genes.__init__
        self.genes = inspect.signature(self.gene_method)

        self.screen_x = 2560
        self.screen_y = 1440

        self.graphs = []
        self.selected_graph = 0
        self.graph_time = self.screen_x
        self.graph_grid_size = 100
        self.sampling_frequency = 100
        
        self.graph_x_size = round(self.screen_x*0.8,-2)
        self.graph_y_size = round(self.screen_y*0.8,-2)
        self.x_offset = (self.screen_x - self.screen_x*0.8)/2
        self.y_offset = (self.screen_y - self.screen_y*0.8)/2

        self.screen = pygame.display.set_mode((self.screen_x,self.screen_y))

        self.events = None
        self.FPS = 60
        self.world_x_size = self.screen_x*4
        self.world_y_size = self.screen_y*4

        self.font = pygame.font.Font("Pompadour.otf", 24)

        self.camera_x = self.world_x_size/2
        self.camera_y = self.world_y_size/2
        self.zoom = 0.25
        self.move_speed = 20/(self.zoom)
        self.zoom_speed = 0.05
        self.selected_person = None

        self.grid = defaultdict(list)
        self.grid_size = 400

        self.toggle_grid = False
        self.toggle_vision_radius = False

        self.day = 0
        self.season = None
        self.mutation_rate = 1

        self.starting_population = 400

        total = 500
        self.permanent_sources_number = 500
        self.food_water_size = 20
        self.food_max = total
        self.water_max = total
        self.food_water_chance = 0.5

    def create_people(self):
        """
        self.people = [Person(x = randint(0,self.world_x_size),
                 y = randint(0,self.world_y_size),
                 grid = None,
                 direction = uniform(0,2*pi),
                 target = None,
                 mate = None,
                 alive = True,
                 sex = "male" if uniform(0,1) > 0.5 else "female",
                 genes = Genes(
                     uniform(2,10),
                     uniform(0.25,1),
                     uniform(1.05,1.1),
                     uniform(0.01,0.1),
                     uniform(100,400),
                     uniform(0,pi*2),
                     uniform(0,1),
                     uniform(10,200),
                     uniform(0,1),
                     uniform(1000,10000)
                 ),
                 age = randint(0,100),
                 postnatal = None,
                 gestational = None,
                 satiety = 500,
                 hydrated = 500,
                 activity = None,
                 colour = (randint(0,255), randint(0,255), randint(0,255))
                 )
                 for _ in range(self.starting_population)]
        """
        self.people = [Person(x = randint(0,self.world_x_size),
                 y = randint(0,self.world_y_size),
                 grid = None,
                 direction = uniform(0,2*pi),
                 target = None,
                 mate = None,
                 alive = True,
                 sex = "male" if uniform(0,1) > 0.5 else "female",
                 genes = Genes(
                     2,
                     3,
                     2,
                     0.05,
                     400,
                     pi,
                     0.5,
                     100,
                     0.5,
                     1000
                 ),
                 age = randint(0,100),
                 postnatal = None,
                 gestational = None,
                 satiety = 500,
                 hydrated = 500,
                 activity = None,
                 colour = (randint(0,255), randint(0,255), randint(0,255))
                 )
                 for _ in range(self.starting_population)]

    
    def create_sources(self):
        for i in range(self.permanent_sources_number):
            x = randint(0,self.world_x_size)
            y = randint(0,self.world_y_size)
            type = "food" if uniform(0,1) > self.food_water_chance else "water"
            p = (x,y,type)
            self.permanent_sources.append(p)
        
    def create_graphs(self):
        for gene in self.genes.parameters:
            if gene != "self":
                self.graphs.append(Graph(gene,
                                   self.gene_dict[gene],
                                   False,
                                   []))
                
        self.graphs.append(Graph("Population",
                                 self.gene_dict["Population"],
                                 False,
                                 []))
        
        self.graphs.append(Graph("Sources",
                                 self.gene_dict["Sources"],
                                 False,
                                 []))
 
    def normalise_coordinate(self, z, xory):
        if xory: return((z - self.camera_y) * self.zoom) + (self.screen_y / 2)
        else:    return((z - self.camera_x) * self.zoom) + (self.screen_x / 2)
    
    def update_simulation(self):
        self.day += 1
        if 0 < self.day % 100000 < 25000: self.season = "Spring"
        elif 25000 < self.day % 100000 < 50000: self.season = "Summer"
        elif 50000 < self.day % 100000 < 75000: self.season = "Autumn"
        else: self.season = "Winter"

        Source.respawn(self)   

        for person in self.people:
            person.step(self)

        self.update_people()
        self.update_grid(self.people)

        if self.day % self.sampling_frequency == 0:
            for graph in self.graphs:
                graph.log(self)

    def simulation_inputs(self):
        self.move_speed = 20/(self.zoom)

        if self.keys[pygame.K_w]:
            self.camera_y -= self.move_speed
        if self.keys[pygame.K_s]:
            self.camera_y += self.move_speed
        if self.keys[pygame.K_a]:
            self.camera_x -= self.move_speed
        if self.keys[pygame.K_d]: 
            self.camera_x += self.move_speed
        if self.keys[pygame.K_e]:
            self.zoom *= (1 + self.zoom_speed)
        if self.keys[pygame.K_q]:
            self.zoom /= (1 + self.zoom_speed)
        if self.keys[pygame.K_r]:
            self.zoom = 1
            self.camera_x = self.world_x_size/2
            self.camera_y = self.world_y_size/2
        if self.keys[pygame.K_LCTRL]:
            self.FPS /= (1 + self.zoom_speed)
            self.FPS = max(60, min(24000, self.FPS))
        if self.keys[pygame.K_LSHIFT]:
            self.FPS *= (1 + self.zoom_speed)
            self.FPS = max(60, min(24000, self.FPS))
        
        self.zoom = max(0.05, min(100, self.zoom))
    
    def update_grid(self, objects):
        for grid_object in objects:
            new_grid_location = int(grid_object.x // self.grid_size), int(grid_object.y // self.grid_size)
            if new_grid_location !=  grid_object.grid:
                if grid_object.grid:
                    self.grid.get(grid_object.grid).remove(grid_object)
                self.grid[new_grid_location].append(grid_object)
                grid_object.grid = new_grid_location

    def update_people(self):
        dead_people = [person for person in self.people if not person.alive]
        for person in dead_people:
            if self.selected_person == person:
                self.selected_person = None
        self.people = [person for person in self.people if person not in dead_people]

    def check_grid(self, person):
        #person_location = (int(person.x // self.grid_size), int(person.y // self.grid_size))
        #return [object for object in self.grid[person_location] if isinstance(object, Source)]
        person_grid_location_x, person_grid_location_y = int(person.x // self.grid_size), int(person.y // self.grid_size)
        grid_vision_range = ceil(person.genes.vision_range / self.grid_size)

        objects = []
        for dx in range(-grid_vision_range, grid_vision_range + 1):
            for dy in range(-grid_vision_range, grid_vision_range + 1):
                grid_location = person_grid_location_x + dx, person_grid_location_y + dy
                grid_objects = self.grid.get(grid_location, [])
                for obj in grid_objects:
                    if person.activity == "food" or person.activity == "water":
                        if isinstance(obj, Source): objects.append(obj)
                    elif person.activity == "mate":
                        if isinstance(obj, Person): objects.append(obj)

        return objects 

    def display_grid(self):
        for i in range(self.world_x_size//self.grid_size + 1):
            x = (i*self.grid_size - self.camera_x) * self.zoom + self.screen_x/2
            y1 = - self.camera_y * self.zoom + self.screen_y/2
            y2 = (self.world_y_size - self.camera_y) * self.zoom + self.screen_y/2
            pygame.draw.line(self.screen, (255,255,255), (x,y1), (x, y2), 1)

        for i in range(self.world_y_size//self.grid_size + 1):
            y = (i*self.grid_size - self.camera_y) * self.zoom + self.screen_y/2
            x1 = - self.camera_x * self.zoom + self.screen_x/2
            x2 = (self.world_x_size - self.camera_x) * self.zoom + self.screen_x/2
            pygame.draw.line(self.screen, (255,255,255), (x1,y), (x2, y), 1)

    def draw_text(self, x, y, text, variable, colour = (255, 255, 255), place = "centre"):
        text = self.font.render(f"{text} {variable}",  True, colour)
        if place == "centre": rect = text.get_rect(center = (x,y))
        elif place == "left": rect = text.get_rect(midleft = (x,y))
        self.screen.blit(text, rect)

    def draw_simulation(self):
        self.screen.fill("#131729")

        for person in self.people:
            person.draw(self)

        for source in self.sources:
            source.draw(self)

        border_rect = pygame.Rect(((-self.camera_x * self.zoom) + self.screen_x/2),((-self.camera_y * self.zoom) + self.screen_y/2),round(self.world_x_size*self.zoom),round(self.world_y_size*self.zoom))
        pygame.draw.rect(self.screen, (255,255,255), border_rect, max(1,round(5*self.zoom)))

    def draw_simulation_ui(self):
        if self.toggle_grid:
            self.display_grid()
        
        mouse_pos = pygame.mouse.get_pos()

        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.selected_person:
                    self.selected_person = None

        for person in self.people:
            if self.toggle_vision_radius:
                person.draw_vision_radius(self)
            person_x = self.normalise_coordinate(person.x, 0)
            person_y = self.normalise_coordinate(person.y, 1)
            if abs(mouse_pos[0] - person_x) < person.genes.size*self.zoom and abs(mouse_pos[1] - person_y) < person.genes.size*self.zoom:
                self.draw_hover_ui(person)
                for event in self.events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.selected_person = person

        if self.selected_person: 
            person_size = self.selected_person.genes.size
            person_x = self.normalise_coordinate(self.selected_person.x, 0)
            person_y = self.normalise_coordinate(self.selected_person.y, 1)
            pygame.draw.circle(self.screen, "gold", (person_x, person_y), max(1,person_size*self.zoom*2))
            self.draw_hover_ui(self.selected_person)
        
        self.draw_text(50, 220, "Season", self.season, (255,255,255), "left")
        self.draw_text(50, 60, "Speed", self.FPS/60, place = "left")
        self.draw_text(50, 100, "Zoom", self.zoom, place = "left")
        self.draw_text(50, 140, "Population", len(self.people), place = "left")
        self.draw_text(50, 180, "Sources Amount", len(self.sources), place = "left")

    def draw_hover_ui(self, person):
        person.draw_vision_radius(self)

        self.draw_text(100, 300, "Current activity:", person.activity, place = "left")
        self.draw_text(100, 340, "Satiety:", person.satiety, place = "left")
        self.draw_text(100, 380, "Hydration:", person.hydrated, place = "left")
        self.draw_text(100, 420, "Age:", person.age, place = "left")
        self.draw_text(100, 460, "Sex:", person.sex, place = "left")
        self.draw_text(100, 500, "Current gestational period:", person.gestational, place = "left")
        self.draw_text(100, 540, "Metabolic rate:", person.metabolic_rate, place = "left")

        count = 0
        for gene in self.genes.parameters:
            if gene == "self":
                continue
            text = str(gene)[0].upper() + gene[1:] + ":"
            gene_value = getattr(person.genes, gene)
            self.draw_text(100, 580+count*40, text, gene_value, place = "left")
            count += 1

        if isinstance(person.target, Person):
            count = 0
            for gene in self.gene.parameters:
                if gene == "self":
                    continue
                text = str(gene)[0].upper() + gene[1:] + ":"
                gene_value = getattr(person.target.genes, gene)
                self.draw_text(700, 500+count*40, text, gene_value, place = "left")
                count += 1

    def graph_inputs(self):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if self.selected_graph < len(self.graphs)-1: 
                        self.selected_graph += 1
                    else:
                        self.selected_graph = 0
                if event.key == pygame.K_LEFT:
                    if self.selected_graph > 0: 
                        self.selected_graph -= 1
                    else:
                        self.selected_graph = len(self.graphs)-1
                if event.key == pygame.K_UP:
                    self.graph_time *= 2
                if event.key == pygame.K_DOWN:
                    self.graph_time /= 2

    def draw_graphs(self):
        self.screen.fill("#131729")
        self.draw_grid()
        self.graphs[self.selected_graph].draw(self)

    def draw_grid(self):
        for i in range(round(self.graph_x_size/self.graph_grid_size)+1):
            x = i*self.graph_grid_size + self.x_offset
            y1 = self.y_offset
            y2 = self.y_offset + round(self.graph_y_size, -2)
            pygame.draw.line(self.screen, "#5B6FC7", (x,y1), (x, y2), 1)

        for i in range(round(self.graph_y_size/self.graph_grid_size)+1):
            y = i*self.graph_grid_size + self.y_offset
            x1 = self.x_offset
            x2 = self.x_offset + round(self.graph_x_size, -2)
            pygame.draw.line(self.screen, "#5B6FC7", (x1,y), (x2, y), 1)

    def draw_graph_ui(self):
        y_size = self.screen_y*0.1*0.25
        x_size = self.graph_x_size/(len(self.graphs))

        for i, graph in enumerate(self.graphs):
            x_pos = self.x_offset + (i)*x_size

            rect = pygame.Rect(x_pos, y_size , x_size, y_size*2)
            surface = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)

            if graph != self.graphs[self.selected_graph]: surface.set_alpha(128)

            pygame.draw.rect(surface, self.gene_dict[graph.gene], surface.get_rect())
            self.screen.blit(surface, rect)

            self.draw_text(x_pos + 0.5*x_size, y_size*2, graph.gene[0].upper()+graph.gene[1:], "", "#000000")