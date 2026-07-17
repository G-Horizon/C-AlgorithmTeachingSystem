from pathlib import Path
import sys

from manim import *


COMMON_DIR = Path(__file__).resolve().parents[2] / "common"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from theme import BACKGROUND, CELL_FILL, CELL_STROKE, FONT, MONO_FONT, MUTED, POINTER_BLUE  # noqa: E402


OLD_STATE = "#fbbf24"
CURRENT_STATE = "#38bdf8"
NEW_STATE = "#34d399"
TRACE_COLOR = "#fef3c7"
CODE_FILL = "#111827"
FORMULA_FILL = "#172554"
FORMULA_STROKE = "#93c5fd"
DIM_FILL = "#1e293b"


class RecurrenceRollingVariablesVisualization(Scene):
    """Show how a recurrence table can be compressed into rolling variables."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        title_group = self.show_intro()
        array_group = self.show_array_window(title_group)
        compact_group = self.show_compact_state(title_group, array_group)
        rolling_group = self.show_rolling_update(title_group, compact_group)
        code_group = self.show_code_mapping(title_group, rolling_group)
        self.show_summary(title_group, code_group)

    def show_intro(self):
        title = Text("递推算法：滚动变量优化", font=FONT, weight="BOLD", font_size=46, color=WHITE)
        subtitle = Text("表可以很长，记忆可以很短", font=FONT, font_size=27, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.22)
        title_group = VGroup(title, subtitle)

        self.play(FadeIn(title, shift=UP * 0.16), Write(subtitle), run_time=0.9)
        self.wait(0.25)
        self.play(title_group.animate.scale(0.66).to_edge(UP, buff=0.22), run_time=0.62)
        return title_group

    def show_array_window(self, title_group):
        heading = Text("完整表很长，但下一格只看最近两个", font=FONT, font_size=31, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.36)

        formula = self.make_formula_card("f[i] = f[i-1] + f[i-2]")
        formula.next_to(heading, DOWN, buff=0.24)

        values = ["0", "1", "1", "2", "3", "5", "8", "13", "21"]
        cells = VGroup(*[self.make_table_cell(index, value) for index, value in enumerate(values)])
        cells.arrange(RIGHT, buff=0.08)
        cells.next_to(formula, DOWN, buff=0.44)

        self.play(FadeIn(heading, shift=UP * 0.1), FadeIn(formula, shift=UP * 0.08), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(cell, shift=UP * 0.08) for cell in cells], lag_ratio=0.04), run_time=0.9)

        for index in [2, 3, 4, 5]:
            arrows = self.make_dependency_arrows(cells[index - 2], cells[index - 1], cells[index])
            calc = Text(
                f"i={index}: {values[index - 2]} + {values[index - 1]} = {values[index]}",
                font=MONO_FONT,
                weight="BOLD",
                font_size=25,
                color=TRACE_COLOR,
            )
            calc.next_to(cells, DOWN, buff=0.46)
            self.play(
                cells[index - 2][0].animate.set_stroke(OLD_STATE, width=3.2),
                cells[index - 1][0].animate.set_stroke(CURRENT_STATE, width=3.2),
                cells[index][0].animate.set_fill("#0f766e", opacity=1).set_stroke(NEW_STATE, width=3.4),
                FadeIn(arrows),
                FadeIn(calc, shift=UP * 0.08),
                run_time=0.42,
            )
            self.wait(0.08)
            self.play(
                cells[index - 2][0].animate.set_fill(CELL_FILL, opacity=1).set_stroke(CELL_STROKE, width=2.0),
                cells[index - 1][0].animate.set_fill(CELL_FILL, opacity=1).set_stroke(CELL_STROKE, width=2.0),
                cells[index][0].animate.set_fill(CELL_FILL, opacity=1).set_stroke(CELL_STROKE, width=2.0),
                FadeOut(arrows),
                FadeOut(calc),
                run_time=0.28,
            )

        note = Text("依赖窗口只有两个旧状态", font=FONT, font_size=25, color=MUTED)
        note.to_edge(DOWN, buff=0.34)
        window = SurroundingRectangle(VGroup(cells[4], cells[5]), color=TRACE_COLOR, buff=0.08, stroke_width=2.8)
        next_rect = SurroundingRectangle(cells[6], color=NEW_STATE, buff=0.08, stroke_width=2.8)
        self.play(
            *[cells[i].animate.set_opacity(0.34) for i in [0, 1, 2, 3, 7, 8]],
            Create(window),
            Create(next_rect),
            FadeIn(note, shift=UP * 0.08),
            run_time=0.65,
        )
        self.wait(0.45)

        group = VGroup(heading, formula, cells, window, next_rect, note)
        return group

    def show_compact_state(self, title_group, array_group):
        self.play(FadeOut(array_group), run_time=0.5)

        heading = Text("把长表压缩成两个旧状态", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.36)

        ghost_values = ["f[0]", "f[1]", "f[2]", "f[3]", "f[i-2]", "f[i-1]", "f[i]"]
        ghost_cells = VGroup(*[self.make_ghost_cell(label) for label in ghost_values]).arrange(RIGHT, buff=0.07)
        ghost_cells.next_to(heading, DOWN, buff=0.42)
        ghost_cells.set_opacity(0.42)

        window = SurroundingRectangle(VGroup(ghost_cells[4], ghost_cells[5]), color=TRACE_COLOR, buff=0.08, stroke_width=2.5)
        a_box = self.make_state_box("a", "f[i-2]", "较旧", OLD_STATE)
        b_box = self.make_state_box("b", "f[i-1]", "较新", CURRENT_STATE)
        boxes = VGroup(a_box, b_box).arrange(RIGHT, buff=0.9)
        boxes.next_to(ghost_cells, DOWN, buff=0.58)

        arrow_a = Arrow(ghost_cells[4].get_bottom(), a_box.get_top(), buff=0.12, color=OLD_STATE, stroke_width=3)
        arrow_b = Arrow(ghost_cells[5].get_bottom(), b_box.get_top(), buff=0.12, color=CURRENT_STATE, stroke_width=3)
        note = Text("只保留下一步还会用到的旧状态", font=FONT, font_size=25, color=MUTED)
        note.to_edge(DOWN, buff=0.34)

        self.play(FadeIn(heading, shift=UP * 0.1), FadeIn(ghost_cells, shift=UP * 0.08), run_time=0.5)
        self.play(Create(window), run_time=0.32)
        self.play(FadeIn(a_box, shift=UP * 0.12), FadeIn(b_box, shift=UP * 0.12), Create(arrow_a), Create(arrow_b), run_time=0.72)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.36)
        self.wait(0.6)

        return VGroup(heading, ghost_cells, window, boxes, arrow_a, arrow_b, note)

    def show_rolling_update(self, title_group, compact_group):
        self.play(FadeOut(compact_group), run_time=0.5)

        heading = Text("每一步：先算 c，再滚动", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.36)
        formula = self.make_formula_card("c = a + b")
        formula.next_to(heading, DOWN, buff=0.23)

        a_box = self.make_variable_box("a", "0", OLD_STATE, "旧旧")
        b_box = self.make_variable_box("b", "1", CURRENT_STATE, "旧新")
        c_box = self.make_variable_box("c", "?", NEW_STATE, "新值")
        boxes = VGroup(a_box, b_box, c_box).arrange(RIGHT, buff=0.68)
        boxes.next_to(formula, DOWN, buff=0.48)

        self.play(FadeIn(heading, shift=UP * 0.1), FadeIn(formula, shift=UP * 0.08), run_time=0.45)
        self.play(FadeIn(a_box, shift=UP * 0.1), FadeIn(b_box, shift=UP * 0.1), FadeIn(c_box, shift=UP * 0.1), run_time=0.62)

        steps = [(2, 0, 1, 1), (3, 1, 1, 2), (4, 1, 2, 3)]
        for step_index, (index, a_value, b_value, c_value) in enumerate(steps):
            trace = Text(
                f"i={index}: c = {a_value} + {b_value} = {c_value}",
                font=MONO_FONT,
                weight="BOLD",
                font_size=25,
                color=TRACE_COLOR,
            )
            trace.to_edge(DOWN, buff=0.48)
            self.play(
                FadeIn(trace, shift=UP * 0.08),
                Transform(c_box.value, self.make_box_value(str(c_value), c_box.value.get_center())),
                c_box[0].animate.set_stroke(NEW_STATE, width=4.0),
                run_time=0.48,
            )

            arrow_a = Arrow(
                b_box.get_bottom() + DOWN * 0.16,
                a_box.get_bottom() + DOWN * 0.16,
                buff=0.08,
                color=OLD_STATE,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.16,
            )
            arrow_b = Arrow(
                c_box.get_bottom() + DOWN * 0.16,
                b_box.get_bottom() + DOWN * 0.16,
                buff=0.08,
                color=CURRENT_STATE,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.16,
            )
            tag_a = self.make_update_tag("a = b", OLD_STATE)
            tag_b = self.make_update_tag("b = c", CURRENT_STATE)
            tag_a.next_to(arrow_a, DOWN, buff=0.08)
            tag_b.next_to(arrow_b, DOWN, buff=0.08)

            self.play(Create(arrow_a), FadeIn(tag_a, shift=UP * 0.05), run_time=0.28)
            self.play(Transform(a_box.value, self.make_box_value(str(b_value), a_box.value.get_center())), run_time=0.3)
            self.play(Create(arrow_b), FadeIn(tag_b, shift=UP * 0.05), run_time=0.28)
            self.play(Transform(b_box.value, self.make_box_value(str(c_value), b_box.value.get_center())), run_time=0.3)

            fade_targets = [arrow_a, arrow_b, tag_a, tag_b, trace]
            if step_index < len(steps) - 1:
                self.play(
                    *[FadeOut(item) for item in fade_targets],
                    Transform(c_box.value, self.make_box_value("?", c_box.value.get_center())),
                    c_box[0].animate.set_stroke(NEW_STATE, width=2.4),
                    run_time=0.34,
                )
            else:
                self.play(*[FadeOut(item) for item in fade_targets], run_time=0.28)

        note = Text("先算新值，避免旧状态被覆盖", font=FONT, font_size=25, color=MUTED)
        note.to_edge(DOWN, buff=0.34)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.38)
        self.wait(0.55)

        return VGroup(heading, formula, boxes, note)

    def show_code_mapping(self, title_group, rolling_group):
        self.play(FadeOut(rolling_group), run_time=0.5)

        heading = Text("盒子滑动，对应三行代码", font=FONT, font_size=32, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.36)

        code = self.make_code_block(
            [
                "long long a = 0, b = 1;",
                "for (int i = 2; i <= n; i++) {",
                "    long long c = a + b;",
                "    a = b;",
                "    b = c;",
                "}",
                "cout << b;",
            ]
        )
        code.next_to(heading, DOWN, buff=0.33).shift(LEFT * 1.45)

        space = self.make_space_transition()
        space.next_to(code, RIGHT, buff=0.64)

        self.play(FadeIn(heading, shift=UP * 0.1), run_time=0.36)
        self.play(FadeIn(code, shift=RIGHT * 0.12), FadeIn(space, shift=LEFT * 0.12), run_time=0.7)

        highlight = SurroundingRectangle(code.lines[2], color=NEW_STATE, buff=0.07, stroke_width=2.8)
        self.play(Create(highlight), code.lines[2].animate.set_color(TRACE_COLOR), run_time=0.42)
        self.wait(0.18)

        second_highlight = SurroundingRectangle(VGroup(code.lines[3], code.lines[4]), color=CURRENT_STATE, buff=0.07, stroke_width=2.8)
        self.play(
            Transform(highlight, second_highlight),
            code.lines[3].animate.set_color(TRACE_COLOR),
            code.lines[4].animate.set_color(TRACE_COLOR),
            run_time=0.5,
        )

        note = Text("空间从保存整张表，变成只保存几个变量", font=FONT, font_size=24, color=MUTED)
        note.to_edge(DOWN, buff=0.34)
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.38)
        self.wait(0.7)

        return VGroup(heading, code, space, highlight, note)

    def show_summary(self, title_group, code_group):
        self.play(FadeOut(code_group), run_time=0.5)

        heading = Text("滚动变量优化检查表", font=FONT, font_size=33, color=WHITE)
        heading.next_to(title_group, DOWN, buff=0.42)

        items = VGroup(
            self.make_summary_item("1", "只保留会再用的状态"),
            self.make_summary_item("2", "先算新值 c"),
            self.make_summary_item("3", "再整体滚动"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        items.next_to(heading, DOWN, buff=0.55)

        self.play(FadeIn(heading, shift=UP * 0.1), run_time=0.36)
        self.play(LaggedStart(*[FadeIn(item, shift=RIGHT * 0.12) for item in items], lag_ratio=0.16), run_time=0.8)
        self.wait(2.0)

    def make_table_cell(self, index, value):
        box = RoundedRectangle(
            width=0.78,
            height=0.86,
            corner_radius=0.08,
            stroke_width=2.0,
            stroke_color=CELL_STROKE,
            fill_color=CELL_FILL,
            fill_opacity=1,
        )
        label = Text(f"f[{index}]", font=MONO_FONT, weight="BOLD", font_size=16, color=MUTED)
        value_text = Text(value, font=MONO_FONT, weight="BOLD", font_size=25, color=WHITE)
        VGroup(label, value_text).arrange(DOWN, buff=0.02).move_to(box.get_center())
        return VGroup(box, label, value_text)

    def make_ghost_cell(self, label):
        box = RoundedRectangle(
            width=0.86,
            height=0.56,
            corner_radius=0.08,
            stroke_width=1.8,
            stroke_color=CELL_STROKE,
            fill_color=DIM_FILL,
            fill_opacity=1,
        )
        text = Text(label, font=MONO_FONT, weight="BOLD", font_size=16, color=WHITE)
        text.move_to(box.get_center())
        return VGroup(box, text)

    def make_state_box(self, name, formula, hint, color):
        box = RoundedRectangle(
            width=2.26,
            height=1.24,
            corner_radius=0.08,
            stroke_width=2.5,
            stroke_color=color,
            fill_color=CELL_FILL,
            fill_opacity=1,
        )
        name_text = Text(name, font=MONO_FONT, weight="BOLD", font_size=34, color=color)
        formula_text = Text(formula, font=MONO_FONT, weight="BOLD", font_size=20, color=WHITE)
        hint_text = Text(hint, font=FONT, font_size=18, color=MUTED)
        VGroup(name_text, formula_text, hint_text).arrange(DOWN, buff=0.05).move_to(box.get_center())
        return VGroup(box, name_text, formula_text, hint_text)

    def make_variable_box(self, name, value, color, hint):
        box = RoundedRectangle(
            width=1.72,
            height=1.42,
            corner_radius=0.08,
            stroke_width=2.4,
            stroke_color=color,
            fill_color=CELL_FILL,
            fill_opacity=1,
        )
        name_text = Text(name, font=MONO_FONT, weight="BOLD", font_size=23, color=color)
        value_text = self.make_box_value(value, box.get_center() + UP * 0.04)
        hint_text = Text(hint, font=FONT, font_size=18, color=MUTED)
        name_text.move_to(box.get_center() + UP * 0.43)
        hint_text.move_to(box.get_center() + DOWN * 0.45)
        group = VGroup(box, name_text, value_text, hint_text)
        group.value = value_text
        return group

    def make_box_value(self, value, center):
        value_text = Text(value, font=MONO_FONT, weight="BOLD", font_size=36, color=WHITE)
        value_text.move_to(center)
        return value_text

    def make_update_tag(self, text, color):
        box = RoundedRectangle(
            width=1.08,
            height=0.38,
            corner_radius=0.08,
            stroke_width=1.8,
            stroke_color=color,
            fill_color=CODE_FILL,
            fill_opacity=1,
        )
        label = Text(text, font=MONO_FONT, weight="BOLD", font_size=17, color=color)
        label.move_to(box.get_center())
        return VGroup(box, label)

    def make_formula_card(self, text):
        box = RoundedRectangle(
            width=3.66,
            height=0.7,
            corner_radius=0.08,
            stroke_width=2.4,
            stroke_color=FORMULA_STROKE,
            fill_color=FORMULA_FILL,
            fill_opacity=0.98,
        )
        label = Text(text, font=MONO_FONT, weight="BOLD", font_size=25, color=WHITE)
        label.move_to(box.get_center())
        return VGroup(box, label)

    def make_dependency_arrows(self, left_cell, right_cell, target_cell):
        left_arrow = Arrow(
            left_cell.get_top() + UP * 0.1,
            target_cell.get_top() + LEFT * 0.13 + UP * 0.1,
            buff=0.08,
            color=OLD_STATE,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.16,
        )
        right_arrow = Arrow(
            right_cell.get_top() + UP * 0.1,
            target_cell.get_top() + RIGHT * 0.13 + UP * 0.1,
            buff=0.08,
            color=CURRENT_STATE,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.16,
        )
        return VGroup(left_arrow, right_arrow)

    def make_code_block(self, lines):
        title = Text("O(1) 滚动变量写法", font=FONT, weight="BOLD", font_size=22, color=CURRENT_STATE)
        code_lines = VGroup(*[Text(line, font=MONO_FONT, font_size=18, color=MUTED) for line in lines])
        code_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.11)
        content = VGroup(title, code_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        box = RoundedRectangle(
            width=5.55,
            height=3.08,
            corner_radius=0.08,
            stroke_width=2.2,
            stroke_color=CURRENT_STATE,
            fill_color=CODE_FILL,
            fill_opacity=0.96,
        )
        content.move_to(box.get_center()).align_to(box, LEFT).shift(RIGHT * 0.28)
        group = VGroup(box, content)
        group.lines = code_lines
        return group

    def make_space_transition(self):
        left = self.make_space_card("数组空间", "O(n)", OLD_STATE)
        right = self.make_space_card("变量空间", "O(1)", NEW_STATE)
        arrow = Arrow(LEFT, RIGHT, color=TRACE_COLOR, stroke_width=3, buff=0.18)
        group = VGroup(left, arrow, right).arrange(RIGHT, buff=0.22)
        return group

    def make_space_card(self, label, value, color):
        box = RoundedRectangle(
            width=1.34,
            height=1.02,
            corner_radius=0.08,
            stroke_width=2.1,
            stroke_color=color,
            fill_color=CELL_FILL,
            fill_opacity=1,
        )
        label_text = Text(label, font=FONT, font_size=17, color=MUTED)
        value_text = Text(value, font=MONO_FONT, weight="BOLD", font_size=27, color=color)
        VGroup(label_text, value_text).arrange(DOWN, buff=0.08).move_to(box.get_center())
        return VGroup(box, label_text, value_text)

    def make_summary_item(self, number, text):
        dot = Circle(radius=0.2, stroke_width=0, fill_color=POINTER_BLUE, fill_opacity=1)
        number_text = Text(number, font=MONO_FONT, weight="BOLD", font_size=18, color=BACKGROUND)
        number_text.move_to(dot.get_center())
        label = Text(text, font=FONT, font_size=26, color=WHITE)
        return VGroup(VGroup(dot, number_text), label).arrange(RIGHT, buff=0.16)
