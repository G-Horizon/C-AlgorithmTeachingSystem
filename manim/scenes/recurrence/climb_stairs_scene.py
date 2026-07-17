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
SOURCE_ONE = "#fbbf24"
SOURCE_TWO = "#38bdf8"
FORMULA_FILL = "#172554"
FORMULA_STROKE = "#93c5fd"
CODE_HIGHLIGHT = "#fef3c7"


class RecurrenceClimbStairsVisualization(Scene):
    """Explain the climb stairs recurrence with last-step classification."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        title_group = self.show_intro()
        stair_group = self.show_state_on_stairs(title_group)
        formula_group = self.show_last_step_sources(stair_group)
        table_group = self.show_table_fill(title_group, formula_group)
        self.show_code_mapping(title_group, table_group)

    def show_intro(self):
        title = Text("递推算法：一维递推爬楼梯", font=FONT, weight="BOLD", font_size=47, color=WHITE)
        subtitle = Text("答案藏在最后一步里", font=FONT, font_size=27, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.22)
        group = VGroup(title, subtitle)

        self.play(FadeIn(title, shift=UP * 0.16), Write(subtitle), run_time=0.95)
        self.wait(0.28)
        self.play(group.animate.scale(0.66).to_edge(UP, buff=0.22), run_time=0.62)
        return group

    def show_state_on_stairs(self, title_group):
        heading = Text("状态：f[i] = 到第 i 阶的方法数", font=FONT, font_size=31, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.42)

        steps = VGroup()
        labels = ["0", "1", "2", "i-2", "i-1", "i"]
        for index, label in enumerate(labels):
            step = self.make_step(label)
            step.move_to(RIGHT * (-3.15 + index * 1.26) + DOWN * (1.2 - index * 0.18))
            steps.add(step)

        state_card = self.make_state_card("f[i]")
        state_card.next_to(steps[-1], UP, buff=0.72).shift(RIGHT * 0.1)

        note = Text("先盯住任意一个当前阶 i", font=FONT, font_size=24, color=MUTED)
        note.to_edge(DOWN, buff=0.32)

        self.play(FadeIn(heading, shift=UP * 0.12), run_time=0.42)
        self.play(LaggedStart(*[FadeIn(step, shift=UP * 0.12) for step in steps], lag_ratio=0.08), run_time=0.95)
        self.play(FadeIn(state_card, shift=UP * 0.1), FadeIn(note, shift=UP * 0.1), run_time=0.55)
        self.wait(0.35)

        group = VGroup(heading, steps, state_card, note)
        group.heading = heading
        group.steps = steps
        group.state_card = state_card
        group.note = note
        return group

    def show_last_step_sources(self, stair_group):
        steps = stair_group.steps
        self.play(FadeOut(stair_group.note), run_time=0.22)

        source_title = Text("最后一步只有两种来源", font=FONT, weight="BOLD", font_size=30, color="#fef3c7")
        source_title.next_to(stair_group.heading, DOWN, buff=0.28)

        one_step = CurvedArrow(
            steps[-2].get_top() + UP * 0.1,
            steps[-1].get_top() + UP * 0.1,
            angle=-TAU / 6,
            color=SOURCE_ONE,
            stroke_width=4,
            tip_length=0.18,
        )
        one_label = Text("走 1 阶", font=FONT, weight="BOLD", font_size=21, color=SOURCE_ONE)
        one_label.move_to(steps[-2].get_top() + UP * 0.86 + RIGHT * 0.34)

        two_step = CurvedArrow(
            steps[-3].get_top() + UP * 0.18,
            steps[-1].get_top() + UP * 0.26,
            angle=-TAU / 5,
            color=SOURCE_TWO,
            stroke_width=4,
            tip_length=0.18,
        )
        two_label = Text("走 2 阶", font=FONT, weight="BOLD", font_size=21, color=SOURCE_TWO)
        two_label.move_to(steps[-3].get_top() + UP * 1.08 + RIGHT * 0.38)

        self.play(FadeIn(source_title, shift=UP * 0.1), run_time=0.35)
        self.play(
            steps[-2][0].animate.set_fill(FOCUS_FILL, opacity=1).set_stroke(SOURCE_ONE, width=3.2),
            steps[-1][0].animate.set_fill(FOCUS_FILL, opacity=1).set_stroke(FOCUS_STROKE, width=3.2),
            Create(one_step),
            FadeIn(one_label, shift=UP * 0.08),
            run_time=0.72,
        )
        self.play(
            steps[-3][0].animate.set_fill(FOCUS_FILL, opacity=1).set_stroke(SOURCE_TWO, width=3.2),
            Create(two_step),
            FadeIn(two_label, shift=UP * 0.08),
            run_time=0.72,
        )
        self.wait(0.25)

        left_source = self.make_source_card("来自 i-1", "f[i-1]", SOURCE_ONE)
        right_source = self.make_source_card("来自 i-2", "f[i-2]", SOURCE_TWO)
        formula = self.make_formula_card("f[i] = f[i-1] + f[i-2]")
        source_group = VGroup(left_source, formula, right_source).arrange(RIGHT, buff=0.3)
        source_group.to_edge(DOWN, buff=0.36)

        merge_arrow_1 = Arrow(left_source.get_right(), formula.get_left(), buff=0.08, color=SOURCE_ONE, stroke_width=3)
        merge_arrow_2 = Arrow(right_source.get_left(), formula.get_right(), buff=0.08, color=SOURCE_TWO, stroke_width=3)

        self.play(FadeIn(left_source, shift=UP * 0.1), FadeIn(right_source, shift=UP * 0.1), run_time=0.48)
        self.play(Create(merge_arrow_1), Create(merge_arrow_2), FadeIn(formula, shift=UP * 0.1), run_time=0.7)

        plus = formula.plus
        self.play(plus.animate.scale(1.28).set_color("#fde68a"), run_time=0.18)
        self.play(plus.animate.scale(1 / 1.28).set_color(WHITE), run_time=0.18)
        self.wait(0.45)

        group = VGroup(
            stair_group,
            source_title,
            one_step,
            one_label,
            two_step,
            two_label,
            left_source,
            right_source,
            formula,
            merge_arrow_1,
            merge_arrow_2,
        )
        group.formula = formula
        return group

    def show_table_fill(self, title_group, formula_group):
        self.play(FadeOut(formula_group), run_time=0.55)

        heading = Text("按顺序填表：每格由前两格推出", font=FONT, font_size=31, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.42)
        formula_note = self.make_formula_card("f[i] = f[i-1] + f[i-2]")
        formula_note.scale(0.78)
        formula_note.next_to(heading, DOWN, buff=0.26)

        cells = VGroup(*[self.make_table_cell(index) for index in range(7)]).arrange(RIGHT, buff=0.12)
        cells.move_to(DOWN * 0.45)

        self.play(FadeIn(heading, shift=UP * 0.1), FadeIn(formula_note, shift=UP * 0.1), run_time=0.52)
        self.play(LaggedStart(*[FadeIn(cell, shift=UP * 0.1) for cell in cells], lag_ratio=0.06), run_time=0.85)
        self.play(self.reveal_cell(cells[0], "1"), self.reveal_cell(cells[1], "1"), run_time=0.6)

        known_values = ["1", "1", "2", "3", "5", "8", "13"]
        values = known_values[2:]
        pointer = None
        for offset, value in enumerate(values, start=2):
            new_pointer = self.make_pointer(f"i = {offset}")
            new_pointer.next_to(cells[offset], UP, buff=0.34)
            arrows = self.make_dependency_arrows(cells[offset - 2], cells[offset - 1], cells[offset])
            calc = Text(
                f"{known_values[offset - 1]} + {known_values[offset - 2]} = {value}",
                font=MONO_FONT,
                weight="BOLD",
                font_size=25,
                color="#fef3c7",
            )
            calc.next_to(cells, DOWN, buff=0.58)

            animations = [
                FadeIn(arrows),
                cells[offset][0].animate.set_fill(FOCUS_FILL, opacity=1).set_stroke(FOCUS_STROKE, width=3.1),
                FadeIn(calc, shift=UP * 0.08),
            ]
            if pointer is None:
                animations.insert(0, FadeIn(new_pointer, shift=UP * 0.1))
                pointer = new_pointer
            else:
                animations.insert(0, Transform(pointer, new_pointer))

            self.play(*animations, run_time=0.5)
            self.play(self.reveal_cell(cells[offset], value), run_time=0.38)
            self.play(FadeOut(arrows), FadeOut(calc), run_time=0.22)

        self.play(FadeOut(pointer), run_time=0.25)
        self.wait(0.35)

        group = VGroup(heading, formula_note, cells)
        group.heading = heading
        group.formula_note = formula_note
        group.cells = cells
        return group

    def show_code_mapping(self, title_group, table_group):
        compact = VGroup(table_group.cells)
        self.play(
            FadeOut(table_group.heading),
            FadeOut(table_group.formula_note),
            compact.animate.scale(0.72).to_edge(LEFT, buff=0.42).shift(DOWN * 0.18),
            title_group.animate.scale(0.9).to_edge(UP, buff=0.18).shift(LEFT * 0.18),
            run_time=0.7,
        )

        code_title = Text("代码：初始化、递推、输出", font=FONT, font_size=29, color=WHITE)
        code_lines = [
            "f[0] = 1;",
            "f[1] = 1;",
            "for (int i = 2; i <= n; ++i) {",
            "    f[i] = f[i - 1] + f[i - 2];",
            "}",
            "cout << f[n];",
        ]
        code = VGroup(
            *[
                Text(line, font=MONO_FONT, font_size=20, color=MUTED)
                for line in code_lines
            ]
        )
        code.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        code_group = VGroup(code_title, code).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        code_group.to_edge(RIGHT, buff=0.36).shift(UP * 0.08)

        self.play(FadeIn(code_title, shift=LEFT * 0.12), run_time=0.35)
        self.play(LaggedStart(*[FadeIn(line, shift=UP * 0.08) for line in code], lag_ratio=0.09), run_time=0.86)

        highlights = [
            SurroundingRectangle(VGroup(code[0], code[1]), color=SOURCE_ONE, buff=0.08, stroke_width=2.7),
            SurroundingRectangle(code[2], color=SOURCE_ONE, buff=0.08, stroke_width=2.7),
            SurroundingRectangle(code[3], color=SOURCE_ONE, buff=0.08, stroke_width=2.7),
            SurroundingRectangle(code[5], color=SOURCE_ONE, buff=0.08, stroke_width=2.7),
        ]
        active = highlights[0]
        self.play(Create(active), code[0].animate.set_color(CODE_HIGHLIGHT), code[1].animate.set_color(CODE_HIGHLIGHT), run_time=0.42)
        self.wait(0.12)
        for index, target in [(1, code[2]), (2, code[3]), (3, code[5])]:
            previous_targets = [code[0], code[1]] if index == 1 else [code[index]]
            self.play(
                active.animate.become(highlights[index]),
                *[line.animate.set_color(MUTED) for line in previous_targets],
                target.animate.set_color(CODE_HIGHLIGHT),
                run_time=0.46,
            )
            self.wait(0.12)

        summary = VGroup(
            self.make_summary_item("1", "最后一步分类"),
            self.make_summary_item("2", "旧状态相加"),
            self.make_summary_item("3", "答案是 f[n]"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        summary.next_to(code_group, DOWN, buff=0.36, aligned_edge=LEFT)

        self.play(FadeIn(summary, shift=UP * 0.14), run_time=0.64)
        self.wait(2.0)

    def make_step(self, label):
        box = RoundedRectangle(
            width=0.9,
            height=0.58,
            corner_radius=0.08,
            stroke_width=2.2,
            stroke_color=CELL_STROKE,
            fill_color=CELL_FILL,
            fill_opacity=1,
        )
        text = Text(label, font=MONO_FONT, weight="BOLD", font_size=22, color=WHITE)
        text.move_to(box.get_center())
        stair_label = Text("阶", font=FONT, font_size=15, color=MUTED)
        stair_label.next_to(box, DOWN, buff=0.08)
        return VGroup(box, text, stair_label)

    def make_state_card(self, text):
        box = RoundedRectangle(
            width=1.08,
            height=0.52,
            corner_radius=0.08,
            stroke_width=2.5,
            stroke_color=FOCUS_STROKE,
            fill_color=FOCUS_FILL,
            fill_opacity=0.96,
        )
        label = Text(text, font=MONO_FONT, weight="BOLD", font_size=24, color=WHITE)
        label.move_to(box.get_center())
        return VGroup(box, label)

    def make_source_card(self, title, value, color):
        box = RoundedRectangle(
            width=1.78,
            height=0.92,
            corner_radius=0.09,
            stroke_width=2.3,
            stroke_color=color,
            fill_color="#1e293b",
            fill_opacity=0.96,
        )
        top = Text(title, font=FONT, font_size=18, color=MUTED)
        bottom = Text(value, font=MONO_FONT, weight="BOLD", font_size=24, color=color)
        VGroup(top, bottom).arrange(DOWN, buff=0.08).move_to(box.get_center())
        return VGroup(box, top, bottom)

    def make_formula_card(self, text):
        box = RoundedRectangle(
            width=3.15,
            height=0.76,
            corner_radius=0.08,
            stroke_width=2.5,
            stroke_color=FORMULA_STROKE,
            fill_color=FORMULA_FILL,
            fill_opacity=0.98,
        )
        parts = VGroup(
            Text("f[i]", font=MONO_FONT, weight="BOLD", font_size=24, color=WHITE),
            Text("=", font=MONO_FONT, weight="BOLD", font_size=24, color=WHITE),
            Text("f[i-1]", font=MONO_FONT, weight="BOLD", font_size=24, color=SOURCE_ONE),
            Text("+", font=MONO_FONT, weight="BOLD", font_size=25, color=WHITE),
            Text("f[i-2]", font=MONO_FONT, weight="BOLD", font_size=24, color=SOURCE_TWO),
        ).arrange(RIGHT, buff=0.08)
        parts.move_to(box.get_center())
        group = VGroup(box, parts)
        group.plus = parts[3]
        return group

    def make_table_cell(self, index):
        box = RoundedRectangle(
            width=1.02,
            height=1.02,
            corner_radius=0.08,
            stroke_width=2.1,
            stroke_color=CELL_STROKE,
            fill_color=CELL_FILL,
            fill_opacity=1,
        )
        label = Text(f"f[{index}]", font=MONO_FONT, weight="BOLD", font_size=20, color="#bae6fd")
        value = Text("?", font=MONO_FONT, weight="BOLD", font_size=29, color=WHITE)
        label.move_to(box.get_center() + UP * 0.24)
        value.move_to(box.get_center() + DOWN * 0.22)
        return VGroup(box, label, value)

    def reveal_cell(self, cell, value):
        new_value = Text(value, font=MONO_FONT, weight="BOLD", font_size=29, color=WHITE)
        new_value.move_to(cell[2].get_center())
        return AnimationGroup(
            cell[0].animate.set_fill(KNOWN_FILL, opacity=1).set_stroke(KNOWN_STROKE, width=2.8),
            Transform(cell[2], new_value),
        )

    def make_dependency_arrows(self, left_cell, right_cell, target_cell):
        left_arrow = Arrow(
            left_cell.get_top() + UP * 0.12,
            target_cell.get_top() + LEFT * 0.16 + UP * 0.12,
            buff=0.08,
            color=SOURCE_TWO,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.14,
        )
        right_arrow = Arrow(
            right_cell.get_top() + UP * 0.12,
            target_cell.get_top() + RIGHT * 0.16 + UP * 0.12,
            buff=0.08,
            color=SOURCE_ONE,
            stroke_width=3,
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
