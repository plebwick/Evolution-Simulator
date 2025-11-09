import pygame

class Graph:
    def __init__(self,
                 gene,
                 value,
                 colour,
                 display,
                 averages = [],
                 medians = [],
                 maximums = [],
                 minimums = []):
        self.gene = gene
        self.value = value
        self.colour = colour
        self.display = display
        self.max_value = 0
        self.min_value = 0
        self.difference = 0
        self.averages = averages
        self.medians = medians
        self.maximums = maximums
        self.minimums = minimums

    def log(self, sim):
        if self.value == "gene":
            values = [getattr(person.genes, self.gene) for person in sim.people]
            length = len(values)
            if values:
                #Find average
                average = sum(values)/length
                
                #Find max
                maximum = max(values)

                #Find min
                minimum = min(values)

                #Find median
                values.sort()
                if length % 2 == 1:
                    median = values[length//2]
                else:
                    first = values[length//2-1]
                    second = values[length//2]
                    median = (first+second)/2

            else:
                average = 0
                median = 0
                minimum = 0
                maximum = 0
        else:
            average = self.value()
            median = 0
            minimum = 0
            maximum = 0

        self.averages.append(average)
        self.medians.append(median)
        self.minimums.append(minimum)
        self.maximums.append(maximum)

    def draw(self,sim):


        averages = self.averages[-round(sim.graph_time):]
        medians = self.medians[-round(sim.graph_time):]
        maximums = self.maximums[-round(sim.graph_time):]
        minimums = self.minimums[-round(sim.graph_time):]

        total = averages + medians #+ maximums + minimums
        
        self.min_value = min(total)-min(total)*0.1 if total else 0
        self.max_value = max(total)+max(total)*0.1 if total else 1

        self.difference = (self.max_value-self.min_value) if (self.max_value-self.min_value) > 0 else 1

        #Draw Average line
        draw_line(self, averages, sim)

        #Draw Median line
        draw_line(self, medians, sim)

        #Draw Max line
        #draw_line(self, maximums, sim)

        #Draw Min line
        #draw_line(self, minimums, sim)

        display_time = min(len(averages), sim.graph_time)

        #draws the text
        sim.draw_text(sim.x_offset, sim.y_offset+sim.graph_y_size+20, f"{display_time} ticks ago", place = "left")
        sim.draw_text(sim.x_offset+sim.graph_x_size, sim.y_offset+sim.graph_y_size+20, "0 ticks ago", place = "left")

        sim.draw_text(sim.x_offset-50, sim.y_offset, round(self.max_value,2), place = "left")
        sim.draw_text(sim.x_offset-50, sim.y_offset+sim.graph_y_size, round(self.min_value,2), place = "left")

def draw_line(self, values, sim):
    step = len(values)/(sim.graph_x_size)

    if len(values) > sim.graph_x_size:
        value_points = [(i+sim.x_offset, (sim.graph_y_size + sim.y_offset - sim.graph_y_size*(values[int(i*step)]-self.min_value)/self.difference))
                for i in range(0, round(sim.graph_x_size))]
    else:
        value_points = [(i/step+sim.x_offset, (sim.graph_y_size + sim.y_offset - sim.graph_y_size*(values[int(i)]-self.min_value)/self.difference))
                for i in range(0, len(values))]

    for i, point in enumerate(value_points):
        if point[1] <= sim.y_offset: value_points.remove(value_points[i])
        elif point[1] >= sim.graph_y_size+sim.y_offset: value_points.remove(value_points[i])


    if len(value_points) > 2: 
        pygame.draw.lines(sim.screen, self.colour, 0, value_points, 4)
        last_value_y = sim.graph_y_size + sim.y_offset - sim.graph_y_size*(values[(len(values))-1]-self.min_value)/self.difference
        last_value = values[(len(values))-1]
    else:
        last_value_y = -100
        last_value = 0

    if last_value_y > sim.y_offset and last_value_y < sim.graph_y_size+sim.y_offset:
        sim.draw_text(sim.x_offset+sim.graph_x_size+15, last_value_y, f"Value: {round(last_value,2)}", place = "left")