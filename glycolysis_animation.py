"""
Sample animation for the concept library: GLYCOLYSIS (overview)

Written for Manim Community Edition (`pip install manim`), same tooling
and setup as osmosis_animation.py in this folder.

TO RENDER (once you have Python + manim installed locally):
    manim -pql glycolysis_animation.py Glycolysis   # quick preview
    manim -pqh glycolysis_animation.py Glycolysis   # final render

Note: like osmosis_animation.py, this avoids Tex()/MathTex() (no LaTeX
install required) and uses Text() only. Targets Manim CE ~0.18+.

SCIENCE NOTE FOR REVIEW: this is deliberately an "overview, not every
intermediate" animation (matching how this concept is scoped in
cell_biology_concepts.md) — real glycolysis is about 10 distinct
enzyme-catalyzed steps with several named intermediate molecules, and
this shows that as an abstract "many steps happen here" sequence rather
than naming each one. The one number worth double-checking carefully:
net ATP yield is stated as "2 ATP net (4 made, 2 spent)" rather than
just "2 ATP" — glycolysis actually produces 4 ATP but consumes 2 during
the earlier "investment phase," and stating only the net number without
that context is a common oversimplification worth avoiding here. Also
worth confirming: this doesn't address what happens to pyruvate next
(aerobic vs. anaerobic pathways) since that's outside this concept's
scope. See the WORKFLOW NOTE in osmosis_animation.py for why review
matters before this is treated as final.
"""

from manim import *
import random

random.seed(21)


class Glycolysis(Scene):
    def construct(self):
        # ---- Title ----
        title = Text("Glycolysis: Splitting Glucose for Energy", font_size=28)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)

        location_label = Text("in the cytoplasm — no oxygen required", font_size=18, color=GRAY)
        location_label.next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(location_label))

        # ---- Glucose ----
        glucose = RegularPolygon(n=6, color=BLUE, fill_opacity=0.4)
        glucose.scale(0.9)
        glucose.move_to([-5, 0, 0])
        glucose_label = Text("Glucose\n(6 carbons)", font_size=18, color=BLUE)
        glucose_label.move_to(glucose.get_center())
        self.play(FadeIn(glucose), FadeIn(glucose_label))
        self.wait(0.3)

        # ---- Abstract "many enzymatic steps" sequence ----
        label = Text(
            "About 10 enzyme-catalyzed steps break glucose down piece by piece",
            font_size=20,
        )
        label.to_edge(DOWN)
        self.play(Write(label))

        step_dots = VGroup(*[
            Dot(radius=0.08, color=GRAY).move_to([x, 0, 0])
            for x in [-3.2, -2.2, -1.2, -0.2, 0.8]
        ])
        self.play(
            glucose.animate.move_to([-4, 0, 0]),
            glucose_label.animate.move_to([-4, 0, 0]),
        )
        self.play(LaggedStart(*[
            Flash(d, color=YELLOW, flash_radius=0.2) for d in step_dots
        ], lag_ratio=0.3), run_time=2)
        self.wait(0.3)

        # ---- Move glucose to the output area, then split into pyruvate ----
        new_label = Text(
            "Net result: one glucose becomes two pyruvate molecules",
            font_size=20,
        ).to_edge(DOWN)

        self.play(
            glucose.animate.move_to([2.0, 0, 0]),
            glucose_label.animate.move_to([2.0, 0, 0]),
            FadeOut(step_dots),
        )

        pyruvate_1 = Triangle(color=ORANGE, fill_opacity=0.5).scale(0.5)
        pyruvate_1.move_to([2.0, 0.8, 0])
        pyruvate_2 = Triangle(color=ORANGE, fill_opacity=0.5).scale(0.5)
        pyruvate_2.move_to([2.0, -0.8, 0])
        pyruvate_label_1 = Text("Pyruvate", font_size=16, color=ORANGE)
        pyruvate_label_1.next_to(pyruvate_1, UP, buff=0.15)
        pyruvate_label_2 = Text("Pyruvate", font_size=16, color=ORANGE)
        pyruvate_label_2.next_to(pyruvate_2, DOWN, buff=0.15)

        self.play(
            ReplacementTransform(label, new_label),
            ReplacementTransform(VGroup(glucose, glucose_label), VGroup(pyruvate_1, pyruvate_2)),
            FadeIn(pyruvate_label_1),
            FadeIn(pyruvate_label_2),
        )
        label = new_label
        self.wait(0.5)

        # ---- Net energy yield ----
        new_label = Text(
            "Net yield per glucose: 2 ATP (4 made, 2 spent earlier) + 2 NADH",
            font_size=20,
        ).to_edge(DOWN)
        self.play(ReplacementTransform(label, new_label))
        label = new_label

        atp_tokens = VGroup()
        for y in [1.5, -1.5]:
            token = Dot(color=GREEN, radius=0.1).move_to([4.2, y, 0])
            token_label = Text("ATP", font_size=14, color=GREEN)
            token_label.next_to(token, UP, buff=0.05)
            atp_tokens.add(VGroup(token, token_label))

        nadh_tokens = VGroup()
        for y in [0.5, -0.5]:
            token = Dot(color=YELLOW, radius=0.1).move_to([4.9, y, 0])
            token_label = Text("NADH", font_size=14, color=YELLOW)
            token_label.next_to(token, UP, buff=0.05)
            nadh_tokens.add(VGroup(token, token_label))

        self.play(
            LaggedStart(*[FadeIn(t) for t in atp_tokens], lag_ratio=0.2),
            LaggedStart(*[FadeIn(t) for t in nadh_tokens], lag_ratio=0.2),
        )
        self.wait(1)

        # ---- Result ----
        result = Text(
            "Glycolysis: glucose → 2 pyruvate, net 2 ATP + 2 NADH,\n"
            "in the cytoplasm, with or without oxygen",
            font_size=22,
            color=GREEN,
        )
        result.next_to(label, UP, buff=0.3)
        self.play(Write(result))
        self.wait(2)
