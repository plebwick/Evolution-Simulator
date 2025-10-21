import pygame, pyautogui, inspect
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
        self.graphs = []

        self.screen_x = 2560
        self.screen_y = 1440

        self.screen = pygame.display.set_mode((self.screen_x,self.screen_y))

        self.events = None
        self.FPS = 60
        self.world_x_size = 2560*4
        self.world_y_size = 1440*4

        self.font = pygame.freetype.Font("font.otf", 24)

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
        self.year_length = 365
        self.mutation_rate = 1

        self.starting_population = 400

        total = 1000
        self.permanent_sources_number = 25
        self.food_water_size = 100
        self.food_max = total/2
        self.water_max = total/2
        self.food_water_chance = 0.5

    def create_people(self):
        self.people = [Person(x = randint(0,self.world_x_size),
                 y = randint(0,self.world_y_size),
                 grid = None,
                 direction = uniform(0,2*pi),
                 target = None,
                 sex = "male" if uniform(0,1) > 0.5 else "female",
                 genes = Genes(
                     uniform(2,10),
                     uniform(0.25,1),
                     uniform(1.05,1.1),
                     uniform(200,600),
                     uniform(0,pi),
                     1,
                     1,
                     1,
                     1
                     #uniform(0,1),
                     #uniform(0,1),
                     #uniform(0,1),
                     #uniform(0,1)),
                 ),
                 age = randint(0,100),
                 postnatal_elapsed = None,
                 current_gestational_period = None,
                 satiety = 1000,
                 hydrated = 1000,
                 current_activity = None
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
        gene_dict = {
            "size": "blue",
            "speed": "red",
            "agility": "yellow",
            "vision_range": "green",
            "vision_angle": "lightgreen",
            "fertility":"#FFFFFF",
            "virility":"#FFFFFF",
            "male_chance":"#FFFFFF",
            "gestation_period":"#FFFFFF"
        }
        gene_method = Genes.__init__
        gene = inspect.signature(gene_method)

        for gene in gene.parameters:
            if gene != "self":
                self.graphs.append(Graph(gene,
                                   gene_dict[gene],
                                   False,
                                   []))
 
    def normalise_coordinate(self, z, xory):
        if xory: return((z - self.camera_y) * self.zoom) + (self.screen_y / 2)
        else:    return((z - self.camera_x) * self.zoom) + (self.screen_x / 2)
    
    def update_simulation(self):
        self.day += 1
        #t0 = perf_counter()
        Source.respawn(self)
        #t1 = perf_counter()
        for person in self.people:
            #s0 = perf_counter()
            person.step(self)
            #s1 = perf_counter()
            #s2 = perf_counter()
            if person.target:
                person.angle_towards_target(self)
                person.check_distance(self)
            else:
                person.decide_current_action(self)
                person.scan(self)
                person.angle_wander(self)
            #s3 = perf_counter()
            person.move(self)
            #s4 = perf_counter()
            #print(f"step={s1-s0:.8f}s | current action={s2-s1:.8f}s | angle={s3-s2:.8f}s | move={s4-s3:.8f}s | ")

        #t2 = perf_counter()
        self.update_grid(self.people)

        if self.day % 100 == 0:
            for graph in self.graphs:
                graph.log(self)
        #t3 = perf_counter()
        #print(f"respawn={t1-t0:.6f}s | step={t2-t1:.6f}s | decide={t3-t2:.6f}s | ")
        #f"respawn={t1-t0:.10f}s | step={t3-t2:.10f}s | decide={t4-t3:.10f}s | "
        #f"scan={t5-t4:.10f}s | angle={t6-t5:.10f}s | move={t7-t6:.10f}s | "
        #f"grid={t8-t7:.10f}s | total={t8-t0:.10f}s"
        #)

    def update_grid(self, objects):
        for grid_object in objects:
            new_grid_location = int(grid_object.x // self.grid_size), int(grid_object.y // self.grid_size)
            if new_grid_location !=  grid_object.grid:
                if grid_object.grid:
                    self.grid.get(grid_object.grid).remove(grid_object)
                self.grid[new_grid_location].append(grid_object)
                grid_object.grid = new_grid_location

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
                    if isinstance(obj, Source):
                        objects.append(obj)
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

    def draw_text(self, x, y, text, variable, colour = (255, 255, 255)):
        text, rect = self.font.render(f"{text} {variable}",  (255, 255, 255))
        self.screen.blit(text, (x, y))

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
        
        mouse_pos = pyautogui.position()

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
        
        self.draw_text(50, 50, "Speed", self.FPS/60)
        self.draw_text(50, 100, "Zoom", self.zoom)
        self.draw_text(50, 150, "Population", len(self.people))
        self.draw_text(50, 200, "Sources Amount", len(self.sources))

    def draw_hover_ui(self, person):
        person.draw_vision_radius(self)

        self.draw_text(100, 300, "Current activity:", person.current_activity)
        self.draw_text(100, 350, "Satiety:", person.satiety)
        self.draw_text(100, 400, "Hydration:", person.hydrated)
        self.draw_text(100, 450, "Age:", person.age)
        self.draw_text(100, 500, "Sex:", person.sex)
        
        gene_method = Genes.__init__
        gene = inspect.signature(gene_method)

        count = 0
        for gene in gene.parameters:
            if gene == "self":
                continue
            text = str(gene)[0].upper() + gene[1:] + ":"
            gene_value = getattr(person.genes, gene)
            self.draw_text(100, 550+count*50, text, gene_value)
            count += 1

    def draw_graphs(self):
        self.screen.fill("#131729")
        chosen_graph = self.graphs[0]
        chosen_graph.draw(self)
        #for graph in self.graphs:
        #    graph.draw(self)