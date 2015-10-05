import math
class FlexCircle(object):

    def __init__(self,radius):
        self.__radius=radius
        self.__area=math.pi*self.__radius**2
        self.__perimeter=2*math.pi*self.__radius
        
    def set_area(self,value):
        self.__area=value
        self.__radius=math.sqrt(self.__area/float(math.pi))
        self.__perimeter=2*math.pi*self.__radius
    def get_area(self):
        return self.__area
    def set_perimeter(self,value):
        self.__perimeter=value
        self.radius=self.__perimeter/(2.*math.pi)
        self.area=math.pi*self.__radius**2
    def get_perimeter(self):
        return self.__perimeter
    def set_radius(self,value):
        self.__radius = value
        self.__perimeter = 2*math.pi*self.__radius
    def get_radius(self):
        return self.__radius
                                
    radius=property(get_radius,set_radius)
    perimeter=property(get_perimeter,set_perimeter)
    area=property(get_area,set_area)
