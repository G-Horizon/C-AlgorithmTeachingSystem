from manim import DOWN, Text, Triangle, VGroup, WHITE, RoundedRectangle

from theme import CELL_FILL, CELL_STROKE, FONT, SORTED_FILL


def make_array_cell(value):
    box = RoundedRectangle(
        width=1.08,
        height=1.08,
        corner_radius=0.1,
        stroke_width=2.5,
        stroke_color=CELL_STROKE,
        fill_color=CELL_FILL,
        fill_opacity=1,
    )
    number = Text(str(value), font=FONT, weight="BOLD", font_size=38, color=WHITE)
    number.move_to(box.get_center())
    return VGroup(box, number)


def make_indices(slot_positions):
    labels = VGroup()
    for index, position in enumerate(slot_positions):
        label = Text(str(index), font=FONT, font_size=20, color="#94a3b8")
        label.move_to(position + DOWN * 0.86)
        labels.add(label)
    return labels


def make_pointer(label, color):
    triangle = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.12)
    text = Text(label, font=FONT, font_size=22, color=color)
    text.next_to(triangle, DOWN, buff=0.05)
    return VGroup(triangle, text)


def pointer_position(slot_position):
    return slot_position + DOWN * 1.15


def place_pointer(pointer, slot_position):
    pointer.move_to(pointer_position(slot_position))


def color_cell(cell, fill, stroke):
    return cell[0].animate.set_fill(fill, opacity=1).set_stroke(stroke, width=3.5)


def reset_cell(cell):
    return cell[0].animate.set_fill(CELL_FILL, opacity=1).set_stroke(CELL_STROKE, width=2.5)


def mark_sorted(cell):
    return cell[0].animate.set_fill(SORTED_FILL, opacity=1).set_stroke("#bbf7d0", width=3)

