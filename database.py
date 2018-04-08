class Database():
    def __init__(self):
        self.area_image_paths = []
        self.angle_image_paths = []
        self.angle_values = {}
        self.area_values = {}
    
    def add_angles(self, file_name, values):
        self.angle_image_paths.append(file_name)
        self.angle_values[file_name] = values


    def add_area(self, file_name, value):
        self.area_image_paths.append(file_name)
        self.area_values[file_name] = value

    def get_area_image_paths(self):
        return self.area_image_paths

    def get_angle_image_paths(self):
        return self.angle_image_paths
