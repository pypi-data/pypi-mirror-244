__version__ = "0.0.5"

from AlgeoMathBlockBuilder import Builder


class AlgeoMathBlock(Builder):
    def __init__(self):
        super().__init__()

    def add_function_graph(self, func_initial, latex):
        self.execute_set(f'"{func_initial}"', f'"{func_initial}(x)={latex}"')

    def add_function_dot(self, name, x, func_initial):
        self.execute_set(name, f'"("+({x})+",{func_initial}("+({x})+"))"')

    def add_polygon(self, name, list):
        polygonStr = ",".join(list)
        self.execute_set(f'"{name}"', f'"Polygon({polygonStr})"')
