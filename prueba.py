from manim import *


class Prueba(Scene):
    def construct(self):
        titulo = Text("Hola Manim", font_size=60)
        self.play(Write(titulo))
        self.play(titulo.animate.to_edge(UP))

        ejes = Axes(x_range=[-3, 3, 1], y_range=[-1, 9, 2], x_length=6, y_length=4)
        parabola = ejes.plot(lambda x: x**2, color=YELLOW)
        etiqueta = Text("y = x²", font_size=32, color=YELLOW).next_to(ejes, RIGHT)

        self.play(Create(ejes))
        self.play(Create(parabola), FadeIn(etiqueta))

        punto = Dot(ejes.c2p(-3, 9), color=RED)
        self.add(punto)
        self.play(MoveAlongPath(punto, parabola), run_time=2)
        self.wait()
