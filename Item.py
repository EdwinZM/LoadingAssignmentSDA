
class Item():
    
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.shape = None
        self.dimensions = []
    
    def get_Colour(self):
        return self.color
    
    def get_Shape(self):
        return self.shape
    
    def get_Dimensions(self):
        return self.dimensions
    
    def get_Position(self):
        return self.position
