from pathlib import Path
import sys

from manim import *


COMMON_DIR = Path(__file__).resolve().parents[2] / "common"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from array_widgets import color_cell, make_array_cell, make_indices, make_pointer, mark_sorted, place_pointer, pointer_position, reset_cell  # noqa: E402
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
)


OK_FILL = "#0f766e"
OK_STROKE = "#5eead4"
WARN_FILL = "#7c2d12"
WARN_STROKE = "#fed7aa"
LIMIT_FILL = "#312e81"
LIMIT_STROKE = "#a5b4fc"
STRING_FILL = "#1d4ed8"
STRING_STROKE = "#bfdbfe"
ARRAY_FILL = "#15803d"
ARRAY_STROKE = "#bbf7d0"


def make_label_box(text, fill, stroke, width=3.0, height=0.82, font_size=26, mono=False):
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.1,
        stroke_width=2.5,
        stroke_color=stroke,
        fill_color=fill,
        fill_opacity=0.94,
    )
    label = Text(text, font=MONO_FONT if mono else FONT, font_size=font_size, color=WHITE)
    label.move_to(box.get_center())
    return VGroup(box, label)


def make_code_block(title_text, code_lines, font_size=17):
    title = Text(title_text, font=FONT, font_size=27, color=WHITE)
    code = Text("\n".join(code_lines), font=MONO_FONT, font_size=font_size, color=MUTED, line_spacing=0.86)
    group = VGroup(title, code).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    return group


def update_cell_text(cell, value, font_size=36):
    label = Text(str(value), font=FONT, weight="BOLD", font_size=font_size, color=WHITE)
    label.move_to(cell[0].get_center())
    return Transform(cell[1], label)


class BigIntegerIntroBase(Scene):
    def show_intro(self, title_text, subtitle_text, title_size=48):
        title = Text(title_text, font=FONT, weight="BOLD", font_size=title_size, color=WHITE)
        subtitle = Text(subtitle_text, font=FONT, font_size=27, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.24)
        self.play(FadeIn(title, shift=UP * 0.18), Write(subtitle), run_time=1.05)
        self.wait(0.45)
        return title, subtitle

    def make_char_row(self, label, values, offset, caption="", cell_width=0.68, cell_height=0.72, font_size=25):
        cells = []
        for value in values:
            box = RoundedRectangle(
                width=cell_width,
                height=cell_height,
                corner_radius=0.08,
                stroke_width=2.3,
                stroke_color=STRING_STROKE,
                fill_color=STRING_FILL,
                fill_opacity=0.94,
            )
            text = Text(str(value), font=MONO_FONT, weight="BOLD", font_size=font_size, color=WHITE)
            text.move_to(box.get_center())
            cells.append(VGroup(box, text))

        cells_group = VGroup(*cells).arrange(RIGHT, buff=0.07).move_to(offset)
        indexes = make_indices([cell.get_center() for cell in cells])
        indexes.scale(0.68)
        indexes.shift(UP * 0.2)

        label_font = MONO_FONT if str(label).isascii() else FONT
        label_text = Text(label, font=label_font, font_size=24, color=WHITE)
        caption_text = Text(caption, font=FONT, font_size=17, color=MUTED)
        label_group = VGroup(label_text, caption_text).arrange(DOWN, buff=0.08)
        label_group.next_to(cells_group, LEFT, buff=0.26)

        row = VGroup(label_group, cells_group, indexes)
        row.cells = cells
        return row

    def make_digit_row(self, label, values, offset, caption="", scale=0.72):
        cells = [make_array_cell(value).scale(scale) for value in values]
        cells_group = VGroup(*cells).arrange(RIGHT, buff=0.1).move_to(offset)
        indexes = make_indices([cell.get_center() for cell in cells])
        indexes.scale(scale)
        indexes.shift(UP * 0.12)

        label_font = MONO_FONT if str(label).isascii() else FONT
        label_text = Text(label, font=label_font, font_size=24, color=WHITE)
        caption_text = Text(caption, font=FONT, font_size=17, color=MUTED)
        label_group = VGroup(label_text, caption_text).arrange(DOWN, buff=0.08)
        label_group.next_to(cells_group, LEFT, buff=0.26)

        row = VGroup(label_group, cells_group, indexes)
        row.cells = cells
        return row

    def show_code_mapping(self, scene_group, title, code_lines, summary, code_size=17):
        self.play(scene_group.animate.scale(0.47).to_edge(LEFT, buff=0.16).shift(UP * 0.02), run_time=0.75)
        code = make_code_block(title, code_lines, font_size=code_size)
        code.to_edge(RIGHT, buff=0.42).shift(UP * 0.02)
        self.play(FadeIn(code, shift=LEFT * 0.2), run_time=0.8)

        summary_text = Text(summary, font=FONT, font_size=21, color=WHITE)
        if summary_text.width > 4.1:
            summary_text.scale_to_fit_width(4.1)
        summary_text.next_to(code, DOWN, buff=0.2, aligned_edge=LEFT)
        self.play(FadeIn(summary_text, shift=UP * 0.12), run_time=0.6)
        self.wait(1.8)
        return VGroup(code, summary_text)


