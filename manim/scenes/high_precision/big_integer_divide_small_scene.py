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
    SORTED_FILL,
)


ACCENT = "#22c55e"
ACCENT_STROKE = "#bbf7d0"
DIVISOR_FILL = "#7c2d12"
DIVISOR_STROKE = "#fed7aa"
REMAINDER_FILL = "#312e81"
REMAINDER_STROKE = "#a5b4fc"
QUOTIENT_FILL = "#0f766e"
QUOTIENT_STROKE = "#5eead4"


class BigIntegerDivideSmallVisualization(Scene):
    """Visualize big integer division by a small integer with long division."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        digits = [9, 8, 7, 6, 5]
        quotient_digits = ["?", "?", "?", "?", "?"]
        steps = [
            {"index": 0, "digit": 9, "before": 0, "pending": 9, "q": 0, "after": 9},
            {"index": 1, "digit": 8, "before": 9, "pending": 98, "q": 8, "after": 2},
            {"index": 2, "digit": 7, "before": 2, "pending": 27, "q": 2, "after": 3},
            {"index": 3, "digit": 6, "before": 3, "pending": 36, "q": 3, "after": 0},
            {"index": 4, "digit": 5, "before": 0, "pending": 5, "q": 0, "after": 5},
        ]

        title, subtitle = self.show_intro()
        self.play(VGroup(title, subtitle).animate.to_edge(UP, buff=0.22).scale(0.66), run_time=0.75)

        long_division = self.show_long_division_hint()
        self.play(FadeOut(long_division), run_time=0.45)

        dividend_row = self.make_digit_row("a", digits, UP * 1.9, "最高位 -> 最低位")
        quotient_row = self.make_digit_row("q", quotient_digits, UP * 0.55, "商从左到右写")
        remainder_panel = self.make_remainder_panel()
        divisor_badge = self.make_divisor_badge(12)
        divisor_badge.next_to(remainder_panel, UP, buff=0.24)

        formula = Text("核心规则：r = r * 10 + 当前数字", font=FONT, font_size=29, color=WHITE)
        formula.move_to(DOWN * 2.75)
        status = Text("余数 r 像一个篮子：每次接住新落下的一位，再决定这一位商是多少", font=FONT, font_size=26, color=MUTED)
        status.next_to(formula, UP, buff=0.18)

        self.play(
            LaggedStart(
                FadeIn(dividend_row, shift=UP * 0.16),
                FadeIn(quotient_row, shift=UP * 0.16),
                FadeIn(remainder_panel, shift=LEFT * 0.12),
                FadeIn(divisor_badge, shift=LEFT * 0.12),
                lag_ratio=0.14,
            ),
            run_time=1.15,
        )
        self.play(Write(status), FadeIn(formula), run_time=0.75)

        scene_group = VGroup(dividend_row, quotient_row, remainder_panel, divisor_badge, status, formula)
        for step in steps:
            self.play_division_step(step, dividend_row, quotient_row, remainder_panel, formula, status)

        trim_text = Text("商的最前面 0 只表示“还不够除”，输出时把它淡出", font=FONT, font_size=27, color="#fef3c7")
        trim_text.move_to(status.get_center())
        self.play(
            Transform(status, trim_text),
            quotient_row.cells[0].animate.set_opacity(0.32),
            run_time=0.55,
        )

        answer = Text("q = 08230 -> 8230，最终余数 r = 5", font=FONT, font_size=31, color="#bbf7d0")
        answer.move_to(formula.get_center())
        self.play(Transform(formula, answer), run_time=0.55)
        self.wait(0.65)

        self.show_code_mapping(scene_group)

    def show_intro(self):
        title = Text("高精度除低精度  Big Integer / int", font=FONT, weight="BOLD", font_size=46, color=WHITE)
        subtitle = Text(
            "像手算长除法一样：从最高位往右走，让余数带着还没分完的部分继续前进",
            font=FONT,
            font_size=27,
            color=MUTED,
        )
        subtitle.next_to(title, DOWN, buff=0.24)
        self.play(FadeIn(title, shift=UP * 0.18), Write(subtitle), run_time=1.1)
        self.wait(0.45)
        return title, subtitle

    def show_long_division_hint(self):
        example = Text("示例：98765 / 12", font=FONT, font_size=38, color=WHITE)
        example.move_to(UP * 1.6)

        board = VGroup(
            Text("12 ) 98765", font=MONO_FONT, font_size=46, color=WHITE),
            Text("先看 9：不够除，商写 0，余数还是 9", font=FONT, font_size=27, color="#bae6fd"),
            Text("再落下 8：98 / 12 = 8，余数 2", font=FONT, font_size=27, color="#fed7aa"),
            Text("余数不是失败，而是下一位计算的起点", font=FONT, font_size=28, color="#bbf7d0"),
        ).arrange(DOWN, buff=0.24)
        board.next_to(example, DOWN, buff=0.35)

        self.play(FadeIn(example, shift=UP * 0.15), FadeIn(board, shift=UP * 0.18), run_time=1.0)
        self.wait(0.95)
        return VGroup(example, board)

    def make_digit_row(self, name, values, offset, caption):
        cells = [make_array_cell(value).scale(0.74) for value in values]
        cells_group = VGroup(*cells).arrange(RIGHT, buff=0.1).move_to(offset).shift(LEFT * 1.15)
        indexes = make_indices([cell.get_center() for cell in cells])
        indexes.scale(0.78)
        indexes.shift(UP * 0.16)

        label = Text(name, font=MONO_FONT, font_size=28, color=WHITE)
        caption_text = Text(caption, font=FONT, font_size=17, color=MUTED)
        label_group = VGroup(label, caption_text).arrange(DOWN, buff=0.08)
        label_group.next_to(cells_group, LEFT, buff=0.28)

        row = VGroup(label_group, cells_group, indexes)
        row.cells = cells
        return row

    def make_remainder_panel(self):
        box = RoundedRectangle(
            width=2.05,
            height=1.22,
            corner_radius=0.1,
            stroke_width=2.8,
            stroke_color=REMAINDER_STROKE,
            fill_color=REMAINDER_FILL,
            fill_opacity=1,
        )
        value = Text("0", font=FONT, weight="BOLD", font_size=40, color=WHITE)
        value.move_to(box.get_center())
        label = Text("余数 r", font=FONT, font_size=24, color=REMAINDER_STROKE)
        label.next_to(box, DOWN, buff=0.12)
        panel = VGroup(box, value, label).to_edge(RIGHT, buff=0.8).shift(UP * 1.15)
        panel.box = box
        panel.value = value
        return panel

    def make_divisor_badge(self, value):
        box = RoundedRectangle(
            width=2.05,
            height=0.62,
            corner_radius=0.1,
            stroke_width=2.4,
            stroke_color=DIVISOR_STROKE,
            fill_color=DIVISOR_FILL,
            fill_opacity=1,
        )
        label = Text(f"除数 b = {value}", font=FONT, font_size=24, color="#ffedd5")
        label.move_to(box.get_center())
        return VGroup(box, label)

    def make_digit_token(self, digit):
        dot = Circle(radius=0.24, fill_color=POINTER_BLUE, fill_opacity=1, stroke_color="#bae6fd", stroke_width=2)
        label = Text(str(digit), font=FONT, weight="BOLD", font_size=24, color=BACKGROUND)
        label.move_to(dot.get_center())
        return VGroup(dot, label)

    def play_division_step(self, step, dividend_row, quotient_row, remainder_panel, formula, status):
        i = step["index"]
        digit = step["digit"]
        before = step["before"]
        pending = step["pending"]
        quotient = step["q"]
        after = step["after"]
        fast = i >= 2

        current_cell = dividend_row.cells[i]
        quotient_cell = quotient_row.cells[i]

        next_formula = Text(
            f"第 {i + 1} 位落下：r = {before} * 10 + {digit} = {pending}",
            font=FONT,
            font_size=27,
            color=WHITE,
        )
        next_formula.move_to(formula.get_center())

        self.play(
            color_cell(current_cell, COMPARE_FILL, "#fde68a"),
            Transform(formula, next_formula),
            run_time=0.35 if fast else 0.55,
        )

        token = self.make_digit_token(digit)
        token.move_to(current_cell.get_center() + UP * 0.08)
        target = remainder_panel.box.get_center() + UP * 0.02
        self.play(FadeIn(token, scale=0.85), run_time=0.18 if fast else 0.26)
        self.play(token.animate.move_to(target), run_time=0.3 if fast else 0.45)

        pending_value = Text(str(pending), font=FONT, weight="BOLD", font_size=40, color=WHITE)
        pending_value.move_to(remainder_panel.box.get_center())
        self.play(Transform(remainder_panel.value, pending_value), FadeOut(token, scale=0.8), run_time=0.28 if fast else 0.42)

        decision = Text(
            f"{pending} / 12 = {quotient}，写入 q[{i}]；{pending} % 12 = {after}，留下新余数",
            font=FONT,
            font_size=25,
            color="#bbf7d0",
        )
        decision.move_to(status.get_center())
        quotient_value = Text(str(quotient), font=FONT, weight="BOLD", font_size=32, color=WHITE)
        quotient_value.move_to(quotient_cell[0].get_center())
        after_value = Text(str(after), font=FONT, weight="BOLD", font_size=40, color=WHITE)
        after_value.move_to(remainder_panel.box.get_center())

        self.play(
            Transform(status, decision),
            color_cell(quotient_cell, QUOTIENT_FILL, QUOTIENT_STROKE),
            Transform(quotient_cell[1], quotient_value),
            Transform(remainder_panel.value, after_value),
            run_time=0.42 if fast else 0.62,
        )
        self.play(mark_sorted(quotient_cell), reset_cell(current_cell), run_time=0.2 if fast else 0.3)

    def show_code_mapping(self, scene_group):
        self.play(scene_group.animate.scale(0.48).to_edge(LEFT, buff=0.16).shift(UP * 0.02), run_time=0.75)

        code_title = Text("核心 C++ 代码", font=FONT, font_size=24, color=WHITE)
        code_lines = [
            "string q;",
            "long long r = 0;",
            "for (char ch : a) {",
            "  r = r * 10 + (ch - '0');",
            "  q.push_back('0' + r / b);",
            "  r %= b;",
            "}",
            "while (q.size() > 1 && q[0]=='0')",
            "  q.erase(q.begin());",
            "cout << q;",
        ]
        code = Text(
            "\n".join(code_lines),
            font=MONO_FONT,
            font_size=15,
            color=MUTED,
            line_spacing=0.82,
        )
        code_group = VGroup(code_title, code).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        code_group.to_edge(RIGHT, buff=0.72).shift(DOWN * 0.12)

        self.play(FadeIn(code_title, shift=LEFT * 0.2), run_time=0.4)
        self.play(FadeIn(code, shift=UP * 0.12), run_time=0.75)

        detail = Text("余数一路传下去", font=FONT, font_size=17, color=WHITE)
        detail.next_to(code_group, DOWN, buff=0.13, aligned_edge=LEFT)
        self.play(FadeIn(detail, shift=UP * 0.16), run_time=0.65)
        self.wait(2.0)
