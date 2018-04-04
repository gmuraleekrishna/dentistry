class Database():
    def __init__(self):
        types = { 'preparation': '', 'after_restoration': '', 'after_one_day': '', 'after_4_weeks': '' }
        self.angle_image_paths = types
        self.area_image_paths = types
        self.angle_values = {}
        self.area_values = {}
    
    def add_angles(self, ptype, path, values):
        self.angle_image_paths[ptype] = path
        self.angle_values[ptype] = values


    def add_area(self, ptype, path, value):
        self.area_image_paths[ptype] = path
        self.area_values[ptype] = value

    def get_area_image_paths(self):
        return self.area_image_paths

    def get_angle_image_paths(self):
        return self.angle_image_paths