class BigIntegerOverflowVisualization(BigIntegerIntroBase):
    """Show why built-in integer types are not enough for huge inputs."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        title, subtitle = self.show_intro(
            "普通整数为什么不够用",
            "高精度的第一步，是承认普通整型只有有限容量",
        )
        self.play(VGroup(title, subtitle).animate.to_edge(UP, buff=0.22).scale(0.68), run_time=0.75)

        capacity_group = self.show_capacity_limits()
        self.play(FadeOut(capacity_group), run_time=0.42)

        train_group = self.show_string_train()
        self.show_code_mapping(
            VGroup(title, subtitle, train_group),
            "读入方式先改变",
            [
                "string s;",
                "cin >> s;",
                "",
                "// process each digit later",
                "for (char ch : s) {",
                "  int digit = ch - '0';",
                "}",
            ],
            "先用 string 保住每一位",
            code_size=17,
        )

    def show_capacity_limits(self):
        heading = Text("变量像容器：容量再大，也有上限", font=FONT, font_size=34, color=WHITE)
        heading.move_to(UP * 1.95)

        int_card = self.make_capacity_card("int", "最大约 2.1e9", "10 位以内常见", LIMIT_FILL, LIMIT_STROKE)
        long_card = self.make_capacity_card("long long", "最大约 9.22e18", "最多 19 位左右", OK_FILL, OK_STROKE)
        cards = VGroup(int_card, long_card).arrange(RIGHT, buff=0.7)
        cards.next_to(heading, DOWN, buff=0.45)

        huge = Text("100000000000000000000", font=MONO_FONT, font_size=29, color="#fef3c7")
        huge.next_to(cards, DOWN, buff=0.52)
        arrow = Arrow(huge.get_top(), long_card.get_bottom(), buff=0.12, color=WARN_STROKE, stroke_width=4)
        warning = make_label_box("超过 long long：会溢出", WARN_FILL, WARN_STROKE, width=4.1, height=0.72, font_size=25)
        warning.next_to(huge, DOWN, buff=0.34)

        self.play(FadeIn(heading, shift=UP * 0.14), run_time=0.5)
        self.play(LaggedStart(FadeIn(int_card, shift=UP * 0.12), FadeIn(long_card, shift=UP * 0.12), lag_ratio=0.16), run_time=0.8)
        self.play(FadeIn(huge, shift=UP * 0.15), GrowArrow(arrow), run_time=0.65)
        self.play(FadeIn(warning, shift=UP * 0.12), long_card[0].animate.set_stroke(WARN_STROKE, width=4), run_time=0.65)
        self.wait(0.75)
        return VGroup(heading, cards, huge, arrow, warning)

    def show_string_train(self):
        heading = Text("换一种想法：不把它当一个数，而是一串数字", font=FONT, font_size=32, color=WHITE)
        heading.move_to(UP * 1.9)

        digits = list("100000000000000000000")
        train = self.make_char_row("s", digits, UP * 0.65, "string 完整保存每一位", cell_width=0.32, cell_height=0.56, font_size=19)
        train[0].shift(LEFT * 0.1)

        note = Text("每一节车厢只装一位：'1'、'0'、'0' ...", font=FONT, font_size=28, color=MUTED)
        note.next_to(train, DOWN, buff=0.5)

        digit_cards = VGroup(
            make_label_box("字符", STRING_FILL, STRING_STROKE, width=1.45, height=0.68, font_size=24),
            Text("->", font=MONO_FONT, font_size=28, color=MUTED),
            make_label_box("数字", ARRAY_FILL, ARRAY_STROKE, width=1.45, height=0.68, font_size=24),
            Text("->", font=MONO_FONT, font_size=28, color=MUTED),
            make_label_box("数组", OK_FILL, OK_STROKE, width=1.45, height=0.68, font_size=24),
        ).arrange(RIGHT, buff=0.18)
        digit_cards.next_to(note, DOWN, buff=0.45)

        self.play(FadeIn(heading, shift=UP * 0.14), run_time=0.5)
        self.play(FadeIn(train, shift=UP * 0.15), run_time=0.8)
        for index in [0, 1, 2, 18, 19, 20]:
            self.play(train.cells[index][0].animate.set_fill(COMPARE_FILL, opacity=1).set_stroke("#fde68a", width=3), run_time=0.08)
        self.play(Write(note), run_time=0.55)
        self.play(FadeIn(digit_cards, shift=UP * 0.12), run_time=0.75)
        self.wait(0.75)
        return VGroup(heading, train, note, digit_cards)

    def make_capacity_card(self, title, limit, hint, fill, stroke):
        box = RoundedRectangle(
            width=3.35,
            height=1.55,
            corner_radius=0.12,
            stroke_width=2.6,
            stroke_color=stroke,
            fill_color=fill,
            fill_opacity=0.92,
        )
        title_text = Text(title, font=MONO_FONT, weight="BOLD", font_size=31, color=WHITE)
        limit_text = Text(limit, font=FONT, font_size=22, color="#e0f2fe")
        hint_text = Text(hint, font=FONT, font_size=19, color=MUTED)
        content = VGroup(title_text, limit_text, hint_text).arrange(DOWN, buff=0.09)
        content.move_to(box.get_center())
        return VGroup(box, content)


class BigIntegerStorageVisualization(BigIntegerIntroBase):
    """Turn a decimal string into an integer digit array."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        title, subtitle = self.show_intro(
            "字符串与数组存储大整数",
            "字符串负责完整读入，数组负责逐位计算",
        )
        self.play(VGroup(title, subtitle).animate.to_edge(UP, buff=0.22).scale(0.68), run_time=0.75)

        char_group = self.show_character_meaning()
        self.play(FadeOut(char_group), run_time=0.42)

        array_group = self.show_array_conversion()
        self.show_code_mapping(
            VGroup(title, subtitle, array_group),
            "字符转数字",
            [
                "string s;",
                "cin >> s;",
                "",
                "vector<int> a;",
                "for (int i = 0; i < s.size(); i++) {",
                "  a.push_back(s[i] - '0');",
                "}",
            ],
            "s[i] - '0' 是字符串和数字数组之间的桥",
            code_size=16,
        )

    def show_character_meaning(self):
        heading = Text("字符串里的每一位，先是字符", font=FONT, font_size=34, color=WHITE)
        heading.move_to(UP * 1.85)

        row = self.make_char_row("s", ["'7'", "'2'", "'4'", "'1'", "'0'", "'5'"], UP * 0.72, '输入："724105"', cell_width=0.88, font_size=24)
        formula = Text("'7' - '0' = 7", font=MONO_FONT, font_size=36, color="#fef3c7")
        formula.next_to(row, DOWN, buff=0.55)

        left = make_label_box("字符 '7'", STRING_FILL, STRING_STROKE, width=2.15, height=0.75, font_size=25)
        right = make_label_box("数字 7", ARRAY_FILL, ARRAY_STROKE, width=2.0, height=0.75, font_size=25)
        bridge = Text("- '0'", font=MONO_FONT, font_size=30, color=MUTED)
        bridge_group = VGroup(left, bridge, right).arrange(RIGHT, buff=0.22)
        bridge_group.next_to(formula, DOWN, buff=0.38)

        self.play(FadeIn(heading, shift=UP * 0.14), FadeIn(row, shift=UP * 0.14), run_time=0.75)
        self.play(color_cell(row.cells[0], COMPARE_FILL, "#fde68a"), FadeIn(formula, shift=UP * 0.12), run_time=0.65)
        self.play(FadeIn(bridge_group, shift=UP * 0.12), run_time=0.65)
        self.wait(0.7)
        return VGroup(heading, row, formula, bridge_group)

    def show_array_conversion(self):
        heading = Text("把字符逐个落入数组，才方便计算", font=FONT, font_size=33, color=WHITE)
        heading.move_to(UP * 2.05)

        chars = self.make_char_row("s", list("724105"), UP * 1.0, '字符串 s', cell_width=0.72, font_size=26)
        digits = self.make_digit_row("a", [" "] * 6, DOWN * 0.35, "数字数组 a", scale=0.68)
        formula = Text("当前：s[i] - '0'", font=MONO_FONT, font_size=29, color=MUTED)
        formula.move_to(DOWN * 1.72)

        self.play(FadeIn(heading, shift=UP * 0.14), FadeIn(chars, shift=UP * 0.12), FadeIn(digits, shift=UP * 0.12), run_time=0.8)
        self.play(FadeIn(formula), run_time=0.35)

        values = [7, 2, 4, 1, 0, 5]
        for index, value in enumerate(values):
            fast = index >= 2
            current = Text(f"i={index}: '{value}' - '0' = {value}", font=MONO_FONT, font_size=29, color=WHITE)
            current.move_to(formula.get_center())
            self.play(
                color_cell(chars.cells[index], COMPARE_FILL, "#fde68a"),
                color_cell(digits.cells[index], ARRAY_FILL, ARRAY_STROKE),
                Transform(formula, current),
                run_time=0.26 if fast else 0.42,
            )
            self.play(update_cell_text(digits.cells[index], value, font_size=32), run_time=0.22 if fast else 0.34)
            self.play(reset_cell(chars.cells[index]), mark_sorted(digits.cells[index]), run_time=0.14 if fast else 0.24)

        sum_text = Text("数组能逐位计算：7 + 2 + 4 + 1 + 0 + 5 = 19", font=FONT, font_size=28, color="#bbf7d0")
        sum_text.move_to(formula.get_center())
        self.play(Transform(formula, sum_text), run_time=0.55)
        self.wait(0.7)
        return VGroup(heading, chars, digits, formula)


