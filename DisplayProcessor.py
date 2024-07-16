class DisplayProcessor:
    
    def __init__(self):
        self.window_width = 0
        self.window_height = 0
        self.count = 0
        self.points = []
        for val_i in range (-10,11,2):
            i = val_i/10.0
            for val_j in range (-10,11,2):
                j = val_j/10.0
                self.points.append((i, j))
        
    def set_window_width(self, window_width):
        self.window_width = window_width
    
    def get_window_width(self):
        return self.window_width
    
    def set_window_height(self, window_height):
        self.window_height = window_height
    
    def get_window_height(self):
        return self.window_height
    
    def update_counter(self):
        self.count = self.count + 1
    
    def get_count(self):
        return self.count
    
    def get_point(self):
        count = self.get_count()
        return self.points[count], count
    
    # def get_point(self, point_number):
        # return self.points[point_number]


