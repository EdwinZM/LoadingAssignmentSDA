class Item:
    def __init__(self, color, shape, dimensions, position):
        self.color = color
        self.shape = shape
        self.dimensions = dimensions
        self.position = position
        self.ID = id(self)

    def get_ID(self):
        return self.ID

    def get_color(self):
        return self.color

    def get_shape(self):
        return self.shape

    def get_dimensions(self):
        return self.dimensions

    def get_position(self):
        return self.position