class BigIntegerReverseStorageVisualization(BigIntegerIntroBase):
    """Explain why high precision arrays usually store digits in reverse order."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        title, subtitle = self.show_intro(
            "为什么常用反向存储",
            "让个位站到下标 0，循环就能像竖式一样从低位开始",
        )
        self.play(VGroup(title, subtitle).animate.to_edge(UP, buff=0.22).scale(0.68), run_time=0.75)

        vertical_group = self.show_vertical_addition()
        self.play(FadeOut(vertical_group), run_time=0.42)

        reverse_group = self.show_reverse_alignment()
        self.show_code_mapping(
            VGroup(title, subtitle, reverse_group),
            "倒序读入，倒序输出",
            [
                "vector<int> a;",
                "for (int i = s.size() - 1; i >= 0; i--)",
                "  a.push_back(s[i] - '0');",
                "",
                "// a[0]: ones, a[1]: tens",
                "for (int i = a.size() - 1; i >= 0; i--)",
                "  cout << a[i];",
            ],
            "第 i 个低位对应 a[i]",
            code_size=16,
        )

    def show_vertical_addition(self):
        heading = Text("竖式计算，总是从个位开始", font=FONT, font_size=34, color=WHITE)
        heading.move_to(UP * 1.95)

        top_number = Text("987", font=MONO_FONT, font_size=48, color=WHITE)
        bottom_number = Text("65", font=MONO_FONT, font_size=48, color=WHITE)
        bottom_number.next_to(top_number, DOWN, buff=0.06).align_to(top_number, RIGHT)
        plus = Text("+", font=MONO_FONT, font_size=48, color=WHITE)
        plus.next_to(bottom_number, LEFT, buff=0.28)
        line = Line(plus.get_left() + LEFT * 0.1, top_number.get_right() + RIGHT * 0.12, color=MUTED, stroke_width=3)
        line.next_to(bottom_number, DOWN, buff=0.08)
        result = Text("1052", font=MONO_FONT, font_size=48, color="#bbf7d0")
        result.next_to(line, DOWN, buff=0.04).align_to(top_number, RIGHT)
        vertical = VGroup(top_number, bottom_number, plus, line, result)
        vertical.move_to(LEFT * 2.5 + DOWN * 0.02)

        ones = RoundedRectangle(
            width=0.48,
            height=1.4,
            corner_radius=0.04,
            stroke_color="#fde68a",
            stroke_width=3,
            fill_opacity=0,
        )
        ones_x = top_number.get_right()[0] - 0.18
        ones_y = (top_number.get_center()[1] + bottom_number.get_center()[1]) / 2
        ones.move_to(RIGHT * ones_x + UP * ones_y)
        note = Text("先算个位：7 + 5，再把进位交给十位", font=FONT, font_size=28, color=MUTED)
        note.move_to(RIGHT * 1.75 + UP * 0.55)

        forward = self.make_digit_row("正向", [9, 8, 7], RIGHT * 1.95 + DOWN * 0.65, "个位在最右边", scale=0.72)
        awkward = Text("正向存储时：a[size-1-i]", font=FONT, font_size=24, color="#fed7aa")
        awkward.next_to(forward, DOWN, buff=0.35)

        self.play(FadeIn(heading, shift=UP * 0.14), FadeIn(vertical, shift=UP * 0.12), run_time=0.75)
        self.play(Create(ones), Write(note), run_time=0.65)
        self.play(FadeIn(forward, shift=UP * 0.12), FadeIn(awkward, shift=UP * 0.12), run_time=0.75)
        self.play(color_cell(forward.cells[2], WARN_FILL, WARN_STROKE), run_time=0.4)
        self.wait(0.75)
        return VGroup(heading, vertical, ones, note, forward, awkward)

    def show_reverse_alignment(self):
        heading = Text("反过来存：个位来到 a[0]", font=FONT, font_size=34, color=WHITE)
        heading.move_to(UP * 2.05)

        normal = self.make_digit_row("987", [9, 8, 7], LEFT * 2.65 + UP * 1.05, "正向看数字", scale=0.66)
        reverse = self.make_digit_row("a", [7, 8, 9], RIGHT * 2.4 + UP * 1.05, "反向数组", scale=0.66)
        arrow = Arrow(normal.get_right(), reverse.get_left(), buff=0.22, color=MUTED, stroke_width=3)
        flip = Text("倒着存", font=FONT, font_size=24, color=MUTED)
        flip.next_to(arrow, UP, buff=0.1)

        a_row = self.make_digit_row("a", [7, 8, 9], UP * -0.25, "987 -> [7,8,9]", scale=0.68)
        b_row = self.make_digit_row("b", [5, 6, 0], DOWN * 1.12, "65 -> [5,6]，缺位补 0", scale=0.68)
        b_row.cells[2][0].set_fill(CELL_FILL, opacity=0.35).set_stroke(CELL_STROKE, opacity=0.45)
        b_row.cells[2][1].set_opacity(0.42)

        rows = VGroup(a_row, b_row)
        pointer = make_pointer("i", POINTER_BLUE).scale(0.82)
        place_pointer(pointer, a_row.cells[0].get_center())
        formula = Text("i=0 对齐个位：7 和 5", font=FONT, font_size=28, color="#fef3c7")
        formula.move_to(DOWN * 2.35)

        self.play(FadeIn(heading, shift=UP * 0.14), FadeIn(normal, shift=UP * 0.12), run_time=0.6)
        self.play(GrowArrow(arrow), FadeIn(flip, shift=UP * 0.08), FadeIn(reverse, shift=UP * 0.12), run_time=0.75)
        self.play(FadeIn(rows, shift=UP * 0.14), FadeIn(pointer), FadeIn(formula), run_time=0.75)

        positions = [cell.get_center() for cell in a_row.cells]
        notes = [
            "i=0 对齐个位：7 和 5",
            "i=1 对齐十位：8 和 6",
            "i=2 对齐百位：9 和 0",
        ]
        for index, text in enumerate(notes):
            current = Text(text, font=FONT, font_size=28, color="#fef3c7" if index < 2 else "#bbf7d0")
            current.move_to(formula.get_center())
            self.play(
                pointer.animate.move_to(pointer_position(positions[index])),
                color_cell(a_row.cells[index], COMPARE_FILL, "#fde68a"),
                color_cell(b_row.cells[index], COMPARE_FILL, "#fde68a"),
                Transform(formula, current),
                run_time=0.42,
            )
            self.play(reset_cell(a_row.cells[index]), reset_cell(b_row.cells[index]), run_time=0.22)

        summary = Text("循环变量 i 从 0 开始，就像竖式从个位开始", font=FONT, font_size=28, color="#bbf7d0")
        summary.move_to(formula.get_center())
        self.play(Transform(formula, summary), FadeOut(pointer), run_time=0.55)
        self.wait(0.7)
        return VGroup(heading, normal, reverse, arrow, flip, rows, formula)
