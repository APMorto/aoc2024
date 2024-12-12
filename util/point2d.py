from enum import Enum
from typing import Union


class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Union[int, float]):
        return Point2D(self.x * other, self.y * other)

    def pairwise_mult(self, other: "Point2D"):
        return Point2D(self.x * other.x, self.y * other.y)

    def dot(self, other: "Point2D"):
        return self.x * other.x + self.y * other.y

    def turn_right(self):
        return Point2D(self.y, -self.x)

    def turn_left(self):
        return Point2D(-self.y, self.x)

    def turn_around(self):
        return Point2D(self.x * -1, self.y * -1)

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

# Default direction pointers.
#Point2D.RIGHT = Point2D(0, 1)
#Point2D.DOWN =  Point2D(1, 0)
#Point2D.LEFT =  Point2D(0, -1)
#Point2D.UP =    Point2D(-1, 0)
class Point2DDirections(Enum):
    RIGHT = Point2D(0, 1)
    DOWN = Point2D(1, 0)
    LEFT = Point2D(0, -1)
    UP = Point2D(-1, 0)

