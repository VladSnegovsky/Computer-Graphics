import FindIntersections as findIntersection

def find_min_max_x(polygon):
    max_x = polygon[1][0]
    min_x = polygon[1][0]
    for i in range(polygon[0]):
        if polygon[i+1][0] > max_x:
            max_x = polygon[i+1][0]
        elif polygon[i+1][0] < min_x:
            min_x = polygon[i+1][0]

    return [min_x, max_x]

def find_result(polygon, point):
    ans = find_min_max_x(polygon)

    if ans[0] > point[0] and ans[1] > point[0]:
        print("Point outside the polygon.")
    elif ans[0] < point[0] and ans[1] < point[0]:
        print("Point outside the polygon.")
    else:
        right_line = ((point[0], point[1]), (ans[1], point[1]))
        left_line = ((ans[0], point[1]), (point[0], point[1]))

        right_line_intersections = 0
        left_line_intersections = 0

        for i in range(polygon[0]):
            if i+2 > polygon[0]:
                if findIntersection.line_intersection(right_line, ((polygon[i+1][0], polygon[i+1][1]), (polygon[1][0], polygon[1][1]))):
                    right_line_intersections = right_line_intersections + 1
                if findIntersection.line_intersection(left_line, ((polygon[i+1][0], polygon[i+1][1]), (polygon[1][0], polygon[1][1]))):
                    left_line_intersections = left_line_intersections + 1
            else:
                if findIntersection.line_intersection(right_line, ((polygon[i+1][0], polygon[i+1][1]), (polygon[i+2][0], polygon[i+2][1]))):
                    right_line_intersections = right_line_intersections + 1
                if findIntersection.line_intersection(left_line, ((polygon[i+1][0], polygon[i+1][1]), (polygon[i+2][0], polygon[i+2][1]))):
                    left_line_intersections = left_line_intersections + 1

        if left_line_intersections == right_line_intersections == 1:
            print("Point inside the polygon.")
        else:
            print("Point outside the polygon.")