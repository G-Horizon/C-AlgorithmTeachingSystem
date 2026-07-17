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
GRID_FILL = "#312e81"
GRID_STROKE = "#a5b4fc"
RESULT_FILL = "#0f766e"
RESULT_STROKE = "#5eead4"
CARRY_FILL = "#7c3aed"
CARRY_STROKE = "#ddd6fe"


class BigIntegerMultiplyBigVisualization(Scene):
    """Visualize big integer multiplication with c[i + j] accumulation."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        a_digits = [3, 2, 1]
        b_digits = [5, 4]
        raw_values = [0, 0, 0, 0, 0]
        normalized_digits = [5, 3, 5, 5, 0]
        contributions = [
            (0, 0, 3, 5),
            (0, 1, 3, 4),
            (1, 0, 2, 5),
            (1, 1, 2, 4),
            (2, 0, 1, 5),
            (2, 1, 1, 4),
        ]

        title, subtitle = self.show_intro()
        self.play(VGroup(title, subtitle).animate.to_edge(UP, buff=0.22).scale(0.66), run_time=0.8)

        storage = self.show_reverse_storage()
        self.play(FadeOut(storage), run_time=0.45)

        a_row = self.make_digit_row("a", a_digits, UP * 1.85, "123 -> [3, 2, 1]")
        b_row = self.make_digit_row("b", b_digits, UP * 0.62, "45 -> [5, 4]")
        c_row = self.make_digit_row("c", raw_values, DOWN * 1.05, "先累加，后进位")

        grid = self.make_grid(a_digits, b_digits)
        grid.to_edge(RIGHT, buff=0.5).shift(UP * 0.72)

        formula = Text("核心规则：a[i] * b[j] 累加到 c[i + j]", font=FONT, font_size=29, color=WHITE)
        formula.move_to(DOWN * 2.82)
        status = Text("先不急着进位，像把每一片乘积都投递到对应格子里", font=FONT, font_size=26, color=MUTED)
        status.next_to(formula, UP, buff=0.16)

        self.play(
            LaggedStart(
                FadeIn(a_row, shift=UP * 0.18),
                FadeIn(b_row, shift=UP * 0.18),
                FadeIn(c_row, shift=UP * 0.18),
                FadeIn(grid, shift=LEFT * 0.16),
                lag_ratio=0.14,
            ),
            run_time=1.2,
        )
        self.play(Write(status), FadeIn(formula), run_time=0.75)

        rows = VGroup(a_row, b_row, c_row, grid, status, formula)
        for step_index, (i, j, a_value, b_value) in enumerate(contributions):
            fast = step_index >= 2
            target_index = i + j
            product = a_value * b_value
            raw_values[target_index] += product
            target_cell = c_row.cells[target_index]
            grid_cell = grid.cells[(j, i)]

            next_formula = Text(
                f"i={i}, j={j}: {a_value} * {b_value} = {product}，放入 c[{i}+{j}] = c[{target_index}]",
                font=FONT,
                font_size=27,
                color=WHITE,
            )
            next_formula.move_to(formula.get_center())

            self.play(
                color_cell(a_row.cells[i], COMPARE_FILL, "#fde68a"),
                color_cell(b_row.cells[j], COMPARE_FILL, "#fde68a"),
                grid_cell.animate.set_fill(GRID_FILL, opacity=1).set_stroke(GRID_STROKE, width=3.5),
                Transform(formula, next_formula),
                run_time=0.38 if fast else 0.58,
            )

            token = self.make_product_token(f"{a_value}x{b_value}", product)
            token.move_to(grid_cell.get_center())
            target_point = target_cell.get_center() + UP * 0.16
            self.play(FadeIn(token, scale=0.85), run_time=0.2 if fast else 0.3)
            self.play(token.animate.move_to(target_point), run_time=0.32 if fast else 0.48)

            update_text = Text(str(raw_values[target_index]), font=FONT, weight="BOLD", font_size=34, color=WHITE)
            update_text.move_to(target_cell[0].get_center())
            self.play(
                color_cell(target_cell, RESULT_FILL, RESULT_STROKE),
                Transform(target_cell[1], update_text),
                FadeOut(token, scale=0.8),
                run_time=0.32 if fast else 0.48,
            )

            after_status = Text(
                f"c[{target_index}] 现在是 {raw_values[target_index]}：同一格可以接住多次贡献",
                font=FONT,
                font_size=26,
                color="#bbf7d0",
            )
            after_status.move_to(status.get_center())
            self.play(Transform(status, after_status), run_time=0.25 if fast else 0.38)

            self.play(
                reset_cell(a_row.cells[i]),
                reset_cell(b_row.cells[j]),
                target_cell[0].animate.set_fill(CELL_FILL, opacity=1).set_stroke(CELL_STROKE, width=2.5),
                grid_cell.animate.set_fill(CELL_FILL, opacity=1).set_stroke(CELL_STROKE, width=2),
                run_time=0.18 if fast else 0.28,
            )

        raw_summary = Text("原始 c = [15, 22, 13, 4, 0]，这些数还不是最终数字", font=FONT, font_size=28, color="#fef3c7")
        raw_summary.move_to(status.get_center())
        self.play(Transform(status, raw_summary), run_time=0.55)
        self.wait(0.45)

        self.normalize_carry(c_row, formula, status, normalized_digits)

        answer = Text("c = [5, 3, 5, 5]，倒序输出 5535", font=FONT, font_size=31, color="#bbf7d0")
        answer.move_to(formula.get_center())
        self.play(Transform(formula, answer), run_time=0.55)
        self.wait(0.65)

        self.show_code_mapping(rows)

    def show_intro(self):
        title = Text("高精度乘高精度 Big Integer * Big Integer", font=FONT, weight="BOLD", font_size=46, color=WHITE)
        subtitle = Text(
            "竖式乘法的秘密：每一对数字的乘积，都落在下标 i + j 的位置",
            font=FONT,
            font_size=27,
            color=MUTED,
        )
        subtitle.next_to(title, DOWN, buff=0.24)
        self.play(FadeIn(title, shift=UP * 0.18), Write(subtitle), run_time=1.1)
        self.wait(0.45)
        return title, subtitle

    def show_reverse_storage(self):
        example = Text("示例：123 * 45", font=FONT, font_size=36, color=WHITE)
        example.move_to(UP * 1.48)

        vertical = VGroup(
            Text("  123", font=MONO_FONT, font_size=44, color=WHITE),
            Text("*  45", font=MONO_FONT, font_size=44, color=WHITE),
            Line(LEFT * 1.22, RIGHT * 1.22, color=MUTED, stroke_width=3),
            Text("  615", font=MONO_FONT, font_size=40, color="#bae6fd"),
            Text(" 4920", font=MONO_FONT, font_size=40, color="#fed7aa"),
            Line(LEFT * 1.22, RIGHT * 1.22, color=MUTED, stroke_width=3),
            Text(" 5535", font=MONO_FONT, font_size=44, color="#bbf7d0"),
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.07)
        vertical.next_to(example, DOWN, buff=0.28)

        hint = Text("代码里反向存储：a = [3, 2, 1]，b = [5, 4]", font=FONT, font_size=29, color=MUTED)
        hint.next_to(vertical, DOWN, buff=0.4)

        rule = Text("因为 10^i * 10^j = 10^(i+j)，所以乘积贡献给 c[i+j]", font=FONT, font_size=28, color="#fef3c7")
        rule.next_to(hint, DOWN, buff=0.3)

        self.play(FadeIn(example, shift=UP * 0.15), FadeIn(vertical, shift=UP * 0.18), run_time=0.9)
        self.play(Write(hint), FadeIn(rule, shift=UP * 0.16), run_time=0.85)
        self.wait(0.8)
        return VGroup(example, vertical, hint, rule)

    def make_digit_row(self, name, values, offset, caption):
        cells = [make_array_cell(value).scale(0.78) for value in values]
        cells_group = VGroup(*cells).arrange(RIGHT, buff=0.1).move_to(offset)
        indexes = make_indices([cell.get_center() for cell in cells])

        label = Text(name, font=MONO_FONT, font_size=28, color=WHITE)
        caption_text = Text(caption, font=FONT, font_size=17, color=MUTED)
        label_group = VGroup(label, caption_text).arrange(DOWN, buff=0.08)
        label_group.next_to(cells_group, LEFT, buff=0.28)

        row = VGroup(label_group, cells_group, indexes)
        row.cells = cells
        return row

    def make_grid(self, a_digits, b_digits):
        group = VGroup()
        cells = {}
        title = Text("乘法网格", font=FONT, font_size=25, color=WHITE)

        header = VGroup()
        empty = Text("", font=FONT, font_size=20)
        header.add(empty)
        for i, digit in enumerate(a_digits):
            header.add(Text(f"a{i}={digit}", font=MONO_FONT, font_size=20, color="#bae6fd"))
        header.arrange(RIGHT, buff=0.16)

        grid_rows = VGroup()
        for j, b_digit in enumerate(b_digits):
            row = VGroup(Text(f"b{j}={b_digit}", font=MONO_FONT, font_size=20, color="#fed7aa"))
            for i, a_digit in enumerate(a_digits):
                box = RoundedRectangle(
                    width=0.72,
                    height=0.56,
                    corner_radius=0.08,
                    stroke_width=2,
                    stroke_color=CELL_STROKE,
                    fill_color=CELL_FILL,
                    fill_opacity=1,
                )
                label = Text(f"c{i + j}", font=MONO_FONT, font_size=19, color=MUTED)
                label.move_to(box.get_center())
                cell = VGroup(box, label)
                cells[(j, i)] = cell
                row.add(cell)
            row.arrange(RIGHT, buff=0.16)
            grid_rows.add(row)
        grid_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)

        body = VGroup(header, grid_rows).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        group.add(title, body)
        group.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        group.cells = cells
        return group

    def make_product_token(self, label, value):
        box = RoundedRectangle(
            width=1.02,
            height=0.54,
            corner_radius=0.1,
            stroke_width=2.4,
            stroke_color=ACCENT_STROKE,
            fill_color=ACCENT,
            fill_opacity=0.95,
        )
        text = Text(f"{label}={value}", font=MONO_FONT, font_size=19, color=WHITE)
        text.move_to(box.get_center())
        return VGroup(box, text)

    def normalize_carry(self, c_row, formula, status, normalized_digits):
        raw_values = [15, 22, 13, 4, 0]
        carry_steps = [
            (0, 15, 5, 1, 23),
            (1, 23, 3, 2, 15),
            (2, 15, 5, 1, 5),
            (3, 5, 5, 0, 0),
        ]

        normalize_title = Text("第二阶段：统一处理进位", font=FONT, font_size=28, color="#fef3c7")
        normalize_title.move_to(status.get_center())
        normalize_formula = Text("从低位到高位：c[i+1] += c[i] / 10，c[i] %= 10", font=FONT, font_size=27, color=WHITE)
        normalize_formula.move_to(formula.get_center())
        self.play(Transform(status, normalize_title), Transform(formula, normalize_formula), run_time=0.55)

        for i, value, digit, carry, next_value in carry_steps:
            fast = i >= 1
            current = c_row.cells[i]
            self.play(color_cell(current, CARRY_FILL, CARRY_STROKE), run_time=0.28 if fast else 0.42)

            step_formula = Text(
                f"i={i}: {value} 留下 {digit}，进位 {carry} 加到下一格",
                font=FONT,
                font_size=27,
                color=WHITE,
            )
            step_formula.move_to(formula.get_center())
            self.play(Transform(formula, step_formula), run_time=0.25 if fast else 0.4)

            digit_label = Text(str(digit), font=FONT, weight="BOLD", font_size=34, color=WHITE)
            digit_label.move_to(current[0].get_center())
            animations = [Transform(current[1], digit_label), mark_sorted(current)]

            if carry > 0:
                next_cell = c_row.cells[i + 1]
                token = self.make_carry_token(carry)
                token.move_to(current.get_center() + UP * 0.58)
                self.play(FadeIn(token), run_time=0.16 if fast else 0.24)
                self.play(token.animate.move_to(next_cell.get_center() + UP * 0.58), run_time=0.24 if fast else 0.36)
                next_label = Text(str(next_value), font=FONT, weight="BOLD", font_size=34, color=WHITE)
                next_label.move_to(next_cell[0].get_center())
                animations.append(Transform(next_cell[1], next_label))
                animations.append(color_cell(next_cell, RESULT_FILL, RESULT_STROKE))
                animations.append(FadeOut(token))
                raw_values[i + 1] = next_value

            self.play(*animations, run_time=0.34 if fast else 0.5)
            if i + 1 < len(c_row.cells):
                self.play(reset_cell(c_row.cells[i + 1]), run_time=0.13 if fast else 0.18)

        trim = Text("最高位 c[4] = 0，清理前导零，结果只保留 [5, 3, 5, 5]", font=FONT, font_size=27, color="#fef3c7")
        trim.move_to(status.get_center())
        self.play(
            Transform(status, trim),
            c_row.cells[4].animate.set_fill("#334155", opacity=0.45).set_stroke("#64748b", width=1.5),
            run_time=0.55,
        )

    def make_carry_token(self, value):
        dot = Circle(radius=0.12, fill_color=CARRY_FILL, fill_opacity=1, stroke_color=CARRY_STROKE, stroke_width=2)
        label = Text(str(value), font=MONO_FONT, font_size=18, color=CARRY_STROKE)
        label.next_to(dot, UP, buff=0.04)
        return VGroup(dot, label)

    def show_code_mapping(self, scene_group):
        self.play(scene_group.animate.scale(0.48).to_edge(LEFT, buff=0.18).shift(UP * 0.02), run_time=0.75)

        code_title = Text("核心 C++ 代码", font=FONT, font_size=24, color=WHITE)
        code_lines = [
            "vector<int> c(n + m, 0);",
            "for (int i = 0; i < n; i++)",
            "  for (int j = 0; j < m; j++)",
            "    c[i+j] += a[i] * b[j];",
            "for (int i = 0; i < c.size(); i++) {",
            "  c[i+1] += c[i] / 10;",
            "  c[i] %= 10;",
            "}",
            "while (c.size() > 1 && c.back()==0)",
            "  c.pop_back();",
        ]
        code = Text(
            "\n".join(code_lines),
            font=MONO_FONT,
            font_size=15,
            color=MUTED,
            line_spacing=0.82,
        )
        code_group = VGroup(code_title, code).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        code_group.to_edge(RIGHT, buff=0.28).shift(DOWN * 0.12)

        self.play(FadeIn(code_title, shift=LEFT * 0.2), run_time=0.4)
        self.play(FadeIn(code, shift=UP * 0.12), run_time=0.75)

        details = VGroup(
            Text("先投递贡献，再整理进位", font=FONT, font_size=17, color=WHITE),
        )
        details.next_to(code_group, DOWN, buff=0.12, aligned_edge=LEFT)

        self.play(FadeIn(details, shift=UP * 0.18), run_time=0.65)
        self.wait(2.0)
