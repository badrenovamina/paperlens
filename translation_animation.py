"""
Sample animation for the concept library: TRANSLATION (mRNA -> protein)

Written for Manim Community Edition (`pip install manim`), same tooling
and setup as osmosis_animation.py in this folder.

TO RENDER (once you have Python + manim installed locally):
    manim -pql translation_animation.py Translation   # quick preview
    manim -pqh translation_animation.py Translation   # final render

Note: like osmosis_animation.py, this avoids Tex()/MathTex() (no LaTeX
install required) and uses Text() only. Targets Manim CE ~0.18+.

SCIENCE NOTE FOR REVIEW: this uses a short made-up 4-codon mRNA sequence
(AUG-GGC-UUC-UAA), not a real gene, chosen so it demonstrates a start
codon, two amino acids being added, and a stop codon in one small
example. The codon-to-amino-acid assignments (AUG=Met/start, GGC=Gly,
UUC=Phe, UAA=stop) follow the standard genetic code and are worth
double-checking specifically, since a wrong codon table entry would be a
clear factual error. The ribosome and tRNA are drawn as simple generic
shapes, not the real multi-subunit ribosome structure or cloverleaf tRNA
shape, and this doesn't show post-translational folding — the "protein"
here is just the linear chain of amino acids. Please confirm this framing
reads correctly before treating it as final — see the WORKFLOW NOTE in
osmosis_animation.py for why that review step matters.
"""

from manim import *

CODONS = ["AUG", "GGC", "UUC", "UAA"]
AMINO_ACIDS = {"AUG": "Met", "GGC": "Gly", "UUC": "Phe", "UAA": "STOP"}
CODON_X_POSITIONS = [-3.6, -1.2, 1.2, 3.6]


class Translation(Scene):
    def construct(self):
        # ---- Title ----
        title = Text("Translation: Building a Protein from mRNA", font_size=28)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)

        # ---- mRNA strand, labeled by codon (3-base groups) ----
        mrna_line = Line([-5, 0, 0], [5, 0, 0], color=GREEN)
        self.play(Create(mrna_line))

        codon_labels = VGroup(*[
            Text(codon, font_size=22, color=GREEN).move_to([x, 0.4, 0])
            for codon, x in zip(CODONS, CODON_X_POSITIONS)
        ])
        self.play(LaggedStart(*[FadeIn(c) for c in codon_labels], lag_ratio=0.15))
        self.wait(0.3)

        label = Text(
            "The ribosome reads the mRNA three bases (one codon) at a time",
            font_size=20,
        )
        label.to_edge(DOWN)
        self.play(Write(label))

        # ---- Ribosome ----
        ribosome = Ellipse(width=1.8, height=1.2, color=GRAY, fill_opacity=0.3)
        ribosome.move_to([CODON_X_POSITIONS[0], 0, 0])
        self.play(FadeIn(ribosome))
        self.wait(0.3)

        # ---- Build the polypeptide chain, one amino acid per non-stop codon ----
        new_label = Text(
            "A matching tRNA brings each codon's amino acid to the ribosome",
            font_size=20,
        ).to_edge(DOWN)
        self.play(ReplacementTransform(label, new_label))
        label = new_label

        chain = VGroup()
        chain_x_positions = [-2.4, -1.2, 0.0]

        for i in range(3):  # first 3 codons carry real amino acids
            codon = CODONS[i]
            amino_acid = AMINO_ACIDS[codon]
            x = CODON_X_POSITIONS[i]

            trna = RegularPolygon(n=6, color=PURPLE, fill_opacity=0.5)
            trna.scale(0.35)
            trna.move_to([x, 2.2, 0])
            trna_label = Text(amino_acid, font_size=16, color=PURPLE)
            trna_label.move_to(trna.get_center())

            self.play(FadeIn(trna), FadeIn(trna_label), ribosome.animate.move_to([x, 0, 0]))

            self.play(
                trna.animate.move_to([chain_x_positions[i], 2.9, 0]),
                trna_label.animate.move_to([chain_x_positions[i], 2.9, 0]),
                run_time=0.6,
            )

            link = Circle(radius=0.3, color=PURPLE, fill_opacity=0.5)
            link.move_to([chain_x_positions[i], 2.9, 0])
            link_label = Text(amino_acid, font_size=16, color=PURPLE)
            link_label.move_to(link.get_center())

            self.play(FadeOut(trna), FadeOut(trna_label), FadeIn(link), FadeIn(link_label))
            chain.add(VGroup(link, link_label))

        self.wait(0.3)

        # ---- Stop codon: translation ends ----
        new_label = Text(
            "Stop codon — no matching tRNA, so the ribosome releases the protein",
            font_size=20,
        ).to_edge(DOWN)
        self.play(
            ReplacementTransform(label, new_label),
            ribosome.animate.move_to([CODON_X_POSITIONS[3], 0, 0]),
        )
        label = new_label
        self.wait(0.5)

        self.play(FadeOut(ribosome))

        protein_box = SurroundingRectangle(chain, color=GREEN)
        protein_label = Text("finished protein", font_size=18, color=GREEN)
        protein_label.next_to(protein_box, UP, buff=0.2)
        self.play(Create(protein_box), FadeIn(protein_label))
        self.wait(1)

        # ---- Result ----
        result = Text(
            "Translation: codons are read 3 bases at a time to build\n"
            "a specific chain of amino acids — a protein",
            font_size=22,
            color=GREEN,
        )
        result.next_to(label, UP, buff=0.5)
        self.play(Write(result))
        self.wait(2)
