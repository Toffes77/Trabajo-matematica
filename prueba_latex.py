from manim import *


class PruebaLatex(Scene):
    def construct(self):
        paso1 = MathTex(r"\int_0^1 x^2 \, dx")
        paso2 = MathTex(r"\left[ \frac{x^3}{3} \right]_0^1")
        paso3 = MathTex(r"\frac{1}{3}")
        self.play(Write(paso1))
        self.wait(0.5)
        self.play(ReplacementTransform(paso1, paso2))
        self.wait(0.5)
        self.play(ReplacementTransform(paso2, paso3))
        self.play(Circumscribe(paso3))
        self.wait()
