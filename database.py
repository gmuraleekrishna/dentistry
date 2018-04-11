from collections import OrderedDict

class Database():
    def __init__(self):
        self.area_image_paths = []
        self.angle_image_paths = []
        self.angle_values = OrderedDict()
        self.area_values = OrderedDict()
        self.data = {}
    def add(self, key, value):
        self.data[key] = value

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
    
    def clear_area(self):
        self.area_image_paths = []
        self.area_values = OrderedDict()
        self.data.pop('area_folder')

    def clear_angle(self):
        self.angle_image_paths = []
        self.angle_values = OrderedDict()
        self.data.pop('angle_folder')
