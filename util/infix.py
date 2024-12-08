class Infix:
    def __init__(self, function):
        self.function = function

    def __ror__(self, other):
        return Infix(lambda x: self.function(other, x))

    def __call__(self, a, b):
        return self.function(a, b)

    def __or__(self, other):
        return self.function(other)