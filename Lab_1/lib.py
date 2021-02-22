from sympy import *
from sympy.geometry import *

def show_result(a_x, a_y, b_x, b_y, c_x, c_y, d_x, d_y, t_x, t_y):
    a = Point(a_x, a_y)
    b = Point(b_x, b_y)
    c = Point(c_x, c_y)
    d = Point(d_x, d_y)
    polygon = Polygon(a, b, c, d)
    point = Point(t_x, t_y)
    print("lib: " + str(polygon.encloses_point(point)))