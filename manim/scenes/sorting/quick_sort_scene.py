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
    SWAP_FILL,
)


LESS_FILL = "#0f766e"
LESS_STROKE = "#5eead4"
GREATER_FILL = "#7c3aed"
GREATER_STROKE = "#c4b5fd"
PIVOT_FILL = "#dc2626"
PIVOT_STROKE = "#fecaca"


class QuickSortVisualization(Scene):
    """A storyboard-style Quick Sort partition visualization."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        title, subtitle = self.show_intro()
        self.play(VGroup(title, subtitle).animate.to_edge(UP, buff=0.22).scale(0.68), run_time=0.8)

        partition_group = self.show_partition_process()
        self.wait(0.65)
        self.show_pseudocode_and_complexity(partition_group)

    def show_intro(self):
        title = Text("快速排序 Quick Sort", font=FONT, weight="BOLD", font_size=54, color=WHITE)
        subtitle = Text(
            "先选一个基准值 pivot，把小的放左边，大的放右边，再递归处理两侧",
            font=FONT,
            font_size=28,
            color=MUTED,
        )
        subtitle.next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(title, shift=UP * 0.2), Write(subtitle), run_time=1.25)
        self.wait(0.55)
        return title, subtitle

    def show_partition_process(self):
        values = [5, 2, 7, 3, 6, 1, 4]
        pivot_value = values[-1]

        heading = Text("第一步：围绕 pivot 完成一次分区", font=FONT, font_size=30, color=WHITE)
        heading.to_edge(UP, buff=1.05)

        cells = [make_array_cell(value) for value in values]
        array_group = VGroup(*cells).arrange(RIGHT, buff=0.16).move_to(ORIGIN + UP * 0.45)
        slot_positions = [cell.get_center() for cell in cells]
        indices = make_indices(slot_positions)

        caption = Text("示例数组，选择最后一个元素作为 pivot", font=FONT, font_size=27, color=MUTED)
        caption.next_to(array_group, UP, buff=0.45)

        self.play(FadeIn(heading, shift=DOWN * 0.15), run_time=0.45)
        self.play(
            FadeIn(caption, shift=DOWN * 0.15),
            LaggedStart(*[FadeIn(cell, shift=UP * 0.2) for cell in cells], lag_ratio=0.08),
            FadeIn(indices),
            run_time=1.0,
        )

        pivot_index = len(values) - 1
        self.play(color_cell(cells[pivot_index], PIVOT_FILL, PIVOT_STROKE), run_time=0.35)

        i_pointer = make_pointer("i", POINTER_BLUE)
        j_pointer = make_pointer("j", POINTER_PINK)
        pivot_pointer = make_pointer("pivot", PIVOT_STROKE)
        i_pointer.move_to(pointer_position(slot_positions[0] + LEFT * 0.9))
        j_pointer.move_to(pointer_position(slot_positions[0]))
        pivot_pointer.move_to(pointer_position(slot_positions[pivot_index]) + DOWN * 0.55)
        pointers = VGroup(i_pointer, j_pointer, pivot_pointer)

        status = Text("i 左侧表示 <= pivot 的区域，j 负责向右扫描", font=FONT, font_size=30, color=WHITE)
        status.to_edge(DOWN, buff=0.28)
        explanation = Text("", font=FONT, font_size=30, color=WHITE)
        explanation.move_to(ORIGIN + DOWN * 0.85)

        self.play(FadeIn(pointers), FadeIn(status, shift=UP * 0.15), run_time=0.55)

        boundary = -1
        for scan in range(pivot_index):
            current = values[scan]
            is_small = current <= pivot_value
            relation = "<=" if is_small else ">"
            action = "放进左侧小区间" if is_small else "留在右侧候选区"
            text = Text(
                f"a[{scan}] = {current} {relation} pivot({pivot_value})，{action}",
                font=FONT,
                font_size=30,
                color=WHITE,
            )
            text.move_to(ORIGIN + DOWN * 0.85)

            self.play(
                j_pointer.animate.move_to(pointer_position(slot_positions[scan])),
                color_cell(cells[scan], COMPARE_FILL, "#fde68a"),
                Transform(explanation, text),
                run_time=0.5,
            )

            if is_small:
                boundary += 1
                self.play(
                    i_pointer.animate.move_to(pointer_position(slot_positions[boundary])),
                    run_time=0.25,
                )
                if boundary != scan:
                    swap_text = Text(
                        f"交换 a[{boundary}] 和 a[{scan}]，扩大小区间",
                        font=FONT,
                        font_size=30,
                        color=WHITE,
                    )
                    swap_text.move_to(ORIGIN + DOWN * 0.85)
                    self.play(
                        Transform(explanation, swap_text),
                        color_cell(cells[boundary], SWAP_FILL, "#fed7aa"),
                        color_cell(cells[scan], SWAP_FILL, "#fed7aa"),
                        run_time=0.26,
                    )
                    self.swap_cells(cells, values, boundary, scan, slot_positions, run_time=0.58)

                self.play(color_cell(cells[boundary], LESS_FILL, LESS_STROKE), run_time=0.22)
            else:
                self.play(color_cell(cells[scan], GREATER_FILL, GREATER_STROKE), run_time=0.22)

        pivot_target = boundary + 1
        place_text = Text(
            f"扫描结束，把 pivot 放到位置 {pivot_target}，它的最终位置确定",
            font=FONT,
            font_size=30,
            color=WHITE,
        )
        place_text.move_to(ORIGIN + DOWN * 0.85)
        self.play(Transform(explanation, place_text), run_time=0.45)
        self.play(
            color_cell(cells[pivot_target], SWAP_FILL, "#fed7aa"),
            color_cell(cells[pivot_index], PIVOT_FILL, PIVOT_STROKE),
            run_time=0.28,
        )
        self.swap_cells(cells, values, pivot_target, pivot_index, slot_positions, run_time=0.68)
        self.play(mark_sorted(cells[pivot_target]), run_time=0.35)

        for index in range(pivot_target):
            self.play(color_cell(cells[index], LESS_FILL, LESS_STROKE), run_time=0.08)
        for index in range(pivot_target + 1, len(cells)):
            self.play(color_cell(cells[index], GREATER_FILL, GREATER_STROKE), run_time=0.08)

        final_text = Text("分区完成：左边 <= 4，右边 > 4；接下来递归处理两侧", font=FONT, font_size=32, color="#bbf7d0")
        final_text.move_to(ORIGIN + DOWN * 0.85)
        self.play(
            Transform(explanation, final_text),
            FadeOut(VGroup(i_pointer, j_pointer, pivot_pointer, status, indices)),
            run_time=0.75,
        )

        return VGroup(heading, caption, VGroup(*cells), explanation)

    def swap_cells(self, cells, values, first, second, slot_positions, run_time=0.6):
        if first == second:
            return
        self.play(
            cells[first].animate(path_arc=-PI / 2).move_to(slot_positions[second]),
            cells[second].animate(path_arc=PI / 2).move_to(slot_positions[first]),
            run_time=run_time,
        )
        cells[first], cells[second] = cells[second], cells[first]
        values[first], values[second] = values[second], values[first]

    def show_pseudocode_and_complexity(self, partition_group):
        self.play(partition_group.animate.scale(0.68).to_edge(LEFT, buff=0.42), run_time=0.8)

        code_title = Text("核心伪代码", font=FONT, font_size=32, color=WHITE)
        code_lines = [
            "quickSort(l, r):",
            "    if l >= r: return",
            "    pivot = a[r]",
            "    pos = partition(l, r)",
            "    quickSort(l, pos - 1)",
            "    quickSort(pos + 1, r)",
        ]
        code = VGroup(
            *[Text(line, font=MONO_FONT, font_size=22, color=MUTED) for line in code_lines]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        code_group = VGroup(code_title, code).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        code_group.to_edge(RIGHT, buff=0.75).shift(UP * 0.65)

        self.play(FadeIn(code_title, shift=LEFT * 0.2), run_time=0.45)
        self.play(LaggedStart(*[Write(line) for line in code], lag_ratio=0.12), run_time=1.35)

        for line in code:
            self.play(line.animate.set_color("#fef3c7"), run_time=0.14)
            self.wait(0.06)
            self.play(line.animate.set_color(MUTED), run_time=0.12)

        complexity = VGroup(
            Text("平均时间复杂度：O(n log n)", font=FONT, font_size=28, color=WHITE),
            Text("最坏时间复杂度：O(n^2)", font=FONT, font_size=28, color=WHITE),
            Text("空间复杂度：O(log n) 递归栈，排序不稳定", font=FONT, font_size=28, color=WHITE),
            Text("优化方向：随机 pivot 或三数取中", font=FONT, font_size=28, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        complexity.next_to(code_group, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(FadeIn(complexity, shift=UP * 0.2), run_time=0.75)
        self.wait(2.0)
