import math
class Circle():
    """
    Circle object with a radius.
    """
    def __init__(self, radius):
        """
        Construct new 'Circle' object.
        
        :param r: the radius.
        """
        self.r = radius
        
    def area(self):
        """
        Computes and returns the area.
        """
        return math.pi*self.r**2
    def perimeter(self):
        """
        Computes and returns the perimeter.
        """
        return 2*math.pi*self.r

