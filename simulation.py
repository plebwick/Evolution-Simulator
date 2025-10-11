class Simulation:
    def __init__(self):    
        self.people = []
        self.sources = []
        self.graphs = []

        self.screen_x = 2560
        self.screen_y = 1440
        self.world_x_size = 2560
        self.world_y_size = 1440
        self.camera_x = self.screen_x/2
        self.camera_y = self.screen_y/2
        self.zoom = 1
        
        self.day = 0
        self.year_length = 365
        self.mutation_rate = 1