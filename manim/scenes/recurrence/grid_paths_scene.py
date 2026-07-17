from pathlib import Path
import sys

from manim import *


COMMON_DIR = Path(__file__).resolve().parents[2] / "common"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from theme import BACKGROUND, CELL_FILL, CELL_STROKE, FONT, MONO_FONT, MUTED, POINTER_BLUE  # noqa: E402


BOUNDARY_COLOR = "#fbbf24"
SOURCE_COLOR = "#38bdf8"
LEFT_SOURCE_COLOR = "#a78bfa"
TARGET_COLOR = "#34d399"
TRACE_COLOR = "#fef3c7"
CODE_FILL = "#111827"
FORMULA_FILL = "#172554"
FORMULA_STROKE = "#93c5fd"
ROBOT_COLOR = "#22c55e"
GOAL_COLOR = "#fb7185"


GRID_VALUES = [
    [1, 1, 1, 1, 1],
    [1, 2, 3, 4, 5],
    [1, 3, 6, 10, 15],
    [1, 4, 10, 20, 35],
]


class RecurrenceGridPathsVisualization(Scene):
    """Visualize grid path counting with a two-dimensional recurrence."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        title_group = self.show_intro()
        map_group = self.show_movement_rule(title_group)
        boundary_group = self.show_boundaries(title_group, map_group)
        dependency_group = self.show_dependency(title_group, boundary_group)
        fill_group = self.show_table_fill(title_group, dependency_group)
        code_group = self.show_code_mapping(title_group, fill_group)
        self.show_summary(title_group, code_group)

    def show_intro(self):
        title = Text("递推算法：路径计数", font=FONT, weight="BOLD", font_size=46, color=WHITE)
        subtitle = Text("走到一个格子的方法数从哪里来", font=FONT, font_size=27, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.22)
        title_group = VGroup(title, subtitle)

        self.play(FadeIn(title, shift=UP * 0.16), Write(subtitle), run_time=0.9)
        self.wait(0.25)
        self.play(title_group.animate.scale(0.66).to_edge(UP, buff=0.22), run_time=0.62)
        return title_group

    def show_movement_rule(self, title_group):
        heading = Text("只能向右或向下，问题就能被逐格推出", font=FONT, font_size=31, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.36)

        grid = self.make_grid(mode="empty", cell_size=0.72)
        grid.next_to(heading, DOWN, buff=0.45)

        robot = self.make_robot()
        robot.move_to(grid.cells[(1, 1)].get_center())

        goal = self.make_goal()
        goal.move_to(grid.cells[(4, 5)].get_center())

        right_arrow = Arrow(
            grid.cells[(1, 1)].get_right() + RIGHT * 0.08,
            grid.cells[(1, 2)].get_left() + LEFT * 0.08,
            buff=0.0,
            color=SOURCE_COLOR,
            stroke_width=4,
        )
        down_arrow = Arrow(
            grid.cells[(1, 1)].get_bottom() + DOWN * 0.08,
            grid.cells[(2, 1)].get_top() + UP * 0.08,
            buff=0.0,
            color=BOUNDARY_COLOR,
            stroke_width=4,
        )
        right_label = Text("向右", font=FONT, weight="BOLD", font_size=22, color=SOURCE_COLOR)
        right_label.next_to(right_arrow, UP, buff=0.1)
        down_label = Text("向下", font=FONT, weight="BOLD", font_size=22, color=BOUNDARY_COLOR)
        down_label.next_to(down_arrow, RIGHT, buff=0.12)

        note = Text("不能回头，所以可以从左上一路推到右下", font=FONT, font_size=25, color=MUTED)
        note.to_edge(DOWN, buff=0.34)

        self.play(FadeIn(heading, shift=UP * 0.1), run_time=0.42)
        self.play(FadeIn(grid, shift=UP * 0.08), FadeIn(robot, scale=0.85), FadeIn(goal, scale=0.85), run_time=0.7)
        self.play(Create(right_arrow), FadeIn(right_label), run_time=0.42)
        self.play(Create(down_arrow), FadeIn(down_label), run_time=0.42)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.36)
        self.wait(0.55)

        return VGroup(heading, grid, robot, goal, right_arrow, down_arrow, right_label, down_label, note)

    def show_boundaries(self, title_group, map_group):
        self.play(FadeOut(map_group), run_time=0.45)

        heading = Text("边界格：只有一种走法", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.36)

        grid = self.make_grid(mode="coord", cell_size=0.68)
        grid.next_to(heading, DOWN, buff=0.42)

        note = Text("第一行只能向右，第一列只能向下", font=FONT, font_size=25, color=MUTED)
        note.to_edge(DOWN, buff=0.34)

        self.play(FadeIn(heading, shift=UP * 0.1), FadeIn(grid, shift=UP * 0.08), run_time=0.62)

        boundary_positions = [(1, col) for col in range(1, 6)] + [(row, 1) for row in range(2, 5)]
        for row, col in boundary_positions:
            cell = grid.cells[(row, col)]
            self.play(
                cell.box.animate.set_fill("#78350f", opacity=1).set_stroke(BOUNDARY_COLOR, width=3.1),
                Transform(cell.label, self.make_cell_label("1", cell.get_center(), 23, BOUNDARY_COLOR)),
                run_time=0.16,
            )

        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.36)
        self.wait(0.5)

        return VGroup(heading, grid, note)

    def show_dependency(self, title_group, boundary_group):
        self.play(FadeOut(boundary_group), run_time=0.45)

        heading = Text("内部格：最后一步来自上方或左方", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.36)

        grid = self.make_grid(mode="value", cell_size=0.64)
        grid.next_to(heading, DOWN, buff=0.44).shift(LEFT * 2.65)

        top_source = grid.cells[(2, 4)]
        left_source = grid.cells[(3, 3)]
        target = grid.cells[(3, 4)]

        top_arrow = Arrow(top_source.get_bottom(), target.get_top(), buff=0.08, color=SOURCE_COLOR, stroke_width=3.4)
        left_arrow = Arrow(left_source.get_right(), target.get_left(), buff=0.08, color=LEFT_SOURCE_COLOR, stroke_width=3.4)

        formula = self.make_formula_card(
            [
                "dp[3][4]",
                "= dp[2][4] + dp[3][3]",
                "= 4 + 6 = 10",
            ],
            width=5.1,
            height=1.7,
        )
        formula.next_to(grid, RIGHT, buff=0.58)

        note = Text("当前格 = 上方路径数 + 左方路径数", font=FONT, font_size=25, color=MUTED)
        note.to_edge(DOWN, buff=0.34)

        self.play(FadeIn(heading, shift=UP * 0.1), FadeIn(grid, shift=UP * 0.08), run_time=0.55)
        self.play(
            top_source.box.animate.set_fill("#075985", opacity=1).set_stroke(SOURCE_COLOR, width=3.2),
            left_source.box.animate.set_fill("#4c1d95", opacity=1).set_stroke(LEFT_SOURCE_COLOR, width=3.2),
            run_time=0.42,
        )
        self.play(
            target.box.animate.set_fill("#064e3b", opacity=1).set_stroke(TARGET_COLOR, width=3.4),
            Create(top_arrow),
            Create(left_arrow),
            FadeIn(formula, shift=LEFT * 0.12),
            run_time=0.7,
        )
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.36)
        self.wait(0.75)

        return VGroup(heading, grid, formula, top_arrow, left_arrow, note)

    def show_table_fill(self, title_group, dependency_group):
        self.play(FadeOut(dependency_group), run_time=0.45)

        heading = Text("按行填表：来源必须先算好", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.36)

        grid = self.make_grid(mode="partial", cell_size=0.64)
        grid.next_to(heading, DOWN, buff=0.38)

        formula = self.make_formula_card(["dp[i][j] = dp[i-1][j] + dp[i][j-1]"], width=6.1, height=0.72)
        formula.to_edge(DOWN, buff=0.34)

        self.play(FadeIn(heading, shift=UP * 0.1), FadeIn(grid, shift=UP * 0.08), FadeIn(formula), run_time=0.62)

        steps = [
            (2, 2, 1, 1, 2),
            (2, 3, 1, 2, 3),
            (2, 4, 1, 3, 4),
            (3, 2, 2, 1, 3),
            (3, 3, 3, 3, 6),
            (3, 4, 4, 6, 10),
            (4, 4, 10, 10, 20),
            (4, 5, 15, 20, 35),
        ]
        for row, col, top_value, left_value, result in steps:
            top_source = grid.cells[(row - 1, col)]
            left_source = grid.cells[(row, col - 1)]
            target = grid.cells[(row, col)]
            calc = Text(
                f"dp[{row}][{col}] = {top_value} + {left_value} = {result}",
                font=MONO_FONT,
                weight="BOLD",
                font_size=23,
                color=TRACE_COLOR,
            )
            calc.next_to(formula, UP, buff=0.16)

            top_arrow = Arrow(top_source.get_bottom(), target.get_top(), buff=0.08, color=SOURCE_COLOR, stroke_width=3)
            left_arrow = Arrow(left_source.get_right(), target.get_left(), buff=0.08, color=LEFT_SOURCE_COLOR, stroke_width=3)

            self.play(
                top_source.box.animate.set_fill("#075985", opacity=1).set_stroke(SOURCE_COLOR, width=3.0),
                left_source.box.animate.set_fill("#4c1d95", opacity=1).set_stroke(LEFT_SOURCE_COLOR, width=3.0),
                target.box.animate.set_fill("#064e3b", opacity=1).set_stroke(TARGET_COLOR, width=3.2),
                Create(top_arrow),
                Create(left_arrow),
                FadeIn(calc, shift=UP * 0.06),
                run_time=0.34,
            )
            self.play(Transform(target.label, self.make_cell_label(str(result), target.get_center(), 23, WHITE)), run_time=0.22)
            self.wait(0.03)
            self.play(
                top_source.box.animate.set_fill(self.base_fill(row - 1, col), opacity=1).set_stroke(self.base_stroke(row - 1, col), width=2.0),
                left_source.box.animate.set_fill(self.base_fill(row, col - 1), opacity=1).set_stroke(self.base_stroke(row, col - 1), width=2.0),
                target.box.animate.set_fill(CELL_FILL, opacity=1).set_stroke(CELL_STROKE, width=2.0),
                FadeOut(top_arrow),
                FadeOut(left_arrow),
                FadeOut(calc),
                run_time=0.26,
            )

        note = Text("从左上到右下推进，依赖关系就不会断", font=FONT, font_size=25, color=MUTED)
        note.next_to(formula, UP, buff=0.16)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.36)
        self.wait(0.55)

        return VGroup(heading, grid, formula, note)

    def show_code_mapping(self, title_group, fill_group):
        self.play(FadeOut(fill_group), run_time=0.45)

        heading = Text("右下角保存整张地图的答案", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.36)

        grid = self.make_grid(mode="value", cell_size=0.54)
        grid.next_to(heading, DOWN, buff=0.46).shift(LEFT * 3.1 + DOWN * 0.05)

        answer = grid.cells[(4, 5)]
        answer_ring = SurroundingRectangle(answer, color=TARGET_COLOR, buff=0.05, stroke_width=3.2)
        answer_text = Text("答案 35", font=FONT, weight="BOLD", font_size=26, color=TARGET_COLOR)
        answer_text.next_to(grid, DOWN, buff=0.22)

        code = self.make_code_block(
            [
                "// boundary",
                "dp[i][1] = 1;",
                "dp[1][j] = 1;",
                "",
                "// transition",
                "dp[i][j] = dp[i-1][j]",
                "         + dp[i][j-1];",
            ]
        )
        code.next_to(grid, RIGHT, buff=0.62)

        self.play(FadeIn(heading, shift=UP * 0.1), run_time=0.36)
        self.play(FadeIn(grid, shift=RIGHT * 0.1), FadeIn(code, shift=LEFT * 0.1), run_time=0.7)
        self.play(Create(answer_ring), FadeIn(answer_text, shift=UP * 0.08), run_time=0.45)

        init_highlight = SurroundingRectangle(VGroup(code.lines[1], code.lines[2]), color=BOUNDARY_COLOR, buff=0.07, stroke_width=2.6)
        self.play(
            Create(init_highlight),
            code.lines[1].animate.set_color(TRACE_COLOR),
            code.lines[2].animate.set_color(TRACE_COLOR),
            run_time=0.46,
        )
        self.wait(0.12)

        formula_highlight = SurroundingRectangle(VGroup(code.lines[5], code.lines[6]), color=TARGET_COLOR, buff=0.07, stroke_width=2.6)
        self.play(
            Transform(init_highlight, formula_highlight),
            code.lines[5].animate.set_color(TRACE_COLOR),
            code.lines[6].animate.set_color(TRACE_COLOR),
            run_time=0.52,
        )

        note = Text("初始化边界，再填内部格，最后输出 dp[n][m]", font=FONT, font_size=25, color=MUTED)
        note.to_edge(DOWN, buff=0.34)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.36)
        self.wait(0.75)

        return VGroup(heading, grid, code, answer_ring, answer_text, init_highlight, note)

    def show_summary(self, title_group, code_group):
        self.play(FadeOut(code_group), run_time=0.45)

        heading = Text("路径计数检查表", font=FONT, font_size=33, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.42)

        items = VGroup(
            self.make_summary_item("1", "第一行、第一列先设 1"),
            self.make_summary_item("2", "内部格看上方和左方"),
            self.make_summary_item("3", "右下角就是答案"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        items.next_to(heading, DOWN, buff=0.55)

        self.play(FadeIn(heading, shift=UP * 0.1), run_time=0.36)
        self.play(LaggedStart(*[FadeIn(item, shift=RIGHT * 0.12) for item in items], lag_ratio=0.16), run_time=0.8)
        self.wait(2.0)

    def make_grid(self, mode, cell_size):
        cells = {}
        rows = VGroup()
        gap = 0.08
        x_step = cell_size + gap
        y_step = cell_size + gap

        for row in range(1, 5):
            row_group = VGroup()
            for col in range(1, 6):
                label, font_size = self.cell_label_for_mode(mode, row, col)
                cell = self.make_cell(label, cell_size, font_size, row, col, mode)
                x = (col - 3) * x_step
                y = (2.5 - row) * y_step
                cell.move_to(RIGHT * x + UP * y)
                row_group.add(cell)
                cells[(row, col)] = cell
            rows.add(row_group)

        grid = VGroup(*rows)
        grid.cells = cells
        return grid

    def cell_label_for_mode(self, mode, row, col):
        if mode == "empty":
            return "", 22
        if mode == "coord":
            return f"dp[{row}][{col}]", 12
        if mode == "value":
            return str(GRID_VALUES[row - 1][col - 1]), 22
        if self.is_boundary(row, col):
            return "1", 22
        if row == 2 and col <= 3:
            return str(GRID_VALUES[row - 1][col - 1]), 22
        if row == 3 and col <= 3:
            return str(GRID_VALUES[row - 1][col - 1]), 22
        if row == 4 and col <= 3:
            return str(GRID_VALUES[row - 1][col - 1]), 22
        return "", 22

    def make_cell(self, label, size, font_size, row, col, mode):
        boundary = self.is_boundary(row, col)
        fill = "#78350f" if mode in {"partial", "value"} and boundary else CELL_FILL
        stroke = BOUNDARY_COLOR if mode in {"partial", "value"} and boundary else CELL_STROKE
        text_color = BOUNDARY_COLOR if mode in {"partial", "value"} and boundary else WHITE

        box = RoundedRectangle(
            width=size,
            height=size,
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

    def make_robot(self):
        body = Circle(radius=0.17, stroke_width=0, fill_color=ROBOT_COLOR, fill_opacity=1)
        head = Circle(radius=0.1, stroke_width=0, fill_color="#bbf7d0", fill_opacity=1)
        head.next_to(body, UP, buff=-0.02)
        eye_left = Dot(radius=0.018, color=BACKGROUND).move_to(head.get_center() + LEFT * 0.035 + UP * 0.01)
        eye_right = Dot(radius=0.018, color=BACKGROUND).move_to(head.get_center() + RIGHT * 0.035 + UP * 0.01)
        return VGroup(body, head, eye_left, eye_right)

    def make_goal(self):
        pole = Line(DOWN * 0.22, UP * 0.22, color=GOAL_COLOR, stroke_width=4)
        flag = Polygon(UP * 0.18, RIGHT * 0.3 + UP * 0.08, UP * -0.02, color=GOAL_COLOR, fill_color=GOAL_COLOR, fill_opacity=1)
        flag.next_to(pole.get_top(), RIGHT, buff=0)
        base = Circle(radius=0.06, stroke_width=0, fill_color=GOAL_COLOR, fill_opacity=1)
        base.next_to(pole.get_bottom(), DOWN, buff=-0.03)
        return VGroup(pole, flag, base)

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
        title = Text("路径计数写法", font=FONT, weight="BOLD", font_size=22, color=SOURCE_COLOR)
        box = RoundedRectangle(
            width=6.75,
            height=3.45,
            corner_radius=0.08,
            stroke_width=2.2,
            stroke_color=SOURCE_COLOR,
            fill_color=CODE_FILL,
            fill_opacity=0.96,
        )

        left_x = -box.width / 2 + 0.36
        title.move_to(RIGHT * (left_x + title.width / 2) + UP * 1.28)

        code_lines = VGroup()
        start_y = 0.82
        line_gap = 0.34
        for index, line in enumerate(lines):
            text = Text(line if line else " ", font=MONO_FONT, font_size=17, color=MUTED)
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

    def is_boundary(self, row, col):
        return row == 1 or col == 1

    def base_fill(self, row, col):
        return "#78350f" if self.is_boundary(row, col) else CELL_FILL

    def base_stroke(self, row, col):
        return BOUNDARY_COLOR if self.is_boundary(row, col) else CELL_STROKE
