import random
import pygame
from copy import deepcopy
import time

pygame.init()

WIDTH = 800
HEIGHT = 800

win = pygame.display.set_mode((WIDTH, HEIGHT))

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

win.fill(black)

pygame.display.set_caption("Convex hull using Jarvis March")

gameMode = False

def cmp_to_key(mycmp):
    class K:
        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

    return K


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


mid = Point(0, 0)


# To identify the points of the convex hull
def Left_index(points):
    """
    Finding the left most point
    """
    minn = 0
    for i in range(1, len(points)):
        if points[i].x < points[minn].x:
            minn = i
        elif points[i].x == points[minn].x:
            if points[i].y > points[minn].y:
                minn = i
    return minn


def orientation(p, q, r):
    """
    To find orientation of ordered triplet (p, q, r).
    The function returns following values
    0 --> p, q and r are colinear
    1 --> Clockwise
    2 --> Counterclockwise
    """
    val = (q.y - p.y) * (r.x - q.x) - \
          (q.x - p.x) * (r.y - q.y)

    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2


def quad(p: Point):
    if p.x >= 0 and p.y >= 0:
        return 1
    if p.x <= 0 and p.y >= 0:
        return 2
    if p.x <= 0 and p.y <= 0:
        return 3
    return 4


# compare function for sorting
def compare(p1, q1):
    p = Point(p1.x - mid.x, p1.y - mid.y)
    q = Point(q1.x - mid.x, q1.y - mid.y)

    one = quad(p)
    two = quad(q)

    if one != two:
        return one < two
    return p.y * q.x < q.y * p.x


def convexHull(points, n):
    # There must be at least 3 points
    if n < 3:
        return

    # Find the leftmost point
    l = Left_index(points)

    hull = []

    p = l
    q = 0
    while True:

        # Add current point to result
        hull.append(deepcopy(points[p]))

        q = (p + 1) % n

        for i in range(n):
            if (orientation(points[p],
                            points[i], points[q]) == 2):
                q = i
        p = q

        # While we don't come to x point
        if p == l:
            break

    # return sorted(hull, key=lambda point: point.x)
    ret = hull
    global mid
    mid = Point(0, 0)
    n = len(ret)
    for i in range(n):
        mid.x += ret[i].x
        mid.y += ret[i].y
        ret[i].x *= n
        ret[i].y *= n

    ret.sort(key=cmp_to_key(compare))
    for j in range(n):
        ret[j] = Point(ret[j].x // n, ret[j].y // n)

    for j in range(0, len(points)):
        pygame.draw.circle(win, white, (points[j].x, points[j].y), 2, 1)

    # To display the convex hull points and the lines connecting them
    for i in range(0, len(hull)):
        # print(hull[i].x, hull[i].y)
        pygame.draw.circle(win, red, (hull[i].x, hull[i].y), 2, 1)
        line_next = (i + 1) % int(len(hull))
        pygame.draw.line(win, white, (hull[i].x, hull[i].y), (hull[line_next].x, hull[line_next].y))

    time.sleep(0.1)
    pygame.display.update()

    return ret


def orientation2(a, b, c):
    res = (b.y - a.y) * (c.x - b.x) - (c.y - b.y) * (b.x - a.x)

    if res == 0:
        return 0
    if res > 0:
        return 1
    return -1


def merger(a: [Point], b: [Point]):
    # n1 -> number of points in polygon a
    # n2 -> number of points in polygon b
    n1 = len(a)
    n2 = len(b)

    ia = 0
    ib = 0
    for i in range(1, n1):
        if a[i].x > a[ia].x:
            ia = i

    # ib -> leftmost point of b
    for i in range(1, n2):
        if b[i].x < b[ib].x:
            ib = i

    # finding the upper tangent
    inda = ia
    indb = ib
    done = 0
    while not done:
        done = 1
        while orientation2(b[indb], a[inda], a[(inda + 1) % n1]) >= 0:
            inda = (inda + 1) % n1

        while orientation2(a[inda], b[indb], b[(n2 + indb - 1) % n2]) <= 0:
            indb = (n2 + indb - 1) % n2
            done = 0

    uppera = inda
    upperb = indb
    inda = ia
    indb = ib
    done = 0
    g = 0
    while not done:  # finding the lower tangent
        done = 1
        while orientation2(a[inda], b[indb], b[(indb + 1) % n2]) >= 0:
            indb = (indb + 1) % n2

        while orientation2(b[indb], a[inda], a[(n1 + inda - 1) % n1]) <= 0:
            inda = (n1 + inda - 1) % n1
            done = 0

    lowera = inda
    lowerb = indb
    ret = []

    # ret contains the convex hull after merging the two convex hulls
    # with the points sorted in anti-clockwise order
    ind = uppera
    ret.append(a[uppera])
    while ind != lowera:
        ind = (ind + 1) % n1
        ret.append(a[ind])

    ind = lowerb
    ret.append(b[lowerb])
    while ind != upperb:
        ind = (ind + 1) % n2
        ret.append(b[ind])


    hull = ret
    # To display the convex hull points and the lines connecting them
    for i in range(0, len(hull)):
        # print(hull[i].x, hull[i].y)
        pygame.draw.circle(win, red, (hull[i].x, hull[i].y), 2, 1)
        line_next = (i + 1) % int(len(hull))
        pygame.draw.line(win, red, (hull[i].x, hull[i].y), (hull[line_next].x, hull[line_next].y))

    time.sleep(0.5)
    pygame.display.update()
    return ret


# Returns the convex hull for the given set of points
def divide(a: [Point]):
    # If the number of points is less than 6 then the
    # function uses the Jarvis march to find the
    # convex hull
    if len(a) <= 10:
        return convexHull(a, len(a))

    # left contains the left half points
    # right contains the right half points
    left = []
    right = []
    for i in range(len(a) // 2):
        left.append(a[i])
    for i in range(len(a) // 2, len(a)):
        right.append(a[i])

    # convex hull for the left and right sets
    left_hull = divide(left)
    right_hull = divide(right)

    # merging the convex hulls
    return merger(left_hull, right_hull)


def main():
    points = []

    i = 0
    while i < 100:
        points.append(Point(random.randint(200, 699), random.randint(200, 599)))
        i = i + 1

    points.sort(key=lambda point: point.x)

    hull = divide(points)
    # To display all the random points
    for j in range(0, len(points)):
        pygame.draw.circle(win, white, (points[j].x, points[j].y), 2, 1)

    # To display the convex hull points and the lines connecting them
    for i in range(0, len(hull)):
        # print(hull[i].x, hull[i].y)
        pygame.draw.circle(win, red, (hull[i].x, hull[i].y), 2, 1)
        line_next = (i + 1) % int(len(hull))
        pygame.draw.line(win, white, (hull[i].x, hull[i].y), (hull[line_next].x, hull[line_next].y))
    while i < 1500:
        # To stop pygame from closing the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                i = 2000
        pygame.display.update()


main()