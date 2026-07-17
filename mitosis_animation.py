"""
Sample animation for the concept library: MITOSIS

Written for Manim Community Edition (`pip install manim`), same tooling
and setup as osmosis_animation.py in this folder.

TO RENDER (once you have Python + manim installed locally):
    manim -pql mitosis_animation.py Mitosis     # quick low-res preview
    manim -pqh mitosis_animation.py Mitosis     # final high quality render

Note: like osmosis_animation.py, this avoids Tex()/MathTex() (no LaTeX
install required) and uses Text() only. Targets Manim CE ~0.18+.

SCIENCE NOTE FOR REVIEW: this simplifies real mitosis for teaching
clarity — it shows 3 chromosomes (not a full human 46) and starts at
prophase, skipping G1/S/G2 of interphase. Sister chromatids are drawn as
an "X" (two chromatids joined at a centromere) and shown separating
equally, one full identical copy to each pole — that even split is the
core concept this animation exists to teach. Please confirm the phase
order/labels and the "identical daughter cells" claim read correctly
before this is treated as final — see the WORKFLOW NOTE in
osmosis_animation.py for why that review step matters.
"""

from manim import *
import random

random.seed(11)  # keep the "random" chromosome placement reproducible


def make_chromosome(color=WHITE, size=0.35):
    """A duplicated chromosome: two sister chromatids joined at a
    centromere, drawn as a simple X (avoids needing real DNA geometry)."""
    a = Line(UP * size, DOWN * size, color=color, stroke_width=6).rotate(PI / 5)
    b = Line(UP * size, DOWN * size, color=color, stroke_width=6).rotate(-PI / 5)
    return VGroup(a, b)


def make_chromatid(color=WHITE, size=0.35):
    """A single, separated chromatid (post-anaphase) — one rod."""
    return Line(UP * size, DOWN * size, color=color, stroke_width=6)


class Mitosis(Scene):
    def construct(self):
        colors = [RED, BLUE, GREEN]

        # ---- Title ----
        title = Text("Mitosis: One Cell Becomes Two Identical Cells", font_size=30)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)

        # ---- Cell + nucleus ----
        cell = Circle(radius=3.0, color=WHITE)
        nucleus = Circle(radius=1.6, color=GRAY)
        self.play(Create(cell), Create(nucleus))

        phase_label = Text(
            "Interphase: DNA is copied but stays loosely packed as chromatin",
            font_size=22,
        )
        phase_label.to_edge(DOWN)
        self.play(Write(phase_label))
        self.wait(0.5)

        # ---- Prophase: chromosomes condense, nuclear envelope breaks down ----
        chromosomes = VGroup(*[
            make_chromosome(color=colors[i]).move_to(
                [random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), 0]
            )
            for i in range(3)
        ])

        new_label = Text(
            "Prophase: chromosomes condense; nuclear envelope breaks down",
            font_size=22,
        ).to_edge(DOWN)

        self.play(
            ReplacementTransform(phase_label, new_label),
            LaggedStart(*[FadeIn(c) for c in chromosomes], lag_ratio=0.15),
            FadeOut(nucleus),
        )
        phase_label = new_label
        self.wait(0.5)

        # ---- Metaphase: chromosomes align at the equator ----
        target_ys = [1.0, 0.0, -1.0]
        new_label = Text(
            "Metaphase: chromosomes line up at the cell's equator",
            font_size=22,
        ).to_edge(DOWN)

        self.play(
            ReplacementTransform(phase_label, new_label),
            *[chromosomes[i].animate.move_to([0, target_ys[i], 0]) for i in range(3)],
        )
        phase_label = new_label
        self.wait(0.5)

        # ---- Anaphase: sister chromatids separate toward opposite poles ----
        new_label = Text(
            "Anaphase: sister chromatids separate, one full set per pole",
            font_size=22,
        ).to_edge(DOWN)

        left_chromatids = VGroup()
        right_chromatids = VGroup()
        split_animations = []
        for i in range(3):
            y = target_ys[i]
            left = make_chromatid(color=colors[i]).move_to([0, y, 0])
            right = make_chromatid(color=colors[i]).move_to([0, y, 0])
            left_chromatids.add(left)
            right_chromatids.add(right)
            split_animations.append(ReplacementTransform(chromosomes[i], VGroup(left, right)))

        self.play(ReplacementTransform(phase_label, new_label), *split_animations)
        phase_label = new_label
        self.wait(0.2)

        self.play(
            *[left_chromatids[i].animate.move_to([-2.2, target_ys[i], 0]) for i in range(3)],
            *[right_chromatids[i].animate.move_to([2.2, target_ys[i], 0]) for i in range(3)],
            run_time=2,
        )
        self.wait(0.3)

        # ---- Telophase: nuclear envelopes reform around each set ----
        new_label = Text(
            "Telophase: a nuclear envelope reforms around each identical set",
            font_size=22,
        ).to_edge(DOWN)

        left_envelope = Circle(radius=1.3, color=GRAY).move_to([-2.2, 0, 0])
        right_envelope = Circle(radius=1.3, color=GRAY).move_to([2.2, 0, 0])

        self.play(
            ReplacementTransform(phase_label, new_label),
            Create(left_envelope),
            Create(right_envelope),
        )
        phase_label = new_label
        self.wait(0.5)

        # ---- Cytokinesis: the cell membrane splits in two ----
        new_label = Text(
            "Cytokinesis: the cell membrane pinches inward and splits",
            font_size=22,
        ).to_edge(DOWN)

        left_membrane = Circle(radius=1.7, color=WHITE).move_to([-2.2, 0, 0])
        right_membrane = Circle(radius=1.7, color=WHITE).move_to([2.2, 0, 0])

        self.play(
            ReplacementTransform(phase_label, new_label),
            FadeOut(cell),
            Create(left_membrane),
            Create(right_membrane),
        )
        phase_label = new_label
        self.wait(0.5)

        # ---- Result ----
        result = Text(
            "Two genetically identical daughter cells",
            font_size=26,
            color=GREEN,
        )
        result.next_to(phase_label, UP, buff=0.3)
        self.play(Write(result))
        self.wait(2)
