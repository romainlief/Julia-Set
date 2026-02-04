import numpy as np


class JuliaSet:
    def __init__(self, max_iter, c: complex) -> None:
        self.max_iter = max_iter
        self.c = c

    def escape_times(self, grid):
        z = grid.copy()
        # Choisir le plus petit dtype entier non signé suffisant pour max_iter
        if self.max_iter <= 255:
            int_dtype = np.uint8
        elif self.max_iter <= 65535:
            int_dtype = np.uint16
        else:
            int_dtype = np.uint32
        M = np.zeros(grid.shape, dtype=int_dtype)

        alive = np.ones(grid.shape, dtype=bool)
        radius2 = 4.0

        for _ in range(self.max_iter):
            # Mettre à jour le masque des points encore "vivants" sans calculer de racine
            still_alive = (z.real * z.real + z.imag * z.imag) <= radius2
            alive &= still_alive

            if not alive.any():
                break

            np.add(M, 1, out=M, where=alive)
            np.multiply(z, z, out=z, where=alive)
            np.add(z, self.c, out=z, where=alive)

        return M
