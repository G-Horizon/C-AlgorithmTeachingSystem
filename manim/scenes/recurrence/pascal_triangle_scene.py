from pathlib import Path
import sys

from manim import *


COMMON_DIR = Path(__file__).resolve().parents[2] / "common"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from theme import BACKGROUND, CELL_FILL, CELL_STROKE, FONT, MONO_FONT, MUTED, POINTER_BLUE  # noqa: E402


BOUNDARY_COLOR = "#fbbf24"
SOURCE_COLOR = "#38bdf8"
TARGET_COLOR = "#34d399"
TRACE_COLOR = "#fef3c7"
CODE_FILL = "#111827"
FORMULA_FILL = "#172554"
FORMULA_STROKE = "#93c5fd"
DIM_FILL = "#1e293b"


PASCAL_VALUES = {
    1: [1],
    2: [1, 1],
    3: [1, 2, 1],
    4: [1, 3, 3, 1],
    5: [1, 4, 6, 4, 1],
    6: [1, 5, 10, 10, 5, 1],
}


class RecurrencePascalTriangleVisualization(Scene):
    """Visualize 2D recurrence through Pascal's triangle."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        title_group = self.show_intro()
        shape_group = self.show_state_shape(title_group)
        boundary_group = self.show_boundaries(title_group, shape_group)
        dependency_group = self.show_dependency(title_group, boundary_group)
        fill_group = self.show_row_fill(title_group, dependency_group)
        code_group = self.show_code_mapping(title_group, fill_group)
        self.show_summary(title_group, code_group)

    def show_intro(self):
        title = Text("递推算法：二维递推", font=FONT, weight="BOLD", font_size=46, color=WHITE)
        subtitle = Text("把一张表从上往下填满", font=FONT, font_size=27, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.22)
        title_group = VGroup(title, subtitle)

        self.play(FadeIn(title, shift=UP * 0.16), Write(subtitle), run_time=0.9)
        self.wait(0.25)
        self.play(title_group.animate.scale(0.66).to_edge(UP, buff=0.22), run_time=0.62)
        return title_group

    def show_state_shape(self, title_group):
        heading = Text("二维状态：每个格子都有行和列", font=FONT, font_size=31, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.36)

        triangle = self.make_pascal_triangle(mode="coord", rows=5, cell_width=0.88, cell_height=0.56, x_gap=0.08, y_gap=0.13)
        triangle.next_to(heading, DOWN, buff=0.42)

        note = Text("一维表是一条线，二维表是一片格子", font=FONT, font_size=25, color=MUTED)
        note.to_edge(DOWN, buff=0.34)

        self.play(FadeIn(heading, shift=UP * 0.1), run_time=0.42)
        for row in range(1, 6):
            row_group = VGroup(*[triangle.cells[(row, col)] for col in range(1, row + 1)])
            self.play(FadeIn(row_group, shift=UP * 0.08), run_time=0.26)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.38)
        self.wait(0.45)

        return VGroup(heading, triangle, note)

    def show_boundaries(self, title_group, shape_group):
        self.play(FadeOut(shape_group), run_time=0.45)

        heading = Text("先把边界条件放好", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.36)

        triangle = self.make_pascal_triangle(mode="boundary", rows=6, cell_width=0.72, cell_height=0.54, x_gap=0.08, y_gap=0.1)
        triangle.next_to(heading, DOWN, buff=0.36)

        note = Text("每一行两端固定为 1，不需要公式推", font=FONT, font_size=25, color=MUTED)
        note.to_edge(DOWN, buff=0.34)

        self.play(FadeIn(heading, shift=UP * 0.1), FadeIn(triangle, shift=UP * 0.08), run_time=0.62)
        for row in range(1, 7):
            targets = [triangle.cells[(row, 1)]]
            if row > 1:
                targets.append(triangle.cells[(row, row)])
            self.play(
                *[
                    cell.box.animate.set_fill("#78350f", opacity=1).set_stroke(BOUNDARY_COLOR, width=3.2)
                    for cell in targets
                ],
                run_time=0.18,
            )
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.36)
        self.wait(0.45)

        return VGroup(heading, triangle, note)

    def show_dependency(self, title_group, boundary_group):
        self.play(FadeOut(boundary_group), run_time=0.45)

        heading = Text("内部格：来自上一行的两个旧状态", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.36)

        triangle = self.make_pascal_triangle(mode="value", rows=6, cell_width=0.72, cell_height=0.54, x_gap=0.08, y_gap=0.1)
        triangle.next_to(heading, DOWN, buff=0.42).shift(LEFT * 2.35 + DOWN * 0.02)

        source_left = triangle.cells[(4, 2)]
        source_right = triangle.cells[(4, 3)]
        target = triangle.cells[(5, 3)]

        formula = self.make_formula_card(
            [
                "f[5][3]",
                "= f[4][2] + f[4][3]",
                "= 3 + 3 = 6",
            ],
            width=4.85,
            height=1.7,
        )
        formula.next_to(triangle, RIGHT, buff=0.58)

        left_arrow = Arrow(source_left.get_bottom(), target.get_top() + LEFT * 0.06, buff=0.08, color=SOURCE_COLOR, stroke_width=3)
        right_arrow = Arrow(source_right.get_bottom(), target.get_top() + RIGHT * 0.06, buff=0.08, color=SOURCE_COLOR, stroke_width=3)

        note = Text("当前格 = 左上方 + 右上方", font=FONT, font_size=25, color=MUTED)
        note.to_edge(DOWN, buff=0.34)

        self.play(FadeIn(heading, shift=UP * 0.1), FadeIn(triangle, shift=UP * 0.08), run_time=0.55)
        self.play(
            source_left.box.animate.set_fill("#075985", opacity=1).set_stroke(SOURCE_COLOR, width=3.2),
            source_right.box.animate.set_fill("#075985", opacity=1).set_stroke(SOURCE_COLOR, width=3.2),
            run_time=0.42,
        )
        self.play(
            target.box.animate.set_fill("#064e3b", opacity=1).set_stroke(TARGET_COLOR, width=3.4),
            Create(left_arrow),
            Create(right_arrow),
            FadeIn(formula, shift=LEFT * 0.12),
            run_time=0.7,
        )
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.36)
        self.wait(0.75)

        return VGroup(heading, triangle, formula, left_arrow, right_arrow, note)

    def show_row_fill(self, title_group, dependency_group):
        self.play(FadeOut(dependency_group), run_time=0.45)

        heading = Text("一行一行向下填表", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.36)

        triangle = self.make_pascal_triangle(mode="partial", rows=6, cell_width=0.72, cell_height=0.54, x_gap=0.08, y_gap=0.1)
        triangle.next_to(heading, DOWN, buff=0.36)

        formula = self.make_formula_card(["f[i][j] = f[i-1][j-1] + f[i-1][j]"], width=5.9, height=0.72)
        formula.to_edge(DOWN, buff=0.34)

        self.play(FadeIn(heading, shift=UP * 0.1), FadeIn(triangle, shift=UP * 0.08), FadeIn(formula), run_time=0.62)

        steps = [
            (4, 2, 1, 2, 3),
            (4, 3, 2, 1, 3),
            (5, 2, 1, 3, 4),
            (5, 3, 3, 3, 6),
            (5, 4, 3, 1, 4),
        ]
        for row, col, left_value, right_value, result in steps:
            source_left = triangle.cells[(row - 1, col - 1)]
            source_right = triangle.cells[(row - 1, col)]
            target = triangle.cells[(row, col)]

            calc = Text(
                f"f[{row}][{col}] = {left_value} + {right_value} = {result}",
                font=MONO_FONT,
                weight="BOLD",
                font_size=23,
                color=TRACE_COLOR,
            )
            calc.next_to(formula, UP, buff=0.16)

            left_arrow = Arrow(source_left.get_bottom(), target.get_top() + LEFT * 0.05, buff=0.08, color=SOURCE_COLOR, stroke_width=3)
            right_arrow = Arrow(source_right.get_bottom(), target.get_top() + RIGHT * 0.05, buff=0.08, color=SOURCE_COLOR, stroke_width=3)

            self.play(
                source_left.box.animate.set_fill("#075985", opacity=1).set_stroke(SOURCE_COLOR, width=3.0),
                source_right.box.animate.set_fill("#075985", opacity=1).set_stroke(SOURCE_COLOR, width=3.0),
                target.box.animate.set_fill("#064e3b", opacity=1).set_stroke(TARGET_COLOR, width=3.2),
                Create(left_arrow),
                Create(right_arrow),
                FadeIn(calc, shift=UP * 0.06),
                run_time=0.36,
            )
            self.play(Transform(target.label, self.make_cell_label(str(result), target.get_center(), 23, WHITE)), run_time=0.24)
            self.wait(0.04)
            self.play(
                source_left.box.animate.set_fill(self.base_fill(row - 1, col - 1), opacity=1).set_stroke(self.base_stroke(row - 1, col - 1), width=2.0),
                source_right.box.animate.set_fill(self.base_fill(row - 1, col), opacity=1).set_stroke(self.base_stroke(row - 1, col), width=2.0),
                target.box.animate.set_fill(CELL_FILL, opacity=1).set_stroke(CELL_STROKE, width=2.0),
                FadeOut(left_arrow),
                FadeOut(right_arrow),
                FadeOut(calc),
                run_time=0.28,
            )

        note = Text("上一行先算好，下一行才有来源", font=FONT, font_size=25, color=MUTED)
        note.next_to(formula, UP, buff=0.16)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.36)
        self.wait(0.55)

        return VGroup(heading, triangle, formula, note)

    def show_code_mapping(self, title_group, fill_group):
        self.play(FadeOut(fill_group), run_time=0.45)

        heading = Text("画面里的箭头，正好对应双重循环", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.36)

        triangle = self.make_pascal_triangle(mode="value", rows=5, cell_width=0.62, cell_height=0.46, x_gap=0.06, y_gap=0.08)
        triangle.next_to(heading, DOWN, buff=0.46).shift(LEFT * 3.0 + DOWN * 0.05)

        code = self.make_code_block(
            [
                "for (int i = 1; i <= n; i++) {",
                "    f[i][1] = f[i][i] = 1;",
                "    for (int j = 2; j < i; j++) {",
                "        f[i][j] = f[i-1][j-1] + f[i-1][j];",
                "    }",
                "}",
            ]
        )
        code.next_to(triangle, RIGHT, buff=0.64)

        self.play(FadeIn(heading, shift=UP * 0.1), run_time=0.36)
        self.play(FadeIn(triangle, shift=RIGHT * 0.1), FadeIn(code, shift=LEFT * 0.1), run_time=0.7)

        boundary_highlight = SurroundingRectangle(code.lines[1], color=BOUNDARY_COLOR, buff=0.07, stroke_width=2.8)
        self.play(Create(boundary_highlight), code.lines[1].animate.set_color(TRACE_COLOR), run_time=0.42)
        self.wait(0.14)

        formula_highlight = SurroundingRectangle(VGroup(code.lines[2], code.lines[3]), color=TARGET_COLOR, buff=0.07, stroke_width=2.8)
        self.play(
            Transform(boundary_highlight, formula_highlight),
            code.lines[2].animate.set_color(TRACE_COLOR),
            code.lines[3].animate.set_color(TRACE_COLOR),
            run_time=0.52,
        )

        note = Text("外层控制行，内层只填内部格", font=FONT, font_size=25, color=MUTED)
        note.to_edge(DOWN, buff=0.34)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.36)
        self.wait(0.75)

        return VGroup(heading, triangle, code, boundary_highlight, note)

    def show_summary(self, title_group, code_group):
        self.play(FadeOut(code_group), run_time=0.45)

        heading = Text("二维递推检查表", font=FONT, font_size=33, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.42)

        items = VGroup(
            self.make_summary_item("1", "边界先放 1"),
            self.make_summary_item("2", "内部看上一行两格"),
            self.make_summary_item("3", "按行向下填表"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        items.next_to(heading, DOWN, buff=0.55)

        self.play(FadeIn(heading, shift=UP * 0.1), run_time=0.36)
        self.play(LaggedStart(*[FadeIn(item, shift=RIGHT * 0.12) for item in items], lag_ratio=0.16), run_time=0.8)
        self.wait(2.0)

    def make_pascal_triangle(self, mode, rows, cell_width, cell_height, x_gap, y_gap):
        cells = {}
        row_groups = VGroup()
        y_step = cell_height + y_gap
        x_step = cell_width + x_gap

        for row in range(1, rows + 1):
            row_cells = VGroup()
            for col in range(1, row + 1):
                if mode == "coord":
                    label = f"f[{row}][{col}]"
                    font_size = 12
                elif mode == "value":
                    label = str(PASCAL_VALUES[row][col - 1])
                    font_size = 22
                elif mode == "boundary":
                    label = "1" if self.is_boundary(row, col) else ""
                    font_size = 22
                else:
                    label = self.partial_label(row, col)
                    font_size = 22

                cell = self.make_cell(label, cell_width, cell_height, font_size, row, col, mode)
                x = (col - (row + 1) / 2) * x_step
                y = -(row - 1) * y_step
                cell.move_to(RIGHT * x + UP * y)
                row_cells.add(cell)
                cells[(row, col)] = cell
            row_groups.add(row_cells)

        triangle = VGroup(*row_groups)
        triangle.cells = cells
        return triangle

    def make_cell(self, label, width, height, font_size, row, col, mode):
        is_boundary = self.is_boundary(row, col)
        fill = "#78350f" if mode in {"boundary", "partial", "value"} and is_boundary else CELL_FILL
        stroke = BOUNDARY_COLOR if mode in {"boundary", "partial", "value"} and is_boundary else CELL_STROKE
        text_color = BOUNDARY_COLOR if mode in {"boundary", "partial", "value"} and is_boundary else WHITE

        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.08,
            stroke_width=2.0,
            stroke_color=stroke,
            fill_color=fill,
            fill_opacity=1,
        )
        label_text = self.make_cell_label(label, box.get_center(), font_size, text_color)
        group = VGroup(box, label_text)
        group.box = box
        group.label = label_text
        return group

    def make_cell_label(self, text, center, font_size, color):
        visible_text = text if text else " "
        label = Text(visible_text, font=MONO_FONT, weight="BOLD", font_size=font_size, color=color)
        label.move_to(center)
        return label

    def make_formula_card(self, lines, width, height):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.08,
            stroke_width=2.4,
            stroke_color=FORMULA_STROKE,
            fill_color=FORMULA_FILL,
            fill_opacity=0.98,
        )
        line_group = VGroup(*[Text(line, font=MONO_FONT, weight="BOLD", font_size=22, color=WHITE) for line in lines])
        line_group.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        line_group.move_to(box.get_center())
        return VGroup(box, line_group)

    def make_code_block(self, lines):
        title = Text("二维递推写法", font=FONT, weight="BOLD", font_size=22, color=SOURCE_COLOR)
        code_lines = VGroup(*[Text(line, font=MONO_FONT, font_size=17, color=MUTED) for line in lines])
        code_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        content = VGroup(title, code_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        box = RoundedRectangle(
            width=6.25,
            height=3.1,
            corner_radius=0.08,
            stroke_width=2.2,
            stroke_color=SOURCE_COLOR,
            fill_color=CODE_FILL,
            fill_opacity=0.96,
        )
        content.move_to(box.get_center()).align_to(box, LEFT).shift(RIGHT * 0.3)
        group = VGroup(box, content)
        group.lines = code_lines
        return group

    def make_summary_item(self, number, text):
        dot = Circle(radius=0.2, stroke_width=0, fill_color=POINTER_BLUE, fill_opacity=1)
        number_text = Text(number, font=MONO_FONT, weight="BOLD", font_size=18, color=BACKGROUND)
        number_text.move_to(dot.get_center())
        label = Text(text, font=FONT, font_size=26, color=WHITE)
        return VGroup(VGroup(dot, number_text), label).arrange(RIGHT, buff=0.16)

    def partial_label(self, row, col):
        if self.is_boundary(row, col):
            return "1"
        if row <= 3:
            return str(PASCAL_VALUES[row][col - 1])
        return ""

    def is_boundary(self, row, col):
        return col == 1 or col == row

    def base_fill(self, row, col):
        return "#78350f" if self.is_boundary(row, col) else CELL_FILL

    def base_stroke(self, row, col):
        return BOUNDARY_COLOR if self.is_boundary(row, col) else CELL_STROKE

