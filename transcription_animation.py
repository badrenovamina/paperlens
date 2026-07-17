"""
Sample animation for the concept library: TRANSCRIPTION (DNA -> mRNA)

Written for Manim Community Edition (`pip install manim`), same tooling
and setup as osmosis_animation.py in this folder.

TO RENDER (once you have Python + manim installed locally):
    manim -pql transcription_animation.py Transcription     # quick preview
    manim -pqh transcription_animation.py Transcription     # final render

Note: like osmosis_animation.py, this avoids Tex()/MathTex() (no LaTeX
install required) and uses Text() only. Targets Manim CE ~0.18+.

SCIENCE NOTE FOR REVIEW: this uses a short made-up 8-base sequence purely
to make the base-pairing rule visible (A-T/A-U, G-C), not a real gene. It
simplifies real transcription for teaching clarity: no promoter-sequence
detail, no 5'/3' directionality labels, and "RNA polymerase unwinds,
copies, and lets the DNA reanneal behind it" is shown as one clean pass
rather than the real elongation-complex geometry. The specific detail
worth double-checking: the base-pairing rule used to derive the mRNA
sequence from the template strand (template T/A/C/G -> mRNA A/U/G/C
respectively) — please confirm those pairings read correctly before this
is treated as final. See the WORKFLOW NOTE in osmosis_animation.py for
why that review step matters.
"""

from manim import *

# A short made-up template strand, chosen so the resulting mRNA happens to
# start with the AUG start codon — a nice, true detail to call out, not a
# coincidence that needs fixing.
TEMPLATE_BASES = ["T", "A", "C", "G", "G", "A", "T", "C"]

# DNA base-pairing rule (template -> coding/non-template strand, same
# alphabet since both strands are DNA):
DNA_COMPLEMENT = {"T": "A", "A": "T", "C": "G", "G": "C"}

# Transcription rule (template -> mRNA). Note T pairs with A, but A pairs
# with U, since RNA has no thymine:
RNA_COMPLEMENT = {"T": "A", "A": "U", "C": "G", "G": "C"}

CODING_BASES = [DNA_COMPLEMENT[b] for b in TEMPLATE_BASES]
MRNA_BASES = [RNA_COMPLEMENT[b] for b in TEMPLATE_BASES]

X_POSITIONS = [-4.2 + 1.2 * i for i in range(len(TEMPLATE_BASES))]


class Transcription(Scene):
    def construct(self):
        # ---- Title ----
        title = Text("Transcription: Copying DNA into mRNA", font_size=30)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)

        # ---- DNA double strand ----
        coding_strand = Line([-5, 1, 0], [5, 1, 0], color=BLUE)
        template_strand = Line([-5, -1, 0], [5, -1, 0], color=ORANGE)
        coding_label = Text("coding strand", font_size=18, color=BLUE)
        coding_label.next_to(coding_strand, LEFT, buff=0.3)
        template_label = Text("template strand", font_size=18, color=ORANGE)
        template_label.next_to(template_strand, LEFT, buff=0.3)

        self.play(
            Create(coding_strand),
            Create(template_strand),
            FadeIn(coding_label),
            FadeIn(template_label),
        )

        coding_letters = VGroup(*[
            Text(b, font_size=24, color=BLUE).move_to([x, 1, 0])
            for b, x in zip(CODING_BASES, X_POSITIONS)
        ])
        template_letters = VGroup(*[
            Text(b, font_size=24, color=ORANGE).move_to([x, -1, 0])
            for b, x in zip(TEMPLATE_BASES, X_POSITIONS)
        ])
        rungs = VGroup(*[
            Line([x, 0.75, 0], [x, -0.75, 0], color=GRAY, stroke_width=2)
            for x in X_POSITIONS
        ])

        self.play(
            LaggedStart(*[FadeIn(l) for l in coding_letters], lag_ratio=0.1),
            LaggedStart(*[FadeIn(l) for l in template_letters], lag_ratio=0.1),
            LaggedStart(*[Create(r) for r in rungs], lag_ratio=0.1),
        )
        self.wait(0.5)

        explain = Text(
            "RNA polymerase reads the template strand and builds a\n"
            "complementary mRNA strand (T pairs with A, A pairs with U)",
            font_size=20,
        )
        explain.to_edge(DOWN)
        self.play(Write(explain))

        # ---- RNA polymerase moves along, synthesizing mRNA base by base ----
        polymerase = Ellipse(width=1.0, height=0.6, color=PURPLE, fill_opacity=0.5)
        polymerase.move_to([X_POSITIONS[0], 0, 0])
        polymerase_label = Text("RNA Pol", font_size=16, color=PURPLE)
        polymerase_label.next_to(polymerase, UP, buff=0.1)
        self.play(FadeIn(polymerase), FadeIn(polymerase_label))
        polymerase_label.add_updater(lambda m: m.next_to(polymerase, UP, buff=0.1))

        mrna_letters = VGroup()
        for i, x in enumerate(X_POSITIONS):
            mrna_base = Text(MRNA_BASES[i], font_size=24, color=GREEN)
            mrna_base.move_to([x, -2.2, 0])
            mrna_letters.add(mrna_base)

            self.play(
                polymerase.animate.move_to([x, 0, 0]),
                FadeOut(rungs[i]),
                FadeIn(mrna_base),
                run_time=0.4,
            )

        polymerase_label.clear_updaters()
        self.play(FadeOut(polymerase), FadeOut(polymerase_label))
        self.wait(0.3)

        mrna_backbone = Line(
            [X_POSITIONS[0], -2.2, 0], [X_POSITIONS[-1], -2.2, 0], color=GREEN
        )
        self.play(Create(mrna_backbone))

        # ---- Call out the start codon ----
        start_box = SurroundingRectangle(mrna_letters[:3], color=YELLOW)
        start_label = Text("AUG — the start codon!", font_size=20, color=YELLOW)
        start_label.next_to(start_box, DOWN, buff=0.2)
        self.play(Create(start_box), Write(start_label))
        self.wait(1)

        # ---- mRNA leaves, DNA strands remain ----
        new_explain = Text(
            "The finished mRNA strand detaches and heads toward\n"
            "the ribosome, where it will be translated into protein",
            font_size=20,
        ).to_edge(DOWN)

        mrna_group = VGroup(mrna_letters, mrna_backbone, start_box, start_label)
        self.play(
            ReplacementTransform(explain, new_explain),
            mrna_group.animate.shift(UP * 0.6),
        )
        self.wait(2)
