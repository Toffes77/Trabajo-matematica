from manim import *
from manim_slides import Slide


class Presentacion(Slide):
    def construct(self):
        titulo = Text("Teorema de Pitágoras", font_size=56)
        self.play(Write(titulo))
        self.next_slide()

        formula = MathTex(r"a^2 + b^2 = c^2", font_size=72)
        self.play(ReplacementTransform(titulo, formula))
        self.next_slide()

        triangulo = Polygon(ORIGIN, 3 * RIGHT, 3 * RIGHT + 2 * UP, color=BLUE)
        triangulo.next_to(formula, DOWN)
        self.play(Create(triangulo))
        self.next_slide()
