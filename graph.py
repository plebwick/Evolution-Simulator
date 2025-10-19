import pygame

class Graph:
    def __init__(self,
                 gene,
                 colour,
                 display,
                 values = []):
        self.gene = gene
        self.colour = colour
        self.display = display
        self.values = values

    def log(self, sim):
        people_length = len(sim.people)
        total = sum(getattr(person.genes, self.gene)for person in sim.people)
        average = total/people_length
        self.values.append(average)

    def draw(self,sim):
        min_value = min(self.values) if self.values else 0
        max_value = max(self.values) if self.values else 1
        scale = (max_value-min_value)/max_value
        if len(self.values) > sim.screen_x:
            step = len(self.values)/(sim.screen_x)
            #y  =  screen_y - screen_y*(value-min_value/(max_value-min_value))
            #y = screen_y  -  ( ( (value - (graph.min)) / (max(((graph.max)-(graph.min)),1))) * 200)
            difference = (max_value-min_value)
            if difference == 0: difference = 1
            points = [(i, (sim.screen_y - sim.screen_y*(self.values[int(i*step)]-min_value)/difference))
                    for i in range(0, sim.screen_x)]
        else:
            points = [(i, (sim.screen_y - self.values[i])*scale)
                    for i in range(0, len(self.values))]

        try:pygame.draw.lines(sim.screen, self.colour, 0, points, 2)
        except:pass