"""
Sample animation for the concept library: FACILITATED DIFFUSION

Written for Manim Community Edition (`pip install manim`), same tooling
and setup as osmosis_animation.py in this folder.

TO RENDER (once you have Python + manim installed locally):
    manim -pql facilitated_diffusion_animation.py FacilitatedDiffusion   # quick preview
    manim -pqh facilitated_diffusion_animation.py FacilitatedDiffusion   # final render

Note: like osmosis_animation.py, this avoids Tex()/MathTex() (no LaTeX
install required) and uses Text() only. Targets Manim CE ~0.18+.

SCIENCE NOTE FOR REVIEW: this shows the core idea — a specific molecule
(here, glucose) that can't cross the lipid bilayer unassisted, moving
through an embedded transport protein, down its concentration gradient,
with no ATP required. It simplifies real facilitated diffusion by using
one generic protein shape rather than distinguishing channel proteins
(passive pores) from carrier proteins (which bind and change shape to
shuttle the molecule through, e.g. GLUT transporters for glucose) — both
are real facilitated diffusion mechanisms. Please confirm the "can't
cross directly, needs a specific protein, still passive/no ATP" framing
reads correctly before this is treated as final — see the WORKFLOW NOTE
in osmosis_animation.py for why that review step matters.
"""

from manim import *
import random

random.seed(9)


class FacilitatedDiffusion(Scene):
    def construct(self):
        # ---- Title ----
        title = Text("Facilitated Diffusion: Crossing via a Helper Protein", font_size=30)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ---- Container + membrane (same pattern as osmosis_animation.py) ----
        container = Rectangle(width=10, height=5, color=WHITE)
        self.play(Create(container))

        membrane = DashedLine(start=[0, 2.5, 0], end=[0, -2.5, 0], color=GRAY)
        self.play(Create(membrane))

        # ---- Transport protein embedded in the membrane ----
        protein = RoundedRectangle(
            width=0.55, height=2.0, corner_radius=0.25, color=PURPLE, fill_opacity=0.6
        )
        protein.move_to([0, 0, 0])
        protein_label = Text("transport protein", font_size=18, color=PURPLE)
        protein_label.next_to(protein, UP, buff=0.3)
        self.play(FadeIn(protein), FadeIn(protein_label))
        self.wait(0.5)
                # ---- Side labels ----
        left_label = Text("High glucose concentration", font_size=20, color=ORANGE)
        left_label.move_to([-3.5, 2.0, 0])
        right_label = Text("Low glucose concentration", font_size=20, color=ORANGE)
        right_label.move_to([3.5, 2.0, 0])
        self.play(FadeIn(left_label), FadeIn(right_label))

        # ---- Glucose molecules: mostly on the high side, a few already
        # on the low side (the uneven starting distribution is what
        # drives net movement toward the low side) ----
        left_molecules = VGroup(*[
            Dot(color=ORANGE, radius=0.12).move_to(
                [random.uniform(-4.5, -0.8), random.uniform(-2, 1.5), 0]
            )
            for _ in range(10)
        ])
        right_molecules = VGroup(*[
            Dot(color=ORANGE, radius=0.12).move_to(
                [random.uniform(0.8, 4.5), random.uniform(-2, 1.5), 0]
            )
            for _ in range(3)
        ])

        self.play(
            LaggedStart(*[FadeIn(m) for m in left_molecules], lag_ratio=0.08),
            LaggedStart(*[FadeIn(m) for m in right_molecules], lag_ratio=0.08),
        )
        self.wait(0.5)
                # ---- A molecule can't cross the bare lipid bilayer alone ----
        blocked_label = Text(
            "Glucose can't cross the lipid bilayer directly — it needs the protein",
            font_size=20,
        )
        blocked_label.to_edge(DOWN)
        self.play(Write(blocked_label))

        blocked_molecule = left_molecules[0]
        original_pos = blocked_molecule.get_center()
        # Try to cross directly, away from the protein — bounce back.
        self.play(blocked_molecule.animate.move_to([-0.3, 1.8, 0]), run_time=0.6)
        self.play(blocked_molecule.animate.move_to(original_pos), run_time=0.6)
        self.wait(0.5)

        # ---- Successful crossings: molecules move through the protein ----
        crossing_label = Text(
            "Molecules pass through the protein's channel, still just\n"
            "moving down their concentration gradient — no ATP needed",
            font_size=20,
        ).to_edge(DOWN)
        self.play(ReplacementTransform(blocked_label, crossing_label))

        crossing_molecules = left_molecules[1:6]  # 5 molecules make the crossing

        # First, funnel them toward the protein's position...
        funnel_animations = [
            mol.animate.move_to([0, random.uniform(-0.6, 0.6), 0])
            for mol in crossing_molecules
        ]
        self.play(*funnel_animations, run_time=1)

        # ...then out the other side, into the low-concentration region.
        exit_animations = [
            mol.animate.move_to([random.uniform(1.0, 4.3), random.uniform(-1.8, 1.5), 0])
            for mol in crossing_molecules
        ]
        self.play(*exit_animations, run_time=2)
        self.wait(0.5)

        # ---- Result ----
        result = Text(
            "Facilitated diffusion: passive transport through a specific\n"
            "protein, high to low concentration — no energy required",
            font_size=22,
            color=GREEN,
        )
        result.next_to(crossing_label, UP, buff=0.3)
        self.play(Write(result))
        self.wait(2)
        

