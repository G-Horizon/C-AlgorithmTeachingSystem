from pathlib import Path
import sys

from manim import *


COMMON_DIR = Path(__file__).resolve().parents[2] / "common"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from theme import BACKGROUND, CELL_FILL, CELL_STROKE, FONT, MONO_FONT, MUTED, POINTER_BLUE  # noqa: E402


KNOWN_FILL = "#15803d"
KNOWN_STROKE = "#bbf7d0"
FOCUS_FILL = "#0f766e"
FOCUS_STROKE = "#5eead4"
ZERO_BASED = "#38bdf8"
ONE_BASED = "#fbbf24"
FORMULA_FILL = "#172554"
FORMULA_STROKE = "#93c5fd"
CODE_HIGHLIGHT = "#fef3c7"
CARD_FILL = "#1e293b"


class RecurrenceFibonacciSequenceVisualization(Scene):
    """Explain Fibonacci recurrence and the difference between 0-based and 1-based indexing."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        title_group = self.show_intro()
        sequence_group = self.show_value_recurrence(title_group)
        compare_group = self.show_index_compare(title_group, sequence_group)
        code_group = self.show_code_mapping(title_group, compare_group)
        self.show_problem_choices(title_group, code_group)

    def show_intro(self):
        title = Text("递推算法：简单数列 Fibonacci", font=FONT, weight="BOLD", font_size=46, color=WHITE)
        subtitle = Text("公式相同，下标先看题目", font=FONT, font_size=27, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.22)
        title_group = VGroup(title, subtitle)

        self.play(FadeIn(title, shift=UP * 0.16), Write(subtitle), run_time=0.95)
        self.wait(0.25)
        self.play(title_group.animate.scale(0.66).to_edge(UP, buff=0.22), run_time=0.62)
        return title_group

    def show_value_recurrence(self, title_group):
        heading = Text("每一项由前两项推出", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.38)

        values = ["0", "1", "1", "2", "3", "5", "8"]
        cells = VGroup(*[self.make_value_cell(index, value) for index, value in enumerate(values)]).arrange(RIGHT, buff=0.12)
        cells.move_to(DOWN * 0.5)

        formula = self.make_formula_card("f[i] = f[i-1] + f[i-2]")
        formula.next_to(heading, DOWN, buff=0.24)

        self.play(FadeIn(heading, shift=UP * 0.1), FadeIn(formula, shift=UP * 0.1), run_time=0.55)
        self.play(LaggedStart(*[FadeIn(cell, shift=UP * 0.1) for cell in cells], lag_ratio=0.06), run_time=0.9)

        for index in range(2, 6):
            arrows = self.make_dependency_arrows(cells[index - 2], cells[index - 1], cells[index])
            calc = Text(
                f"{values[index - 2]} + {values[index - 1]} = {values[index]}",
                font=MONO_FONT,
                weight="BOLD",
                font_size=27,
                color=CODE_HIGHLIGHT,
            )
            calc.next_to(cells, DOWN, buff=0.56)
            self.play(
                cells[index - 2][0].animate.set_stroke(ONE_BASED, width=3.0),
                cells[index - 1][0].animate.set_stroke(ZERO_BASED, width=3.0),
                cells[index][0].animate.set_fill(FOCUS_FILL, opacity=1).set_stroke(FOCUS_STROKE, width=3.2),
                FadeIn(arrows),
                FadeIn(calc, shift=UP * 0.08),
                run_time=0.48,
            )
            self.wait(0.08)
            self.play(
                cells[index - 2][0].animate.set_fill(KNOWN_FILL, opacity=1).set_stroke(KNOWN_STROKE, width=2.5),
                cells[index - 1][0].animate.set_fill(KNOWN_FILL, opacity=1).set_stroke(KNOWN_STROKE, width=2.5),
                cells[index][0].animate.set_fill(KNOWN_FILL, opacity=1).set_stroke(KNOWN_STROKE, width=2.5),
                FadeOut(arrows),
                FadeOut(calc),
                run_time=0.34,
            )

        note = Text("数值递推固定：当前项 = 左边两项之和", font=FONT, font_size=25, color=MUTED)
        note.to_edge(DOWN, buff=0.32)
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.42)
        self.wait(0.38)

        group = VGroup(heading, formula, cells, note)
        return group

    def show_index_compare(self, title_group, sequence_group):
        self.play(FadeOut(sequence_group), run_time=0.55)

        heading = Text("同一串数，可以有两种常见下标", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.38)

        zero_label = self.make_mode_label("0-based", ZERO_BASED)
        one_label = self.make_mode_label("1-based", ONE_BASED)

        zero_values = [("f[0]", "0"), ("f[1]", "1"), ("f[2]", "1"), ("f[3]", "2"), ("f[4]", "3"), ("f[5]", "5"), ("f[6]", "8")]
        one_values = [("F[1]", "1"), ("F[2]", "1"), ("F[3]", "2"), ("F[4]", "3"), ("F[5]", "5"), ("F[6]", "8")]
        zero_cells = VGroup(*[self.make_index_cell(label, value, ZERO_BASED) for label, value in zero_values]).arrange(RIGHT, buff=0.1)
        one_cells = VGroup(*[self.make_index_cell(label, value, ONE_BASED) for label, value in one_values]).arrange(RIGHT, buff=0.1)

        zero_cells.next_to(heading, DOWN, buff=0.42).shift(RIGHT * 0.36)
        one_cells.next_to(zero_cells, DOWN, buff=0.56).align_to(zero_cells[1], LEFT)
        zero_label.next_to(zero_cells, LEFT, buff=0.22)
        one_label.next_to(one_cells, LEFT, buff=0.22)

        connector = Text("数值很像，下标不同", font=FONT, font_size=24, color="#fef3c7")
        connector.next_to(zero_cells, DOWN, buff=0.16)

        self.play(FadeIn(heading, shift=UP * 0.1), run_time=0.42)
        self.play(FadeIn(zero_label, shift=RIGHT * 0.08), FadeIn(one_label, shift=RIGHT * 0.08), run_time=0.35)
        self.play(LaggedStart(*[FadeIn(cell, shift=UP * 0.08) for cell in zero_cells], lag_ratio=0.04), run_time=0.82)
        self.play(LaggedStart(*[FadeIn(cell, shift=UP * 0.08) for cell in one_cells], lag_ratio=0.05), run_time=0.74)
        self.play(FadeIn(connector, shift=UP * 0.08), run_time=0.38)

        self.play(
            zero_cells[0][0].animate.set_stroke(ZERO_BASED, width=3.5),
            zero_cells[1][0].animate.set_stroke(ZERO_BASED, width=3.5),
            one_cells[0][0].animate.set_stroke(ONE_BASED, width=3.5),
            one_cells[1][0].animate.set_stroke(ONE_BASED, width=3.5),
            run_time=0.52,
        )
        self.wait(0.55)

        group = VGroup(heading, zero_label, one_label, zero_cells, one_cells, connector)
        group.zero_cells = zero_cells
        group.one_cells = one_cells
        return group

    def show_code_mapping(self, title_group, compare_group):
        self.play(FadeOut(compare_group), run_time=0.55)

        heading = Text("下标决定初始化和循环起点", font=FONT, font_size=31, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.36)

        left_code = self.make_code_block(
            "0-based",
            [
                "f[0] = 0;",
                "f[1] = 1;",
                "for (int i = 2; i <= n; i++) {",
                "    f[i] = f[i - 1] + f[i - 2];",
                "}",
                "cout << f[n];",
            ],
            ZERO_BASED,
        )
        right_code = self.make_code_block(
            "1-based",
            [
                "f[1] = 1;",
                "f[2] = 1;",
                "for (int i = 3; i <= n; i++) {",
                "    f[i] = f[i - 1] + f[i - 2];",
                "}",
                "cout << f[n];",
            ],
            ONE_BASED,
        )
        code_pair = VGroup(left_code, right_code).arrange(RIGHT, buff=0.55)
        code_pair.next_to(heading, DOWN, buff=0.34)

        self.play(FadeIn(heading, shift=UP * 0.1), run_time=0.38)
        self.play(FadeIn(left_code, shift=RIGHT * 0.12), FadeIn(right_code, shift=LEFT * 0.12), run_time=0.72)

        left_init = SurroundingRectangle(VGroup(left_code.lines[0], left_code.lines[1]), color=ZERO_BASED, buff=0.07, stroke_width=2.6)
        right_init = SurroundingRectangle(VGroup(right_code.lines[0], right_code.lines[1]), color=ONE_BASED, buff=0.07, stroke_width=2.6)
        self.play(Create(left_init), Create(right_init), run_time=0.42)
        self.wait(0.2)

        left_loop = SurroundingRectangle(left_code.lines[2], color=ZERO_BASED, buff=0.07, stroke_width=2.6)
        right_loop = SurroundingRectangle(right_code.lines[2], color=ONE_BASED, buff=0.07, stroke_width=2.6)
        self.play(
            Transform(left_init, left_loop),
            Transform(right_init, right_loop),
            left_code.lines[2].animate.set_color(CODE_HIGHLIGHT),
            right_code.lines[2].animate.set_color(CODE_HIGHLIGHT),
            run_time=0.52,
        )
        self.wait(0.3)

        note = Text("第一个未知格不同，所以循环起点不同", font=FONT, font_size=24, color=MUTED)
        note.to_edge(DOWN, buff=0.34)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.38)
        self.wait(0.45)

        group = VGroup(heading, code_pair, left_init, right_init, note)
        return group

    def show_problem_choices(self, title_group, code_group):
        self.play(FadeOut(code_group), run_time=0.55)

        heading = Text("看到题目，先翻译定义", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.38)

        zero_card = self.make_problem_card("题目说", "F(0)=0, F(1)=1", "从 f[0] 开始", ZERO_BASED)
        one_card = self.make_problem_card("题目说", "F(1)=1, F(2)=1", "从 F[1] 开始", ONE_BASED)
        cards = VGroup(zero_card, one_card).arrange(RIGHT, buff=0.58)
        cards.next_to(heading, DOWN, buff=0.46)

        answer_zero = self.make_answer_tag("答案：f[n]", ZERO_BASED)
        answer_one = self.make_answer_tag("答案：F[n]", ONE_BASED)
        answer_zero.next_to(zero_card, DOWN, buff=0.22)
        answer_one.next_to(one_card, DOWN, buff=0.22)

        self.play(FadeIn(heading, shift=UP * 0.1), run_time=0.36)
        self.play(FadeIn(zero_card, shift=UP * 0.1), FadeIn(one_card, shift=UP * 0.1), run_time=0.62)
        self.play(FadeIn(answer_zero, shift=UP * 0.08), FadeIn(answer_one, shift=UP * 0.08), run_time=0.42)
        self.wait(0.4)

        summary = VGroup(
            self.make_summary_item("1", "先看下标"),
            self.make_summary_item("2", "放好初始格"),
            self.make_summary_item("3", "从第一个未知格循环"),
        ).arrange(RIGHT, buff=0.38)
        summary.to_edge(DOWN, buff=0.48)
        self.play(FadeIn(summary, shift=UP * 0.14), run_time=0.62)
        self.wait(2.0)

    def make_value_cell(self, index, value):
        box = RoundedRectangle(
            width=0.98,
            height=1.02,
            corner_radius=0.08,
            stroke_width=2.1,
            stroke_color=CELL_STROKE,
            fill_color=CELL_FILL,
            fill_opacity=1,
        )
        value_text = Text(value, font=MONO_FONT, weight="BOLD", font_size=31, color=WHITE)
        label = Text(f"位置 {index}", font=FONT, font_size=15, color=MUTED)
        value_text.move_to(box.get_center() + UP * 0.16)
        label.move_to(box.get_center() + DOWN * 0.29)
        return VGroup(box, value_text, label)

    def make_index_cell(self, label, value, color):
        box = RoundedRectangle(
            width=0.96,
            height=0.88,
            corner_radius=0.08,
            stroke_width=2.0,
            stroke_color=CELL_STROKE,
            fill_color=CELL_FILL,
            fill_opacity=1,
        )
        top = Text(label, font=MONO_FONT, weight="BOLD", font_size=18, color=color)
        bottom = Text(value, font=MONO_FONT, weight="BOLD", font_size=27, color=WHITE)
        VGroup(top, bottom).arrange(DOWN, buff=0.03).move_to(box.get_center())
        return VGroup(box, top, bottom)

    def make_mode_label(self, text, color):
        box = RoundedRectangle(
            width=1.24,
            height=0.48,
            corner_radius=0.08,
            stroke_width=2.0,
            stroke_color=color,
            fill_color="#111827",
            fill_opacity=1,
        )
        label = Text(text, font=MONO_FONT, weight="BOLD", font_size=19, color=color)
        label.move_to(box.get_center())
        return VGroup(box, label)

    def make_formula_card(self, text):
        box = RoundedRectangle(
            width=3.5,
            height=0.72,
            corner_radius=0.08,
            stroke_width=2.4,
            stroke_color=FORMULA_STROKE,
            fill_color=FORMULA_FILL,
            fill_opacity=0.98,
        )
        label = Text(text, font=MONO_FONT, weight="BOLD", font_size=25, color=WHITE)
        label.move_to(box.get_center())
        return VGroup(box, label)

    def make_dependency_arrows(self, left_cell, right_cell, target_cell):
        left_arrow = Arrow(
            left_cell.get_top() + UP * 0.1,
            target_cell.get_top() + LEFT * 0.15 + UP * 0.1,
            buff=0.08,
            color=ONE_BASED,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.16,
        )
        right_arrow = Arrow(
            right_cell.get_top() + UP * 0.1,
            target_cell.get_top() + RIGHT * 0.15 + UP * 0.1,
            buff=0.08,
            color=ZERO_BASED,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.16,
        )
        return VGroup(left_arrow, right_arrow)

    def make_code_block(self, title, lines, color):
        title_text = Text(title, font=MONO_FONT, weight="BOLD", font_size=23, color=color)
        code_lines = VGroup(*[Text(line, font=MONO_FONT, font_size=18, color=MUTED) for line in lines])
        code_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        content = VGroup(title_text, code_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        box = RoundedRectangle(
            width=4.98,
            height=2.55,
            corner_radius=0.08,
            stroke_width=2.1,
            stroke_color=color,
            fill_color="#111827",
            fill_opacity=0.95,
        )
        content.move_to(box.get_center()).align_to(box, LEFT).shift(RIGHT * 0.24)
        group = VGroup(box, content)
        group.lines = code_lines
        return group

    def make_problem_card(self, label, definition, hint, color):
        box = RoundedRectangle(
            width=4.1,
            height=1.55,
            corner_radius=0.08,
            stroke_width=2.3,
            stroke_color=color,
            fill_color=CARD_FILL,
            fill_opacity=0.98,
        )
        top = Text(label, font=FONT, font_size=19, color=MUTED)
        middle = Text(definition, font=MONO_FONT, weight="BOLD", font_size=24, color=WHITE)
        bottom = Text(hint, font=FONT, font_size=21, color=color)
        VGroup(top, middle, bottom).arrange(DOWN, buff=0.09).move_to(box.get_center())
        return VGroup(box, top, middle, bottom)

    def make_answer_tag(self, text, color):
        box = RoundedRectangle(
            width=2.05,
            height=0.5,
            corner_radius=0.08,
            stroke_width=2.0,
            stroke_color=color,
            fill_color="#111827",
            fill_opacity=1,
        )
        label = Text(text, font=FONT, weight="BOLD", font_size=19, color=color)
        label.move_to(box.get_center())
        return VGroup(box, label)

    def make_summary_item(self, number, text):
        dot = Circle(radius=0.18, stroke_width=0, fill_color=POINTER_BLUE, fill_opacity=1)
        number_text = Text(number, font=MONO_FONT, weight="BOLD", font_size=17, color=BACKGROUND)
        number_text.move_to(dot.get_center())
        label = Text(text, font=FONT, font_size=22, color=WHITE)
        return VGroup(VGroup(dot, number_text), label).arrange(RIGHT, buff=0.14)
