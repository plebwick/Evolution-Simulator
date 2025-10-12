class Simulation:
    def __init__(self):    
        self.people = []
        self.sources = []
        self.graphs = []

        self.FPS = 60
        self.screen_x = 2560
        self.screen_y = 1440
        self.world_x_size = 10240
        self.world_y_size = 5760
        self.camera_x = self.world_x_size/2
        self.camera_y = self.world_y_size/2
        self.zoom = 1
        self.move_speed = 20/(self.zoom*self.zoom)
        self.zoom_speed = 0.05

        self.day = 0
        self.year_length = 365
        self.mutation_rate = 1

    def create_people():
        pass