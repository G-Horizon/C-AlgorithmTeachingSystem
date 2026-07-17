from pathlib import Path
import sys

from manim import *


COMMON_DIR = Path(__file__).resolve().parents[2] / "common"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from array_widgets import (  # noqa: E402
    color_cell,
    make_array_cell,
    make_indices,
    make_pointer,
    mark_sorted,
    place_pointer,
    pointer_position,
    reset_cell,
)
from theme import (  # noqa: E402
    BACKGROUND,
    COMPARE_FILL,
    FONT,
    MONO_FONT,
    MUTED,
    POINTER_BLUE,
    POINTER_PINK,
)


COUNT_FILL = "#0f766e"
COUNT_STROKE = "#5eead4"
OUTPUT_FILL = "#2563eb"
OUTPUT_STROKE = "#93c5fd"


class CountingSortVisualization(Scene):
    """A storyboard-style Counting Sort visualization."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        values = [3, 1, 2, 3, 0, 2]
        max_value = 3
        counts = [0] * (max_value + 1)

        title, subtitle = self.show_intro()
        self.play(VGroup(title, subtitle).animate.to_edge(UP, buff=0.22).scale(0.7), run_time=0.8)

        input_cells = [make_array_cell(value) for value in values]
        input_group = VGroup(*input_cells).arrange(RIGHT, buff=0.18).shift(UP * 1.75)
        input_positions = [cell.get_center() for cell in input_cells]
        input_indices = make_indices(input_positions)
        input_label = Text("原数组：逐个扫描", font=FONT, font_size=26, color=MUTED)
        input_label.next_to(input_group, LEFT, buff=0.5)

        count_cells = [make_array_cell(0) for _ in range(max_value + 1)]
        count_group = VGroup(*count_cells).arrange(RIGHT, buff=0.36).move_to(ORIGIN)
        count_positions = [cell.get_center() for cell in count_cells]
        count_indices = make_indices(count_positions)
        count_label = Text("count 桶：下标就是数值", font=FONT, font_size=26, color=MUTED)
        count_label.next_to(count_group, LEFT, buff=0.5)

        output_cells = [make_array_cell(" ") for _ in values]
        output_group = VGroup(*output_cells).arrange(RIGHT, buff=0.18).shift(DOWN * 1.75)
        output_positions = [cell.get_center() for cell in output_cells]
        output_label = Text("输出数组：按桶展开", font=FONT, font_size=26, color=MUTED)
        output_label.next_to(output_group, LEFT, buff=0.5)

        self.play(
            FadeIn(input_label, shift=RIGHT * 0.2),
            LaggedStart(*[FadeIn(cell, shift=UP * 0.2) for cell in input_cells], lag_ratio=0.08),
            FadeIn(input_indices),
            run_time=1.0,
        )
        self.play(
            FadeIn(count_label, shift=RIGHT * 0.2),
            LaggedStart(*[FadeIn(cell, shift=UP * 0.2) for cell in count_cells], lag_ratio=0.08),
            FadeIn(count_indices),
            run_time=0.9,
        )
        self.play(
            FadeIn(output_label, shift=RIGHT * 0.2),
            LaggedStart(*[FadeIn(cell, shift=UP * 0.2) for cell in output_cells], lag_ratio=0.06),
            run_time=0.85,
        )

        scan_pointer = make_pointer("scan", POINTER_BLUE)
        bucket_pointer = make_pointer("x", POINTER_PINK)
        place_pointer(scan_pointer, input_positions[0])
        bucket_pointer.move_to(pointer_position(count_positions[values[0]]) + DOWN * 0.48)

        status = Text("第一步：统计每个数出现了几次", font=FONT, font_size=30, color=WHITE)
        status.to_edge(DOWN, buff=0.22)
        explanation = Text("", font=FONT, font_size=30, color=WHITE)
        explanation.move_to(UP * 0.95)

        self.play(FadeIn(VGroup(scan_pointer, bucket_pointer)), FadeIn(status, shift=UP * 0.15), run_time=0.55)

        for index, value in enumerate(values):
            fast = index >= 3
            text = Text(
                f"读到 a[{index}] = {value}，所以 count[{value}] 加 1",
                font=FONT,
                font_size=30,
                color=WHITE,
            )
            text.move_to(UP * 0.95)
            self.play(
                scan_pointer.animate.move_to(pointer_position(input_positions[index])),
                bucket_pointer.animate.move_to(pointer_position(count_positions[value]) + DOWN * 0.48),
                color_cell(input_cells[index], COMPARE_FILL, "#fde68a"),
                color_cell(count_cells[value], COUNT_FILL, COUNT_STROKE),
                Transform(explanation, text),
                run_time=0.34 if fast else 0.55,
            )
            counts[value] += 1
            self.play(self.update_cell_text(count_cells[value], counts[value]), run_time=0.24 if fast else 0.42)
            self.play(reset_cell(input_cells[index]), reset_cell(count_cells[value]), run_time=0.14 if fast else 0.24)

        counted = Text("统计完成：count[x] 记录了 x 的出现次数", font=FONT, font_size=30, color="#bbf7d0")
        counted.move_to(UP * 0.95)
        self.play(Transform(explanation, counted), run_time=0.55)
        self.wait(0.35)

        fill_status = Text("第二步：从小到大查看桶，把数写回输出数组", font=FONT, font_size=30, color=WHITE)
        fill_status.to_edge(DOWN, buff=0.22)
        self.play(Transform(status, fill_status), FadeOut(scan_pointer), run_time=0.55)

        write_pointer = make_pointer("write", POINTER_BLUE)
        place_pointer(write_pointer, output_positions[0])
        self.play(FadeIn(write_pointer), run_time=0.3)

        write_index = 0
        for value, amount in enumerate(counts):
            bucket_text = Text(
                f"count[{value}] = {amount}，写出 {amount} 个 {value}",
                font=FONT,
                font_size=30,
                color=WHITE,
            )
            bucket_text.move_to(UP * 0.95)
            self.play(
                bucket_pointer.animate.move_to(pointer_position(count_positions[value]) + DOWN * 0.48),
                color_cell(count_cells[value], COUNT_FILL, COUNT_STROKE),
                Transform(explanation, bucket_text),
                run_time=0.35,
            )

            for _ in range(amount):
                self.play(
                    write_pointer.animate.move_to(pointer_position(output_positions[write_index])),
                    color_cell(output_cells[write_index], OUTPUT_FILL, OUTPUT_STROKE),
                    run_time=0.24,
                )
                self.play(self.update_cell_text(output_cells[write_index], value), run_time=0.22)
                self.play(mark_sorted(output_cells[write_index]), run_time=0.14)
                write_index += 1

            self.play(reset_cell(count_cells[value]), run_time=0.18)

        final_text = Text("有序结果：[0, 1, 2, 2, 3, 3]", font=FONT, font_size=34, color="#bbf7d0")
        final_text.move_to(UP * 0.95)
        self.play(
            Transform(explanation, final_text),
            FadeOut(VGroup(bucket_pointer, write_pointer, status, input_indices, count_indices)),
            run_time=0.75,
        )
        self.wait(0.7)

        self.show_pseudocode_and_complexity(
            VGroup(input_group, input_label),
            VGroup(count_group, count_label),
            VGroup(output_group, output_label),
            explanation,
        )

    def update_cell_text(self, cell, value):
        label = Text(str(value), font=FONT, weight="BOLD", font_size=38, color=WHITE)
        label.move_to(cell[0].get_center())
        return Transform(cell[1], label)

    def show_intro(self):
        title = Text("计数排序 Counting Sort", font=FONT, weight="BOLD", font_size=54, color=WHITE)
        subtitle = Text(
            "不再两两比较：用一个计数桶记住每个数出现了几次",
            font=FONT,
            font_size=28,
            color=MUTED,
        )
        subtitle.next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(title, shift=UP * 0.2), Write(subtitle), run_time=1.3)
        self.wait(0.55)
        return title, subtitle

    def show_pseudocode_and_complexity(self, input_group, count_group, output_group, explanation):
        arrays = VGroup(input_group, count_group, output_group, explanation)
        self.play(arrays.animate.scale(0.68).to_edge(LEFT, buff=0.42), run_time=0.8)

        code_title = Text("核心伪代码", font=FONT, font_size=32, color=WHITE)
        code_lines = [
            "for x in a:",
            "    count[x] += 1",
            "for value in range(K):",
            "    repeat count[value] times:",
            "        output.push_back(value)",
        ]
        code = VGroup(
            *[Text(line, font=MONO_FONT, font_size=22, color=MUTED) for line in code_lines]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        code_group = VGroup(code_title, code).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        code_group.to_edge(RIGHT, buff=0.75).shift(UP * 0.6)

        self.play(FadeIn(code_title, shift=LEFT * 0.2), run_time=0.5)
        self.play(LaggedStart(*[Write(line) for line in code], lag_ratio=0.14), run_time=1.35)

        for line in code:
            self.play(line.animate.set_color("#fef3c7"), run_time=0.14)
            self.wait(0.06)
            self.play(line.animate.set_color(MUTED), run_time=0.12)

        complexity = VGroup(
            Text("时间复杂度：O(n + K)", font=FONT, font_size=28, color=WHITE),
            Text("空间复杂度：O(K)", font=FONT, font_size=28, color=WHITE),
            Text("适用场景：数值范围 K 不大，且能映射到下标", font=FONT, font_size=28, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        complexity.next_to(code_group, DOWN, buff=0.55, aligned_edge=LEFT)

        self.play(FadeIn(complexity, shift=UP * 0.2), run_time=0.8)
        self.wait(2.0)
