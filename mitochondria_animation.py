"""
Sample animation for the concept library: MITOCHONDRIA
("the powerhouse of the cell")

Written for Manim Community Edition (`pip install manim`), same tooling
and setup as osmosis_animation.py in this folder.

TO RENDER (once you have Python + manim installed locally):
    manim -pql mitochondria_animation.py Mitochondria   # quick preview
    manim -pqh mitochondria_animation.py Mitochondria   # final render

Note: like osmosis_animation.py, this avoids Tex()/MathTex() (no LaTeX
install required) and uses Text() only. Targets Manim CE ~0.18+.

SCIENCE NOTE FOR REVIEW: this shows the core "powerhouse" idea — a
double membrane (smooth outer, folded inner), the folds (cristae)
increasing surface area for ATP production, a matrix containing its own
DNA, and ATP being produced and released. It deliberately skips the
actual electron transport chain / chemiosmosis mechanism (that's its own
concept — ATP synthase, task #11 in the roadmap) and just shows "ATP
comes out of the cristae" as a black box. Please confirm the outer/inner
membrane and cristae description read correctly, and that treating ATP
production as a black box here (rather than explaining chemiosmosis) is
the right call for this concept vs. the separate ATP synthase animation
— see the WORKFLOW NOTE in osmosis_animation.py for why that review step
matters.
"""

from manim import *
import random

random.seed(5)  # keep the "random" ribosome dot placement reproducible

# Fixed positions for the finger-shaped cristae (folds of the inner
# membrane) — hand-placed rather than computed, to keep this simple and
# match the style of the other concept scripts.
CRISTAE = [
    (-1.6, 0.55, 20), (-1.6, -0.55, -20),
    (0.0, 0.75, 0), (0.0, -0.75, 0),
    (1.6, 0.55, -20), (1.6, -0.55, 20),
]


class Mitochondria(Scene):
    def construct(self):
        # ---- Title ----
        title = Text("Mitochondria: The Cell's Powerhouse", font_size=30)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)

        # ---- Outer membrane ----
        outer_membrane = Ellipse(width=6.2, height=3.4, color=WHITE)
        self.play(Create(outer_membrane))

        label = Text("Outer membrane: smooth boundary", font_size=20)
        label.to_edge(DOWN)
        self.play(Write(label))
        self.wait(0.5)

        # ---- Inner membrane, folded into cristae ----
        inner_membrane = Ellipse(width=4.6, height=2.3, color=PINK)
        cristae = VGroup()
        for x, y, deg in CRISTAE:
            finger = Ellipse(width=1.0, height=0.22, color=PINK, fill_opacity=0.4, stroke_width=2)
            finger.rotate(deg * DEGREES)
            finger.move_to([x, y, 0])
            cristae.add(finger)

        new_label = Text(
            "Inner membrane folds into cristae — more surface area for making ATP",
            font_size=20,
        ).to_edge(DOWN)

        self.play(
            ReplacementTransform(label, new_label),
            Create(inner_membrane),
            LaggedStart(*[FadeIn(c) for c in cristae], lag_ratio=0.1),
        )
        label = new_label
        self.wait(0.5)

        # ---- Matrix: its own DNA + ribosomes ----
        mito_dna = Circle(radius=0.18, color=ORANGE, stroke_width=3)
        mito_dna.move_to([0, 0, 0])
        ribosomes = VGroup(*[
            Dot(color=GRAY, radius=0.05).move_to(
                [random.uniform(-0.7, 0.7), random.uniform(-0.3, 0.3), 0]
            )
            for _ in range(6)
        ])

        new_label = Text(
            "Matrix: contains its own DNA and enzymes for the Krebs cycle",
            font_size=20,
        ).to_edge(DOWN)

        self.play(
            ReplacementTransform(label, new_label),
            Create(mito_dna),
            LaggedStart(*[FadeIn(r) for r in ribosomes], lag_ratio=0.1),
        )
        label = new_label
        self.wait(0.5)

        # ---- ATP production at the cristae ----
        new_label = Text(
            "Aerobic respiration at the cristae produces ATP",
            font_size=20,
        ).to_edge(DOWN)
        self.play(ReplacementTransform(label, new_label))
        label = new_label

        atp_origins = [(-1.6, 0.55), (0.0, 0.75), (1.6, 0.55), (-1.6, -0.55)]
        for x, y in atp_origins:
            atp_dot = Dot(color=GREEN, radius=0.09).move_to([x, y, 0])
            atp_text = Text("ATP", font_size=14, color=GREEN)
            atp_text.next_to(atp_dot, UP, buff=0.05)
            atp_token = VGroup(atp_dot, atp_text)

            outward = [x * 1.8, y * 1.8, 0]
            self.play(FadeIn(atp_token), run_time=0.3)
            self.play(atp_token.animate.move_to(outward), run_time=0.6)
            self.play(FadeOut(atp_token), run_time=0.3)

        self.wait(0.3)

        # ---- Result ----
        result = Text(
            "Fuel + oxygen in, ATP out — the cell's energy currency",
            font_size=24,
            color=GREEN,
        )
        result.next_to(label, UP, buff=0.3)
        self.play(Write(result))
        self.wait(2)
