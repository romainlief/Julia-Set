from Julia import JuliaSet
import numpy as np


class JuliaRenderer:
    def __init__(self, function: JuliaSet) -> None:
        self.function = function

    def render(self, grid):
        return self.function.escape_times(grid)