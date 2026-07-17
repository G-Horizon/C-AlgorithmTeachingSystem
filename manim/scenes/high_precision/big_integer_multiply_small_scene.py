from pathlib import Path
import sys

from manim import *


COMMON_DIR = Path(__file__).resolve().parents[2] / "common"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from array_widgets import (  # noqa: E402
    color_cell,
    make_array_cell,
    make_indices,
    make_pointer,
    mark_sorted,
    pointer_position,
    reset_cell,
)
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


CARRY_FILL = "#7c3aed"
CARRY_STROKE = "#ddd6fe"
RESULT_FILL = "#0f766e"
RESULT_STROKE = "#5eead4"
MULTIPLY_FILL = "#c2410c"
MULTIPLY_STROKE = "#fed7aa"


class BigIntegerMultiplySmallVisualization(Scene):
    """Visualize multiplying a reversed big integer by a small integer."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        a_digits = [5, 6, 7, 8, 9]
        result_digits = [0, 8, 1, 5, 8, 1, 1]
        multiplier = 12

        title, subtitle = self.show_intro()
        self.play(VGroup(title, subtitle).animate.to_edge(UP, buff=0.22).scale(0.66), run_time=0.8)

        storage_group = self.show_reverse_storage()
        self.play(FadeOut(storage_group), run_time=0.45)

        a_row = self.make_digit_row("a", a_digits, UP * 1.25, "98765 的反向数组")
        c_row = self.make_digit_row("c", [" "] * len(result_digits), DOWN * 0.18, "结果先反向生成")
        rows = VGroup(a_row, c_row)

        multiplier_card = self.make_multiplier_card(multiplier)
        multiplier_card.to_edge(RIGHT, buff=0.72).shift(UP * 1.38)

        carry_box, carry_text = self.make_carry_badge(0)
        carry_group = VGroup(carry_box, carry_text)
        carry_group.next_to(multiplier_card, DOWN, buff=0.32)

        formula = Text("每一位都做：t = a[i] * b + carry", font=FONT, font_size=28, color=WHITE)
        formula.move_to(DOWN * 2.52)
        status = Text("b 是普通整数，a 的每一位依次和它相乘", font=FONT, font_size=27, color=MUTED)
        status.next_to(formula, UP, buff=0.16)

        self.play(
            LaggedStart(
                FadeIn(a_row, shift=UP * 0.2),
                FadeIn(c_row, shift=UP * 0.2),
                FadeIn(multiplier_card, shift=LEFT * 0.15),
                FadeIn(carry_group, shift=LEFT * 0.15),
                lag_ratio=0.15,
            ),
            run_time=1.1,
        )
        self.play(Write(status), FadeIn(formula), run_time=0.7)

        a_positions = [cell.get_center() for cell in a_row.cells]
        c_positions = [cell.get_center() for cell in c_row.cells]
        pointer = make_pointer("i", POINTER_BLUE).scale(0.86)
        pointer.move_to(pointer_position(a_positions[0]))
        self.play(FadeIn(pointer), run_time=0.35)

        carry = 0
        for i, digit_value in enumerate(a_digits):
            t = digit_value * multiplier + carry
            result_digit = t % 10
            next_carry = t // 10
            fast = i >= 2

            self.play(pointer.animate.move_to(pointer_position(a_positions[i])), run_time=0.24 if fast else 0.38)

            next_formula = Text(
                f"i={i}: t = {digit_value} * {multiplier} + {carry} = {t}，写 {result_digit}，进位 {next_carry}",
                font=FONT,
                font_size=27,
                color=WHITE,
            )
            next_formula.move_to(formula.get_center())

            self.play(
                color_cell(a_row.cells[i], COMPARE_FILL, "#fde68a"),
                multiplier_card[0].animate.set_fill(MULTIPLY_FILL, opacity=1).set_stroke(MULTIPLY_STROKE, width=3.5),
                Transform(formula, next_formula),
                run_time=0.32 if fast else 0.55,
            )

            self.play(
                color_cell(c_row.cells[i], RESULT_FILL, RESULT_STROKE),
                self.update_cell_text(c_row.cells[i], result_digit),
                run_time=0.28 if fast else 0.44,
            )

            self.show_carry_move(i, c_positions, next_carry, fast=fast)

            next_carry_text = Text(f"carry = {next_carry}", font=FONT, font_size=26, color=WHITE)
            next_carry_text.move_to(carry_text.get_center())
            self.play(Transform(carry_text, next_carry_text), run_time=0.22 if fast else 0.34)

            self.play(
                reset_cell(a_row.cells[i]),
                multiplier_card[0].animate.set_fill(MULTIPLY_FILL, opacity=0.92).set_stroke(MULTIPLY_STROKE, width=2.5),
                mark_sorted(c_row.cells[i]),
                run_time=0.16 if fast else 0.25,
            )
            carry = next_carry

        carry_status = Text("主循环结束，carry = 11，还不能丢掉：继续按十进制拆位", font=FONT, font_size=28, color="#fef3c7")
        carry_status.move_to(status.get_center())
        self.play(Transform(status, carry_status), pointer.animate.move_to(pointer_position(c_positions[5])), run_time=0.55)

        index = len(a_digits)
        while carry > 0:
            result_digit = carry % 10
            next_carry = carry // 10
            split_formula = Text(
                f"剩余进位：{carry} % 10 = {result_digit}，下一轮 carry = {next_carry}",
                font=FONT,
                font_size=28,
                color=WHITE,
            )
            split_formula.move_to(formula.get_center())

            self.play(
                pointer.animate.move_to(pointer_position(c_positions[index])),
                Transform(formula, split_formula),
                run_time=0.4,
            )
            self.play(
                color_cell(c_row.cells[index], RESULT_FILL, RESULT_STROKE),
                self.update_cell_text(c_row.cells[index], result_digit),
                run_time=0.38,
            )
            next_carry_text = Text(f"carry = {next_carry}", font=FONT, font_size=26, color=WHITE)
            next_carry_text.move_to(carry_text.get_center())
            self.play(Transform(carry_text, next_carry_text), mark_sorted(c_row.cells[index]), run_time=0.34)
            carry = next_carry
            index += 1

        answer = Text("c = [0, 8, 1, 5, 8, 1, 1]，倒序输出 1185180", font=FONT, font_size=31, color="#bbf7d0")
        answer.move_to(formula.get_center())
        self.play(Transform(formula, answer), FadeOut(pointer), run_time=0.65)
        self.wait(0.75)

        self.show_code_mapping(VGroup(rows, multiplier_card, carry_group, status, formula))

    def show_intro(self):
        title = Text("高精度乘低精度 Big Integer * Small Int", font=FONT, weight="BOLD", font_size=48, color=WHITE)
        subtitle = Text(
            "把竖式乘法变成一条传送带：当前位留下个位，剩下的高位继续当进位",
            font=FONT,
            font_size=27,
            color=MUTED,
        )
        subtitle.next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(title, shift=UP * 0.2), Write(subtitle), run_time=1.15)
        self.wait(0.45)
        return title, subtitle

    def show_reverse_storage(self):
        normal_title = Text("示例：98765 * 12", font=FONT, font_size=36, color=WHITE)
        normal_title.move_to(UP * 1.45)

        vertical = VGroup(
            Text("  98765", font=MONO_FONT, font_size=42, color=WHITE),
            Text("*    12", font=MONO_FONT, font_size=42, color=WHITE),
            Line(LEFT * 1.55, RIGHT * 1.55, color=MUTED, stroke_width=3),
            Text("1185180", font=MONO_FONT, font_size=42, color="#bbf7d0"),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.12)
        vertical.next_to(normal_title, DOWN, buff=0.35)

        hint = Text("大整数仍然反向存储；小整数 b 直接保留成一个普通变量", font=FONT, font_size=28, color=MUTED)
        hint.next_to(vertical, DOWN, buff=0.45)

        reverse_a = Text("98765 -> a = [5, 6, 7, 8, 9]", font=MONO_FONT, font_size=29, color="#bae6fd")
        multiplier_b = Text("b = 12", font=MONO_FONT, font_size=29, color="#fed7aa")
        reverse_group = VGroup(reverse_a, multiplier_b).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        reverse_group.next_to(hint, DOWN, buff=0.34)

        self.play(FadeIn(normal_title, shift=UP * 0.15), FadeIn(vertical, shift=UP * 0.2), run_time=0.85)
        self.play(Write(hint), FadeIn(reverse_group, shift=UP * 0.18), run_time=0.85)
        self.wait(0.75)
        return VGroup(normal_title, vertical, hint, reverse_group)

    def make_digit_row(self, name, values, offset, caption):
        cells = [make_array_cell(value).scale(0.86) for value in values]
        cells_group = VGroup(*cells).arrange(RIGHT, buff=0.12).move_to(offset)
        indexes = make_indices([cell.get_center() for cell in cells])

        label = Text(name, font=MONO_FONT, font_size=29, color=WHITE)
        caption_text = Text(caption, font=FONT, font_size=17, color=MUTED)
        label_group = VGroup(label, caption_text).arrange(DOWN, buff=0.08)
        label_group.next_to(cells_group, LEFT, buff=0.32)

        row = VGroup(label_group, cells_group, indexes)
        row.cells = cells
        return row

    def make_multiplier_card(self, multiplier):
        box = RoundedRectangle(
            width=2.05,
            height=0.9,
            corner_radius=0.12,
            stroke_width=2.5,
            stroke_color=MULTIPLY_STROKE,
            fill_color=MULTIPLY_FILL,
            fill_opacity=0.92,
        )
        text = Text(f"b = {multiplier}", font=MONO_FONT, weight="BOLD", font_size=30, color=WHITE)
        text.move_to(box.get_center())
        return VGroup(box, text)

    def make_carry_badge(self, carry):
        box = RoundedRectangle(
            width=2.2,
            height=0.74,
            corner_radius=0.12,
            stroke_width=2.5,
            stroke_color=CARRY_STROKE,
            fill_color=CARRY_FILL,
            fill_opacity=0.94,
        )
        text = Text(f"carry = {carry}", font=FONT, font_size=26, color=WHITE)
        text.move_to(box.get_center())
        return box, text

    def show_carry_move(self, index, positions, carry_value, fast=False):
        if carry_value == 0:
            return
        start = positions[index] + UP * 0.58
        end_index = min(index + 1, len(positions) - 1)
        end = positions[end_index] + UP * 0.58

        dot = Circle(radius=0.11, fill_color=CARRY_FILL, fill_opacity=1, stroke_color=CARRY_STROKE, stroke_width=2)
        label = Text(str(carry_value), font=MONO_FONT, font_size=18, color=CARRY_STROKE)
        label.next_to(dot, UP, buff=0.04)
        token = VGroup(dot, label).move_to(start)

        self.play(FadeIn(token), run_time=0.12 if fast else 0.18)
        self.play(token.animate.move_to(end), run_time=0.25 if fast else 0.36)
        self.play(FadeOut(token), run_time=0.1 if fast else 0.15)

    def update_cell_text(self, cell, value):
        label = Text(str(value), font=FONT, weight="BOLD", font_size=34, color=WHITE)
        label.move_to(cell[0].get_center())
        return Transform(cell[1], label)

    def show_code_mapping(self, scene_group):
        self.play(scene_group.animate.scale(0.62).to_edge(LEFT, buff=0.35).shift(UP * 0.08), run_time=0.75)

        code_title = Text("核心 C++ 代码", font=FONT, font_size=28, color=WHITE)
        code_lines = [
            "vector<int> multiply(vector<int> a, int b) {",
            "    vector<int> c;",
            "    int carry = 0;",
            "    for (int i = 0; i < a.size(); i++) {",
            "        int t = a[i] * b + carry;",
            "        c.push_back(t % 10);",
            "        carry = t / 10;",
            "    }",
            "    while (carry) {",
            "        c.push_back(carry % 10);",
            "        carry /= 10;",
            "    }",
            "    return c;",
            "}",
        ]
        code = VGroup(
            *[Text(line, font=MONO_FONT, font_size=15, color=MUTED) for line in code_lines]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        code_group = VGroup(code_title, code).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        code_group.to_edge(RIGHT, buff=0.28).shift(DOWN * 0.42)

        self.play(FadeIn(code_title, shift=LEFT * 0.2), run_time=0.42)
        self.play(LaggedStart(*[Write(line) for line in code], lag_ratio=0.1), run_time=1.25)

        details = VGroup(
            Text("最后用 while(carry) 拆完剩余进位", font=FONT, font_size=18, color=WHITE),
            Text("阶乘循环可直接复用 multiply()", font=FONT, font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        details.next_to(code_group, DOWN, buff=0.18, aligned_edge=LEFT)

        self.play(FadeIn(details, shift=UP * 0.2), run_time=0.65)
        self.wait(2.0)
