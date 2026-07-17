"""
Sample animation for the concept library: OSMOSIS

This is written for Manim Community Edition (the actively maintained fork —
`pip install manim`, not the older 3b1b "ManimGL"). This is the same family
of tooling 3Blue1Brown's videos are built with, so this is a genuine example
of the pipeline, not a simplified stand-in.

TO RENDER (once you have Python + manim installed locally):
    manim -pql osmosis_animation.py Osmosis     # quick low-res preview
    manim -pqh osmosis_animation.py Osmosis     # final high quality render

Note: manim requires a working LaTeX install for Tex()/MathTex() text —
this script avoids that and uses Text() only, so it has fewer setup
dependencies. Also note Manim's API shifts slightly between versions;
if a parameter name below errors, check `manim --version` and the docs
for that version (this targets Manim CE ~0.18+).

WORKFLOW NOTE: treat a first draft of a script like this as a starting
point, not ground truth. You (or a reviewer) should sanity-check the
science and visuals before rendering. Don't skip the human review step —
an animation that's visually convincing but scientifically wrong is
worse than no animation.
"""

from manim import *
import random

random.seed(7)  # keep the "random" molecule placement reproducible


class Osmosis(Scene):
    def construct(self):
        # ---- Title ----
        title = Text("Osmosis: Water Movement Across a Membrane", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ---- Container ----
        container = Rectangle(width=10, height=5, color=WHITE)
        self.play(Create(container))

        # ---- Membrane (dashed line = pores water can pass, solute can't) ----
        membrane = DashedLine(
            start=[0, 2.5, 0],
            end=[0, -2.5, 0],
            color=GRAY,
        )
        membrane_label = Text("semi-permeable membrane", font_size=20, color=GRAY)
        membrane_label.next_to(membrane, UP, buff=0.2)
        self.play(Create(membrane), FadeIn(membrane_label))

        # ---- Side labels ----
        left_label = Text("High solute\n(low water)", font_size=22, color=ORANGE)
        left_label.move_to([-3.5, 2.0, 0])
        right_label = Text("Low solute\n(high water)", font_size=22, color=BLUE)
        right_label.move_to([3.5, 2.0, 0])
        self.play(FadeIn(left_label), FadeIn(right_label))

        # ---- Solute molecules: stay on the left, can't cross membrane ----
        solutes = VGroup(*[
            Dot(color=ORANGE, radius=0.12).move_to(
                [random.uniform(-4.5, -0.5), random.uniform(-2, 1.3), 0]
            )
            for _ in range(10)
        ])

        # ---- Water molecules: start unevenly distributed ----
        water_left = VGroup(*[
            Dot(color=BLUE, radius=0.1).move_to(
                [random.uniform(-4.5, -0.5), random.uniform(-1.8, -0.3), 0]
            )
            for _ in range(4)
        ])
        water_right = VGroup(*[
            Dot(color=BLUE, radius=0.1).move_to(
                [random.uniform(0.5, 4.5), random.uniform(-2, 1.5), 0]
            )
            for _ in range(12)
        ])

        self.play(
            LaggedStart(*[FadeIn(s) for s in solutes], lag_ratio=0.05),
            LaggedStart(*[FadeIn(w) for w in water_left], lag_ratio=0.05),
            LaggedStart(*[FadeIn(w) for w in water_right], lag_ratio=0.05),
        )
        self.wait(0.5)

        # ---- Explanation text ----
        explain = Text(
            "Water moves toward higher solute concentration\n"
            "to balance concentration on both sides",
            font_size=22,
        )
        explain.to_edge(DOWN)
        self.play(Write(explain))

        # ---- Animate net water movement: right -> left ----
        movers = water_right[:6]
        move_animations = []
        for dot in movers:
            target = [random.uniform(-4.5, -0.5), random.uniform(-2, 1.3), 0]
            move_animations.append(dot.animate.move_to(target))

        self.play(*move_animations, run_time=3, rate_func=smooth)
        self.wait(1)

        # ---- Result ----
        result = Text(
            "Net water movement equalizes concentration",
            font_size=24,
            color=GREEN,
        )
        result.next_to(explain, UP, buff=0.3)
        self.play(Write(result))
        self.wait(2)
