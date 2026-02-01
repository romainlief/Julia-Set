from const import (
    WIDTH,
    HEIGHT,
    RE_MIN,
    RE_MAX,
    IM_MIN,
    IM_MAX,
    C_RE,
    C_IM,
)

from Julia import JuliaSet
from Cgrid import ComplexGrid
from renderer import JuliaRenderer
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets


class Simulation:
    def __init__(
        self,
        width=WIDTH,
        height=HEIGHT,
        re_min=RE_MIN,
        re_max=RE_MAX,
        im_min=IM_MIN,
        im_max=IM_MAX,
    ) -> None:
        self.max_iter = 200
        self.c = complex(C_RE, C_IM)
        self.julia_function = JuliaSet(self.max_iter, self.c)
        self.grid = ComplexGrid(width, height, re_min, re_max, im_min, im_max)
        self.renderer = JuliaRenderer(self.julia_function)
        self.paused = False
        # Cache des rendus par viewport (LRU simple)
        self._render_cache = {}
        self._cache_order = []
        self._cache_max = 100

    def run(self):
        grid = self.grid.grid()
        M = self.renderer.render(grid)

        fig, ax = plt.subplots(figsize=(12, 7))
        # Réserver de l'espace sur la droite pour les contrôles
        fig.subplots_adjust(right=0.80)
        ax.set_aspect("equal", adjustable="box")
        img = ax.imshow(
            M,
            extent=(
                self.grid.re_min,
                self.grid.re_max,
                self.grid.im_min,
                self.grid.im_max,
            ),
            cmap="Greys",
            interpolation="bilinear",
            origin="upper",
        )
        # fig.colorbar(img, ax=ax) decommenter pour afficher une barre de couleur
        ax.set_title("Julia Set")
        ax.set_xlabel("Re")
        ax.set_ylabel("Im")

        # Dessiner une cible (croix) au centre de la fenêtre
        re_c = (self.grid.re_min + self.grid.re_max) / 2.0
        im_c = (self.grid.im_min + self.grid.im_max) / 2.0
        # Garder des références pour mise à jour
        self.fig = fig
        self.ax = ax
        self.img = img
        self.vline = ax.axvline(re_c, color="white", linewidth=1.0, alpha=0.8)
        self.hline = ax.axhline(im_c, color="white", linewidth=1.0, alpha=0.8)

        # Dessiner des boutons pour déplacer la vue (côte à côte, en haut à droite)
        ax_btn_up = plt.axes([0.8, 0.85, 0.08, 0.05])  # type: ignore
        btn_up = widgets.Button(ax_btn_up, "Up")
        btn_up.on_clicked(lambda event: self.move_viewport(0, 0.1))

        ax_btn_down = plt.axes([0.9, 0.85, 0.08, 0.05])  # type: ignore
        btn_down = widgets.Button(ax_btn_down, "Down")
        btn_down.on_clicked(lambda event: self.move_viewport(0, -0.1))

        ax_btn_left = plt.axes([0.8, 0.75, 0.08, 0.05])  # type: ignore
        btn_left = widgets.Button(ax_btn_left, "Left")
        btn_left.on_clicked(lambda event: self.move_viewport(-0.1, 0))

        ax_btn_right = plt.axes([0.9, 0.75, 0.08, 0.05])  # type: ignore
        btn_right = widgets.Button(ax_btn_right, "Right")
        btn_right.on_clicked(lambda event: self.move_viewport(0.1, 0))

        ax_btn_zoom_in = plt.axes([0.8, 0.65, 0.08, 0.05])  # type: ignore
        btn_zoom_in = widgets.Button(ax_btn_zoom_in, "Zoom In")
        btn_zoom_in.on_clicked(lambda event: self.zoom_viewport(0.8))

        ax_btn_zoom_out = plt.axes([0.9, 0.65, 0.08, 0.05])  # type: ignore
        btn_zoom_out = widgets.Button(ax_btn_zoom_out, "Zoom Out")
        btn_zoom_out.on_clicked(lambda event: self.zoom_viewport(1.25))

        ax_btn_reset = plt.axes([0.85, 0.55, 0.1, 0.05])  # type: ignore
        btn_reset = widgets.Button(ax_btn_reset, "Reset View")
        btn_reset.on_clicked(lambda event: self.reset_viewport())

        plt.show()

    def move_viewport(self, delta_re, delta_im):
        re_width = self.grid.re_max - self.grid.re_min
        im_height = self.grid.im_max - self.grid.im_min
        re_shift = delta_re * re_width
        im_shift = delta_im * im_height

        self.grid.re_min += re_shift
        self.grid.re_max += re_shift
        self.grid.im_min += im_shift
        self.grid.im_max += im_shift

        self.re_compute()

        self.recenter_viewport()

    def zoom_viewport(self, zoom_factor):
        re_center = (self.grid.re_min + self.grid.re_max) / 2.0
        im_center = (self.grid.im_min + self.grid.im_max) / 2.0
        re_width = (self.grid.re_max - self.grid.re_min) * zoom_factor
        im_height = (self.grid.im_max - self.grid.im_min) * zoom_factor

        self.grid.re_min = re_center - re_width / 2.0
        self.grid.re_max = re_center + re_width / 2.0
        self.grid.im_min = im_center - im_height / 2.0
        self.grid.im_max = im_center + im_height / 2.0

        self.re_compute()

        self.recenter_viewport()

    def reset_viewport(self):
        self.paused = True
        self.grid.re_min = RE_MIN
        self.grid.re_max = RE_MAX
        self.grid.im_min = IM_MIN
        self.grid.im_max = IM_MAX

        self.re_compute()

        # Recentrer la cible
        self.recenter_viewport()

    def recenter_viewport(self):
        re_c = (self.grid.re_min + self.grid.re_max) / 2.0
        im_c = (self.grid.im_min + self.grid.im_max) / 2.0
        self.vline.set_xdata([re_c, re_c])
        self.hline.set_ydata([im_c, im_c])

        # Rafraîchir l'affichage
        self.ax.figure.canvas.draw_idle()

    def move_to_a_viewport(self, re, im):
        re_c = re
        im_c = im
        self.paused = False
        re_width = self.grid.re_max - self.grid.re_min
        im_height = self.grid.im_max - self.grid.im_min

        self.grid.re_min = re_c - re_width / 2.0
        self.grid.re_max = re_c + re_width / 2.0
        self.grid.im_min = im_c - im_height / 2.0
        self.grid.im_max = im_c + im_height / 2.0

        self.re_compute()
        while True:
            if self.paused:
                break
            self.zoom_viewport(0.8)
            plt.pause(0.1)

    def re_compute(self):
        # Essayer de récupérer depuis le cache
        key = self._viewport_key()
        M = self._render_cache.get(key)
        if M is None:
            M = self.renderer.render(self.grid.grid())
            self._put_cache(key, M)
        self.img.set_data(M)
        self.img.set_extent(
            (
                self.grid.re_min,
                self.grid.re_max,
                self.grid.im_min,
                self.grid.im_max,
            )
        )
        # self.print_viewport()

    def _viewport_key(self):
        # Quantification pour éviter les clés flottantes quasi-identiques
        q = 1e-12
        return (
            round(self.grid.re_min / q) * q,
            round(self.grid.re_max / q) * q,
            round(self.grid.im_min / q) * q,
            round(self.grid.im_max / q) * q,
            self.grid.width,
            self.grid.height,
            self.julia_function.max_iter,
            float(self.c.real),
            float(self.c.imag),
        )

    def _put_cache(self, key, value):
        if key in self._render_cache:
            return
        self._render_cache[key] = value
        self._cache_order.append(key)
        if len(self._cache_order) > self._cache_max:
            old = self._cache_order.pop(0)
            self._render_cache.pop(old, None)

    def print_viewport(self):
        print(
            f"Re_min: {self.grid.re_min}, Re_max: {self.grid.re_max}, Im_min: {self.grid.im_min}, Im_max: {self.grid.im_max}"
        )
