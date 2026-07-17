"""
Sample animation for the concept library: CELL MEMBRANE STRUCTURE
(the phospholipid bilayer)

Written for Manim Community Edition (`pip install manim`), same tooling
and setup as osmosis_animation.py in this folder.

TO RENDER (once you have Python + manim installed locally):
    manim -pql cell_membrane_animation.py CellMembrane   # quick preview
    manim -pqh cell_membrane_animation.py CellMembrane   # final render

Note: like osmosis_animation.py, this avoids Tex()/MathTex() (no LaTeX
install required) and uses Text() only. Targets Manim CE ~0.18+.

SCIENCE NOTE FOR REVIEW: this shows the core "fluid mosaic model" idea —
a bilayer of phospholipids (hydrophilic heads facing the water on both
sides, hydrophobic tails hiding from water in the middle) studded with
an embedded protein, and it's fluid (components can drift sideways). It
skips cholesterol, glycoproteins/glycolipids, and the asymmetry between
the two leaflets — all real but left out for a first-pass intro
animation. Please confirm the head/tail orientation and the "fluid"
claim read correctly before this is treated as final — see the WORKFLOW
NOTE in osmosis_animation.py for why that review step matters.
"""

from manim import *
import random

random.seed(3)  # keep the "random" water molecule scatter reproducible

ROW_X_POSITIONS = [-4.2 + 1.2 * i for i in range(8)]


def make_phospholipid(head_point, flip=False, color_head=BLUE, color_tail=YELLOW):
    """A phospholipid: a hydrophilic head (dot) with two hydrophobic
    tails (lines) hanging off it. flip=True puts the head on the
    opposite side, for the bottom row of the bilayer."""
    head = Dot(radius=0.14, color=color_head)
    tail_a = Line(ORIGIN, DOWN * 0.65 + LEFT * 0.08, color=color_tail, stroke_width=4)
    tail_b = Line(ORIGIN, DOWN * 0.65 + RIGHT * 0.08, color=color_tail, stroke_width=4)
    group = VGroup(head, tail_a, tail_b)
    if flip:
        group.rotate(PI)
    group.shift(head_point - head.get_center())
    return group


class CellMembrane(Scene):
    def construct(self):
        # ---- Title ----
        title = Text("The Cell Membrane: A Phospholipid Bilayer", font_size=30)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)

        # ---- Water on both sides ----
        outside_water = VGroup(*[
            Dot(color=BLUE_E, radius=0.06).move_to(
                [random.uniform(-4.5, 4.5), random.uniform(1.6, 2.6), 0]
            )
            for _ in range(14)
        ])
        inside_water = VGroup(*[
            Dot(color=BLUE_E, radius=0.06).move_to(
                [random.uniform(-4.5, 4.5), random.uniform(-2.6, -1.6), 0]
            )
            for _ in range(14)
        ])
        outside_label = Text("Extracellular fluid (water)", font_size=18, color=BLUE_E)
        outside_label.move_to([0, 2.9, 0])
        inside_label = Text("Cytoplasm (water)", font_size=18, color=BLUE_E)
        inside_label.move_to([0, -2.9, 0])

        self.play(
            LaggedStart(*[FadeIn(d) for d in outside_water], lag_ratio=0.05),
            LaggedStart(*[FadeIn(d) for d in inside_water], lag_ratio=0.05),
            FadeIn(outside_label),
            FadeIn(inside_label),
        )
        self.wait(0.3)

        # ---- Build the bilayer ----
        top_row = VGroup(*[
            make_phospholipid([x, 0.9, 0], flip=False) for x in ROW_X_POSITIONS
        ])
        bottom_row = VGroup(*[
            make_phospholipid([x, -0.9, 0], flip=True) for x in ROW_X_POSITIONS
        ])

        self.play(
            LaggedStart(*[FadeIn(p) for p in top_row], lag_ratio=0.08),
            LaggedStart(*[FadeIn(p) for p in bottom_row], lag_ratio=0.08),
        )
        self.wait(0.3)

        # ---- Label head vs tail ----
        head_label = Text("hydrophilic head\n(attracted to water)", font_size=18, color=BLUE)
        head_label.move_to([-5.6, 0.9, 0])
        tail_label = Text("hydrophobic tail\n(avoids water)", font_size=18, color=YELLOW)
        tail_label.move_to([-5.6, 0.0, 0])

        head_arrow = Arrow(
            head_label.get_right(), top_row[0][0].get_center(), buff=0.15, color=BLUE, stroke_width=2
        )
        tail_arrow = Arrow(
            tail_label.get_right(), top_row[0][1].get_center(), buff=0.15, color=YELLOW, stroke_width=2
        )

        self.play(
            FadeIn(head_label), FadeIn(tail_label),
            Create(head_arrow), Create(tail_arrow),
        )
        self.wait(1)
        self.play(FadeOut(head_label), FadeOut(tail_label), FadeOut(head_arrow), FadeOut(tail_arrow))

        # ---- Embedded membrane protein ----
        protein = RoundedRectangle(
            width=0.55, height=2.1, corner_radius=0.25, color=PURPLE, fill_opacity=0.6
        )
        protein.move_to([1.8, 0, 0])
        protein_label = Text("membrane protein", font_size=18, color=PURPLE)
        protein_label.next_to(protein, UP, buff=1.0)
        protein_arrow = Arrow(
            protein_label.get_bottom(), protein.get_top(), buff=0.1, color=PURPLE, stroke_width=2
        )

        self.play(FadeIn(protein), FadeIn(protein_label), Create(protein_arrow))
        self.wait(1)
        self.play(FadeOut(protein_label), FadeOut(protein_arrow))
        self.play(FadeOut(outside_label), FadeOut(inside_label))

        # ---- Demonstrate fluidity: a lipid drifts sideways ----
        explain = Text(
            "The membrane is fluid — phospholipids and proteins\n"
            "can drift sideways within the layer",
            font_size=20,
        )
        explain.to_edge(DOWN)
        mover = top_row[0]
        self.play(Write(explain), mover.animate.shift(RIGHT * 2.0), run_time=2.5)
        self.wait(1)

        # ---- Result ----
        result = Text(
            "Fluid mosaic model: a dynamic bilayer studded with proteins",
            font_size=24,
            color=GREEN,
        )
        result.next_to(explain, UP, buff=0.3)
        self.play(Write(result))
        self.wait(2)
