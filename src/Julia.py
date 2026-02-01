import numpy as np


class JuliaSet:
    def __init__(self, max_iter, c: complex) -> None:
        self.max_iter = max_iter
        self.c = c

    def escape_times(self, grid):
        z = grid.copy()
        M = np.zeros(grid.shape, dtype=np.int32)

        for _ in range(self.max_iter):
            alive = np.abs(z) <= 2.0
            M[alive] += 1
            z[alive] = z[alive] * z[alive] + self.c

        return M
