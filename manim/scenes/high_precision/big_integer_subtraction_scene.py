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
)


BORROW_FILL = "#be123c"
BORROW_STROKE = "#fecdd3"
RESULT_FILL = "#0f766e"
RESULT_STROKE = "#5eead4"
TRIM_FILL = "#475569"
TRIM_STROKE = "#94a3b8"


class BigIntegerSubtractionVisualization(Scene):
    """A storyboard-style high precision subtraction visualization."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        a_digits = [0, 0, 0, 1]
        b_digits = [9, 9, 9, 0]
        result_digits = [1, 0, 0, 0]

        title, subtitle = self.show_intro()
        self.play(VGroup(title, subtitle).animate.to_edge(UP, buff=0.22).scale(0.68), run_time=0.8)

        storage_group = self.show_reverse_storage()
        self.play(FadeOut(storage_group), run_time=0.45)

        a_row = self.make_digit_row("a", a_digits, UP * 1.45, "1000 的反向数组")
        b_row = self.make_digit_row("b", b_digits, UP * 0.2, "999 的反向数组，缺位补 0", ghost_indexes={3})
        c_row = self.make_digit_row("c", [" "] * len(result_digits), DOWN * 1.05, "先生成反向结果，再清理前导零")

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

        borrow_box, borrow_text = self.make_borrow_badge(0)
        borrow_group = VGroup(borrow_box, borrow_text).to_edge(RIGHT, buff=0.78).shift(UP * 1.7)

        formula = Text("", font=FONT, font_size=28, color=WHITE)
        formula.move_to(DOWN * 2.38)
        status = Text("从个位开始：当前位不够减，就向更高位借 1", font=FONT, font_size=28, color=MUTED)
        status.next_to(formula, UP, buff=0.16)

        self.play(FadeIn(i_pointer), FadeIn(borrow_group), FadeIn(status), run_time=0.6)

        borrow = 0
        for i in range(4):
            a_value = a_digits[i]
            b_value = b_digits[i]
            raw = a_value - borrow - b_value
            next_borrow = 1 if raw < 0 else 0
            digit = raw + 10 if raw < 0 else raw
            fast = i >= 2

            self.play(i_pointer.animate.move_to(pointer_position(positions[i])), run_time=0.22 if fast else 0.36)

            if raw < 0:
                formula_text = f"i={i}: t = {a_value} - {borrow} - {b_value} = {raw}，借位后写 {digit}"
            else:
                formula_text = f"i={i}: t = {a_value} - {borrow} - {b_value} = {raw}，直接写 {digit}"
            next_formula = Text(formula_text, font=FONT, font_size=27, color=WHITE)
            next_formula.move_to(formula.get_center())

            self.play(
                color_cell(a_row.cells[i], COMPARE_FILL, "#fde68a"),
                color_cell(b_row.cells[i], COMPARE_FILL, "#fde68a"),
                Transform(formula, next_formula),
                run_time=0.34 if fast else 0.58,
            )

            if raw < 0:
                self.show_borrow_move(i, positions, borrow_group)

            self.play(
                color_cell(c_row.cells[i], RESULT_FILL, RESULT_STROKE),
                self.update_cell_text(c_row.cells[i], digit),
                run_time=0.32 if fast else 0.5,
            )

            next_borrow_text = Text(f"borrow = {next_borrow}", font=FONT, font_size=26, color=WHITE)
            next_borrow_text.move_to(borrow_text.get_center())
            self.play(Transform(borrow_text, next_borrow_text), run_time=0.24 if fast else 0.36)

            self.play(
                reset_cell(a_row.cells[i]),
                reset_cell(b_row.cells[i]),
                mark_sorted(c_row.cells[i]),
                run_time=0.18 if fast else 0.28,
            )
            borrow = next_borrow

        raw_result = Text("先得到 c = [1, 0, 0, 0]，但最高位的 0 不能输出", font=FONT, font_size=30, color="#fef3c7")
        raw_result.move_to(formula.get_center())
        self.play(Transform(formula, raw_result), FadeOut(i_pointer), FadeOut(borrow_group), run_time=0.7)
        self.wait(0.25)

        for index in [3, 2, 1]:
            trim_text = Text(f"c.back() 是 0，删除下标 {index}", font=FONT, font_size=30, color="#fef3c7")
            trim_text.move_to(formula.get_center())
            self.play(
                Transform(formula, trim_text),
                color_cell(c_row.cells[index], TRIM_FILL, TRIM_STROKE),
                run_time=0.36,
            )
            self.play(FadeOut(c_row.cells[index], shift=UP * 0.18), run_time=0.28)

        answer = Text("保留最后一位：倒序输出 1", font=FONT, font_size=32, color="#bbf7d0")
        answer.move_to(formula.get_center())
        self.play(Transform(formula, answer), FadeOut(status), run_time=0.65)
        self.wait(0.7)

        self.show_code_mapping(rows, formula)

    def show_intro(self):
        title = Text("高精度减法 Big Integer Subtraction", font=FONT, weight="BOLD", font_size=50, color=WHITE)
        subtitle = Text(
            "把借位变成一个 borrow 标记：当前位不够减，就给下一位记一笔账",
            font=FONT,
            font_size=27,
            color=MUTED,
        )
        subtitle.next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(title, shift=UP * 0.2), Write(subtitle), run_time=1.25)
        self.wait(0.55)
        return title, subtitle

    def show_reverse_storage(self):
        normal_title = Text("输入：1000 - 999", font=FONT, font_size=34, color=WHITE)
        normal_title.move_to(UP * 1.25)

        vertical = VGroup(
            Text(" 1000", font=MONO_FONT, font_size=42, color=WHITE),
            Text("-  999", font=MONO_FONT, font_size=42, color=WHITE),
            Line(LEFT * 1.25, RIGHT * 1.25, color=MUTED, stroke_width=3),
            Text("    1", font=MONO_FONT, font_size=42, color="#bbf7d0"),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.12)
        vertical.next_to(normal_title, DOWN, buff=0.35)

        hint = Text("本课先约定被减数不小于减数，专注看借位过程", font=FONT, font_size=28, color=MUTED)
        hint.next_to(vertical, DOWN, buff=0.45)

        self.play(FadeIn(normal_title, shift=UP * 0.15), FadeIn(vertical, shift=UP * 0.2), run_time=0.9)
        self.play(Write(hint), run_time=0.8)
        self.wait(0.7)

        reverse_a = Text("1000 -> a = [0, 0, 0, 1]", font=MONO_FONT, font_size=29, color="#bae6fd")
        reverse_b = Text(" 999 -> b = [9, 9, 9]", font=MONO_FONT, font_size=29, color="#fecdd3")
        reverse_group = VGroup(reverse_a, reverse_b).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        reverse_group.next_to(hint, DOWN, buff=0.38)
        self.play(FadeIn(reverse_group, shift=UP * 0.18), run_time=0.8)
        self.wait(0.7)
        return VGroup(normal_title, vertical, hint, reverse_group)

    def make_digit_row(self, name, values, offset, caption, ghost_indexes=None):
        ghost_indexes = ghost_indexes or set()
        cells = [make_array_cell(value) for value in values]
        cells_group = VGroup(*cells).arrange(RIGHT, buff=0.22).move_to(offset)
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

    def make_borrow_badge(self, borrow):
        box = RoundedRectangle(
            width=1.95,
            height=0.72,
            corner_radius=0.12,
            stroke_width=2.5,
            stroke_color=BORROW_STROKE,
            fill_color=BORROW_FILL,
            fill_opacity=0.95,
        )
        text = Text(f"borrow = {borrow}", font=FONT, font_size=26, color=WHITE)
        text.move_to(box.get_center())
        return box, text

    def show_borrow_move(self, index, positions, borrow_group):
        start = positions[index] + UP * 0.54
        if index + 1 < len(positions):
            end = positions[index + 1] + UP * 0.54
        else:
            end = positions[index] + RIGHT * 1.2 + UP * 0.54

        dot = Circle(radius=0.12, fill_color=BORROW_FILL, fill_opacity=1, stroke_color=BORROW_STROKE, stroke_width=2)
        dot.move_to(start)
        label = Text("借 1", font=FONT, font_size=20, color=BORROW_STROKE)
        label.next_to(dot, UP, buff=0.05)
        borrow_token = VGroup(dot, label)
        self.play(FadeIn(borrow_token), run_time=0.16)
        self.play(borrow_token.animate.move_to(end), borrow_group.animate.set_color(BORROW_STROKE), run_time=0.38)
        self.play(FadeOut(borrow_token), borrow_group.animate.set_color(WHITE), run_time=0.16)

    def update_cell_text(self, cell, value):
        label = Text(str(value), font=FONT, weight="BOLD", font_size=38, color=WHITE)
        label.move_to(cell[0].get_center())
        return Transform(cell[1], label)

    def show_code_mapping(self, rows, formula):
        self.play(VGroup(rows, formula).animate.scale(0.68).to_edge(LEFT, buff=0.4), run_time=0.8)

        code_title = Text("核心 C++ 代码", font=FONT, font_size=31, color=WHITE)
        code_lines = [
            "int borrow = 0;",
            "for (int i = 0; i < a.size(); i++) {",
            "    int t = a[i] - borrow - b[i];",
            "    if (t < 0) { t += 10; borrow = 1; }",
            "    else borrow = 0;",
            "    c.push_back(t);",
            "}",
            "while (c.size() > 1 && c.back() == 0)",
            "    c.pop_back();",
        ]
        code = VGroup(
            *[Text(line, font=MONO_FONT, font_size=20, color=MUTED) for line in code_lines]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        code_group = VGroup(code_title, code).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        code_group.to_edge(RIGHT, buff=0.45).shift(UP * 0.52)

        self.play(FadeIn(code_title, shift=LEFT * 0.2), run_time=0.45)
        self.play(LaggedStart(*[Write(line) for line in code], lag_ratio=0.12), run_time=1.35)

        for line in code:
            self.play(line.animate.set_color("#fef3c7"), run_time=0.12)
            self.wait(0.05)
            self.play(line.animate.set_color(MUTED), run_time=0.1)

        details = VGroup(
            Text("前提：本课先处理 a >= b", font=FONT, font_size=25, color=WHITE),
            Text("borrow=1：当前位已经向高位借过 1", font=FONT, font_size=25, color=WHITE),
            Text("t<0：当前结果位加 10，下一位继续减 1", font=FONT, font_size=25, color=WHITE),
            Text("最后清理结果最高位多余的 0", font=FONT, font_size=25, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        details.next_to(code_group, DOWN, buff=0.4, aligned_edge=LEFT)

        self.play(FadeIn(details, shift=UP * 0.2), run_time=0.75)
        self.wait(2.0)
