from pathlib import Path
import sys

from manim import *


COMMON_DIR = Path(__file__).resolve().parents[2] / "common"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from theme import BACKGROUND, CELL_FILL, CELL_STROKE, FONT, MONO_FONT, MUTED, POINTER_BLUE  # noqa: E402


KNOWN_FILL = "#166534"
KNOWN_STROKE = "#86efac"
READY_FILL = "#075985"
READY_STROKE = "#7dd3fc"
ERROR_FILL = "#7f1d1d"
ERROR_STROKE = "#fca5a5"
WARN = "#fb7185"
CODE_FILL = "#111827"
CODE_STROKE = "#475569"
ACCENT = "#fbbf24"


class RecurrenceInitialBoundaryVisualization(Scene):
    """Show how initial values, loop starts, and array bounds make recurrence safe."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        title_group = self.show_intro()
        broken_group = self.show_missing_initial_values(title_group)
        boundary_group = self.show_out_of_bounds(title_group, broken_group)
        repaired_group = self.show_repair(title_group, boundary_group)
        code_group = self.show_code_mapping(title_group, repaired_group)
        self.show_boundary_checklist(title_group, code_group)

    def show_intro(self):
        title = Text("递推算法：初始条件与边界", font=FONT, weight="BOLD", font_size=48, color=WHITE)
        subtitle = Text("公式正确，还要让每一次读取都合法", font=FONT, font_size=27, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.22)
        group = VGroup(title, subtitle)

        self.play(FadeIn(title, shift=UP * 0.16), Write(subtitle), run_time=0.95)
        self.wait(0.32)
        self.play(group.animate.scale(0.66).to_edge(UP, buff=0.2), run_time=0.65)
        return group

    def show_missing_initial_values(self, title_group):
        heading = Text("只有递推式，状态链仍然无法启动", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.42)

        formula = self.make_formula("f[i] = f[i - 1] + f[i - 2]", READY_STROKE)
        formula.next_to(heading, DOWN, buff=0.34)
        row = self.make_state_row(["?", "?", "?", "?", "?", "?", "?"], fill=CELL_FILL, stroke=CELL_STROKE)
        row.next_to(formula, DOWN, buff=0.48)

        labels = VGroup(*[
            Text(f"f[{index}]", font=MONO_FONT, font_size=17, color=MUTED).next_to(cell, DOWN, buff=0.1)
            for index, cell in enumerate(row)
        ])
        arrows = VGroup(
            CurvedArrow(row[0].get_top(), row[2].get_top(), angle=-TAU / 7, color=WARN, stroke_width=3),
            CurvedArrow(row[1].get_top(), row[2].get_top(), angle=-TAU / 7, color=WARN, stroke_width=3),
        )
        note = Text("没有已知初值，f[2] 也只能得到问号", font=FONT, font_size=26, color=WARN)
        note.to_edge(DOWN, buff=0.38)

        self.play(FadeIn(heading, shift=UP * 0.1), FadeIn(formula, shift=UP * 0.08), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(cell, shift=UP * 0.08) for cell in row], lag_ratio=0.08), FadeIn(labels), run_time=0.8)
        self.play(Create(arrows), row[0][0].animate.set_fill(ERROR_FILL), row[1][0].animate.set_fill(ERROR_FILL), run_time=0.5)
        self.play(
            LaggedStart(*[cell[0].animate.set_fill(ERROR_FILL).set_stroke(ERROR_STROKE, width=2.8) for cell in row[2:]], lag_ratio=0.1),
            FadeIn(note, shift=UP * 0.08),
            run_time=0.9,
        )
        self.wait(0.42)
        return VGroup(heading, formula, row, labels, arrows, note)

    def show_out_of_bounds(self, title_group, broken_group):
        self.play(FadeOut(broken_group), run_time=0.42)

        heading = Text("先看依赖，再决定循环起点", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.42)

        code = self.make_code_card(
            [
                "for (int i = 1; i <= n; i++) {",
                "    f[i] = f[i - 1] + f[i - 2];",
                "}",
            ],
            "错误起点",
            ERROR_STROKE,
            6.4,
            2.05,
        )
        code.next_to(heading, DOWN, buff=0.34).shift(LEFT * 2.4)

        valid = self.make_cell("f[0]", CELL_FILL, CELL_STROKE, 1.65, 0.82, 24)
        current = self.make_cell("f[1]", READY_FILL, READY_STROKE, 1.65, 0.82, 24)
        invalid = self.make_cell("f[-1]", ERROR_FILL, ERROR_STROKE, 1.65, 0.82, 24)
        cells = VGroup(invalid, valid, current).arrange(RIGHT, buff=0.22)
        cells.next_to(code, RIGHT, buff=0.55).shift(DOWN * 0.05)
        boundary_line = DashedLine(
            (invalid.get_right() + valid.get_left()) / 2 + DOWN * 1.0,
            (invalid.get_right() + valid.get_left()) / 2 + UP * 1.0,
            color=WARN,
            stroke_width=2.5,
        )
        outside = Text("数组外", font=FONT, font_size=20, color=WARN).next_to(invalid, DOWN, buff=0.14)
        inside = Text("合法下标", font=FONT, font_size=20, color=MUTED).next_to(VGroup(valid, current), DOWN, buff=0.14)

        arrow_zero = Arrow(current.get_top(), valid.get_top(), path_arc=1.0, buff=0.12, color=POINTER_BLUE, stroke_width=3)
        arrow_negative = Arrow(current.get_bottom(), invalid.get_bottom(), path_arc=-1.0, buff=0.12, color=WARN, stroke_width=3)
        note = Text("i = 1 时，i - 2 = -1", font=MONO_FONT, weight="BOLD", font_size=29, color=WARN)
        note.to_edge(DOWN, buff=0.38)

        self.play(FadeIn(heading, shift=UP * 0.1), FadeIn(code, shift=RIGHT * 0.1), run_time=0.62)
        self.play(FadeIn(cells, shift=LEFT * 0.08), Create(boundary_line), FadeIn(outside), FadeIn(inside), run_time=0.65)
        self.play(Create(arrow_zero), Create(arrow_negative), FadeIn(note, shift=UP * 0.08), run_time=0.7)
        self.play(Indicate(invalid, color=ERROR_STROKE, scale_factor=1.08), run_time=0.55)
        self.wait(0.42)
        return VGroup(heading, code, cells, boundary_line, outside, inside, arrow_zero, arrow_negative, note)

    def show_repair(self, title_group, boundary_group):
        self.play(FadeOut(boundary_group), run_time=0.42)

        heading = Text("先点亮初值，再从第一个未知状态出发", font=FONT, font_size=31, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.42)
        row = self.make_state_row(["?", "?", "?", "?", "?", "?", "?"], fill=CELL_FILL, stroke=CELL_STROKE)
        row.next_to(heading, DOWN, buff=0.58)
        labels = VGroup(*[
            Text(f"f[{index}]", font=MONO_FONT, font_size=17, color=MUTED).next_to(cell, DOWN, buff=0.1)
            for index, cell in enumerate(row)
        ])

        steps = VGroup(
            self.make_badge("1", "写初值", KNOWN_STROKE),
            self.make_badge("2", "定起点 i = 2", ACCENT),
            self.make_badge("3", "向右递推", READY_STROKE),
        ).arrange(RIGHT, buff=0.28)
        steps.to_edge(DOWN, buff=0.3)

        self.play(FadeIn(heading, shift=UP * 0.08), FadeIn(row, shift=UP * 0.08), FadeIn(labels), run_time=0.68)
        self.play(FadeIn(steps[0], shift=RIGHT * 0.08), run_time=0.35)
        for index in (0, 1):
            self.play(self.set_cell(row[index], "1", KNOWN_FILL, KNOWN_STROKE), run_time=0.3)

        self.play(FadeIn(steps[1], shift=RIGHT * 0.08), run_time=0.35)
        values = [2, 3, 5, 8, 13]
        self.play(FadeIn(steps[2], shift=RIGHT * 0.08), run_time=0.35)
        for index, value in enumerate(values, start=2):
            left_arrow = CurvedArrow(row[index - 2].get_top(), row[index].get_top(), angle=-TAU / 8, color=POINTER_BLUE, stroke_width=2.8)
            right_arrow = CurvedArrow(row[index - 1].get_top(), row[index].get_top(), angle=-TAU / 8, color=ACCENT, stroke_width=2.8)
            self.play(Create(left_arrow), Create(right_arrow), run_time=0.2)
            self.play(self.set_cell(row[index], str(value), READY_FILL, READY_STROKE), run_time=0.25)
            self.play(FadeOut(left_arrow), FadeOut(right_arrow), run_time=0.16)

        self.wait(0.45)
        group = VGroup(heading, row, labels, steps)
        group.row = row
        return group

    def show_code_mapping(self, title_group, repaired_group):
        self.play(FadeOut(repaired_group), run_time=0.42)

        heading = Text("数组容量、初值、循环起点缺一不可", font=FONT, font_size=31, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.42)

        row = self.make_state_row(["1", "1", "2", "3", "5", "8", "13"], fill=READY_FILL, stroke=READY_STROKE)
        row[0][0].set_fill(KNOWN_FILL).set_stroke(KNOWN_STROKE)
        row[1][0].set_fill(KNOWN_FILL).set_stroke(KNOWN_STROKE)
        row.scale(0.58).to_edge(LEFT, buff=0.52).shift(DOWN * 0.12)
        labels = VGroup(*[
            Text(f"f[{index}]", font=MONO_FONT, font_size=15, color=MUTED).next_to(cell, DOWN, buff=0.08)
            for index, cell in enumerate(row)
        ])

        code = self.make_code_card(
            [
                "vector<long long> f(n + 2, 0);",
                "f[0] = 1;",
                "f[1] = 1;",
                "for (int i = 2; i <= n; i++)",
                "    f[i] = f[i-1] + f[i-2];",
                "cout << f[n];",
            ],
            "安全递推",
            READY_STROKE,
            7.1,
            3.55,
        )
        code.to_edge(RIGHT, buff=0.48).shift(DOWN * 0.12)

        notes = VGroup(
            Text("① 留出合法下标", font=FONT, font_size=21, color=MUTED),
            Text("② 最小状态先已知", font=FONT, font_size=21, color=KNOWN_STROKE),
            Text("③ 从第一个未知状态开始", font=FONT, font_size=21, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        notes.next_to(row, DOWN, buff=0.42, aligned_edge=LEFT)

        self.play(FadeIn(heading, shift=UP * 0.08), FadeIn(row, shift=RIGHT * 0.08), FadeIn(labels), FadeIn(code, shift=LEFT * 0.08), run_time=0.72)
        for index, note in enumerate(notes):
            line_group = code.lines[0:1] if index == 0 else code.lines[1:3] if index == 1 else code.lines[3:5]
            highlight = SurroundingRectangle(line_group, color=[READY_STROKE, KNOWN_STROKE, ACCENT][index], buff=0.06, stroke_width=2.5)
            self.play(FadeIn(note, shift=RIGHT * 0.06), Create(highlight), run_time=0.42)
            self.wait(0.12)
            self.play(FadeOut(highlight), run_time=0.2)

        self.wait(0.42)
        return VGroup(heading, row, labels, code, notes)

    def show_boundary_checklist(self, title_group, code_group):
        self.play(FadeOut(code_group), run_time=0.42)

        heading = Text("最后用极小输入做边界体检", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.42)
        cases = VGroup(
            self.make_case("n = 0", "1"),
            self.make_case("n = 1", "1"),
            self.make_case("n = 2", "2"),
        ).arrange(RIGHT, buff=0.4)
        cases.next_to(heading, DOWN, buff=0.42)

        checklist = VGroup(
            self.make_check("状态定义覆盖最小输入"),
            self.make_check("每个依赖下标都存在"),
            self.make_check("循环从第一个未知状态开始"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        checklist.next_to(cases, DOWN, buff=0.5)

        footer = Text("先定义  →  再初始化  →  最后递推", font=FONT, weight="BOLD", font_size=29, color=ACCENT)
        footer.to_edge(DOWN, buff=0.28)

        self.play(FadeIn(heading, shift=UP * 0.08), run_time=0.35)
        self.play(LaggedStart(*[FadeIn(case, shift=UP * 0.08) for case in cases], lag_ratio=0.14), run_time=0.72)
        self.play(LaggedStart(*[FadeIn(item, shift=RIGHT * 0.08) for item in checklist], lag_ratio=0.14), run_time=0.8)
        self.play(FadeIn(footer, shift=UP * 0.08), run_time=0.42)
        self.wait(1.8)

    def make_state_row(self, values, fill, stroke):
        return VGroup(*[self.make_cell(value, fill, stroke, 1.36, 0.84, 25) for value in values]).arrange(RIGHT, buff=0.16)

    def make_cell(self, text, fill, stroke, width, height, font_size):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.09,
            stroke_width=2.3,
            stroke_color=stroke,
            fill_color=fill,
            fill_opacity=1,
        )
        label = Text(text, font=MONO_FONT, weight="BOLD", font_size=font_size, color=WHITE)
        label.move_to(box.get_center())
        return VGroup(box, label)

    def set_cell(self, cell, value, fill, stroke):
        label = Text(value, font=MONO_FONT, weight="BOLD", font_size=25, color=WHITE).move_to(cell[1])
        return AnimationGroup(
            cell[0].animate.set_fill(fill, opacity=1).set_stroke(stroke, width=3),
            Transform(cell[1], label),
        )

    def make_formula(self, text, stroke):
        box = RoundedRectangle(
            width=6.8,
            height=0.9,
            corner_radius=0.08,
            stroke_width=2.4,
            stroke_color=stroke,
            fill_color=CODE_FILL,
            fill_opacity=0.96,
        )
        label = Text(text, font=MONO_FONT, weight="BOLD", font_size=26, color=WHITE).move_to(box)
        return VGroup(box, label)

    def make_badge(self, number, text, color):
        circle = Circle(radius=0.22, stroke_width=0, fill_color=color, fill_opacity=1)
        digit = Text(number, font=MONO_FONT, weight="BOLD", font_size=18, color=BACKGROUND).move_to(circle)
        label = Text(text, font=FONT, font_size=23, color=WHITE)
        return VGroup(VGroup(circle, digit), label).arrange(RIGHT, buff=0.13)

    def make_code_card(self, lines, title, stroke, width, height):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.1,
            stroke_width=2.3,
            stroke_color=stroke,
            fill_color=CODE_FILL,
            fill_opacity=0.97,
        )
        heading = Text(title, font=FONT, weight="BOLD", font_size=21, color=stroke)
        code_lines = VGroup(*[Text(line, font=MONO_FONT, font_size=18, color=MUTED) for line in lines])
        code_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        content = VGroup(heading, code_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        content.move_to(box.get_center())
        group = VGroup(box, content)
        group.lines = code_lines
        return group

    def make_case(self, input_text, output_text):
        box = RoundedRectangle(
            width=2.65,
            height=1.22,
            corner_radius=0.1,
            stroke_width=2.3,
            stroke_color=KNOWN_STROKE,
            fill_color=KNOWN_FILL,
            fill_opacity=0.95,
        )
        input_label = Text(input_text, font=MONO_FONT, font_size=22, color=MUTED)
        output_label = Text(f"答案 {output_text}", font=FONT, weight="BOLD", font_size=24, color=WHITE)
        content = VGroup(input_label, output_label).arrange(DOWN, buff=0.08).move_to(box)
        return VGroup(box, content)

    def make_check(self, text):
        dot = Circle(radius=0.17, stroke_width=0, fill_color=KNOWN_STROKE, fill_opacity=1)
        mark = Text("✓", font=FONT, weight="BOLD", font_size=17, color=BACKGROUND).move_to(dot)
        label = Text(text, font=FONT, font_size=25, color=WHITE)
        return VGroup(VGroup(dot, mark), label).arrange(RIGHT, buff=0.15)
