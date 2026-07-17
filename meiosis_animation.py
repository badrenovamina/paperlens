"""
Sample animation for the concept library: MEIOSIS I vs MEIOSIS II

Written for Manim Community Edition (`pip install manim`), same tooling
and setup as osmosis_animation.py in this folder.

TO RENDER (once you have Python + manim installed locally):
    manim -pql meiosis_animation.py Meiosis     # quick low-res preview
    manim -pqh meiosis_animation.py Meiosis     # final high quality render

Note: like osmosis_animation.py, this avoids Tex()/MathTex() (no LaTeX
install required) and uses Text() only. Targets Manim CE ~0.18+.

SCIENCE NOTE FOR REVIEW: this simplifies real meiosis for teaching
clarity — it tracks 2 homologous chromosome pairs (not a full human 23),
and Meiosis I here shows one specific, fixed assortment of which homolog
goes to which pole, not realistic random independent assortment. It also
does NOT model crossing over (chromosome recombination during prophase
I). Because of that second simplification, the 4 final cells in this
specific animation only represent 2 distinct genetic combinations (each
appearing twice, as identical sister chromatids), not 4 fully unique
ones — real meiosis relies on crossing over, not just independent
assortment, to make all 4 gametes genetically distinct. The final result
line is worded as a general statement about meiosis rather than a
literal claim about these exact 4 drawn cells, to stay accurate. Please
confirm this framing is acceptable before treating this as final — see
the WORKFLOW NOTE in osmosis_animation.py for why that review step
matters.
"""

from manim import *
import random

random.seed(17)


def make_chromosome(color=WHITE, size=0.35):
    """A duplicated chromosome: two sister chromatids joined at a
    centromere, drawn as a simple X."""
    a = Line(UP * size, DOWN * size, color=color, stroke_width=6).rotate(PI / 5)
    b = Line(UP * size, DOWN * size, color=color, stroke_width=6).rotate(-PI / 5)
    return VGroup(a, b)


def make_chromatid(color=WHITE, size=0.35):
    """A single, separated chromatid — one rod."""
    return Line(UP * size, DOWN * size, color=color, stroke_width=6)


