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
    place_pointer,
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
    SORTED_FILL,
    SWAP_FILL,
)


CARRY_FILL = "#7c3aed"
CARRY_STROKE = "#ddd6fe"
RESULT_FILL = "#0f766e"
RESULT_STROKE = "#5eead4"


class BigIntegerAdditionVisualization(Scene):
    """A storyboard-style high precision addition visualization."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        a_digits = [5, 6, 7, 8, 9]
        b_digits = [5, 6, 7, 8, 0]
        result_digits = [0, 3, 5, 7, 0, 1]

        title, subtitle = self.show_intro()
        self.play(VGroup(title, subtitle).animate.to_edge(UP, buff=0.22).scale(0.68), run_time=0.8)

        storage_group = self.show_reverse_storage()
        self.play(FadeOut(storage_group), run_time=0.45)

        a_row = self.make_digit_row("a", a_digits, UP * 1.45, "98765 的反向数组")
        b_row = self.make_digit_row("b", b_digits, UP * 0.2, "8765 的反向数组，缺位补 0", ghost_indexes={4})
        c_row = self.make_digit_row("c", [" "] * len(result_digits), DOWN * 1.05, "结果数组 c 逐位生成")

        rows = VGroup(a_row, b_row, c_row)
        self.play(
            LaggedStart(
                FadeIn(a_row, shift=UP * 0.2),
                FadeIn(b_row, shift=UP * 0.2),
                FadeIn(c_row, shift=UP * 0.2),
                lag_ratio=0.16,
            ),
            run_time=1.2,
        )

        positions = [cell.get_center() for cell in a_row.cells]
        i_pointer = make_pointer("i", POINTER_BLUE)
        place_pointer(i_pointer, positions[0])

        carry_box, carry_text = self.make_carry_badge(0)
        carry_group = VGroup(carry_box, carry_text).to_edge(RIGHT, buff=0.78).shift(UP * 1.7)

        formula = Text("", font=FONT, font_size=28, color=WHITE)
        formula.move_to(DOWN * 2.38)
        status = Text("从个位开始：同一列相加，再处理进位", font=FONT, font_size=28, color=MUTED)
        status.next_to(formula, UP, buff=0.16)

        self.play(FadeIn(i_pointer), FadeIn(carry_group), FadeIn(status), run_time=0.6)

        carry = 0
        for i in range(5):
            a_value = a_digits[i]
            b_value = b_digits[i]
            total = carry + a_value + b_value
            digit = total % 10
            next_carry = total // 10
            fast = i >= 2

            self.play(i_pointer.animate.move_to(pointer_position(positions[i])), run_time=0.22 if fast else 0.36)

            next_formula = Text(
                f"i={i}: t = {carry} + {a_value} + {b_value} = {total}，写 {digit}，进位 {next_carry}",
                font=FONT,
                font_size=28,
                color=WHITE,
            )
            next_formula.move_to(formula.get_center())

            self.play(
                color_cell(a_row.cells[i], COMPARE_FILL, "#fde68a"),
                color_cell(b_row.cells[i], COMPARE_FILL, "#fde68a"),
                Transform(formula, next_formula),
                run_time=0.34 if fast else 0.58,
            )

            self.play(
                color_cell(c_row.cells[i], RESULT_FILL, RESULT_STROKE),
                self.update_cell_text(c_row.cells[i], digit),
                run_time=0.34 if fast else 0.52,
            )

            if next_carry:
                self.show_carry_move(i, positions, carry_group)

            next_carry_text = Text(f"carry = {next_carry}", font=FONT, font_size=26, color=WHITE)
            next_carry_text.move_to(carry_text.get_center())
            self.play(Transform(carry_text, next_carry_text), run_time=0.24 if fast else 0.36)

            self.play(
                reset_cell(a_row.cells[i]),
                reset_cell(b_row.cells[i]),
                mark_sorted(c_row.cells[i]),
                run_time=0.18 if fast else 0.28,
            )
            carry = next_carry

        final_note = Text("循环结束后 carry 仍为 1，需要新增最高位", font=FONT, font_size=30, color="#fef3c7")
        final_note.move_to(formula.get_center())
        self.play(Transform(formula, final_note), run_time=0.55)
        self.play(
            i_pointer.animate.move_to(pointer_position(c_row.cells[5].get_center())),
            color_cell(c_row.cells[5], CARRY_FILL, CARRY_STROKE),
            run_time=0.45,
        )
        self.play(self.update_cell_text(c_row.cells[5], 1), run_time=0.35)
        self.play(mark_sorted(c_row.cells[5]), run_time=0.3)

        answer = Text("c = [0, 3, 5, 7, 0, 1]，倒序输出：107530", font=FONT, font_size=32, color="#bbf7d0")
        answer.move_to(formula.get_center())
        self.play(
            Transform(formula, answer),
            FadeOut(i_pointer),
            FadeOut(carry_group),
            FadeOut(status),
            run_time=0.75,
        )
        self.wait(0.7)

        self.show_code_mapping(rows, formula)

    def show_intro(self):
        title = Text("高精度加法 Big Integer Addition", font=FONT, weight="BOLD", font_size=52, color=WHITE)
        subtitle = Text(
            "把大整数拆成一位一位，从个位开始模拟竖式相加",
            font=FONT,
            font_size=27,
            color=MUTED,
        )
        subtitle.next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(title, shift=UP * 0.2), Write(subtitle), run_time=1.25)
        self.wait(0.55)
        return title, subtitle

    def show_reverse_storage(self):
        normal_title = Text("输入：98765 + 8765", font=FONT, font_size=34, color=WHITE)
        normal_title.move_to(UP * 1.25)

        vertical = VGroup(
            Text("  98765", font=MONO_FONT, font_size=42, color=WHITE),
            Text("+  8765", font=MONO_FONT, font_size=42, color=WHITE),
            Line(LEFT * 1.45, RIGHT * 1.45, color=MUTED, stroke_width=3),
            Text("107530", font=MONO_FONT, font_size=42, color="#bbf7d0"),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.12)
        vertical.next_to(normal_title, DOWN, buff=0.35)

        hint = Text("竖式从个位开始，所以数组也让个位站在下标 0", font=FONT, font_size=28, color=MUTED)
        hint.next_to(vertical, DOWN, buff=0.45)

        self.play(FadeIn(normal_title, shift=UP * 0.15), FadeIn(vertical, shift=UP * 0.2), run_time=0.9)
        self.play(Write(hint), run_time=0.8)
        self.wait(0.7)

        reverse_a = Text("98765 -> a = [5, 6, 7, 8, 9]", font=MONO_FONT, font_size=29, color="#bae6fd")
        reverse_b = Text(" 8765 -> b = [5, 6, 7, 8]", font=MONO_FONT, font_size=29, color="#fecdd3")
        reverse_group = VGroup(reverse_a, reverse_b).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        reverse_group.next_to(hint, DOWN, buff=0.38)
        self.play(FadeIn(reverse_group, shift=UP * 0.18), run_time=0.8)
        self.wait(0.7)
        return VGroup(normal_title, vertical, hint, reverse_group)

    def make_digit_row(self, name, values, offset, caption, ghost_indexes=None):
        ghost_indexes = ghost_indexes or set()
        cells = [make_array_cell(value) for value in values]
        cells_group = VGroup(*cells).arrange(RIGHT, buff=0.18).move_to(offset)
        indexes = make_indices([cell.get_center() for cell in cells])

        label = Text(name, font=MONO_FONT, font_size=32, color=WHITE)
        label.next_to(cells_group, LEFT, buff=0.45)
        caption_text = Text(caption, font=FONT, font_size=22, color=MUTED)
        caption_text.next_to(cells_group, RIGHT, buff=0.45)

        for index in ghost_indexes:
            cells[index][0].set_fill(CELL_FILL, opacity=0.38).set_stroke(CELL_STROKE, opacity=0.45)
            cells[index][1].set_opacity(0.45)

        row = VGroup(label, cells_group, indexes, caption_text)
        row.cells = cells
        return row

    def make_carry_badge(self, carry):
        box = RoundedRectangle(
            width=1.75,
            height=0.72,
            corner_radius=0.12,
            stroke_width=2.5,
            stroke_color=CARRY_STROKE,
            fill_color=CARRY_FILL,
            fill_opacity=0.95,
        )
        text = Text(f"carry = {carry}", font=FONT, font_size=26, color=WHITE)
        text.move_to(box.get_center())
        return box, text

    def show_carry_move(self, index, positions, carry_group):
        start = positions[index] + UP * 0.52
        if index + 1 < len(positions):
            end = positions[index + 1] + UP * 0.52
        else:
            end = positions[index] + RIGHT * 1.25 + UP * 0.52

        dot = Circle(radius=0.12, fill_color=CARRY_FILL, fill_opacity=1, stroke_color=CARRY_STROKE, stroke_width=2)
        dot.move_to(start)
        label = Text("进位", font=FONT, font_size=20, color=CARRY_STROKE)
        label.next_to(dot, UP, buff=0.05)
        carry_token = VGroup(dot, label)
        self.play(FadeIn(carry_token), run_time=0.16)
        self.play(carry_token.animate.move_to(end), carry_group.animate.set_color(CARRY_STROKE), run_time=0.38)
        self.play(FadeOut(carry_token), carry_group.animate.set_color(WHITE), run_time=0.16)

    def update_cell_text(self, cell, value):
        label = Text(str(value), font=FONT, weight="BOLD", font_size=38, color=WHITE)
        label.move_to(cell[0].get_center())
        return Transform(cell[1], label)

    def show_code_mapping(self, rows, formula):
        self.play(VGroup(rows, formula).animate.scale(0.66).to_edge(LEFT, buff=0.4), run_time=0.8)

        code_title = Text("核心 C++ 代码", font=FONT, font_size=31, color=WHITE)
        code_lines = [
            "int carry = 0;",
            "for (int i = 0; i < n; i++) {",
            "    int t = carry + a[i] + b[i];",
            "    c.push_back(t % 10);",
            "    carry = t / 10;",
            "}",
            "if (carry) c.push_back(carry);",
        ]
        code = VGroup(
            *[Text(line, font=MONO_FONT, font_size=22, color=MUTED) for line in code_lines]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        code_group = VGroup(code_title, code).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        code_group.to_edge(RIGHT, buff=0.58).shift(UP * 0.48)

        self.play(FadeIn(code_title, shift=LEFT * 0.2), run_time=0.45)
        self.play(LaggedStart(*[Write(line) for line in code], lag_ratio=0.14), run_time=1.35)

        for line in code:
            self.play(line.animate.set_color("#fef3c7"), run_time=0.14)
            self.wait(0.06)
            self.play(line.animate.set_color(MUTED), run_time=0.12)

        details = VGroup(
            Text("反向存储：a[0] 是个位", font=FONT, font_size=26, color=WHITE),
            Text("当前位：t % 10", font=FONT, font_size=26, color=WHITE),
            Text("下一位进位：t / 10", font=FONT, font_size=26, color=WHITE),
            Text("复杂度：O(max(lenA, lenB))", font=FONT, font_size=26, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        details.next_to(code_group, DOWN, buff=0.48, aligned_edge=LEFT)

        self.play(FadeIn(details, shift=UP * 0.2), run_time=0.75)
        self.wait(2.0)
