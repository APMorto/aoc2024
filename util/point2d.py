from typing import Union, Tuple


class Point2D:
    DIRECTIONS: Tuple["Point2D"]
    RIGHT: "Point2D"
    DOWN: "Point2D"
    LEFT: "Point2D"
    UP: "Point2D"

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def turn_right(self):
        return Point2D(self.y, -self.x)

    def turn_left(self):
        return Point2D(-self.y, self.x)

    def turn_around(self):
        return Point2D(self.x * -1, self.y * -1)

    def row_major(self, width: int):
        return self.x + self.y * width

    def get_adjacent_ortho(self):
        for o in Point2D.DIRECTIONS:
            yield self + o

    def pairwise_mult(self, other: "Point2D"):
        return Point2D(self.x * other.x, self.y * other.y)

    def dot(self, other: "Point2D"):
        return self.x * other.x + self.y * other.y

    def manhattan_distance(self, other: "Point2D"):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def adjacent_within_2_manhatten_distance(self):
        for ro, co in (       (-2, 0),
                    (-1, -1), (-1, 0), (-1, 1),
           (0, -2), (0, -1),           (0, 1),  (0, 2),
                    (1, -1),  (1, 0),  (1, 1),
                              (2, 0)):
            yield Point2D(self.x + co, self.y + ro)

    def adjacent_within_3_manhatten_distance(self):
        for ro, co in (               (-3, 0),
                            (-2, -1),  (-2, 0), (-2, 1),
                 (-1, -2),  (-1, -1), (-1, 0), (-1, 1), (-1, 2),
        (0, -3), (0, -2),   (0, -1),           (0, 1),  (0, 2),  (0, 3),
                 (1, -2),   (1, -1),  (1, 0),  (1, 1),  (1, 2),
                            (2, -1),  (2, 0),  (2, 1),
                                      (3, 0)):
            yield Point2D(self.x + co, self.y + ro)

    def points_within_manhatten_distance(self, dist: int):
        for y in range(self.y - dist, self.y + dist + 1):
            width = abs(dist - abs(self.y - y))
            for x in range(self.x - width, self.x + width + 1):
                yield Point2D(x, y)

    def __add__(self, other):
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Union[int, float]):
        return Point2D(self.x * other, self.y * other)

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __iter__(self):
        return iter((self.x, self.y))

    def __hash__(self):
        return hash((self.x, self.y))
        #a = self.x # https://stackoverflow.com/questions/919612/mapping-two-integers-to-one-in-a-unique-and-deterministic-way
        #b = self.y # Slower.
        #return (a * a + a + b) if a >= b else (a + b * b)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y

# Default direction pointers.
Point2D.RIGHT = Point2D(0, 1)
Point2D.DOWN =  Point2D(1, 0)
Point2D.LEFT =  Point2D(0, -1)
Point2D.UP =    Point2D(-1, 0)
Point2D.DIRECTIONS = (Point2D.RIGHT, Point2D.DOWN, Point2D.LEFT, Point2D.UP)

