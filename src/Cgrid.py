import numpy as np


class ComplexGrid:
    def __init__(
        self,
        width,
        height,
        re_min,
        re_max,
        im_min,
        im_max,
        flip_im=True,
        dtype=np.complex128,
    ):
        self.width = width
        self.height = height
        self.re_min = re_min
        self.re_max = re_max
        self.im_min = im_min
        self.im_max = im_max
        self.flip_im = flip_im
        # Permettre complex64 pour réduire mémoire/temps si souhaité
        self.dtype = np.dtype(dtype)

    def grid(self):
        re = np.linspace(self.re_min, self.re_max, self.width)
        if self.flip_im:
            im = np.linspace(self.im_max, self.im_min, self.height)
        else:
            im = np.linspace(self.im_min, self.im_max, self.height)
        # Convertir au dtype cible si nécessaire (ex.: complex64)
        return (re + im[:, None] * 1j).astype(self.dtype, copy=False)
