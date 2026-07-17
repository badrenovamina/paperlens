"""
Sample animation for the concept library: DNA REPLICATION (semi-conservative)

Written for Manim Community Edition (`pip install manim`), same tooling
and setup as osmosis_animation.py in this folder.

TO RENDER (once you have Python + manim installed locally):
    manim -pql dna_replication_animation.py DNAReplication   # quick preview
    manim -pqh dna_replication_animation.py DNAReplication   # final render

Note: like osmosis_animation.py, this avoids Tex()/MathTex() (no LaTeX
install required) and uses Text() only. Targets Manim CE ~0.18+.

SCIENCE NOTE FOR REVIEW: this shows the core "semi-conservative" idea —
the double helix unwinds, and each original strand serves as a template
for one new complementary strand, so each resulting molecule has one old
strand and one new strand. It simplifies real replication a lot: real
DNA polymerase only synthesizes 5' to 3', so one new strand (the
"leading" strand) is made continuously while the other (the "lagging"
strand) is made in short pieces (Okazaki fragments) and stitched
together by DNA ligase — this animation shows both new strands being
built smoothly and simultaneously instead, and doesn't distinguish
helicase/primase/polymerase/ligase as separate enzymes. It also uses a
short made-up 8-base sequence, not a real gene. Please confirm the
"semi-conservative, one old + one new strand per result" framing reads
correctly before this is treated as final — see the WORKFLOW NOTE in
osmosis_animation.py for why that review step matters.
"""

from manim import *

STRAND_A_BASES = ["A", "T", "G", "C", "C", "T", "A", "G"]

DNA_COMPLEMENT = {"T": "A", "A": "T", "C": "G", "G": "C"}

STRAND_B_BASES = [DNA_COMPLEMENT[b] for b in STRAND_A_BASES]

X_POSITIONS = [-4.2 + 1.2 * i for i in range(len(STRAND_A_BASES))]


class DNAReplication(Scene):
    def construct(self):
        # ---- Title ----
        title = Text("DNA Replication: Semi-Conservative Copying", font_size=28)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)

        # ---- Original double helix (shown flat, not literally helical) ----
        strand_a = Line([-5, 1, 0], [5, 1, 0], color=BLUE)
        strand_b = Line([-5, -1, 0], [5, -1, 0], color=ORANGE)
        self.play(Create(strand_a), Create(strand_b))

        strand_a_letters = VGroup(*[
            Text(b, font_size=22, color=BLUE).move_to([x, 1, 0])
            for b, x in zip(STRAND_A_BASES, X_POSITIONS)
        ])
        strand_b_letters = VGroup(*[
            Text(b, font_size=22, color=ORANGE).move_to([x, -1, 0])
            for b, x in zip(STRAND_B_BASES, X_POSITIONS)
        ])
        rungs = VGroup(*[
            Line([x, 0.75, 0], [x, -0.75, 0], color=GRAY, stroke_width=2)
            for x in X_POSITIONS
        ])

        self.play(
            LaggedStart(*[FadeIn(l) for l in strand_a_letters], lag_ratio=0.1),
            LaggedStart(*[FadeIn(l) for l in strand_b_letters], lag_ratio=0.1),
            LaggedStart(*[Create(r) for r in rungs], lag_ratio=0.1),
        )
        self.wait(0.3)

        # ---- Helicase unwinds: strands separate, rungs disappear ----
        label = Text(
            "Helicase unwinds the double helix, separating the two strands",
            font_size=20,
        )
        label.to_edge(DOWN)

        self.play(
            Write(label),
            strand_a.animate.shift(UP * 0.8),
            strand_a_letters.animate.shift(UP * 0.8),
            strand_b.animate.shift(DOWN * 0.8),
            strand_b_letters.animate.shift(DOWN * 0.8),
            LaggedStart(*[FadeOut(r) for r in rungs], lag_ratio=0.05),
        )
        self.wait(0.3)

        # ---- DNA polymerase builds a new complementary strand off EACH
        # original strand ----
        new_label = Text(
            "DNA polymerase builds a new complementary strand off each original",
            font_size=20,
        ).to_edge(DOWN)
        self.play(ReplacementTransform(label, new_label))
        label = new_label

        new_bases_for_a = [DNA_COMPLEMENT[b] for b in STRAND_A_BASES]
        new_bases_for_b = [DNA_COMPLEMENT[b] for b in STRAND_B_BASES]

        # strand_a is now at y=1.8 (after the unwind shift) — the new
        # strand paired with it sits just below, at y=1.45.
        new_strand_for_a = VGroup(*[
            Text(b, font_size=22, color=GREEN).move_to([x, 1.45, 0])
            for b, x in zip(new_bases_for_a, X_POSITIONS)
        ])
        # strand_b is now at y=-1.8 — its new strand sits just above.
        new_strand_for_b = VGroup(*[
            Text(b, font_size=22, color=GREEN).move_to([x, -1.45, 0])
            for b, x in zip(new_bases_for_b, X_POSITIONS)
        ])

        self.play(
            LaggedStart(*[FadeIn(l) for l in new_strand_for_a], lag_ratio=0.08),
            LaggedStart(*[FadeIn(l) for l in new_strand_for_b], lag_ratio=0.08),
        )
        self.wait(0.3)

        # ---- Each pair moves apart into its own complete double helix ----
        new_label = Text(
            "Each new molecule has one original strand and one new strand",
            font_size=20,
        ).to_edge(DOWN)

        top_group = VGroup(strand_a, strand_a_letters, new_strand_for_a)
        bottom_group = VGroup(strand_b, strand_b_letters, new_strand_for_b)

        self.play(
            ReplacementTransform(label, new_label),
            top_group.animate.shift(UP * 1.0),
            bottom_group.animate.shift(DOWN * 1.0),
        )
        label = new_label

        top_tag = Text("1 old (blue) + 1 new (green) strand", font_size=18, color=GREEN)
        top_tag.next_to(top_group, UP, buff=0.15)
        bottom_tag = Text("1 old (orange) + 1 new (green) strand", font_size=18, color=GREEN)
        bottom_tag.next_to(bottom_group, DOWN, buff=0.15)
        self.play(FadeIn(top_tag), FadeIn(bottom_tag))
        self.wait(1)

        # ---- Result ----
        result = Text(
            "Semi-conservative replication: every new DNA molecule keeps\n"
            "one original strand and gains one newly made strand",
            font_size=22,
            color=GREEN,
        )
        result.move_to([0, 0, 0])
        self.play(Write(result))
        self.wait(2)
