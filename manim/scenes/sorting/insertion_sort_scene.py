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


KEY_FILL = "#7c3aed"
KEY_STROKE = "#c4b5fd"


class InsertionSortVisualization(Scene):
    """A storyboard-style Insertion Sort visualization."""

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

        self.play(mark_sorted(cells[0]), run_time=0.45)

        status = Text("左侧区间保持有序；取出 key 插进去", font=FONT, font_size=28, color=WHITE)
        status.to_edge(DOWN, buff=0.38)
        self.play(FadeIn(status, shift=UP * 0.15), run_time=0.6)

        i_pointer = make_pointer("i", POINTER_BLUE)
        j_pointer = make_pointer("j", POINTER_PINK)
        pointers = VGroup(i_pointer, j_pointer)
        place_pointer(i_pointer, slot_positions[1])
        place_pointer(j_pointer, slot_positions[0])

        comparison_text = Text("", font=FONT, font_size=32, color=WHITE)
        comparison_text.move_to(UP * 1.72)
        self.play(FadeIn(pointers), run_time=0.45)

        n = len(values)
        for i in range(1, n):
            fast = i >= 3
            pass_label = Text(f"第 {i} 轮：把 a[{i}] 插入左侧有序区", font=FONT, font_size=28, color="#bae6fd")
            pass_label.to_edge(LEFT, buff=0.7).to_edge(UP, buff=1.1)
            self.play(Transform(caption, pass_label), run_time=0.35 if fast else 0.45)

            key_value = values[i]
            key_cell = cells[i]
            j = i - 1

            self.play(
                i_pointer.animate.move_to(pointer_position(slot_positions[i])),
                j_pointer.animate.move_to(pointer_position(slot_positions[j])),
                color_cell(key_cell, KEY_FILL, KEY_STROKE),
                run_time=0.32 if fast else 0.5,
            )
            self.play(key_cell.animate.move_to(slot_positions[i] + UP * 1.05), run_time=0.35 if fast else 0.55)

            take_text = Text(f"取出 key = {key_value}，当前位置变成空位", font=FONT, font_size=32, color=WHITE)
            take_text.move_to(UP * 1.72)
            self.play(Transform(comparison_text, take_text), run_time=0.3 if fast else 0.45)

            while j >= 0 and values[j] > key_value:
                compare_text = Text(
                    f"a[{j}]={values[j]} > key={key_value}，向右移动",
                    font=FONT,
                    font_size=32,
                    color=WHITE,
                )
                compare_text.move_to(UP * 1.72)
                self.play(
                    j_pointer.animate.move_to(pointer_position(slot_positions[j])),
                    color_cell(cells[j], COMPARE_FILL, "#fde68a"),
                    Transform(comparison_text, compare_text),
                    run_time=0.22 if fast else 0.38,
                )
                self.play(cells[j].animate.move_to(slot_positions[j + 1]), run_time=0.32 if fast else 0.55)
                values[j + 1] = values[j]
                cells[j + 1] = cells[j]
                j -= 1
                if j >= 0:
                    self.play(j_pointer.animate.move_to(pointer_position(slot_positions[j])), run_time=0.14 if fast else 0.24)

            insert_index = j + 1
            if j >= 0:
                stop_text = Text(
                    f"a[{j}]={values[j]} <= key={key_value}，停在它右边",
                    font=FONT,
                    font_size=32,
                    color=WHITE,
                )
            else:
                stop_text = Text("已经到达开头，key 插到最左侧", font=FONT, font_size=32, color=WHITE)
            stop_text.move_to(UP * 1.72)
            self.play(Transform(comparison_text, stop_text), run_time=0.25 if fast else 0.4)

            self.play(key_cell.animate.move_to(slot_positions[insert_index]), run_time=0.35 if fast else 0.58)
            values[insert_index] = key_value
            cells[insert_index] = key_cell

            for index in range(i + 1):
                self.play(mark_sorted(cells[index]), run_time=0.08 if fast else 0.12)

            summary = Text("key 已插回，左侧有序区扩大一格", font=FONT, font_size=28, color=WHITE)
            summary.to_edge(DOWN, buff=0.38)
            self.play(Transform(status, summary), run_time=0.28 if fast else 0.4)
            self.wait(0.1 if fast else 0.35)

        final_caption = Text("排序完成：[1, 2, 4, 5, 8]", font=FONT, font_size=34, color="#bbf7d0")
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
        title = Text("插入排序 Insertion Sort", font=FONT, weight="BOLD", font_size=54, color=WHITE)
        subtitle = Text(
            "像整理扑克牌：取出一张，插入左侧合适位置",
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
            "for i in range(1, n):",
            "    key = a[i]",
            "    j = i - 1",
            "    while j >= 0 and a[j] > key:",
            "        a[j + 1] = a[j]",
            "        j -= 1",
            "    a[j + 1] = key",
        ]
        code = VGroup(
            *[Text(line, font=MONO_FONT, font_size=22, color=MUTED) for line in code_lines]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        code_group = VGroup(code_title, code).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        code_group.to_edge(RIGHT, buff=0.7).shift(UP * 0.45)

        self.play(FadeIn(code_title, shift=LEFT * 0.2), run_time=0.5)
        self.play(LaggedStart(*[Write(line) for line in code], lag_ratio=0.13), run_time=1.5)

        for line in code:
            self.play(line.animate.set_color("#fef3c7"), run_time=0.14)
            self.wait(0.06)
            self.play(line.animate.set_color(MUTED), run_time=0.12)

        complexity = VGroup(
            Text("最好：O(n)，平均 / 最坏：O(n²)", font=FONT, font_size=28, color=WHITE),
            Text("空间复杂度：O(1)", font=FONT, font_size=28, color=WHITE),
            Text("特点：稳定，适合接近有序的数据", font=FONT, font_size=28, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        complexity.next_to(code_group, DOWN, buff=0.48, aligned_edge=LEFT)

        self.play(FadeIn(complexity, shift=UP * 0.2), run_time=0.8)
        self.wait(2.0)
