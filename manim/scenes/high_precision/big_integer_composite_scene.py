from pathlib import Path
import sys

from manim import *


COMMON_DIR = Path(__file__).resolve().parents[2] / "common"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from array_widgets import color_cell, make_array_cell, make_indices, mark_sorted, reset_cell  # noqa: E402
from theme import (  # noqa: E402
    BACKGROUND,
    CELL_FILL,
    CELL_STROKE,
    COMPARE_FILL,
    FONT,
    MONO_FONT,
    MUTED,
    POINTER_BLUE,
    POINTER_PINK,
)


MUL_FILL = "#c2410c"
MUL_STROKE = "#fed7aa"
ADD_FILL = "#0f766e"
ADD_STROKE = "#5eead4"
STATE_FILL = "#1d4ed8"
STATE_STROKE = "#bfdbfe"
RESULT_FILL = "#15803d"
RESULT_STROKE = "#bbf7d0"
WARN_FILL = "#7c2d12"
WARN_STROKE = "#fed7aa"


class BigIntegerCompositeVisualization(Scene):
    """Show how high precision functions become factorial and Fibonacci algorithms."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        title, subtitle = self.show_intro()
        self.play(VGroup(title, subtitle).animate.to_edge(UP, buff=0.22).scale(0.66), run_time=0.75)

        toolbox = self.show_toolbox()
        self.play(FadeOut(toolbox), run_time=0.4)

        factorial_group = self.show_factorial_ladder()
        self.play(FadeOut(factorial_group), run_time=0.45)

        fibonacci_group = self.show_fibonacci_rails()
        self.show_code_mapping(VGroup(title, subtitle, fibonacci_group))

    def show_intro(self):
        title = Text("高精度综合：阶乘与 Fibonacci", font=FONT, weight="BOLD", font_size=48, color=WHITE)
        subtitle = Text(
            "前面学会的是零件；这一节把零件放进循环，让大数算法真的跑起来",
            font=FONT,
            font_size=27,
            color=MUTED,
        )
        subtitle.next_to(title, DOWN, buff=0.24)
        self.play(FadeIn(title, shift=UP * 0.18), Write(subtitle), run_time=1.05)
        self.wait(0.45)
        return title, subtitle

    def show_toolbox(self):
        heading = Text("算法外壳不同，复用的高精度函数不变", font=FONT, font_size=34, color=WHITE)
        heading.move_to(UP * 1.5)

        mul_card = self.make_function_card("mul(ans, i)", "阶乘每级乘一次", MUL_FILL, MUL_STROKE)
        add_card = self.make_function_card("add(a, b)", "Fibonacci 每轮加一次", ADD_FILL, ADD_STROKE)
        cards = VGroup(mul_card, add_card).arrange(RIGHT, buff=0.7)
        cards.next_to(heading, DOWN, buff=0.55)

        note = Text("重点从“怎么进位”切换到“什么时候调用函数、怎样更新状态”", font=FONT, font_size=28, color="#fef3c7")
        note.next_to(cards, DOWN, buff=0.5)

        group = VGroup(heading, cards, note)
        self.play(FadeIn(heading, shift=UP * 0.14), run_time=0.55)
        self.play(LaggedStart(FadeIn(mul_card, shift=UP * 0.12), FadeIn(add_card, shift=UP * 0.12), lag_ratio=0.18), run_time=0.85)
        self.play(Write(note), run_time=0.6)
        self.wait(0.75)
        return group

    def show_factorial_ladder(self):
        heading = Text("阶乘：答案沿着台阶一路相乘", font=FONT, font_size=31, color=WHITE)
        heading.to_edge(LEFT, buff=0.72).shift(UP * 2.25)

        ans_card = self.make_value_card("ans", "1", RESULT_FILL, RESULT_STROKE, width=2.8, height=1.15)
        ans_card.move_to(UP * 1.15 + LEFT * 3.45)

        steps = VGroup()
        labels = ["×2", "×3", "×4", "×5"]
        for index, label in enumerate(labels):
            step = self.make_step_box(label)
            step.move_to(LEFT * 1.95 + RIGHT * index * 1.25 + DOWN * (1.15 - index * 0.34))
            steps.add(step)

        arrows = VGroup()
        for left, right in zip(steps[:-1], steps[1:]):
            arrows.add(Arrow(left.get_right(), right.get_left(), buff=0.08, color=MUTED, stroke_width=3, max_tip_length_to_length_ratio=0.18))

        formula = Text("ans = 1", font=MONO_FONT, font_size=30, color="#bae6fd")
        formula.move_to(RIGHT * 2.45 + UP * 1.15)
        status = Text("从 2 开始循环，每一轮都调用一次高精度乘低精度", font=FONT, font_size=26, color=MUTED)
        status.next_to(formula, DOWN, buff=0.28)

        self.play(FadeIn(heading, shift=UP * 0.12), FadeIn(ans_card, shift=UP * 0.12), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(step, shift=UP * 0.12) for step in steps], lag_ratio=0.12), FadeIn(arrows), run_time=0.9)
        self.play(FadeIn(formula), Write(status), run_time=0.65)

        values = [2, 6, 24, 120]
        current = 1
        for index, (step, value) in enumerate(zip(steps, values)):
            multiplier = index + 2
            next_formula = Text(f"ans = {current} * {multiplier} = {value}", font=MONO_FONT, font_size=30, color=WHITE)
            next_formula.move_to(formula.get_center())
            self.play(
                step[0].animate.set_fill(MUL_FILL, opacity=1).set_stroke(MUL_STROKE, width=3.5),
                Transform(formula, next_formula),
                run_time=0.42,
            )
            self.play(self.update_value(ans_card, value), run_time=0.35)
            self.play(step[0].animate.set_fill(RESULT_FILL, opacity=1).set_stroke(RESULT_STROKE, width=3.0), run_time=0.24)
            current = value

        array_row = self.make_digit_row("120", [0, 2, 1], RIGHT * 2.45 + DOWN * 0.98, "倒序数组")
        final_note = Text("数值变长也没关系：只要函数能处理大数，外层循环不用改", font=FONT, font_size=25, color="#bbf7d0")
        final_note.next_to(array_row, DOWN, buff=0.32)
        self.play(FadeIn(array_row, shift=UP * 0.15), Transform(status, final_note), run_time=0.7)
        self.play(LaggedStart(*[mark_sorted(cell) for cell in array_row.cells], lag_ratio=0.1), run_time=0.45)
        self.wait(0.65)
        return VGroup(heading, ans_card, steps, arrows, formula, status, array_row)

    def show_fibonacci_rails(self):
        heading = Text("Fibonacci：两条轨道向前滚动", font=FONT, font_size=31, color=WHITE)
        heading.to_edge(LEFT, buff=0.72).shift(UP * 2.25)

        a_card = self.make_value_card("a", "0", STATE_FILL, STATE_STROKE)
        b_card = self.make_value_card("b", "1", STATE_FILL, STATE_STROKE)
        c_card = self.make_value_card("c = a + b", "1", ADD_FILL, ADD_STROKE, width=2.8)
        cards = VGroup(a_card, b_card, c_card).arrange(RIGHT, buff=0.55)
        cards.move_to(UP * 0.95)

        plus = Text("+", font=MONO_FONT, font_size=36, color="#fef3c7")
        plus.move_to((a_card.get_right() + b_card.get_left()) / 2)
        arrow_to_c = Arrow(b_card.get_right(), c_card.get_left(), buff=0.16, color=MUTED, stroke_width=3)

        shift_rule = Text("更新规则：c = add(a, b)，然后 a = b，b = c", font=FONT, font_size=27, color=MUTED)
        shift_rule.move_to(DOWN * 0.45)
        sequence = Text("0, 1", font=MONO_FONT, font_size=31, color="#bae6fd")
        sequence.move_to(DOWN * 1.38)

        self.play(FadeIn(heading, shift=UP * 0.12), FadeIn(cards, shift=UP * 0.14), FadeIn(plus), FadeIn(arrow_to_c), run_time=0.85)
        self.play(Write(shift_rule), FadeIn(sequence, shift=UP * 0.12), run_time=0.65)

        a, b = 0, 1
        sequence_text = "0, 1"
        for index in range(5):
            c = a + b
            formula = Text(f"第 {index + 1} 轮：{a} + {b} = {c}", font=FONT, font_size=28, color=WHITE)
            formula.move_to(shift_rule.get_center())
            self.play(
                a_card[0].animate.set_fill(COMPARE_FILL, opacity=1).set_stroke("#fde68a", width=3.4),
                b_card[0].animate.set_fill(COMPARE_FILL, opacity=1).set_stroke("#fde68a", width=3.4),
                Transform(shift_rule, formula),
                run_time=0.35,
            )
            self.play(self.update_value(c_card, c), run_time=0.28)

            a, b = b, c
            sequence_text += f", {c}"
            next_preview = a + b
            next_sequence = Text(sequence_text, font=MONO_FONT, font_size=31, color="#bae6fd")
            next_sequence.move_to(sequence.get_center())
            self.play(
                self.update_value(a_card, a),
                self.update_value(b_card, b),
                self.update_value(c_card, next_preview),
                Transform(sequence, next_sequence),
                run_time=0.42,
            )
            self.play(
                a_card[0].animate.set_fill(STATE_FILL, opacity=1).set_stroke(STATE_STROKE, width=2.6),
                b_card[0].animate.set_fill(STATE_FILL, opacity=1).set_stroke(STATE_STROKE, width=2.6),
                run_time=0.18,
            )

        final = Text("真正的 n 很大时，a、b、c 都换成高精度数组；递推结构完全一样", font=FONT, font_size=25, color="#bbf7d0")
        final.move_to(shift_rule.get_center())
        self.play(Transform(shift_rule, final), run_time=0.55)
        self.wait(0.7)
        return VGroup(heading, cards, plus, arrow_to_c, shift_rule, sequence)

    def show_code_mapping(self, scene_group):
        self.play(scene_group.animate.scale(0.47).to_edge(LEFT, buff=0.16).shift(UP * 0.02), run_time=0.75)

        title = Text("循环外壳", font=FONT, font_size=25, color=WHITE)
        code_lines = [
            "vector<int> ans(1, 1);",
            "for (int i = 2; i <= n; i++)",
            "  ans = mul(ans, i);",
            "",
            "vector<int> a(1, 0), b(1, 1);",
            "for (int i = 2; i <= n; i++) {",
            "  vector<int> c = add(a, b);",
            "  a = b;",
            "  b = c;",
            "}",
        ]
        code = Text("\n".join(code_lines), font=MONO_FONT, font_size=16, color=MUTED, line_spacing=0.86)
        code_group = VGroup(title, code).arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        code_group.to_edge(RIGHT, buff=0.42).shift(UP * 0.02)

        self.play(FadeIn(title, shift=LEFT * 0.2), run_time=0.35)
        self.play(FadeIn(code, shift=UP * 0.12), run_time=0.75)

        summary = Text("先封装函数，再组合算法", font=FONT, font_size=20, color=WHITE)
        summary.next_to(code_group, DOWN, buff=0.17, aligned_edge=LEFT)
        self.play(FadeIn(summary, shift=UP * 0.12), run_time=0.55)
        self.wait(2.0)

    def make_function_card(self, code, caption, fill, stroke):
        box = RoundedRectangle(
            width=3.6,
            height=1.28,
            corner_radius=0.1,
            stroke_width=2.6,
            stroke_color=stroke,
            fill_color=fill,
            fill_opacity=0.96,
        )
        code_text = Text(code, font=MONO_FONT, weight="BOLD", font_size=29, color=WHITE)
        caption_text = Text(caption, font=FONT, font_size=20, color="#e0f2fe")
        content = VGroup(code_text, caption_text).arrange(DOWN, buff=0.12)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def make_step_box(self, label):
        box = RoundedRectangle(
            width=1.02,
            height=0.72,
            corner_radius=0.08,
            stroke_width=2.5,
            stroke_color=MUL_STROKE,
            fill_color=WARN_FILL,
            fill_opacity=0.92,
        )
        text = Text(label, font=MONO_FONT, weight="BOLD", font_size=28, color=WHITE)
        text.move_to(box.get_center())
        return VGroup(box, text)

    def make_value_card(self, label, value, fill, stroke, width=2.2, height=1.08):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.1,
            stroke_width=2.6,
            stroke_color=stroke,
            fill_color=fill,
            fill_opacity=0.96,
        )
        label_text = Text(label, font=FONT, font_size=20, color="#dbeafe")
        value_text = Text(str(value), font=MONO_FONT, weight="BOLD", font_size=34, color=WHITE)
        content = VGroup(label_text, value_text).arrange(DOWN, buff=0.08)
        content.move_to(box.get_center())
        card = VGroup(box, label_text, value_text)
        card.value = value_text
        return card

    def update_value(self, card, value):
        next_text = Text(str(value), font=MONO_FONT, weight="BOLD", font_size=34, color=WHITE)
        next_text.move_to(card.value.get_center())
        return Transform(card.value, next_text)

    def make_digit_row(self, name, values, offset, caption):
        cells = [make_array_cell(value).scale(0.7) for value in values]
        cells_group = VGroup(*cells).arrange(RIGHT, buff=0.08).move_to(offset)
        indexes = make_indices([cell.get_center() for cell in cells])
        indexes.scale(0.68)
        indexes.shift(UP * 0.16)

        label = Text(name, font=MONO_FONT, font_size=24, color=WHITE)
        caption_text = Text(caption, font=FONT, font_size=17, color=MUTED)
        label_group = VGroup(label, caption_text).arrange(DOWN, buff=0.06)
        label_group.next_to(cells_group, LEFT, buff=0.25)

        row = VGroup(label_group, cells_group, indexes)
        row.cells = cells
        return row
