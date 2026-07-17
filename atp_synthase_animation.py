"""
Sample animation for the concept library: ATP SYNTHASE / CHEMIOSMOSIS

Written for Manim Community Edition (`pip install manim`), same tooling
and setup as osmosis_animation.py in this folder.

TO RENDER (once you have Python + manim installed locally):
    manim -pql atp_synthase_animation.py ATPSynthase   # quick preview
    manim -pqh atp_synthase_animation.py ATPSynthase   # final render

Note: like osmosis_animation.py, this avoids Tex()/MathTex() (no LaTeX
install required) and uses Text() only. Targets Manim CE ~0.18+.

SCIENCE NOTE FOR REVIEW: this is meant as the "zoom in" companion to
mitochondria_animation.py, which deliberately treated ATP production as
a black box. This one shows specifically how a proton (H+) gradient gets
converted into ATP: H+ ions flow through ATP synthase down their
concentration gradient, and that flow is shown driving a rotating part
of the enzyme, which is linked to ADP + phosphate combining into ATP.
Real simplifications worth flagging: (1) this treats the H+ gradient as
already existing rather than showing the electron transport chain that
actually builds it — that's a separate, much larger topic; (2) ATP
synthase's real structure (F0 membrane-embedded rotor + F1 catalytic
head, and the actual rotary catalysis mechanism) is simplified into a
generic channel-plus-spinning-circle shape, not accurate molecular
structure. Please confirm the core "H+ flow spins ATP synthase, which
powers ADP + Pi -> ATP" claim reads correctly before this is treated as
final — see the WORKFLOW NOTE in osmosis_animation.py for why that
review step matters.
"""

from manim import *
import random

random.seed(13)


class ATPSynthase(Scene):
    def construct(self):
        # ---- Title ----
        title = Text("ATP Synthase: Turning a Proton Gradient into ATP", font_size=26)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)

        # ---- Membrane ----
        membrane_top = Line([-5, 0.6, 0], [5, 0.6, 0], color=WHITE)
        membrane_bottom = Line([-5, -0.6, 0], [5, -0.6, 0], color=WHITE)
        self.play(Create(membrane_top), Create(membrane_bottom))

        top_label = Text("intermembrane space — high H+ concentration", font_size=16, color=GRAY)
        top_label.move_to([0, 2.6, 0])
        bottom_label = Text("matrix — low H+ concentration", font_size=16, color=GRAY)
        bottom_label.move_to([0, -2.6, 0])
        self.play(FadeIn(top_label), FadeIn(bottom_label))

        # ---- H+ ions, concentrated above the membrane ----
        protons = VGroup(*[
            Text("+", font_size=18, color=RED).move_to(
                [random.uniform(-4.5, 4.5), random.uniform(1.0, 2.2), 0]
            )
            for _ in range(14)
        ])
        self.play(LaggedStart(*[FadeIn(p) for p in protons], lag_ratio=0.05))
        self.wait(0.3)

        # ---- ATP synthase embedded in the membrane ----
        channel = RoundedRectangle(
            width=0.6, height=1.6, corner_radius=0.2, color=TEAL, fill_opacity=0.5
        )
        channel.move_to([0, 0, 0])
        head = Circle(radius=0.55, color=TEAL, fill_opacity=0.4)
        head.move_to([0, -1.1, 0])
        rotor_marker = Line(head.get_center(), head.get_center() + RIGHT * 0.45, color=WHITE)
        synthase_label = Text("ATP synthase", font_size=18, color=TEAL)
        synthase_label.next_to(channel, LEFT, buff=1.0)
        synthase_arrow = Arrow(
            synthase_label.get_right(), channel.get_left(), buff=0.1, color=TEAL, stroke_width=2
        )

        self.play(
            FadeIn(channel), FadeIn(head), Create(rotor_marker),
            FadeIn(synthase_label), Create(synthase_arrow),
        )
        self.wait(0.5)
        self.play(FadeOut(synthase_label), FadeOut(synthase_arrow))

        # ---- H+ flows through, spinning the rotor ----
        label = Text(
            "H+ flows down its gradient, through ATP synthase, spinning it like a turbine",
            font_size=18,
        )
        label.to_edge(DOWN)
        self.play(Write(label))

        flowing = protons[:6]
        flow_animations = [
            p.animate.move_to([0, random.uniform(-0.5, 0.5), 0]) for p in flowing
        ]
        self.play(*flow_animations, run_time=1.2)
        self.play(
            Rotate(rotor_marker, angle=3 * PI, about_point=head.get_center()),
            *[
                p.animate.move_to([random.uniform(-4.5, 4.5), random.uniform(-2.2, -1.0), 0])
                for p in flowing
            ],
            run_time=2,
        )
        self.wait(0.3)

        # ---- ADP + Pi -> ATP ----
        new_label = Text(
            "That spin drives ADP + phosphate (Pi) combining into ATP",
            font_size=18,
        ).to_edge(DOWN)
        self.play(ReplacementTransform(label, new_label))
        label = new_label

        adp = Text("ADP", font_size=16, color=ORANGE).move_to([-0.9, -1.1, 0])
        pi = Text("Pi", font_size=16, color=ORANGE).move_to([0.9, -1.1, 0])
        self.play(FadeIn(adp), FadeIn(pi))
        self.play(adp.animate.move_to([-0.15, -1.1, 0]), pi.animate.move_to([0.15, -1.1, 0]))

        atp_token = Text("ATP", font_size=20, color=GREEN).move_to([0, -1.1, 0])
        self.play(ReplacementTransform(VGroup(adp, pi), atp_token))
        self.play(atp_token.animate.shift(DOWN * 0.6))
        self.wait(0.5)

        # ---- Result ----
        result = Text(
            "Chemiosmosis: the H+ gradient built by the electron transport\n"
            "chain flows through ATP synthase, powering most of the cell's ATP",
            font_size=20,
            color=GREEN,
        )
        result.next_to(label, UP, buff=0.3)
        self.play(Write(result))
        self.wait(2)
