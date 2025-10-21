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
        if people_length > 0: average = total/people_length
        self.values.append(average)

    def draw(self,sim):
        graph_x_size = round(sim.screen_x*0.8,-2)
        graph_y_size = round(sim.screen_y*0.8,-2)

        x_offset = (sim.screen_x - graph_x_size)/2
        y_offset = (sim.screen_y - graph_y_size)/2

        grid_size = 100
        for i in range(round(graph_x_size/grid_size)+1):
            x = i*grid_size + x_offset
            y1 = y_offset
            y2 = y_offset + round(graph_y_size, -2)
            pygame.draw.line(sim.screen, (255,255,255), (x,y1), (x, y2), 1)

        for i in range(round(graph_y_size/grid_size)+1):
            y = i*grid_size + y_offset
            x1 = x_offset
            x2 = x_offset + round(graph_x_size, -2)
            pygame.draw.line(sim.screen, (255,255,255), (x1,y), (x2, y), 1)
        
        min_value = min(self.values) if self.values else 0
        max_value = max(self.values) if self.values else 1
        step = len(self.values)/(graph_x_size)
        difference = (max_value-min_value)
        if difference == 0: difference = 1
        if len(self.values) > graph_x_size:
            points = [(i+x_offset, (graph_y_size + y_offset - graph_y_size*(self.values[int(i*step)]-min_value)/difference))
                    for i in range(0, round(graph_x_size))]
        else:
            points = [(i+x_offset, (graph_y_size + y_offset - graph_y_size*(self.values[int(i*step)]-min_value)/difference))
                    for i in range(0, len(self.values))]

        try:pygame.draw.lines(sim.screen, self.colour, 0, points, 2)
        except:pass

        sim.draw_text(x_offset-50, y_offset, max_value, "")
        sim.draw_text(x_offset-50, y_offset+graph_y_size, min_value, "")