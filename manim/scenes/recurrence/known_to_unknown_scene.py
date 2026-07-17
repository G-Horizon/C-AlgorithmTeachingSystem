from pathlib import Path
import sys

from manim import *


COMMON_DIR = Path(__file__).resolve().parents[2] / "common"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from theme import BACKGROUND, CELL_FILL, CELL_STROKE, FONT, MONO_FONT, MUTED, POINTER_BLUE  # noqa: E402


KNOWN_FILL = "#15803d"
KNOWN_STROKE = "#bbf7d0"
FOCUS_FILL = "#0f766e"
FOCUS_STROKE = "#5eead4"
UNKNOWN_FILL = "#334155"
UNKNOWN_STROKE = "#94a3b8"
ARROW_COLOR = "#fbbf24"
CODE_HIGHLIGHT = "#fef3c7"


class RecurrenceKnownToUnknownVisualization(Scene):
    """Show how recurrence expands the known area from old states to new states."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        title_group = self.show_intro()
        table_group = self.show_initial_states(title_group)
        self.show_first_unknown(table_group)
        self.show_known_area_growth(table_group)
        self.show_code_mapping(title_group, table_group)

    def show_intro(self):
        title = Text("递推算法：从已知推出未知", font=FONT, weight="BOLD", font_size=48, color=WHITE)
        subtitle = Text("先有旧格子，才有新格子", font=FONT, font_size=27, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.22)
        title_group = VGroup(title, subtitle)

        self.play(FadeIn(title, shift=UP * 0.16), Write(subtitle), run_time=0.95)
        self.wait(0.28)
        self.play(title_group.animate.scale(0.66).to_edge(UP, buff=0.22), run_time=0.62)
        return title_group

    def show_initial_states(self, title_group):
        heading = Text("先把确定的起点放进表里", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.38)

        cells = VGroup(*[self.make_state_cell(index) for index in range(1, 7)]).arrange(RIGHT, buff=0.14)
        cells.move_to(DOWN * 0.48)

        note = Text("右边的问号不是答案，它们在等旧状态来推出", font=FONT, font_size=24, color=MUTED)
        note.next_to(cells, DOWN, buff=0.82)

        self.play(FadeIn(heading, shift=UP * 0.12), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(cell, shift=UP * 0.12) for cell in cells], lag_ratio=0.08), run_time=0.9)
        self.play(
            self.reveal_cell(cells[0], "1"),
            self.reveal_cell(cells[1], "2"),
            run_time=0.65,
        )

        known_band = self.make_known_band(cells, 2)
        self.play(FadeIn(known_band, shift=UP * 0.08), FadeIn(note, shift=UP * 0.12), run_time=0.62)
        self.wait(0.35)

        group = VGroup(heading, cells, known_band, note)
        group.heading = heading
        group.cells = cells
        group.known_band = known_band
        group.note = note
        group.known_count = 2
        return group

    def show_first_unknown(self, table_group):
        cells = table_group.cells
        self.play(FadeOut(table_group.note), run_time=0.25)

        first_unknown_label = Text("第一个未知格", font=FONT, font_size=23, color="#bae6fd")
        first_unknown_label.next_to(cells[2], UP, buff=0.36)

        formula = Text("f[3] = f[2] + f[1]", font=MONO_FONT, weight="BOLD", font_size=31, color=WHITE)
        formula.move_to(UP * 1.45)

        calc = Text("2 + 1 = 3", font=MONO_FONT, weight="BOLD", font_size=34, color=ARROW_COLOR)
        calc.next_to(formula, DOWN, buff=0.22)

        arrows = self.make_dependency_arrows(cells[0], cells[1], cells[2])
        self.play(
            cells[2][0].animate.set_fill(FOCUS_FILL, opacity=1).set_stroke(FOCUS_STROKE, width=3.4),
            FadeIn(first_unknown_label, shift=UP * 0.1),
            run_time=0.35,
        )
        self.play(FadeIn(arrows), FadeIn(formula, shift=UP * 0.1), run_time=0.62)
        self.play(FadeIn(calc, shift=UP * 0.08), run_time=0.35)
        self.wait(0.25)
        self.play(self.reveal_cell(cells[2], "3"), run_time=0.58)

        new_band = self.make_known_band(cells, 3)
        self.play(Transform(table_group.known_band, new_band), run_time=0.5)
        table_group.known_count = 3
        self.wait(0.25)

        self.play(FadeOut(first_unknown_label), FadeOut(arrows), FadeOut(calc), run_time=0.35)
        table_group.formula = formula

    def show_known_area_growth(self, table_group):
        cells = table_group.cells
        formula = table_group.formula
        values = {3: "5", 4: "8", 5: "13"}
        formulas = {
            3: ("i = 4", "f[4] = f[3] + f[2]", "3 + 2 = 5"),
            4: ("i = 5", "f[5] = f[4] + f[3]", "5 + 3 = 8"),
            5: ("i = 6", "f[6] = f[5] + f[4]", "8 + 5 = 13"),
        }

        pointer = self.make_pointer("i = 4")
        pointer.next_to(cells[3], UP, buff=0.34)
        self.play(FadeIn(pointer, shift=UP * 0.1), run_time=0.35)

        current_formula = formula
        current_calc = None

        for index in [3, 4, 5]:
            pointer_target = self.make_pointer(formulas[index][0])
            pointer_target.next_to(cells[index], UP, buff=0.34)

            new_formula = Text(formulas[index][1], font=MONO_FONT, weight="BOLD", font_size=31, color=WHITE)
            new_formula.move_to(current_formula.get_center())

            calc = Text(formulas[index][2], font=MONO_FONT, weight="BOLD", font_size=33, color=ARROW_COLOR)
            calc.next_to(new_formula, DOWN, buff=0.22)

            arrows = self.make_dependency_arrows(cells[index - 2], cells[index - 1], cells[index])
            self.play(
                Transform(pointer, pointer_target),
                Transform(current_formula, new_formula),
                cells[index][0].animate.set_fill(FOCUS_FILL, opacity=1).set_stroke(FOCUS_STROKE, width=3.4),
                run_time=0.45,
            )
            if current_calc is not None:
                self.play(FadeOut(current_calc), run_time=0.12)
            self.play(FadeIn(arrows), FadeIn(calc, shift=UP * 0.08), run_time=0.45)
            self.play(self.reveal_cell(cells[index], values[index]), run_time=0.52)

            new_band = self.make_known_band(cells, index + 1)
            self.play(Transform(table_group.known_band, new_band), run_time=0.42)
            table_group.known_count = index + 1
            self.play(FadeOut(arrows), run_time=0.22)
            current_calc = calc

        self.play(FadeOut(pointer), FadeOut(current_calc), FadeOut(current_formula), run_time=0.4)
        table_group.remove(table_group.note)

    def show_code_mapping(self, title_group, table_group):
        self.play(FadeOut(table_group.heading), run_time=0.25)

        compact_table = VGroup(table_group.cells, table_group.known_band)
        self.play(
            compact_table.animate.scale(0.72).to_edge(LEFT, buff=0.42).shift(DOWN * 0.15),
            title_group.animate.scale(0.9).to_edge(UP, buff=0.18).shift(LEFT * 0.22),
            run_time=0.7,
        )

        code_title = Text("循环顺序来自依赖关系", font=FONT, font_size=29, color=WHITE)
        code_lines = [
            "f[1] = 1;",
            "f[2] = 2;",
            "for (int i = 3; i <= n; ++i) {",
            "    f[i] = f[i - 1] + f[i - 2];",
            "}",
        ]
        code = VGroup(
            *[
                Text(
                    line,
                    font=MONO_FONT,
                    font_size=21,
                    color=MUTED,
                )
                for line in code_lines
            ]
        )
        code.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        code_group = VGroup(code_title, code).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        code_group.to_edge(RIGHT, buff=0.42).shift(UP * 0.08)

        self.play(FadeIn(code_title, shift=LEFT * 0.12), run_time=0.35)
        self.play(LaggedStart(*[FadeIn(line, shift=UP * 0.08) for line in code], lag_ratio=0.11), run_time=0.86)

        highlight_box = SurroundingRectangle(code[2], color=ARROW_COLOR, buff=0.08, stroke_width=2.8)
        self.play(Create(highlight_box), code[2].animate.set_color(CODE_HIGHLIGHT), run_time=0.42)
        self.wait(0.2)
        self.play(
            highlight_box.animate.become(SurroundingRectangle(code[3], color=ARROW_COLOR, buff=0.08, stroke_width=2.8)),
            code[2].animate.set_color(MUTED),
            code[3].animate.set_color(CODE_HIGHLIGHT),
            run_time=0.52,
        )

        summary = VGroup(
            self.make_summary_item("1", "先初始化"),
            self.make_summary_item("2", "看依赖"),
            self.make_summary_item("3", "按方向推进"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        summary.next_to(code_group, DOWN, buff=0.38, aligned_edge=LEFT)

        self.play(FadeIn(summary, shift=UP * 0.14), run_time=0.65)
        self.wait(2.0)

    def make_state_cell(self, index):
        box = RoundedRectangle(
            width=1.08,
            height=1.12,
            corner_radius=0.08,
            stroke_width=2.2,
            stroke_color=UNKNOWN_STROKE,
            fill_color=UNKNOWN_FILL,
            fill_opacity=1,
        )
        label = Text(f"f[{index}]", font=MONO_FONT, weight="BOLD", font_size=22, color="#bae6fd")
        value = Text("?", font=MONO_FONT, weight="BOLD", font_size=31, color=WHITE)
        label.move_to(box.get_center() + UP * 0.28)
        value.move_to(box.get_center() + DOWN * 0.22)
        return VGroup(box, label, value)

    def reveal_cell(self, cell, value):
        new_value = Text(value, font=MONO_FONT, weight="BOLD", font_size=31, color=WHITE)
        new_value.move_to(cell[2].get_center())
        return AnimationGroup(
            cell[0].animate.set_fill(KNOWN_FILL, opacity=1).set_stroke(KNOWN_STROKE, width=3),
            Transform(cell[2], new_value),
        )

    def make_known_band(self, cells, count):
        left = cells[0].get_left()[0]
        right = cells[count - 1].get_right()[0]
        width = right - left + 0.12
        band = RoundedRectangle(
            width=width,
            height=0.26,
            corner_radius=0.08,
            stroke_width=0,
            fill_color="#22c55e",
            fill_opacity=0.82,
        )
        band.move_to(RIGHT * ((left + right) / 2) + DOWN * 1.55)
        label = Text("已知区", font=FONT, weight="BOLD", font_size=21, color="#dcfce7")
        label.next_to(band, DOWN, buff=0.12)
        return VGroup(band, label)

    def make_dependency_arrows(self, left_cell, right_cell, target_cell):
        left_arrow = Arrow(
            left_cell.get_top() + UP * 0.12,
            target_cell.get_top() + LEFT * 0.18 + UP * 0.12,
            buff=0.08,
            color=ARROW_COLOR,
            stroke_width=3.2,
            max_tip_length_to_length_ratio=0.14,
        )
        right_arrow = Arrow(
            right_cell.get_top() + UP * 0.12,
            target_cell.get_top() + RIGHT * 0.18 + UP * 0.12,
            buff=0.08,
            color=POINTER_BLUE,
            stroke_width=3.2,
            max_tip_length_to_length_ratio=0.14,
        )
        return VGroup(left_arrow, right_arrow)

    def make_pointer(self, text):
        box = RoundedRectangle(
            width=1.0,
            height=0.42,
            corner_radius=0.08,
            stroke_width=2,
            stroke_color=FOCUS_STROKE,
            fill_color=FOCUS_FILL,
            fill_opacity=0.98,
        )
        label = Text(text, font=MONO_FONT, weight="BOLD", font_size=20, color=WHITE)
        label.move_to(box.get_center())
        return VGroup(box, label)

    def make_summary_item(self, number, text):
        dot = Circle(radius=0.18, stroke_width=0, fill_color=POINTER_BLUE, fill_opacity=1)
        number_text = Text(number, font=MONO_FONT, weight="BOLD", font_size=17, color=BACKGROUND)
        number_text.move_to(dot.get_center())
        label = Text(text, font=FONT, font_size=23, color=WHITE)
        return VGroup(VGroup(dot, number_text), label).arrange(RIGHT, buff=0.16)