class Meiosis(Scene):
    def construct(self):
        # ---- Title ----
        title = Text("Meiosis: One Cell Becomes Four Non-Identical Cells", font_size=28)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ---- Cell + nucleus ----
        cell = Circle(radius=3.0, color=WHITE)
        nucleus = Circle(radius=1.6, color=GRAY)
        self.play(Create(cell), Create(nucleus))

        # Two homologous pairs — one chromosome from each "parent," same
        # gene content, drawn in two shades so you can tell them apart.
        # Pair 1 = red shades, Pair 2 = blue shades. Each is already
        # duplicated (drawn as an X), same as the start of Mitosis.
        pair1_a = make_chromosome(color=RED).move_to([-1.0, 0.6, 0])
        pair1_b = make_chromosome(color=RED_E).move_to([-1.0, -0.6, 0])
        pair2_a = make_chromosome(color=BLUE).move_to([1.0, 0.6, 0])
        pair2_b = make_chromosome(color=BLUE_E).move_to([1.0, -0.6, 0])
        chromosomes = VGroup(pair1_a, pair1_b, pair2_a, pair2_b)

        label = Text(
            "Starting cell: 2 homologous pairs, each chromosome already duplicated",
            font_size=20,
        )
        label.to_edge(DOWN)

        self.play(
            Write(label),
            LaggedStart(*[FadeIn(c) for c in chromosomes], lag_ratio=0.15),
            FadeOut(nucleus),
        )
        self.wait(0.5)

        # ---- Meiosis I, Metaphase: homologous PAIRS line up together ----
        new_label = Text(
            "Meiosis I — Metaphase I: homologous pairs line up together",
            font_size=20,
        ).to_edge(DOWN)

        self.play(
            ReplacementTransform(label, new_label),
            pair1_a.animate.move_to([0, 1.3, 0]),
            pair1_b.animate.move_to([0, 0.7, 0]),
            pair2_a.animate.move_to([0, -0.7, 0]),
            pair2_b.animate.move_to([0, -1.3, 0]),
        )
        label = new_label
        self.wait(0.5)

        # ---- Meiosis I, Anaphase: whole homologs (still duplicated)
        # separate to opposite poles — this is the reduction division ----
        new_label = Text(
            "Anaphase I: whole homologs separate — each pole gets one of each pair",
            font_size=20,
        ).to_edge(DOWN)

        self.play(
            ReplacementTransform(label, new_label),
            pair1_a.animate.move_to([-2.2, 0.6, 0]),
            pair2_a.animate.move_to([-2.2, -0.6, 0]),
            pair1_b.animate.move_to([2.2, 0.6, 0]),
            pair2_b.animate.move_to([2.2, -0.6, 0]),
            run_time=2,
        )
        label = new_label
        self.wait(0.3)

        # ---- Cytokinesis I: two haploid cells, chromosomes still
        # duplicated ----
        new_label = Text(
            "End of Meiosis I: 2 haploid cells, chromosomes still duplicated",
            font_size=20,
        ).to_edge(DOWN)

        left_cell = Circle(radius=1.7, color=WHITE).move_to([-2.2, 0, 0])
        right_cell = Circle(radius=1.7, color=WHITE).move_to([2.2, 0, 0])

        self.play(
            ReplacementTransform(label, new_label),
            FadeOut(cell),
            Create(left_cell),
            Create(right_cell),
        )
        label = new_label
        self.wait(0.5)

        # ---- Meiosis II: sister chromatids separate in EACH cell,
        # same mechanics as ordinary Mitosis, happening in both cells
        # at once ----
        new_label = Text(
            "Meiosis II: sister chromatids separate in each cell (like Mitosis)",
            font_size=20,
        ).to_edge(DOWN)
        self.play(ReplacementTransform(label, new_label))
        label = new_label

        far_left_chromatids = VGroup()
        mid_left_chromatids = VGroup()
        mid_right_chromatids = VGroup()
        far_right_chromatids = VGroup()
        split_animations = []

        for chromo, color in [(pair1_a, RED), (pair2_a, BLUE)]:
            far = make_chromatid(color=color).move_to(chromo.get_center())
            mid = make_chromatid(color=color).move_to(chromo.get_center())
            far_left_chromatids.add(far)
            mid_left_chromatids.add(mid)
            split_animations.append(ReplacementTransform(chromo, VGroup(far, mid)))

        for chromo, color in [(pair1_b, RED_E), (pair2_b, BLUE_E)]:
            mid = make_chromatid(color=color).move_to(chromo.get_center())
            far = make_chromatid(color=color).move_to(chromo.get_center())
            mid_right_chromatids.add(mid)
            far_right_chromatids.add(far)
            split_animations.append(ReplacementTransform(chromo, VGroup(mid, far)))

        self.play(*split_animations)
        self.wait(0.2)

        # Move each chromatid set outward to its own sub-pole — 4 poles
        # total now, 2 within each of the 2 cells from Meiosis I.
        self.play(
            *[m.animate.shift(LEFT * 1.6) for m in far_left_chromatids],
            *[m.animate.shift(RIGHT * 0.9) for m in mid_left_chromatids],
            *[m.animate.shift(LEFT * 0.9) for m in mid_right_chromatids],
            *[m.animate.shift(RIGHT * 1.6) for m in far_right_chromatids],
            run_time=2,
        )
        self.wait(0.3)

        # ---- Cytokinesis II: four haploid cells total ----
        new_label = Text(
            "Cytokinesis II: four haploid cells, each with single chromosomes",
            font_size=20,
        ).to_edge(DOWN)

        far_left_cell = Circle(radius=1.0, color=WHITE).move_to([-3.8, 0, 0])
        mid_left_cell = Circle(radius=1.0, color=WHITE).move_to([-1.3, 0, 0])
        mid_right_cell = Circle(radius=1.0, color=WHITE).move_to([1.3, 0, 0])
        far_right_cell = Circle(radius=1.0, color=WHITE).move_to([3.8, 0, 0])

        self.play(
            ReplacementTransform(label, new_label),
            FadeOut(left_cell),
            FadeOut(right_cell),
            Create(far_left_cell),
            Create(mid_left_cell),
            Create(mid_right_cell),
            Create(far_right_cell),
        )
        label = new_label
        self.wait(0.5)

        # ---- Result ----
        result = Text(
            "Meiosis: 4 haploid cells — genetically distinct thanks to\n"
            "independent assortment and crossing over",
            font_size=22,
            color=GREEN,
        )
        result.next_to(label, UP, buff=0.3)
        self.play(Write(result))
        self.wait(2)
