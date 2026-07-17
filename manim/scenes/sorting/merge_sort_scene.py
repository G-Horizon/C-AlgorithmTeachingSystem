from pathlib import Path
import sys

from manim import *


COMMON_DIR = Path(__file__).resolve().parents[2] / "common"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from array_widgets import (  # noqa: E402
    color_cell,
    make_array_cell,
    make_pointer,
    mark_sorted,
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
    SORTED_FILL,
)


LEFT_FILL = "#2563eb"
LEFT_STROKE = "#93c5fd"
RIGHT_FILL = "#7c3aed"
RIGHT_STROKE = "#c4b5fd"
OUTPUT_FILL = "#0f766e"
OUTPUT_STROKE = "#5eead4"


class MergeSortVisualization(Scene):
    """A storyboard-style Merge Sort visualization."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        values = [6, 3, 5, 1, 4, 2]

        title, subtitle = self.show_intro()
        self.play(VGroup(title, subtitle).animate.to_edge(UP, buff=0.22).scale(0.68), run_time=0.8)

        split_group = self.show_split_tree(values)
        self.wait(0.5)
        self.play(FadeOut(split_group), run_time=0.8)

        merge_group, final_array = self.show_merge_process()
        self.wait(0.65)
        self.show_pseudocode_and_complexity(merge_group, final_array)

    def show_intro(self):
        title = Text("归并排序 Merge Sort", font=FONT, weight="BOLD", font_size=54, color=WHITE)
        subtitle = Text(
            "先把数组不断拆小，再把有序小段稳定地合并成大段",
            font=FONT,
            font_size=28,
            color=MUTED,
        )
        subtitle.next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(title, shift=UP * 0.2), Write(subtitle), run_time=1.25)
        self.wait(0.55)
        return title, subtitle

    def show_split_tree(self, values):
        heading = Text("第一步：递归拆分，直到每段只剩 1 个元素", font=FONT, font_size=30, color=WHITE)
        heading.to_edge(UP, buff=1.05)

        layers = [
            [[6, 3, 5, 1, 4, 2]],
            [[6, 3, 5], [1, 4, 2]],
            [[6, 3], [5], [1, 4], [2]],
            [[6], [3], [5], [1], [4], [2]],
        ]
        y_positions = [2.0, 0.85, -0.3, -1.45]
        layer_groups = VGroup()

        for layer, y in zip(layers, y_positions):
            groups = VGroup(*[self.make_segment(segment, scale=0.55) for segment in layer])
            groups.arrange(RIGHT, buff=0.55).move_to(y * UP)
            layer_groups.add(groups)

        connector_group = VGroup()
        for upper_layer, lower_layer in zip(layer_groups[:-1], layer_groups[1:]):
            for child in lower_layer:
                parent = min(upper_layer, key=lambda item: abs(item.get_x() - child.get_x()))
                line = Line(
                    parent.get_bottom() + DOWN * 0.05,
                    child.get_top() + UP * 0.05,
                    color="#334155",
                    stroke_width=2,
                )
                connector_group.add(line)

        labels = VGroup(
            Text("拆", font=FONT, font_size=24, color="#bae6fd").next_to(layer_groups[0], LEFT, buff=0.38),
            Text("拆", font=FONT, font_size=24, color="#bae6fd").next_to(layer_groups[1], LEFT, buff=0.38),
            Text("拆到单点", font=FONT, font_size=24, color="#bbf7d0").next_to(layer_groups[3], LEFT, buff=0.38),
        )

        self.play(FadeIn(heading, shift=DOWN * 0.15), run_time=0.45)
        self.play(FadeIn(layer_groups[0], shift=UP * 0.2), run_time=0.55)
        for index in range(1, len(layer_groups)):
            self.play(
                LaggedStart(
                    FadeIn(layer_groups[index], shift=DOWN * 0.15),
                    FadeIn(connector_group[: len(connector_group) * index // (len(layer_groups) - 1)]),
                    lag_ratio=0.2,
                ),
                run_time=0.75,
            )
            self.play(FadeIn(labels[min(index - 1, len(labels) - 1)]), run_time=0.25)

        note = Text("单个元素天然有序，接下来开始向上合并", font=FONT, font_size=30, color="#bbf7d0")
        note.to_edge(DOWN, buff=0.32)
        self.play(FadeIn(note, shift=UP * 0.15), run_time=0.55)

        return VGroup(heading, layer_groups, connector_group, labels, note)

    def show_merge_process(self):
        heading = Text("第二步：合并两个有序段", font=FONT, font_size=30, color=WHITE)
        heading.to_edge(UP, buff=1.05)

        left_values = [3, 5, 6]
        right_values = [1, 2, 4]
        output_values = []

        left_cells = [make_array_cell(value) for value in left_values]
        right_cells = [make_array_cell(value) for value in right_values]
        output_cells = [make_array_cell(" ") for _ in range(6)]

        left_group = VGroup(*left_cells).arrange(RIGHT, buff=0.18).shift(UP * 1.0 + LEFT * 2.35)
        right_group = VGroup(*right_cells).arrange(RIGHT, buff=0.18).shift(UP * 1.0 + RIGHT * 2.35)
        output_group = VGroup(*output_cells).arrange(RIGHT, buff=0.18).shift(DOWN * 1.15)

        left_positions = [cell.get_center() for cell in left_cells]
        right_positions = [cell.get_center() for cell in right_cells]
        output_positions = [cell.get_center() for cell in output_cells]

        left_label = Text("左段：已有序", font=FONT, font_size=26, color=MUTED).next_to(left_group, UP, buff=0.3)
        right_label = Text("右段：已有序", font=FONT, font_size=26, color=MUTED).next_to(right_group, UP, buff=0.3)
        output_label = Text("合并结果", font=FONT, font_size=26, color=MUTED).next_to(output_group, UP, buff=0.35)

        self.play(FadeIn(heading, shift=DOWN * 0.15), run_time=0.45)
        self.play(
            LaggedStart(
                FadeIn(left_label),
                FadeIn(right_label),
                FadeIn(output_label),
                FadeIn(left_group, shift=UP * 0.2),
                FadeIn(right_group, shift=UP * 0.2),
                FadeIn(output_group, shift=UP * 0.2),
                lag_ratio=0.12,
            ),
            run_time=1.0,
        )

        i_pointer = make_pointer("i", POINTER_BLUE)
        j_pointer = make_pointer("j", POINTER_PINK)
        write_pointer = make_pointer("write", "#5eead4")
        i_pointer.move_to(pointer_position(left_positions[0]))
        j_pointer.move_to(pointer_position(right_positions[0]))
        write_pointer.move_to(pointer_position(output_positions[0]))
        pointers = VGroup(i_pointer, j_pointer, write_pointer)
        self.play(FadeIn(pointers), run_time=0.45)

        status = Text("每次比较两个段的最左端，把更小的写入结果", font=FONT, font_size=30, color=WHITE)
        status.to_edge(DOWN, buff=0.28)
        explanation = Text("", font=FONT, font_size=30, color=WHITE)
        explanation.move_to(ORIGIN + UP * 0.05)
        self.play(FadeIn(status, shift=UP * 0.15), run_time=0.45)

        i = 0
        j = 0
        write_index = 0
        while i < len(left_values) and j < len(right_values):
            left_value = left_values[i]
            right_value = right_values[j]
            choose_left = left_value <= right_value
            chosen = left_value if choose_left else right_value
            source_cell = left_cells[i] if choose_left else right_cells[j]
            source_fill = LEFT_FILL if choose_left else RIGHT_FILL
            source_stroke = LEFT_STROKE if choose_left else RIGHT_STROKE
            text = Text(
                f"比较 {left_value} 和 {right_value}，写入更小的 {chosen}",
                font=FONT,
                font_size=30,
                color=WHITE,
            )
            text.move_to(ORIGIN + UP * 0.05)

            self.play(
                i_pointer.animate.move_to(pointer_position(left_positions[i])),
                j_pointer.animate.move_to(pointer_position(right_positions[j])),
                write_pointer.animate.move_to(pointer_position(output_positions[write_index])),
                color_cell(left_cells[i], COMPARE_FILL, "#fde68a"),
                color_cell(right_cells[j], COMPARE_FILL, "#fde68a"),
                Transform(explanation, text),
                run_time=0.55,
            )
            self.play(color_cell(source_cell, source_fill, source_stroke), run_time=0.18)
            self.play(
                color_cell(output_cells[write_index], OUTPUT_FILL, OUTPUT_STROKE),
                self.update_cell_text(output_cells[write_index], chosen),
                run_time=0.32,
            )
            self.play(mark_sorted(output_cells[write_index]), reset_cell(left_cells[i]), reset_cell(right_cells[j]), run_time=0.22)

            output_values.append(chosen)
            if choose_left:
                i += 1
            else:
                j += 1
            write_index += 1

        while i < len(left_values):
            value = left_values[i]
            text = Text(f"右段已用完，直接接上左段剩余的 {value}", font=FONT, font_size=30, color=WHITE)
            text.move_to(ORIGIN + UP * 0.05)
            self.play(
                i_pointer.animate.move_to(pointer_position(left_positions[i])),
                write_pointer.animate.move_to(pointer_position(output_positions[write_index])),
                color_cell(left_cells[i], LEFT_FILL, LEFT_STROKE),
                Transform(explanation, text),
                run_time=0.42,
            )
            self.play(
                color_cell(output_cells[write_index], OUTPUT_FILL, OUTPUT_STROKE),
                self.update_cell_text(output_cells[write_index], value),
                run_time=0.28,
            )
            self.play(mark_sorted(output_cells[write_index]), reset_cell(left_cells[i]), run_time=0.18)
            output_values.append(value)
            i += 1
            write_index += 1

        while j < len(right_values):
            value = right_values[j]
            text = Text(f"左段已用完，直接接上右段剩余的 {value}", font=FONT, font_size=30, color=WHITE)
            text.move_to(ORIGIN + UP * 0.05)
            self.play(
                j_pointer.animate.move_to(pointer_position(right_positions[j])),
                write_pointer.animate.move_to(pointer_position(output_positions[write_index])),
                color_cell(right_cells[j], RIGHT_FILL, RIGHT_STROKE),
                Transform(explanation, text),
                run_time=0.42,
            )
            self.play(
                color_cell(output_cells[write_index], OUTPUT_FILL, OUTPUT_STROKE),
                self.update_cell_text(output_cells[write_index], value),
                run_time=0.28,
            )
            self.play(mark_sorted(output_cells[write_index]), reset_cell(right_cells[j]), run_time=0.18)
            output_values.append(value)
            j += 1
            write_index += 1

        final_text = Text("合并完成：[1, 2, 3, 4, 5, 6]", font=FONT, font_size=34, color="#bbf7d0")
        final_text.move_to(ORIGIN + UP * 0.05)
        self.play(
            Transform(explanation, final_text),
            FadeOut(VGroup(i_pointer, j_pointer, write_pointer, status)),
            run_time=0.65,
        )

        return (
            VGroup(heading, left_label, right_label, output_label, left_group, right_group, output_group, explanation),
            output_group,
        )

    def make_segment(self, values, scale=0.62):
        cells = [make_array_cell(value) for value in values]
        group = VGroup(*cells).arrange(RIGHT, buff=0.08).scale(scale)
        return group

    def update_cell_text(self, cell, value):
        label = Text(str(value), font=FONT, weight="BOLD", font_size=38, color=WHITE)
        label.move_to(cell[0].get_center())
        return Transform(cell[1], label)

    def show_pseudocode_and_complexity(self, merge_group, final_array):
        self.play(merge_group.animate.scale(0.66).to_edge(LEFT, buff=0.32), run_time=0.8)

        code_title = Text("核心伪代码", font=FONT, font_size=32, color=WHITE)
        code_lines = [
            "mergeSort(l, r):",
            "    if l == r: return",
            "    mid = (l + r) / 2",
            "    mergeSort(l, mid)",
            "    mergeSort(mid + 1, r)",
            "    merge two sorted halves",
        ]
        code = VGroup(
            *[Text(line, font=MONO_FONT, font_size=22, color=MUTED) for line in code_lines]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        code_group = VGroup(code_title, code).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        code_group.to_edge(RIGHT, buff=0.75).shift(UP * 0.6)

        self.play(FadeIn(code_title, shift=LEFT * 0.2), run_time=0.45)
        self.play(LaggedStart(*[Write(line) for line in code], lag_ratio=0.12), run_time=1.35)

        for line in code:
            self.play(line.animate.set_color("#fef3c7"), run_time=0.14)
            self.wait(0.05)
            self.play(line.animate.set_color(MUTED), run_time=0.12)

        complexity = VGroup(
            Text("时间复杂度：O(n log n)", font=FONT, font_size=28, color=WHITE),
            Text("空间复杂度：O(n)", font=FONT, font_size=28, color=WHITE),
            Text("特点：稳定排序，也能顺手统计逆序对", font=FONT, font_size=28, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        complexity.next_to(code_group, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(FadeIn(complexity, shift=UP * 0.2), run_time=0.75)
        self.wait(2.0)
