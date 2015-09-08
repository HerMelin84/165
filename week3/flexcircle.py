import math
class FlexCircle():

    def __init__(self,radius):
        self.radius =radius
        self.area=math.pi*self.radius**2
        self.perimeter=2*math.pi*self.radius

        def set_area(self):
            self.area=math.pi*self.radius**2
            set_radius()
            set_perimeter()
        def get_area(self):
            return self.area
        def set_perimeter(self):
            self.perimeter=2*math.pi*self.radius
            set_radius()
            set_area()
        def get_perimeter(self):
            return self.perimeter
        def set_radius(self):
            self.radius = self.perimeter/(2.*math.pi)
            set_perimeter()
            set_area()
        def get_radius(self):
            return self.perimeter/(2.*math.pi)
            
        radius=property(get_radius,set_radius)
        area=property(get_area,set_area)
        perimeter=property(get_perimeter,set_perimeter)
