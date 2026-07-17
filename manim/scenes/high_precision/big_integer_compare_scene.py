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
)


WIN_FILL = "#0f766e"
WIN_STROKE = "#5eead4"
SIGN_FILL = "#be123c"
SIGN_STROKE = "#fecdd3"
LENGTH_FILL = "#7c3aed"
LENGTH_STROKE = "#ddd6fe"


class BigIntegerCompareVisualization(Scene):
    """Visualize comparing big integers before signed subtraction."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        title, subtitle = self.show_intro()
        self.play(VGroup(title, subtitle).animate.to_edge(UP, buff=0.22).scale(0.66), run_time=0.8)

        compare_group = self.show_length_compare()
        self.play(FadeOut(compare_group), run_time=0.45)

        lexical_group = self.show_same_length_compare()
        self.play(FadeOut(lexical_group), run_time=0.45)

        signed_group = self.show_signed_subtraction_flow()
        self.show_code_mapping(signed_group)

    def show_intro(self):
        title = Text("大数比较与符号处理 Big Integer Compare", font=FONT, weight="BOLD", font_size=48, color=WHITE)
        subtitle = Text(
            "先判断绝对值大小，再决定是否交换减法顺序和输出负号",
            font=FONT,
            font_size=27,
            color=MUTED,
        )
        subtitle.next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(title, shift=UP * 0.2), Write(subtitle), run_time=1.15)
        self.wait(0.45)
        return title, subtitle

    def show_length_compare(self):
        question = Text("例题：12345 - 987654", font=FONT, font_size=36, color=WHITE)
        question.move_to(UP * 1.45)

        left_len = self.make_length_badge("len(12345)", "5")
        right_len = self.make_length_badge("len(987654)", "6")
        relation = Text("5 < 6", font=MONO_FONT, font_size=40, color="#fef3c7")
        group = VGroup(left_len, relation, right_len).arrange(RIGHT, buff=0.5)
        group.next_to(question, DOWN, buff=0.55)

        verdict = Text("长度不同：位数更多的数字一定更大", font=FONT, font_size=30, color=MUTED)
        verdict.next_to(group, DOWN, buff=0.55)

        sign = self.make_sign_card("|12345| < |987654|", "答案需要负号")
        sign.next_to(verdict, DOWN, buff=0.38)

        self.play(FadeIn(question, shift=UP * 0.2), run_time=0.6)
        self.play(LaggedStart(FadeIn(left_len), FadeIn(relation), FadeIn(right_len), lag_ratio=0.2), run_time=0.9)
        self.play(Write(verdict), run_time=0.65)
        self.play(FadeIn(sign, shift=UP * 0.18), run_time=0.65)
        self.wait(0.75)
        return VGroup(question, group, verdict, sign)

    def show_same_length_compare(self):
        title = Text("长度相同：从最高位开始一格一格比较", font=FONT, font_size=34, color=WHITE)
        title.move_to(UP * 2.0)

        top = self.make_digit_row("x", list("82312"), UP * 0.85, "同样都是 5 位")
        bottom = self.make_digit_row("y", list("82299"), DOWN * 0.25, "第一处不同决定大小")
        rows = VGroup(top, bottom)

        positions = [cell.get_center() for cell in top.cells]
        pointer = self.make_top_pointer("i", POINTER_BLUE)
        pointer.move_to(self.top_pointer_position(positions[0]))

        note = Text("从最高位开始，找到第一处不同", font=FONT, font_size=27, color=MUTED)
        note.move_to(DOWN * 1.95)

        final_note = Text("所以 82312 > 82299，因为第一处不同是 3 > 2", font=FONT, font_size=30, color="#bbf7d0")
        final_note.move_to(note.get_center())

        self.play(FadeIn(title, shift=UP * 0.15), FadeIn(rows, shift=UP * 0.2), FadeIn(pointer), run_time=0.9)
        self.play(Write(note), run_time=0.7)

        for index in range(2):
            self.play(
                pointer.animate.move_to(self.top_pointer_position(positions[index])),
                color_cell(top.cells[index], COMPARE_FILL, "#fde68a"),
                color_cell(bottom.cells[index], COMPARE_FILL, "#fde68a"),
                run_time=0.4,
            )
            self.play(reset_cell(top.cells[index]), reset_cell(bottom.cells[index]), run_time=0.22)

        fixed_note = Text("前两位 8、2 相同，第三位出现分歧：3 > 2", font=FONT, font_size=29, color="#fef3c7")
        fixed_note.move_to(note.get_center())
        self.play(
            Transform(note, fixed_note),
            pointer.animate.move_to(self.top_pointer_position(positions[2])),
            color_cell(top.cells[2], WIN_FILL, WIN_STROKE),
            color_cell(bottom.cells[2], SIGN_FILL, SIGN_STROKE),
            run_time=0.65,
        )
        self.play(Transform(note, final_note), mark_sorted(top.cells[2]), run_time=0.55)
        self.wait(0.75)
        return VGroup(title, rows, pointer, note)

    def show_signed_subtraction_flow(self):
        question = Text("回到 12345 - 987654：左边更小，先交换再减", font=FONT, font_size=33, color=WHITE)
        question.move_to(UP * 2.15)

        sign_card = self.make_sign_card("cmp(a, b) < 0", 'sign = "-"')
        sign_card.to_edge(LEFT, buff=0.62).shift(UP * 0.65)

        a_row = self.make_digit_row("big", [4, 5, 6, 7, 8, 9], UP * 0.45, "987654")
        b_row = self.make_digit_row("small", [5, 4, 3, 2, 1, 0], DOWN * 0.72, "12345 补 0", ghost_indexes={5})
        c_row = self.make_digit_row("diff", [" "] * 6, DOWN * 1.88, "绝对值差")
        rows = VGroup(a_row, b_row, c_row).scale(0.66).move_to(RIGHT * 2.15 + DOWN * 0.12)

        flow = VGroup(
            Text("1. 比较：12345 更小", font=FONT, font_size=24, color=WHITE),
            Text("2. 记录：sign = '-'", font=FONT, font_size=24, color=WHITE),
            Text("3. 交换：987654 - 12345", font=FONT, font_size=24, color=WHITE),
            Text("4. 调用 subtractAbs", font=FONT, font_size=24, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        flow.next_to(sign_card, DOWN, buff=0.42, aligned_edge=LEFT)

        formula = Text("diff = 975309，最终输出：-975309", font=FONT, font_size=31, color="#bbf7d0")
        formula.move_to(DOWN * 2.95)

        self.play(FadeIn(question, shift=UP * 0.15), run_time=0.45)
        self.play(FadeIn(sign_card, shift=UP * 0.16), LaggedStart(*[Write(line) for line in flow], lag_ratio=0.18), run_time=1.2)
        self.play(FadeIn(rows, shift=UP * 0.2), run_time=0.8)

        result_digits = [9, 0, 3, 5, 7, 9]
        positions = [cell.get_center() for cell in a_row.cells]
        pointer = make_pointer("i", POINTER_PINK).scale(0.78)
        pointer.move_to(pointer_position(positions[0]) + RIGHT * 0.02)
        self.play(FadeIn(pointer), run_time=0.35)

        for i, digit in enumerate(result_digits):
            fast = i >= 2
            self.play(
                pointer.animate.move_to(pointer_position(positions[i]) + RIGHT * 0.02),
                color_cell(a_row.cells[i], COMPARE_FILL, "#fde68a"),
                color_cell(b_row.cells[i], COMPARE_FILL, "#fde68a"),
                run_time=0.22 if fast else 0.34,
            )
            self.play(
                color_cell(c_row.cells[i], WIN_FILL, WIN_STROKE),
                self.update_cell_text(c_row.cells[i], digit),
                run_time=0.24 if fast else 0.38,
            )
            self.play(
                reset_cell(a_row.cells[i]),
                reset_cell(b_row.cells[i]),
                mark_sorted(c_row.cells[i]),
                run_time=0.16 if fast else 0.24,
            )

        self.play(FadeOut(pointer), FadeIn(formula, shift=UP * 0.1), run_time=0.55)
        self.wait(0.75)
        return VGroup(question, sign_card, flow, rows, formula)

    def make_top_pointer(self, label, color):
        triangle = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI)
        text = Text(label, font=FONT, font_size=22, color=color)
        text.next_to(triangle, UP, buff=0.05)
        return VGroup(triangle, text)

    def top_pointer_position(self, slot_position):
        return slot_position + UP * 0.95

    def make_digit_row(self, name, values, offset, caption, ghost_indexes=None):
        ghost_indexes = ghost_indexes or set()
        cells = [make_array_cell(value) for value in values]
        cells_group = VGroup(*cells).arrange(RIGHT, buff=0.14).move_to(offset)
        indexes = make_indices([cell.get_center() for cell in cells])

        label = Text(name, font=MONO_FONT, font_size=28, color=WHITE)
        label.next_to(cells_group, LEFT, buff=0.32)
        caption_text = Text(caption, font=FONT, font_size=20, color=MUTED)
        caption_text.next_to(cells_group, RIGHT, buff=0.32)

        for index in ghost_indexes:
            cells[index][0].set_fill(CELL_FILL, opacity=0.38).set_stroke(CELL_STROKE, opacity=0.45)
            cells[index][1].set_opacity(0.45)

        row = VGroup(label, cells_group, indexes, caption_text)
        row.cells = cells
        return row

    def make_length_badge(self, label, value):
        box = RoundedRectangle(
            width=2.55,
            height=1.18,
            corner_radius=0.12,
            stroke_width=2.5,
            stroke_color=LENGTH_STROKE,
            fill_color=LENGTH_FILL,
            fill_opacity=0.9,
        )
        label_text = Text(label, font=MONO_FONT, font_size=21, color="#ede9fe")
        value_text = Text(value, font=MONO_FONT, weight="BOLD", font_size=36, color=WHITE)
        content = VGroup(label_text, value_text).arrange(DOWN, buff=0.08)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def make_sign_card(self, top_text, bottom_text):
        box = RoundedRectangle(
            width=3.25,
            height=1.15,
            corner_radius=0.12,
            stroke_width=2.5,
            stroke_color=SIGN_STROKE,
            fill_color=SIGN_FILL,
            fill_opacity=0.92,
        )
        top = Text(top_text, font=MONO_FONT, font_size=22, color="#ffe4e6")
        bottom = Text(bottom_text, font=FONT, weight="BOLD", font_size=28, color=WHITE)
        content = VGroup(top, bottom).arrange(DOWN, buff=0.08)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def update_cell_text(self, cell, value):
        label = Text(str(value), font=FONT, weight="BOLD", font_size=38, color=WHITE)
        label.move_to(cell[0].get_center())
        return Transform(cell[1], label)

    def show_code_mapping(self, scene_group):
        self.play(scene_group.animate.scale(0.62).to_edge(LEFT, buff=0.35).shift(UP * 0.12), run_time=0.75)

        code_title = Text("核心 C++ 代码", font=FONT, font_size=31, color=WHITE)
        code_lines = [
            "int cmp(string a, string b) {",
            "    if (a.size() != b.size())",
            "        return a.size() > b.size() ? 1 : -1;",
            "    for (int i = 0; i < a.size(); i++)",
            "        if (a[i] != b[i]) return a[i] > b[i] ? 1 : -1;",
            "    return 0;",
            "}",
            "if (cmp(a, b) < 0) { swap(a, b); sign = '-'; }",
            "answer = subtractAbs(a, b);",
        ]
        code = VGroup(
            *[Text(line, font=MONO_FONT, font_size=18, color=MUTED) for line in code_lines]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        code_group = VGroup(code_title, code).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        code_group.to_edge(RIGHT, buff=0.32).shift(UP * 0.42)

        self.play(FadeIn(code_title, shift=LEFT * 0.2), run_time=0.42)
        self.play(LaggedStart(*[Write(line) for line in code], lag_ratio=0.11), run_time=1.25)

        details = VGroup(
            Text("比较只看长度和最高位，不做任何借位", font=FONT, font_size=24, color=WHITE),
            Text("负号只由原始 a、b 的大小决定", font=FONT, font_size=24, color=WHITE),
            Text("真正的逐位减法复用上一课 subtractAbs", font=FONT, font_size=24, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        details.next_to(code_group, DOWN, buff=0.36, aligned_edge=LEFT)

        self.play(FadeIn(details, shift=UP * 0.2), run_time=0.65)
        self.wait(2.0)
