from pathlib import Path
import sys

from manim import *


COMMON_DIR = Path(__file__).resolve().parents[2] / "common"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from theme import BACKGROUND, CELL_FILL, CELL_STROKE, FONT, MONO_FONT, MUTED, POINTER_BLUE  # noqa: E402


BOTTOM_COLOR = "#fbbf24"
SOURCE_COLOR = "#38bdf8"
RIGHT_SOURCE_COLOR = "#a78bfa"
TARGET_COLOR = "#34d399"
TRACE_COLOR = "#fef3c7"
CODE_FILL = "#111827"
FORMULA_FILL = "#172554"
FORMULA_STROKE = "#93c5fd"
PATH_COLOR = "#fb7185"
DP_FILL = "#064e3b"
BOTTOM_FILL = "#78350f"


TOWER_VALUES = {
    1: [7],
    2: [3, 8],
    3: [8, 1, 0],
    4: [2, 7, 4, 4],
    5: [4, 5, 2, 6, 5],
}

DP_VALUES = {
    1: [30],
    2: [23, 21],
    3: [20, 13, 10],
    4: [7, 12, 10, 10],
    5: [4, 5, 2, 6, 5],
}


class RecurrenceNumberTowerVisualization(Scene):
    """Visualize bottom-up max path recurrence on a number tower."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        title_group = self.show_intro()
        rule_group = self.show_path_rule(title_group)
        state_group = self.show_state_definition(title_group, rule_group)
        dependency_group = self.show_dependency(title_group, state_group)
        fill_group = self.show_bottom_up_fill(title_group, dependency_group)
        code_group = self.show_code_mapping(title_group, fill_group)
        self.show_summary(title_group, code_group)

    def show_intro(self):
        title = Text("递推算法：数塔递推", font=FONT, weight="BOLD", font_size=46, color=WHITE)
        subtitle = Text("从底层答案推回顶端", font=FONT, font_size=27, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.22)
        title_group = VGroup(title, subtitle)

        self.play(FadeIn(title, shift=UP * 0.16), Write(subtitle), run_time=0.9)
        self.wait(0.25)
        self.play(title_group.animate.scale(0.66).to_edge(UP, buff=0.22), run_time=0.62)
        return title_group

    def show_path_rule(self, title_group):
        heading = Text("每一步只能走向左下或右下", font=FONT, font_size=31, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.36)

        tower = self.make_tower(mode="raw", rows=5, cell_width=0.76, cell_height=0.54, x_gap=0.12, y_gap=0.14)
        tower.next_to(heading, DOWN, buff=0.44)

        start = tower.cells[(1, 1)]
        left_child = tower.cells[(2, 1)]
        right_child = tower.cells[(2, 2)]
        left_arrow = Arrow(start.get_bottom(), left_child.get_top(), buff=0.08, color=SOURCE_COLOR, stroke_width=3.3)
        right_arrow = Arrow(start.get_bottom(), right_child.get_top(), buff=0.08, color=RIGHT_SOURCE_COLOR, stroke_width=3.3)

        note = Text("路径会一路向下，不能回头", font=FONT, font_size=25, color=MUTED)
        note.to_edge(DOWN, buff=0.34)

        self.play(FadeIn(heading, shift=UP * 0.1), FadeIn(tower, shift=UP * 0.08), run_time=0.64)
        self.play(
            start.box.animate.set_fill("#4c1d95", opacity=1).set_stroke(PATH_COLOR, width=3.2),
            Create(left_arrow),
            Create(right_arrow),
            run_time=0.55,
        )
        self.play(
            left_child.box.animate.set_fill("#075985", opacity=1).set_stroke(SOURCE_COLOR, width=3.0),
            right_child.box.animate.set_fill("#4c1d95", opacity=1).set_stroke(RIGHT_SOURCE_COLOR, width=3.0),
            FadeIn(note, shift=UP * 0.08),
            run_time=0.45,
        )
        self.wait(0.55)

        return VGroup(heading, tower, left_arrow, right_arrow, note)

    def show_state_definition(self, title_group, rule_group):
        self.play(FadeOut(rule_group), run_time=0.45)

        heading = Text("换个方向：先让底层成为已知状态", font=FONT, font_size=31, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.36)

        tower = self.make_tower(mode="bottom", rows=5, cell_width=0.74, cell_height=0.54, x_gap=0.12, y_gap=0.12)
        tower.next_to(heading, DOWN, buff=0.42).shift(LEFT * 2.55)

        formula = self.make_formula_card(
            [
                "f[i][j]",
                "从 a[i][j]",
                "走到底的最大和",
            ],
            width=4.8,
            height=1.75,
        )
        formula.next_to(tower, RIGHT, buff=0.68)

        note = Text("站在底层时，没有下一步：f[n][j] = a[n][j]", font=FONT, font_size=25, color=MUTED)
        note.to_edge(DOWN, buff=0.34)

        self.play(FadeIn(heading, shift=UP * 0.1), FadeIn(tower, shift=UP * 0.08), run_time=0.62)
        self.play(FadeIn(formula, shift=LEFT * 0.12), run_time=0.45)

        for col in range(1, 6):
            cell = tower.cells[(5, col)]
            self.play(
                cell.box.animate.set_fill(BOTTOM_FILL, opacity=1).set_stroke(BOTTOM_COLOR, width=3.1),
                cell.label.animate.set_color(BOTTOM_COLOR),
                run_time=0.16,
            )

        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.36)
        self.wait(0.5)

        return VGroup(heading, tower, formula, note)

    def show_dependency(self, title_group, state_group):
        self.play(FadeOut(state_group), run_time=0.45)

        heading = Text("当前格 = 自己 + 下面两格里的较大者", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.36)

        tower = self.make_tower(mode="dependency", rows=5, cell_width=0.74, cell_height=0.54, x_gap=0.12, y_gap=0.12)
        tower.next_to(heading, DOWN, buff=0.42).shift(LEFT * 2.45)

        target = tower.cells[(4, 2)]
        left_source = tower.cells[(5, 2)]
        right_source = tower.cells[(5, 3)]

        formula = self.make_formula_card(
            [
                "f[4][2]",
                "= 7 + max(5, 2)",
                "= 12",
            ],
            width=5.0,
            height=1.7,
        )
        formula.next_to(tower, RIGHT, buff=0.62)

        left_arrow = Arrow(left_source.get_top(), target.get_bottom() + LEFT * 0.05, buff=0.08, color=SOURCE_COLOR, stroke_width=3)
        right_arrow = Arrow(right_source.get_top(), target.get_bottom() + RIGHT * 0.05, buff=0.08, color=RIGHT_SOURCE_COLOR, stroke_width=3)

        note = Text("选择的是后续最大和，不是只看下一格数字", font=FONT, font_size=25, color=MUTED)
        note.to_edge(DOWN, buff=0.34)

        self.play(FadeIn(heading, shift=UP * 0.1), FadeIn(tower, shift=UP * 0.08), run_time=0.55)
        self.play(
            left_source.box.animate.set_fill("#075985", opacity=1).set_stroke(SOURCE_COLOR, width=3.2),
            right_source.box.animate.set_fill("#4c1d95", opacity=1).set_stroke(RIGHT_SOURCE_COLOR, width=3.2),
            run_time=0.42,
        )
        self.play(
            target.box.animate.set_fill(DP_FILL, opacity=1).set_stroke(TARGET_COLOR, width=3.4),
            Create(left_arrow),
            Create(right_arrow),
            FadeIn(formula, shift=LEFT * 0.12),
            run_time=0.7,
        )
        self.play(Transform(target.label, self.make_cell_label("12", target.get_center(), 23, WHITE)), run_time=0.25)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.36)
        self.wait(0.75)

        return VGroup(heading, tower, formula, left_arrow, right_arrow, note)

    def show_bottom_up_fill(self, title_group, dependency_group):
        self.play(FadeOut(dependency_group), run_time=0.45)

        heading = Text("自底向上：每一层都依赖下一层", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.36)

        tower = self.make_tower(mode="fill", rows=5, cell_width=0.74, cell_height=0.54, x_gap=0.12, y_gap=0.11)
        tower.next_to(heading, DOWN, buff=0.38)

        formula = self.make_formula_card(["f[i][j] = a[i][j] + max(f[i+1][j], f[i+1][j+1])"], width=7.4, height=0.72)
        formula.to_edge(DOWN, buff=0.34)

        self.play(FadeIn(heading, shift=UP * 0.1), FadeIn(tower, shift=UP * 0.08), FadeIn(formula), run_time=0.62)

        filled_positions = {(5, col) for col in range(1, 6)}
        steps = [
            (4, 1, 2, 4, 5, 7),
            (4, 2, 7, 5, 2, 12),
            (4, 3, 4, 2, 6, 10),
            (4, 4, 4, 6, 5, 10),
            (3, 1, 8, 7, 12, 20),
            (3, 2, 1, 12, 10, 13),
            (3, 3, 0, 10, 10, 10),
            (2, 1, 3, 20, 13, 23),
            (2, 2, 8, 13, 10, 21),
            (1, 1, 7, 23, 21, 30),
        ]

        for row, col, raw_value, left_value, right_value, result in steps:
            left_source = tower.cells[(row + 1, col)]
            right_source = tower.cells[(row + 1, col + 1)]
            target = tower.cells[(row, col)]

            calc = Text(
                f"f[{row}][{col}] = {raw_value} + max({left_value}, {right_value}) = {result}",
                font=MONO_FONT,
                weight="BOLD",
                font_size=21,
                color=TRACE_COLOR,
            )
            calc.next_to(formula, UP, buff=0.14)

            left_arrow = Arrow(left_source.get_top(), target.get_bottom() + LEFT * 0.05, buff=0.08, color=SOURCE_COLOR, stroke_width=2.8)
            right_arrow = Arrow(right_source.get_top(), target.get_bottom() + RIGHT * 0.05, buff=0.08, color=RIGHT_SOURCE_COLOR, stroke_width=2.8)

            self.play(
                left_source.box.animate.set_fill("#075985", opacity=1).set_stroke(SOURCE_COLOR, width=3.0),
                right_source.box.animate.set_fill("#4c1d95", opacity=1).set_stroke(RIGHT_SOURCE_COLOR, width=3.0),
                target.box.animate.set_fill(DP_FILL, opacity=1).set_stroke(TARGET_COLOR, width=3.2),
                Create(left_arrow),
                Create(right_arrow),
                FadeIn(calc, shift=UP * 0.06),
                run_time=0.3,
            )
            self.play(Transform(target.label, self.make_cell_label(str(result), target.get_center(), 23, WHITE)), run_time=0.2)
            filled_positions.add((row, col))
            self.wait(0.02)
            self.play(
                left_source.box.animate.set_fill(self.fill_base_color(row + 1, col, filled_positions), opacity=1).set_stroke(self.fill_base_stroke(row + 1, col, filled_positions), width=2.0),
                right_source.box.animate.set_fill(self.fill_base_color(row + 1, col + 1, filled_positions), opacity=1).set_stroke(self.fill_base_stroke(row + 1, col + 1, filled_positions), width=2.0),
                target.box.animate.set_fill(self.fill_base_color(row, col, filled_positions), opacity=1).set_stroke(self.fill_base_stroke(row, col, filled_positions), width=2.0),
                FadeOut(left_arrow),
                FadeOut(right_arrow),
                FadeOut(calc),
                run_time=0.24,
            )

        note = Text("下面一层算好，上面一层才有可靠来源", font=FONT, font_size=25, color=MUTED)
        note.next_to(formula, UP, buff=0.16)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.36)
        self.wait(0.55)

        return VGroup(heading, tower, formula, note)

    def show_code_mapping(self, title_group, fill_group):
        self.play(FadeOut(fill_group), run_time=0.45)

        heading = Text("顶端 f[1][1] 汇总出最大路径和", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.36)

        tower = self.make_tower(mode="dp", rows=5, cell_width=0.58, cell_height=0.44, x_gap=0.08, y_gap=0.08)
        tower.next_to(heading, DOWN, buff=0.48).shift(LEFT * 3.0 + DOWN * 0.05)

        answer = tower.cells[(1, 1)]
        answer_ring = SurroundingRectangle(answer, color=TARGET_COLOR, buff=0.05, stroke_width=3.2)
        answer_text = Text("答案 30", font=FONT, weight="BOLD", font_size=25, color=TARGET_COLOR)
        answer_text.next_to(tower, DOWN, buff=0.22)

        code = self.make_code_block(
            [
                "for (int j = 1; j <= n; j++)",
                "    f[n][j] = a[n][j];",
                "",
                "for (int i = n - 1; i >= 1; i--) {",
                "    for (int j = 1; j <= i; j++) {",
                "        f[i][j] = a[i][j]",
                "          + max(f[i+1][j], f[i+1][j+1]);",
                "    }",
                "}",
            ]
        )
        code.next_to(tower, RIGHT, buff=0.62).align_to(tower, UP).shift(DOWN * 0.06)

        self.play(FadeIn(heading, shift=UP * 0.1), run_time=0.36)
        self.play(FadeIn(tower, shift=RIGHT * 0.1), FadeIn(code, shift=LEFT * 0.1), run_time=0.7)
        self.play(Create(answer_ring), FadeIn(answer_text, shift=UP * 0.08), run_time=0.45)

        bottom_highlight = SurroundingRectangle(VGroup(code.lines[0], code.lines[1]), color=BOTTOM_COLOR, buff=0.07, stroke_width=2.6)
        self.play(
            Create(bottom_highlight),
            code.lines[0].animate.set_color(TRACE_COLOR),
            code.lines[1].animate.set_color(TRACE_COLOR),
            run_time=0.46,
        )
        self.wait(0.12)

        transition_highlight = SurroundingRectangle(VGroup(code.lines[3], code.lines[4], code.lines[5], code.lines[6]), color=TARGET_COLOR, buff=0.07, stroke_width=2.6)
        self.play(
            Transform(bottom_highlight, transition_highlight),
            code.lines[3].animate.set_color(TRACE_COLOR),
            code.lines[4].animate.set_color(TRACE_COLOR),
            code.lines[5].animate.set_color(TRACE_COLOR),
            code.lines[6].animate.set_color(TRACE_COLOR),
            run_time=0.52,
        )

        note = Text("先初始化底层，再让 i 倒着向上走", font=FONT, font_size=25, color=MUTED)
        note.to_edge(DOWN, buff=0.34)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.36)
        self.wait(0.75)

        return VGroup(heading, tower, code, answer_ring, answer_text, bottom_highlight, note)

    def show_summary(self, title_group, code_group):
        self.play(FadeOut(code_group), run_time=0.45)

        heading = Text("数塔递推检查表", font=FONT, font_size=33, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.42)

        items = VGroup(
            self.make_summary_item("1", "状态表示从当前格走到底"),
            self.make_summary_item("2", "底层直接成为已知状态"),
            self.make_summary_item("3", "看左下和右下，倒着往上填"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        items.next_to(heading, DOWN, buff=0.55)

        self.play(FadeIn(heading, shift=UP * 0.1), run_time=0.36)
        self.play(LaggedStart(*[FadeIn(item, shift=RIGHT * 0.12) for item in items], lag_ratio=0.16), run_time=0.8)
        self.wait(2.0)

    def make_tower(self, mode, rows, cell_width, cell_height, x_gap, y_gap):
        cells = {}
        row_groups = VGroup()
        y_step = cell_height + y_gap
        x_step = cell_width + x_gap

        for row in range(1, rows + 1):
            row_cells = VGroup()
            for col in range(1, row + 1):
                label, font_size = self.cell_label_for_mode(mode, row, col)
                cell = self.make_cell(label, cell_width, cell_height, font_size, row, col, mode)
                x = (col - (row + 1) / 2) * x_step
                y = -(row - 1) * y_step
                cell.move_to(RIGHT * x + UP * y)
                row_cells.add(cell)
                cells[(row, col)] = cell
            row_groups.add(row_cells)

        tower = VGroup(*row_groups)
        tower.cells = cells
        return tower

    def cell_label_for_mode(self, mode, row, col):
        if mode == "raw":
            return str(TOWER_VALUES[row][col - 1]), 22
        if mode == "bottom":
            return str(TOWER_VALUES[row][col - 1]) if row == 5 else "?", 22
        if mode == "dependency":
            if row == 5:
                return str(DP_VALUES[row][col - 1]), 22
            if row == 4:
                return str(TOWER_VALUES[row][col - 1]), 22
            return "?", 22
        if mode == "fill":
            return str(DP_VALUES[row][col - 1]) if row == 5 else " ", 22
        if mode == "dp":
            return str(DP_VALUES[row][col - 1]), 22
        return " ", 22

    def make_cell(self, label, width, height, font_size, row, col, mode):
        fill = CELL_FILL
        stroke = CELL_STROKE
        text_color = WHITE

        if mode in {"bottom", "dependency", "fill", "dp"} and row == 5:
            fill = BOTTOM_FILL
            stroke = BOTTOM_COLOR
            text_color = BOTTOM_COLOR
        if mode == "dp" and row < 5:
            fill = DP_FILL
            stroke = TARGET_COLOR

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
        line_group = VGroup(*[Text(line, font=MONO_FONT, weight="BOLD", font_size=21, color=WHITE) for line in lines])
        line_group.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        line_group.move_to(box.get_center())
        return VGroup(box, line_group)

    def make_code_block(self, lines):
        title = Text("数塔递推写法", font=FONT, weight="BOLD", font_size=22, color=SOURCE_COLOR)
        box = RoundedRectangle(
            width=7.1,
            height=4.0,
            corner_radius=0.08,
            stroke_width=2.2,
            stroke_color=SOURCE_COLOR,
            fill_color=CODE_FILL,
            fill_opacity=0.96,
        )

        left_x = -box.width / 2 + 0.34
        title.move_to(RIGHT * (left_x + title.width / 2) + UP * 1.52)

        code_lines = VGroup()
        start_y = 1.08
        line_gap = 0.31
        for index, line in enumerate(lines):
            text = Text(line if line else " ", font=MONO_FONT, font_size=15.5, color=MUTED)
            text.move_to(RIGHT * (left_x + text.width / 2) + UP * (start_y - index * line_gap))
            code_lines.add(text)

        group = VGroup(box, title, code_lines)
        group.lines = code_lines
        return group

    def make_summary_item(self, number, text):
        dot = Circle(radius=0.2, stroke_width=0, fill_color=POINTER_BLUE, fill_opacity=1)
        number_text = Text(number, font=MONO_FONT, weight="BOLD", font_size=18, color=BACKGROUND)
        number_text.move_to(dot.get_center())
        label = Text(text, font=FONT, font_size=26, color=WHITE)
        return VGroup(VGroup(dot, number_text), label).arrange(RIGHT, buff=0.16)

    def fill_base_color(self, row, col, filled_positions):
        if row == 5:
            return BOTTOM_FILL
        if (row, col) in filled_positions:
            return DP_FILL
        return CELL_FILL

    def fill_base_stroke(self, row, col, filled_positions):
        if row == 5:
            return BOTTOM_COLOR
        if (row, col) in filled_positions:
            return TARGET_COLOR
        return CELL_STROKE
