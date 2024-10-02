class Item:
    def __init__(self, color, shape, dimensions, position):
        self.color = color
        self.shape = shape
        self.dimensions = dimensions
        self.position = position
    
    def get_Colour(self):
        return self.color

    def get_Shape(self):
        return self.shape

    def get_Dimensions(self):
        return self.dimensions

    def get_Position(self):
        return self.position
