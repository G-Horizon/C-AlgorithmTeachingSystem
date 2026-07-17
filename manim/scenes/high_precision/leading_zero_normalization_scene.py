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


ACCENT = "#22c55e"
ACCENT_STROKE = "#bbf7d0"
WARN_FILL = "#7c2d12"
WARN_STROKE = "#fed7aa"
STRING_FILL = "#0f766e"
STRING_STROKE = "#5eead4"


class LeadingZeroNormalizationVisualization(Scene):
    """Visualize trimming redundant leading zeros in high precision results."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        title, subtitle = self.show_intro()
        self.play(VGroup(title, subtitle).animate.to_edge(UP, buff=0.22).scale(0.68), run_time=0.75)

        rule_card = self.show_core_rule()
        self.play(FadeOut(rule_card), run_time=0.4)

        array_group = self.show_reversed_array_case()
        zero_group = self.show_zero_edge_case()
        visible_context = self.compress_top_cases(array_group, zero_group)
        string_group = self.show_string_case()

        scene_group = VGroup(visible_context, string_group, title, subtitle)
        self.show_code_mapping(scene_group)

    def show_intro(self):
        title = Text("前导零与边界整理  Normalize", font=FONT, weight="BOLD", font_size=46, color=WHITE)
        subtitle = Text(
            "高精度函数算完以后，最后一步不是输出，而是把结果整理成唯一、干净的表示",
            font=FONT,
            font_size=27,
            color=MUTED,
        )
        subtitle.next_to(title, DOWN, buff=0.24)
        self.play(FadeIn(title, shift=UP * 0.18), Write(subtitle), run_time=1.05)
        self.wait(0.45)
        return title, subtitle

    def show_core_rule(self):
        headline = Text("多余的最高位 0 要删掉，但数字 0 自己必须留下", font=FONT, font_size=36, color=WHITE)
        headline.move_to(UP * 1.35)

        good = self.make_label_box("00123  ->  123", "#14532d", "#86efac", 4.1, 0.75)
        keep_zero = self.make_label_box("0000  ->  0", "#312e81", "#a5b4fc", 3.3, 0.75)
        boxes = VGroup(good, keep_zero).arrange(RIGHT, buff=0.55)
        boxes.next_to(headline, DOWN, buff=0.52)

        note = Text("这一步会反复出现在减法、乘法、除法的收尾处", font=FONT, font_size=29, color="#fef3c7")
        note.next_to(boxes, DOWN, buff=0.5)

        group = VGroup(headline, boxes, note)
        self.play(FadeIn(headline, shift=UP * 0.15), run_time=0.55)
        self.play(LaggedStart(FadeIn(good, shift=UP * 0.12), FadeIn(keep_zero, shift=UP * 0.12), lag_ratio=0.18), run_time=0.75)
        self.play(Write(note), run_time=0.55)
        self.wait(0.75)
        return group

    def show_reversed_array_case(self):
        heading = Text("倒序数组：最高位在 back()", font=FONT, font_size=28, color=WHITE)
        heading.to_edge(LEFT, buff=0.7).shift(UP * 2.25)

        row = self.make_digit_row("c", [1, 0, 0, 0], LEFT * 2.05 + UP * 1.25, "raw: [1, 0, 0, 0]")
        formula = Text("while (c.size() > 1 && c.back() == 0)", font=MONO_FONT, font_size=23, color="#bae6fd")
        formula.next_to(row, DOWN, buff=0.5, aligned_edge=LEFT)

        status = Text("从最高位开始看：最后一个 0 不属于数值本身", font=FONT, font_size=25, color=MUTED)
        status.next_to(formula, DOWN, buff=0.22, aligned_edge=LEFT)

        self.play(FadeIn(heading, shift=UP * 0.12), FadeIn(row, shift=UP * 0.14), run_time=0.75)
        self.play(FadeIn(formula), Write(status), run_time=0.65)

        for remove_index in [3, 2, 1]:
            active_cell = row.cells[remove_index]
            msg = Text(f"c.back() 是 0，且长度 > 1：pop_back()", font=FONT, font_size=25, color="#fed7aa")
            msg.move_to(status.get_center())
            self.play(color_cell(active_cell, WARN_FILL, WARN_STROKE), Transform(status, msg), run_time=0.42)
            self.play(active_cell.animate.shift(UP * 0.28).set_opacity(0.0), run_time=0.34)

        normalized = self.make_digit_row("c", [1], row.get_center(), "normalized: [1]")
        normalized.shift(LEFT * 0.72)
        result = Text("倒序输出：1", font=FONT, font_size=27, color=ACCENT_STROKE)
        result.next_to(status, DOWN, buff=0.24, aligned_edge=LEFT)
        done = Text("留下的 [1] 才是规范结果", font=FONT, font_size=25, color=ACCENT_STROKE)
        done.move_to(status.get_center())

        self.play(Transform(row, normalized), Transform(status, done), FadeIn(result, shift=UP * 0.12), run_time=0.65)
        self.wait(0.35)
        return VGroup(heading, row, formula, status, result)

    def show_zero_edge_case(self):
        heading = Text("边界：全是 0 也不能删空", font=FONT, font_size=28, color=WHITE)
        heading.to_edge(RIGHT, buff=0.72).shift(UP * 2.25)

        row = self.make_digit_row("c", [0, 0, 0], RIGHT * 3.0 + UP * 1.25, "raw: [0, 0, 0]")
        guard = Text("size > 1 保护最后一个 0", font=FONT, font_size=25, color="#fef3c7")
        guard.next_to(row, DOWN, buff=0.48, aligned_edge=LEFT)
        self.play(FadeIn(heading, shift=UP * 0.12), FadeIn(row, shift=UP * 0.14), FadeIn(guard), run_time=0.75)

        for remove_index in [2, 1]:
            active_cell = row.cells[remove_index]
            self.play(color_cell(active_cell, COMPARE_FILL, "#fde68a"), run_time=0.25)
            self.play(active_cell.animate.shift(UP * 0.25).set_opacity(0.0), run_time=0.28)

        last_note = Text("现在 size == 1，停止：答案就是 0", font=FONT, font_size=25, color=ACCENT_STROKE)
        last_note.move_to(guard.get_center())
        self.play(mark_sorted(row.cells[0]), Transform(guard, last_note), run_time=0.5)
        self.wait(0.35)
        return VGroup(heading, row, guard)

    def show_string_case(self):
        heading = Text("除法商字符串：从左侧跳过 0", font=FONT, font_size=28, color=WHITE)
        heading.move_to(DOWN * 0.68)

        chars = list("0008230")
        row = self.make_char_row("q", chars, DOWN * 1.55, 'raw: "0008230"')
        status = Text("start 指针向右走，直到最后一个 0 之前停止", font=FONT, font_size=25, color=MUTED)
        status.next_to(row, DOWN, buff=0.38)

        self.play(FadeIn(heading, shift=UP * 0.12), FadeIn(row, shift=UP * 0.12), Write(status), run_time=0.8)

        for index in [0, 1, 2]:
            msg = Text(f"q[{index}] 是前导 0：start++", font=FONT, font_size=25, color="#fed7aa")
            msg.move_to(status.get_center())
            self.play(color_cell(row.cells[index], WARN_FILL, WARN_STROKE), Transform(status, msg), run_time=0.35)
            self.play(row.cells[index].animate.set_opacity(0.22), run_time=0.25)

        for index in [3, 4, 5, 6]:
            self.play(mark_sorted(row.cells[index]), run_time=0.08)

        answer = Text('q.substr(start) = "8230"', font=FONT, font_size=27, color=ACCENT_STROKE)
        answer.next_to(status, DOWN, buff=0.22)
        edge = Text('"0000" 也会留下最后一个 "0"', font=FONT, font_size=24, color="#bae6fd")
        edge.next_to(answer, DOWN, buff=0.18)
        done = Text("字符串版本和数组版本，本质都是“保留一个 0”", font=FONT, font_size=25, color=ACCENT_STROKE)
        done.move_to(status.get_center())
        self.play(Transform(status, done), FadeIn(answer, shift=UP * 0.12), FadeIn(edge, shift=UP * 0.12), run_time=0.65)
        self.wait(0.5)
        return VGroup(heading, row, status, answer, edge)

    def compress_top_cases(self, array_group, zero_group):
        details = VGroup(array_group[2], array_group[3], array_group[4], zero_group[2])
        visible = VGroup(array_group[0], array_group[1], zero_group[0], zero_group[1])
        self.play(FadeOut(details), run_time=0.35)
        self.play(visible.animate.scale(0.72).shift(UP * 0.16), run_time=0.5)
        return visible

    def show_code_mapping(self, scene_group):
        self.play(scene_group.animate.scale(0.47).to_edge(LEFT, buff=0.15).shift(UP * 0.02), run_time=0.75)

        title = Text("规范化函数", font=FONT, font_size=25, color=WHITE)
        code_lines = [
            "void normalize(vector<int>& c) {",
            "  while (c.size() > 1",
            "      && c.back() == 0)",
            "    c.pop_back();",
            "}",
            "",
            "string trim(const string& q) {",
            "  int i = 0;",
            "  while (i + 1 < q.size()",
            "      && q[i] == '0') i++;",
            "  return q.substr(i);",
            "}",
        ]
        code = Text("\n".join(code_lines), font=MONO_FONT, font_size=15, color=MUTED, line_spacing=0.82)
        code_group = VGroup(title, code).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        code_group.to_edge(RIGHT, buff=0.42).shift(DOWN * 0.05)

        self.play(FadeIn(title, shift=LEFT * 0.2), run_time=0.35)
        self.play(FadeIn(code, shift=UP * 0.12), run_time=0.75)

        summary = Text("收尾先规范，再输出", font=FONT, font_size=18, color=WHITE)
        summary.next_to(code_group, DOWN, buff=0.14, aligned_edge=LEFT)
        self.play(FadeIn(summary, shift=UP * 0.12), run_time=0.6)
        self.wait(2.0)

    def make_label_box(self, text, fill, stroke, width, height):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.1,
            stroke_width=2.5,
            stroke_color=stroke,
            fill_color=fill,
            fill_opacity=1,
        )
        label = Text(text, font=MONO_FONT, font_size=30, color=WHITE)
        label.move_to(box.get_center())
        return VGroup(box, label)

    def make_digit_row(self, name, values, offset, caption):
        cells = [make_array_cell(value).scale(0.72) for value in values]
        cells_group = VGroup(*cells).arrange(RIGHT, buff=0.09).move_to(offset)
        indexes = make_indices([cell.get_center() for cell in cells])
        indexes.scale(0.72)
        indexes.shift(UP * 0.12)

        label = Text(name, font=MONO_FONT, font_size=26, color=WHITE)
        caption_text = Text(caption, font=FONT, font_size=16, color=MUTED)
        label_group = VGroup(label, caption_text).arrange(DOWN, buff=0.08)
        label_group.next_to(cells_group, LEFT, buff=0.24)

        row = VGroup(label_group, cells_group, indexes)
        row.cells = cells
        return row

    def make_char_row(self, name, values, offset, caption):
        cells = []
        for value in values:
            box = RoundedRectangle(
                width=0.74,
                height=0.74,
                corner_radius=0.08,
                stroke_width=2.4,
                stroke_color=STRING_STROKE,
                fill_color=STRING_FILL,
                fill_opacity=1,
            )
            char = Text(value, font=MONO_FONT, weight="BOLD", font_size=28, color=WHITE)
            char.move_to(box.get_center())
            cells.append(VGroup(box, char))

        cells_group = VGroup(*cells).arrange(RIGHT, buff=0.07).move_to(offset)
        indexes = make_indices([cell.get_center() for cell in cells])
        indexes.scale(0.66)
        indexes.shift(UP * 0.22)

        label = Text(name, font=MONO_FONT, font_size=26, color=WHITE)
        caption_text = Text(caption, font=FONT, font_size=16, color=MUTED)
        label_group = VGroup(label, caption_text).arrange(DOWN, buff=0.08)
        label_group.next_to(cells_group, LEFT, buff=0.24)

        row = VGroup(label_group, cells_group, indexes)
        row.cells = cells
        return row
