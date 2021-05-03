import copy

import pygame


# checks whether the point crosses the convex hull
# or not
def orientation(a, b, c):
    res = ((b[1] - a[1]) * (c[0] - b[0]) -
           (c[1] - b[1]) * (b[0] - a[0]))

    if (res == 0):
        return 0
    if (res > 0):
        return 1
    return -1


# Returns the square of distance between two input points
def sqDist(p1, p2):
    return ((p1[0] - p2[0]) * (p1[0] - p2[0]) +
            (p1[1] - p2[1]) * (p1[1] - p2[1]))


# Checks whether the point is inside the convex hull or not
def inside(a, p):
    # Initialize the centroid of the convex hull
    mid = [0, 0]

    n = len(a)

    # Multiplying with n to avoid floating point
    # arithmetic.
    p[0] *= n
    p[1] *= n
    for i in range(n):
        mid[0] += a[i][0]
        mid[1] += a[i][1]
        a[i][0] *= n
        a[i][1] *= n

    # if the mid and the given point lies always
    # on the same side w.r.t every edge of the
    # convex hull, then the point lies inside
    # the convex hull
    for i in range(n):

        j = (i + 1) % n
        x1 = a[i][0]
        x2 = a[j][0]
        y1 = a[i][1]
        y2 = a[j][1]
        a1 = y1 - y2
        b1 = x2 - x1
        c1 = x1 * y2 - y1 * x2
        for_mid = a1 * mid[0] + b1 * mid[1] + c1
        for_p = a1 * p[0] + b1 * p[1] + c1
        if for_mid * for_p < 0:
            return False

    return True


# Adds a point p to given convex hull a[]
def addPoint(a, p):
    # If point is inside p
    arr = copy.deepcopy(a)
    prr = p.copy()

    if inside(arr, prr):
        return

    # point having minimum distance from the point p
    ind = 0
    n = len(a)
    for i in range(1, n):
        if sqDist(p, a[i]) < sqDist(p, a[ind]):
            ind = i

    # Find the upper tangent
    up = ind
    while orientation(p, a[up], a[(up + 1) % n]) >= 0:
        up = (up + 1) % n

    # Find the lower tangent
    low = ind
    while orientation(p, a[low], a[(n + low - 1) % n]) <= 0:
        low = (n + low - 1) % n

    # Initialize result
    ret = []

    # making the final hull by traversing points
    # from up to low of given convex hull.
    curr = up
    ret.append(a[curr])
    while curr != low:
        curr = (curr + 1) % n
        ret.append(a[curr])

    # Modify the original vector
    ret.append(p)
    a.clear()
    for i in range(len(ret)):
        a.append(ret[i])


class Canvas:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color = {
            'BLACK': (0, 0, 0),
            'WHITE': (255, 255, 255),
            'BLUE': (0, 0, 255),
            'GREEN': (0, 255, 0),
            'RED': (255, 0, 0)
        }
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.exit = False
        self.points = []
        self.hull = []

        pygame.init()
        pygame.display.set_caption("Convex hull")

    def update(self, fps):

        clock = pygame.time.Clock()

        while not self.exit:
            clock.tick(fps)
            self.__update_events()
            self.__render()
            pygame.display.flip()

        pygame.quit()


    def __update_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
            if event.type == pygame.MOUSEBUTTONUP:
                pos_x, pos_y = pygame.mouse.get_pos()
                self.points.append([pos_x, pos_y])
                addPoint(self.hull, [pos_x, pos_y])

    def __render(self):
        self.__fill_background(self.color['BLACK'])
        self.__draw_polyline(self.hull, self.color['BLUE'])
        self.__draw_points(self.points, self.color['RED'])


    def __fill_background(self, color):
        self.screen.fill(color)

    def __draw_points(self, points, color):
        for p in points:
            pygame.draw.circle(self.screen, color, p, 3)

    def __draw_polyline(self, points, color):
        if len(points) < 2:
            return

        point = points[0]
        points = points[1:] + [points[0]]

        for p in points:
            pygame.draw.line(self.screen, color, point, p, 2)
            point = p


# Driver code
if __name__ == "__main__":

    # the set of points in the convex hull in clockwise order
    a = [[50, 250], [100, 100], [250, 100], [300, 300]]
    n = len(a)

    canvas = Canvas(400, 400)
    canvas.points = copy.deepcopy(a)
    canvas.hull = copy.deepcopy(a)
    canvas.update(30)
