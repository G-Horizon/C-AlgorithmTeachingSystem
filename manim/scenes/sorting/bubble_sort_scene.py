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


class BubbleSortVisualization(Scene):
    """A storyboard-style Bubble Sort visualization."""

    def construct(self):
        self.camera.background_color = BACKGROUND

        values = [5, 1, 4, 2, 8]
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

        status = Text("从左到右扫描：比较相邻元素", font=FONT, font_size=28, color=WHITE)
        status.to_edge(DOWN, buff=0.38)
        self.play(FadeIn(status, shift=UP * 0.15), run_time=0.6)

        left_pointer = make_pointer("j", POINTER_BLUE)
        right_pointer = make_pointer("j+1", POINTER_PINK)
        pointers = VGroup(left_pointer, right_pointer)
        place_pointer(left_pointer, slot_positions[0])
        place_pointer(right_pointer, slot_positions[1])

        comparison_text = Text("", font=FONT, font_size=34, color=WHITE)
        comparison_text.move_to(UP * 1.72)

        self.play(FadeIn(pointers), run_time=0.45)

        sorted_label = None
        n = len(values)
        for pass_index in range(n - 1):
            pass_number = pass_index + 1
            pass_label = Text(f"第 {pass_number} 轮", font=FONT, font_size=30, color="#bae6fd")
            pass_label.to_edge(LEFT, buff=0.7).to_edge(UP, buff=1.1)

            if pass_index == 0:
                self.play(Transform(caption, pass_label), run_time=0.45)
            else:
                self.play(Transform(caption, pass_label), run_time=0.35)

            upper = n - pass_index - 1
            for j in range(upper):
                fast = pass_index >= 2
                compare_run_time = 0.25 if fast else 0.45
                swap_run_time = 0.45 if fast else 0.75
                wait_time = 0.08 if fast else 0.25

                self.play(
                    left_pointer.animate.move_to(pointer_position(slot_positions[j])),
                    right_pointer.animate.move_to(pointer_position(slot_positions[j + 1])),
                    run_time=0.35 if not fast else 0.2,
                )

                left_value = values[j]
                right_value = values[j + 1]
                relation = ">" if left_value > right_value else "<="
                action = "交换" if left_value > right_value else "不交换"
                next_comparison = Text(
                    f"{left_value} {relation} {right_value}，{action}",
                    font=FONT,
                    font_size=34,
                    color=WHITE,
                )
                next_comparison.move_to(UP * 1.72)

                self.play(
                    color_cell(cells[j], COMPARE_FILL, "#fde68a"),
                    color_cell(cells[j + 1], COMPARE_FILL, "#fde68a"),
                    Transform(comparison_text, next_comparison),
                    run_time=compare_run_time,
                )
                self.wait(wait_time)

                if left_value > right_value:
                    self.play(
                        color_cell(cells[j], SWAP_FILL, "#fed7aa"),
                        color_cell(cells[j + 1], SWAP_FILL, "#fed7aa"),
                        run_time=0.18 if fast else 0.28,
                    )
                    self.play(
                        cells[j].animate(path_arc=-PI / 2).move_to(slot_positions[j + 1]),
                        cells[j + 1].animate(path_arc=PI / 2).move_to(slot_positions[j]),
                        run_time=swap_run_time,
                    )
                    cells[j], cells[j + 1] = cells[j + 1], cells[j]
                    values[j], values[j + 1] = values[j + 1], values[j]

                self.play(
                    reset_cell(cells[j]),
                    reset_cell(cells[j + 1]),
                    run_time=0.22 if not fast else 0.12,
                )

            sorted_index = n - pass_index - 1
            self.play(mark_sorted(cells[sorted_index]), run_time=0.45)

            sorted_region = VGroup(*cells[sorted_index:])
            new_sorted_label = Text("已排序区域", font=FONT, font_size=24, color="#86efac")
            new_sorted_label.next_to(sorted_region, UP, buff=0.18)

            if sorted_label is None:
                sorted_label = new_sorted_label
                self.play(FadeIn(sorted_label, shift=DOWN * 0.1), run_time=0.35)
            else:
                self.play(Transform(sorted_label, new_sorted_label), run_time=0.35)

            summary = Text(
                "本轮结束：当前最大值已经到达最终位置",
                font=FONT,
                font_size=28,
                color=WHITE,
            )
            summary.to_edge(DOWN, buff=0.38)
            self.play(Transform(status, summary), run_time=0.4)
            self.wait(0.35 if pass_index < 2 else 0.12)

        self.play(mark_sorted(cells[0]), run_time=0.4)
        final_caption = Text("排序完成：[1, 2, 4, 5, 8]", font=FONT, font_size=34, color="#bbf7d0")
        final_caption.next_to(VGroup(*cells), UP, buff=0.5)
        self.play(
            Transform(caption, final_caption),
            FadeOut(pointers),
            FadeOut(indices),
            FadeOut(comparison_text),
            FadeOut(status),
            FadeOut(sorted_label),
            run_time=0.8,
        )
        self.wait(0.7)

        self.show_pseudocode_and_complexity(cells, caption)

    def show_intro(self):
        title = Text("冒泡排序 Bubble Sort", font=FONT, weight="BOLD", font_size=56, color=WHITE)
        subtitle = Text(
            "相邻比较，必要时交换；每一轮把最大值推到右侧",
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
            "for i in range(n):",
            "    for j in range(n - i - 1):",
            "        if a[j] > a[j + 1]:",
            "            swap(a[j], a[j + 1])",
        ]
        code = VGroup(
            *[Text(line, font=MONO_FONT, font_size=24, color=MUTED) for line in code_lines]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        code_group = VGroup(code_title, code).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        code_group.to_edge(RIGHT, buff=0.95).shift(UP * 0.45)

        self.play(FadeIn(code_title, shift=LEFT * 0.2), run_time=0.5)
        self.play(LaggedStart(*[Write(line) for line in code], lag_ratio=0.18), run_time=1.4)

        for line in code:
            self.play(line.animate.set_color("#fef3c7"), run_time=0.18)
            self.wait(0.12)
            self.play(line.animate.set_color(MUTED), run_time=0.16)

        complexity = VGroup(
            Text("时间复杂度：平均 / 最坏 O(n²)", font=FONT, font_size=28, color=WHITE),
            Text("空间复杂度：O(1)", font=FONT, font_size=28, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        complexity.next_to(code_group, DOWN, buff=0.55, aligned_edge=LEFT)

        self.play(FadeIn(complexity, shift=UP * 0.2), run_time=0.8)
        self.wait(2.0)

