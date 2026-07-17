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
    SWAP_FILL,
)


MIN_FILL = "#2563eb"
MIN_STROKE = "#93c5fd"


class SelectionSortVisualization(Scene):
    """A storyboard-style Selection Sort visualization."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        values = [6, 3, 5, 1, 4]
        cells = [make_array_cell(value) for value in values]
        array_group = VGroup(*cells).arrange(RIGHT, buff=0.22).move_to(ORIGIN)
        slot_positions = [cell.get_center() for cell in cells]

        title, subtitle = self.show_intro()
        self.play(VGroup(title, subtitle).animate.to_edge(UP, buff=0.25).scale(0.72), run_time=0.8)

        caption = Text("初始数组", font=FONT, font_size=28, color=MUTED)
        caption.next_to(array_group, UP, buff=0.45)
        indices = make_indices(slot_positions)

        self.play(
            FadeIn(caption, shift=DOWN * 0.2),
            LaggedStart(*[FadeIn(cell, shift=UP * 0.25) for cell in cells], lag_ratio=0.12),
            FadeIn(indices),
            run_time=1.2,
        )
        self.wait(0.5)

        status = Text("每一轮：在未排序区找最小值", font=FONT, font_size=28, color=WHITE)
        status.to_edge(DOWN, buff=0.38)
        self.play(FadeIn(status, shift=UP * 0.15), run_time=0.6)

        i_pointer = make_pointer("i", POINTER_BLUE)
        j_pointer = make_pointer("j", POINTER_PINK)
        min_pointer = make_pointer("min", "#a78bfa")
        pointers = VGroup(i_pointer, j_pointer, min_pointer)

        place_pointer(i_pointer, slot_positions[0])
        place_pointer(j_pointer, slot_positions[1])
        min_pointer.move_to(pointer_position(slot_positions[0]) + DOWN * 0.52)

        comparison_text = Text("", font=FONT, font_size=32, color=WHITE)
        comparison_text.move_to(UP * 1.72)

        self.play(FadeIn(pointers), run_time=0.45)

        n = len(values)
        for i in range(n - 1):
            fast = i >= 2
            pass_label = Text(f"第 {i + 1} 轮：确定位置 {i}", font=FONT, font_size=30, color="#bae6fd")
            pass_label.to_edge(LEFT, buff=0.7).to_edge(UP, buff=1.1)
            self.play(Transform(caption, pass_label), run_time=0.35 if fast else 0.45)

            min_index = i
            self.play(
                i_pointer.animate.move_to(pointer_position(slot_positions[i])),
                min_pointer.animate.move_to(pointer_position(slot_positions[i]) + DOWN * 0.52),
                color_cell(cells[min_index], MIN_FILL, MIN_STROKE),
                run_time=0.35 if fast else 0.55,
            )

            assume_text = Text(
                f"先假设 a[{i}] = {values[i]} 最小",
                font=FONT,
                font_size=32,
                color=WHITE,
            )
            assume_text.move_to(UP * 1.72)
            self.play(Transform(comparison_text, assume_text), run_time=0.3 if fast else 0.45)

            for j in range(i + 1, n):
                self.play(
                    j_pointer.animate.move_to(pointer_position(slot_positions[j])),
                    run_time=0.18 if fast else 0.32,
                )

                left_value = values[j]
                min_value = values[min_index]
                better = left_value < min_value
                relation = "<" if better else ">="
                action = "更新 minIndex" if better else "保持不变"
                next_comparison = Text(
                    f"a[{j}]={left_value} {relation} {min_value}，{action}",
                    font=FONT,
                    font_size=32,
                    color=WHITE,
                )
                next_comparison.move_to(UP * 1.72)

                self.play(
                    color_cell(cells[j], COMPARE_FILL, "#fde68a"),
                    Transform(comparison_text, next_comparison),
                    run_time=0.2 if fast else 0.38,
                )
                self.wait(0.06 if fast else 0.18)

                if better:
                    old_min_index = min_index
                    min_index = j
                    self.play(
                        reset_cell(cells[old_min_index]),
                        color_cell(cells[min_index], MIN_FILL, MIN_STROKE),
                        min_pointer.animate.move_to(pointer_position(slot_positions[min_index]) + DOWN * 0.52),
                        run_time=0.24 if fast else 0.45,
                    )
                else:
                    self.play(reset_cell(cells[j]), run_time=0.12 if fast else 0.22)

            if min_index != i:
                swap_text = Text(
                    f"把最小值 {values[min_index]} 交换到位置 {i}",
                    font=FONT,
                    font_size=32,
                    color=WHITE,
                )
                swap_text.move_to(UP * 1.72)
                self.play(
                    Transform(comparison_text, swap_text),
                    color_cell(cells[i], SWAP_FILL, "#fed7aa"),
                    color_cell(cells[min_index], SWAP_FILL, "#fed7aa"),
                    run_time=0.28 if fast else 0.42,
                )
                self.play(
                    cells[i].animate(path_arc=-PI / 2).move_to(slot_positions[min_index]),
                    cells[min_index].animate(path_arc=PI / 2).move_to(slot_positions[i]),
                    run_time=0.45 if fast else 0.75,
                )
                cells[i], cells[min_index] = cells[min_index], cells[i]
                values[i], values[min_index] = values[min_index], values[i]
            else:
                keep_text = Text("最小值已经在当前位置，无需交换", font=FONT, font_size=32, color=WHITE)
                keep_text.move_to(UP * 1.72)
                self.play(Transform(comparison_text, keep_text), run_time=0.28 if fast else 0.42)

            self.play(mark_sorted(cells[i]), run_time=0.32 if fast else 0.45)
            summary = Text("已排序区向右扩大一格", font=FONT, font_size=28, color=WHITE)
            summary.to_edge(DOWN, buff=0.38)
            self.play(Transform(status, summary), run_time=0.28 if fast else 0.4)
            self.wait(0.12 if fast else 0.35)

        self.play(mark_sorted(cells[-1]), run_time=0.4)
        final_caption = Text("排序完成：[1, 3, 4, 5, 6]", font=FONT, font_size=34, color="#bbf7d0")
        final_caption.next_to(VGroup(*cells), UP, buff=0.5)
        self.play(
            Transform(caption, final_caption),
            FadeOut(pointers),
            FadeOut(indices),
            FadeOut(comparison_text),
            FadeOut(status),
            run_time=0.8,
        )
        self.wait(0.7)

        self.show_pseudocode_and_complexity(cells, caption)

    def show_intro(self):
        title = Text("选择排序 Selection Sort", font=FONT, weight="BOLD", font_size=54, color=WHITE)
        subtitle = Text(
            "每一轮选择未排序区的最小值，放到当前最左侧",
            font=FONT,
            font_size=28,
            color=MUTED,
        )
        subtitle.next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(title, shift=UP * 0.2), Write(subtitle), run_time=1.3)
        self.wait(0.6)
        return title, subtitle

    def show_pseudocode_and_complexity(self, cells, caption):
        final_array = VGroup(*cells, caption)
        self.play(final_array.animate.scale(0.78).to_edge(LEFT, buff=0.85), run_time=0.8)

        code_title = Text("核心伪代码", font=FONT, font_size=32, color=WHITE)
        code_lines = [
            "for i in range(n - 1):",
            "    minIndex = i",
            "    for j in range(i + 1, n):",
            "        if a[j] < a[minIndex]:",
            "            minIndex = j",
            "    swap(a[i], a[minIndex])",
        ]
        code = VGroup(
            *[Text(line, font=MONO_FONT, font_size=23, color=MUTED) for line in code_lines]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        code_group = VGroup(code_title, code).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        code_group.to_edge(RIGHT, buff=0.85).shift(UP * 0.45)

        self.play(FadeIn(code_title, shift=LEFT * 0.2), run_time=0.5)
        self.play(LaggedStart(*[Write(line) for line in code], lag_ratio=0.14), run_time=1.5)

        for line in code:
            self.play(line.animate.set_color("#fef3c7"), run_time=0.16)
            self.wait(0.08)
            self.play(line.animate.set_color(MUTED), run_time=0.14)

        complexity = VGroup(
            Text("时间复杂度：始终 O(n²)", font=FONT, font_size=28, color=WHITE),
            Text("空间复杂度：O(1)", font=FONT, font_size=28, color=WHITE),
            Text("特点：交换次数少，但不稳定", font=FONT, font_size=28, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        complexity.next_to(code_group, DOWN, buff=0.5, aligned_edge=LEFT)

        self.play(FadeIn(complexity, shift=UP * 0.2), run_time=0.8)
        self.wait(2.0)
