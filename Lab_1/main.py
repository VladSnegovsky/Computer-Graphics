from graphics import *
import lib
import FindResult as function

# Point A
a_x = 1
a_y = 1
# Point B
b_x = 3
b_y = 5
# Point C
c_x = 7
c_y = 4
# Point D
d_x = 5
d_y = 1
# Point Test
t_x = 3
t_y = 0

lib.show_result(a_x, a_y, b_x, b_y, c_x, c_y, d_x, d_y, t_x, t_y)

polygon = [4, [a_x,a_y], [b_x,b_y], [c_x,c_y], [d_x,d_y]]
point = [t_x,t_y]
function.find_result(polygon, point)

window = GraphWin("Window", 800, 600)
polygon = Polygon(Point(a_x * 100, a_y * 100), Point(b_x * 100, b_y * 100),
                  Point(c_x * 100, c_y * 100), Point(d_x * 100, d_y * 100))
point = Point(t_x * 100, t_y * 100)
polygon.draw(window)
point.draw(window)
window.getMouse()
window.close()