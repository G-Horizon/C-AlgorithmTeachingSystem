from pathlib import Path
import sys

from manim import *


COMMON_DIR = Path(__file__).resolve().parents[2] / "common"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from theme import BACKGROUND, CELL_FILL, CELL_STROKE, FONT, MONO_FONT, MUTED, POINTER_BLUE  # noqa: E402


STATE_FILL = "#1d4ed8"
STATE_STROKE = "#93c5fd"
QUESTION_FILL = "#334155"
QUESTION_STROKE = "#94a3b8"
KNOWN_FILL = "#15803d"
KNOWN_STROKE = "#bbf7d0"
FOCUS_FILL = "#0f766e"
FOCUS_STROKE = "#5eead4"
WARN_FILL = "#7c2d12"
WARN_STROKE = "#fed7aa"


class RecurrenceStateVisualization(Scene):
    """Introduce recurrence state as a record of progress."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        title, subtitle = self.show_intro()
        self.play(VGroup(title, subtitle).animate.to_edge(UP, buff=0.22).scale(0.66), run_time=0.72)

        problem_group = self.show_big_question()
        stair_group = self.show_stair_states(problem_group)
        definition_group = self.show_definition(stair_group)
        table_group = self.show_question_table(problem_group, stair_group, definition_group)
        self.show_code_mapping(VGroup(title, subtitle), table_group)

    def show_intro(self):
        title = Text("递推算法：什么是状态", font=FONT, weight="BOLD", font_size=50, color=WHITE)
        subtitle = Text("先记录进度，再推出答案", font=FONT, font_size=28, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.24)
        self.play(FadeIn(title, shift=UP * 0.18), Write(subtitle), run_time=1.0)
        self.wait(0.35)
        return title, subtitle

    def show_big_question(self):
        card = RoundedRectangle(
            width=6.2,
            height=1.45,
            corner_radius=0.12,
            stroke_width=2.5,
            stroke_color=QUESTION_STROKE,
            fill_color=QUESTION_FILL,
            fill_opacity=0.96,
        )
        question = Text("走到第 n 阶有多少种方法？", font=FONT, weight="BOLD", font_size=34, color=WHITE)
        question.move_to(card.get_center())
        unknown = Text("n = ?", font=MONO_FONT, weight="BOLD", font_size=40, color="#fb923c")
        unknown.next_to(card, RIGHT, buff=0.45)
        hint = Text("只盯着终点，问题还是一大团", font=FONT, font_size=25, color=MUTED)
        hint.next_to(card, DOWN, buff=0.28)

        group = VGroup(card, question, unknown, hint)
        self.play(FadeIn(card, shift=UP * 0.1), Write(question), FadeIn(unknown, shift=LEFT * 0.12), run_time=0.85)
        self.play(FadeIn(hint, shift=UP * 0.12), run_time=0.45)
        self.wait(0.42)
        return group

    def show_stair_states(self, problem_group):
        self.play(problem_group.animate.scale(0.5).to_edge(LEFT, buff=0.42).shift(UP * 1.72), run_time=0.65)

        heading = Text("把终点拆成沿途进度", font=FONT, font_size=31, color=WHITE)
        heading.move_to(UP * 2.05 + RIGHT * 1.12)

        step_labels = ["0", "1", "2", "3", "4", "5", "i"]
        steps = VGroup()
        state_cards = VGroup()
        arrows = VGroup()

        for index, label in enumerate(step_labels):
            x = -3.35 + index * 1.05
            y = -1.52 + index * 0.18
            step = self.make_step(label)
            step.move_to(RIGHT * x + UP * y)
            steps.add(step)

            state_label = f"f[{label}]"
            if label == "i":
                state_label = "f[i]"
            state_card = self.make_state_card(state_label)
            state_card.move_to(step.get_center() + UP * 0.92)
            state_cards.add(state_card)

            arrows.add(Arrow(state_card.get_bottom(), step[0].get_top(), buff=0.08, color="#64748b", stroke_width=2.2))

        progress_note = Text("i 表示当前走到哪一阶", font=FONT, font_size=24, color="#bae6fd")
        progress_note.next_to(steps, DOWN, buff=0.46)

        self.play(FadeIn(heading, shift=UP * 0.12), run_time=0.45)
        self.play(LaggedStart(*[FadeIn(step, shift=UP * 0.12) for step in steps], lag_ratio=0.08), run_time=0.95)
        self.play(FadeIn(progress_note, shift=UP * 0.1), run_time=0.42)
        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.12) for card in state_cards], lag_ratio=0.07),
            FadeIn(arrows),
            run_time=1.05,
        )
        self.wait(0.35)

        group = VGroup(heading, steps, state_cards, arrows, progress_note)
        group.steps = steps
        group.state_cards = state_cards
        return group

    def show_definition(self, stair_group):
        box = RoundedRectangle(
            width=3.95,
            height=1.26,
            corner_radius=0.12,
            stroke_width=2.7,
            stroke_color=FOCUS_STROKE,
            fill_color="#134e4a",
            fill_opacity=0.96,
        )
        title = Text("把状态读成一句人话", font=FONT, font_size=18, color="#ccfbf1")
        meaning = Text("f[i] = 到第 i 阶的方法数", font=FONT, weight="BOLD", font_size=24, color=WHITE)
        rule = Text("状态 = 位置 + 记录的信息", font=FONT, font_size=17, color="#fef3c7")
        content = VGroup(title, meaning, rule).arrange(DOWN, buff=0.1)
        content.move_to(box.get_center())
        definition = VGroup(box, content)
        definition.to_edge(RIGHT, buff=0.28).shift(UP * 1.42)

        bottom_note = Text("f[i] 不是神秘符号，它只是第 i 阶的记录盒子", font=FONT, font_size=25, color=MUTED)
        bottom_note.to_edge(DOWN, buff=0.28)

        self.play(FadeIn(definition, shift=LEFT * 0.15), Write(bottom_note), run_time=0.75)

        for index in [2, 3, 6]:
            card = stair_group.state_cards[index]
            self.play(
                card[0].animate.set_fill(FOCUS_FILL, opacity=1).set_stroke(FOCUS_STROKE, width=3.2),
                stair_group.steps[index][0].animate.set_fill(FOCUS_FILL, opacity=1).set_stroke(FOCUS_STROKE, width=3.2),
                run_time=0.34,
            )
            self.play(
                card[0].animate.set_fill(STATE_FILL, opacity=1).set_stroke(STATE_STROKE, width=2.5),
                stair_group.steps[index][0].animate.set_fill(CELL_FILL, opacity=1).set_stroke(CELL_STROKE, width=2.3),
                run_time=0.22,
            )

        self.wait(0.35)
        group = VGroup(definition, bottom_note)
        group.card = definition
        group.note = bottom_note
        return group

    def show_question_table(self, problem_group, stair_group, definition_group):
        self.play(
            FadeOut(problem_group),
            FadeOut(stair_group),
            FadeOut(definition_group.note),
            definition_group.card.animate.scale(0.72).to_edge(UP, buff=0.28).shift(RIGHT * 1.3),
            run_time=0.65,
        )
        definition_group.remove(definition_group.note)

        heading = Text("从“问全部”变成“问每个位置”", font=FONT, font_size=32, color=WHITE)
        heading.to_edge(LEFT, buff=0.62).shift(UP * 1.65)

        question_cards = VGroup(
            self.make_small_question("到 0 阶？"),
            self.make_small_question("到 1 阶？"),
            self.make_small_question("到 2 阶？"),
            self.make_small_question("到 i 阶？"),
        ).arrange(RIGHT, buff=0.24)
        question_cards.next_to(heading, DOWN, buff=0.52, aligned_edge=LEFT)

        table = self.make_state_table()
        table.move_to(DOWN * 1.23)
        table_title = Text("状态表：每个格子负责一个小问题", font=FONT, font_size=23, color=MUTED)
        table_title.move_to(UP * 0.2)

        self.play(FadeIn(heading, shift=UP * 0.12), run_time=0.42)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.1) for card in question_cards], lag_ratio=0.1), run_time=0.85)
        self.play(FadeIn(table_title, shift=UP * 0.1), FadeIn(table, shift=UP * 0.12), run_time=0.75)

        values = ["1", "1", "?", "?", "?", "?"]
        for index, value in enumerate(values):
            self.play(self.update_table_value(table.cells[index], value, known=index < 2), run_time=0.28)

        note = Text("本节重点：先说清 f[i] 记录什么，下一节再推出公式", font=FONT, font_size=25, color="#bbf7d0")
        note.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note, shift=UP * 0.12), run_time=0.58)
        self.wait(0.55)

        group = VGroup(definition_group, heading, question_cards, table_title, table, note)
        group.table = table
        group.heading = heading
        group.question_cards = question_cards
        group.table_title = table_title
        return group

    def show_code_mapping(self, title_group, table_group):
        self.play(
            FadeOut(table_group.heading),
            FadeOut(table_group.question_cards),
            FadeOut(table_group.table_title),
            run_time=0.32,
        )
        table_group.remove(table_group.heading, table_group.question_cards, table_group.table_title)

        self.play(
            table_group.animate.scale(0.62).to_edge(LEFT, buff=0.35).shift(DOWN * 0.18),
            title_group.animate.scale(0.85).to_edge(UP, buff=0.18).shift(LEFT * 0.15),
            run_time=0.7,
        )

        code_title = Text("代码里先写状态含义", font=FONT, font_size=29, color=WHITE)
        code_lines = [
            "// f[i] 表示走到第 i 阶的方法数",
            "long long f[N];",
            "f[0] = 1;",
            "f[1] = 1;",
            "// 答案在 f[n]",
        ]
        code = VGroup(
            *[
                Text(
                    line,
                    font=FONT if "表示" in line or "答案" in line else MONO_FONT,
                    font_size=20 if "表示" in line or "答案" in line else 22,
                    color=MUTED,
                )
                for line in code_lines
            ]
        )
        code.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        code_group = VGroup(code_title, code).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        code_group.to_edge(RIGHT, buff=0.52).shift(UP * 0.15)

        self.play(FadeIn(code_title, shift=LEFT * 0.14), run_time=0.38)
        self.play(LaggedStart(*[FadeIn(line, shift=UP * 0.08) for line in code], lag_ratio=0.11), run_time=0.95)
        for line in [code[0], code[1], code[-1]]:
            self.play(line.animate.set_color("#fef3c7"), run_time=0.16)
            self.wait(0.08)
            self.play(line.animate.set_color(MUTED), run_time=0.14)

        summary = VGroup(
            self.make_summary_item("1", "它记录什么？"),
            self.make_summary_item("2", "下标表示什么？"),
            self.make_summary_item("3", "答案在哪个格子？"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        summary.next_to(code_group, DOWN, buff=0.46, aligned_edge=LEFT)

        self.play(FadeIn(summary, shift=UP * 0.16), run_time=0.75)
        self.wait(2.0)

    def make_step(self, label):
        box = RoundedRectangle(
            width=0.82,
            height=0.54,
            corner_radius=0.08,
            stroke_width=2.3,
            stroke_color=CELL_STROKE,
            fill_color=CELL_FILL,
            fill_opacity=1,
        )
        index = Text(label, font=MONO_FONT, weight="BOLD", font_size=25, color=WHITE)
        index.move_to(box.get_center())
        step_label = Text("阶", font=FONT, font_size=16, color=MUTED)
        step_label.next_to(box, DOWN, buff=0.08)
        return VGroup(box, index, step_label)

    def make_state_card(self, label):
        box = RoundedRectangle(
            width=0.92,
            height=0.48,
            corner_radius=0.08,
            stroke_width=2.5,
            stroke_color=STATE_STROKE,
            fill_color=STATE_FILL,
            fill_opacity=0.96,
        )
        text = Text(label, font=MONO_FONT, weight="BOLD", font_size=23, color=WHITE)
        text.move_to(box.get_center())
        return VGroup(box, text)

    def make_small_question(self, text):
        box = RoundedRectangle(
            width=1.64,
            height=0.68,
            corner_radius=0.09,
            stroke_width=2,
            stroke_color=QUESTION_STROKE,
            fill_color=QUESTION_FILL,
            fill_opacity=0.95,
        )
        label = Text(text, font=FONT, font_size=22, color=WHITE)
        label.move_to(box.get_center())
        return VGroup(box, label)

    def make_state_table(self):
        cells = VGroup()
        labels = ["f[0]", "f[1]", "f[2]", "f[3]", "...", "f[n]"]
        value_labels = ["1", "1", "?", "?", "?", "?"]
        for index, label in enumerate(labels):
            box = RoundedRectangle(
                width=1.18,
                height=1.05,
                corner_radius=0.08,
                stroke_width=2.2,
                stroke_color=CELL_STROKE,
                fill_color=CELL_FILL,
                fill_opacity=1,
            )
            top = Text(label, font=MONO_FONT, font_size=21, color="#bae6fd")
            value = Text(value_labels[index], font=MONO_FONT, weight="BOLD", font_size=28, color=WHITE)
            top.move_to(box.get_center() + UP * 0.23)
            value.move_to(box.get_center() + DOWN * 0.22)
            value.set_opacity(0)
            cell = VGroup(box, top, value)
            cell.value = value
            cells.add(cell)

        cells.arrange(RIGHT, buff=0.12)
        cells.cells = cells
        return cells

    def update_table_value(self, cell, value, known=False):
        color = "#bbf7d0" if known else WHITE
        animations = [cell.value.animate.set_opacity(1).set_color(color)]
        if known:
            animations.append(cell[0].animate.set_fill(KNOWN_FILL, opacity=1).set_stroke(KNOWN_STROKE, width=2.8))
        else:
            animations.append(cell[0].animate.set_fill(WARN_FILL, opacity=0.92).set_stroke(WARN_STROKE, width=2.3))
        return AnimationGroup(*animations)

    def make_summary_item(self, number, text):
        dot = Circle(radius=0.18, stroke_width=0, fill_color=POINTER_BLUE, fill_opacity=1)
        number_text = Text(number, font=MONO_FONT, weight="BOLD", font_size=17, color=BACKGROUND)
        number_text.move_to(dot.get_center())
        label = Text(text, font=FONT, font_size=24, color=WHITE)
        item = VGroup(VGroup(dot, number_text), label).arrange(RIGHT, buff=0.16)
        return item
