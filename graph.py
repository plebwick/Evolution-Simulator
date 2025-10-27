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
        values = self.values[-round(sim.graph_time):]

        min_value = min(values)-min(values)*0.1 if values else 0
        max_value = max(values)+max(values)*0.1 if values else 1

        step = len(values)/(sim.graph_x_size)

        difference = (max_value-min_value)
        if len(values) > sim.graph_x_size:
            points = [(i+sim.x_offset, (sim.graph_y_size + sim.y_offset - sim.graph_y_size*(values[int(i*step)]-min_value)/difference))
                    for i in range(0, round(sim.graph_x_size))]
        else:
            points = [(i+sim.x_offset, (sim.graph_y_size + sim.y_offset - sim.graph_y_size*(values[int(i)]-min_value)/difference))
                    for i in range(0, len(values))]

        if len(points) > 2: pygame.draw.lines(sim.screen, self.colour, 0, points, 4)

        display_time = min(len(values), sim.graph_time)

        #draws the text
        sim.draw_text(sim.x_offset, sim.y_offset+sim.graph_y_size+10, display_time, "ticks ago")
        sim.draw_text(sim.x_offset+sim.graph_x_size, sim.y_offset+sim.graph_y_size+10, 0, "ticks ago")

        sim.draw_text(sim.x_offset-50, sim.y_offset, round(max_value,2), "")
        sim.draw_text(sim.x_offset-50, sim.y_offset+sim.graph_y_size, round(min_value,2), "")
