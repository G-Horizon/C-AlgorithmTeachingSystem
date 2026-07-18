from pathlib import Path
import sys

from manim import *


COMMON_DIR = Path(__file__).resolve().parents[2] / "common"
if str(COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(COMMON_DIR))

from theme import BACKGROUND, FONT, MONO_FONT, MUTED, POINTER_BLUE  # noqa: E402


BLUE = "#2563eb"
BLUE_LIGHT = "#93c5fd"
GREEN = "#15803d"
GREEN_LIGHT = "#bbf7d0"
ORANGE = "#c2410c"
ORANGE_LIGHT = "#fed7aa"
SLATE = "#1e293b"
SLATE_LIGHT = "#64748b"
PURPLE = "#7e22ce"
PURPLE_LIGHT = "#d8b4fe"


class RecursionScene(Scene):
    """Shared visual language for the nine recursion lessons."""

    pace_factor = 4.0

    def setup(self):
        self.camera.background_color = BACKGROUND

    def play(self, *animations, **kwargs):
        if "run_time" in kwargs:
            kwargs["run_time"] *= self.pace_factor
        return super().play(*animations, **kwargs)

    def wait(self, duration=1, *args, **kwargs):
        return super().wait(duration * self.pace_factor, *args, **kwargs)

    def intro(self, title, subtitle):
        heading = Text(title, font=FONT, weight="BOLD", font_size=43, color=WHITE)
        subheading = Text(subtitle, font=FONT, font_size=24, color=MUTED)
        group = VGroup(heading, subheading).arrange(DOWN, buff=0.18)
        self.play(FadeIn(heading, shift=UP * 0.14), Write(subheading), run_time=0.72)
        self.wait(0.18)
        self.play(group.animate.scale(0.68).to_edge(UP, buff=0.18), run_time=0.55)
        return group

    def card(self, text, width=2.1, height=0.78, fill=SLATE, stroke=SLATE_LIGHT, size=25, font=MONO_FONT):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.1,
            stroke_width=2.5,
            stroke_color=stroke,
            fill_color=fill,
            fill_opacity=0.97,
        )
        label = Text(text, font=font, weight="BOLD", font_size=size, color=WHITE)
        label.move_to(box)
        return VGroup(box, label)

    def note(self, text, color=GREEN_LIGHT):
        label = Text(text, font=FONT, weight="BOLD", font_size=26, color=color)
        label.to_edge(DOWN, buff=0.28)
        return label

    def code_panel(self, lines, title="代码映射", width=5.6):
        labels = VGroup(
            *[
                Text(line, font=MONO_FONT, font_size=20, color=WHITE if index else BLUE_LIGHT)
                for index, line in enumerate(lines)
            ]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        heading = Text(title, font=FONT, font_size=20, color=MUTED)
        content = VGroup(heading, labels).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        box = RoundedRectangle(
            width=width,
            height=content.height + 0.48,
            corner_radius=0.12,
            stroke_width=2,
            stroke_color=SLATE_LIGHT,
            fill_color="#111827",
            fill_opacity=0.98,
        )
        content.move_to(box)
        return VGroup(box, content)


class RecursionSelfCallVisualization(RecursionScene):
    def construct(self):
        self.intro("递归算法：函数为什么能调用自己", "同一种任务，规模一次比一次小")
        cards = VGroup(*[self.card(f"solve({n})", fill=BLUE, stroke=BLUE_LIGHT) for n in [4, 3, 2, 1]])
        cards.arrange(RIGHT, buff=0.62).shift(UP * 0.35)
        arrows = VGroup(
            *[Arrow(cards[i].get_right(), cards[i + 1].get_left(), buff=0.08, color=POINTER_BLUE) for i in range(3)]
        )
        scales = VGroup(*[Text(label, font=FONT, font_size=17, color=MUTED) for label in ["规模 4", "规模 3", "规模 2", "最小任务"]])
        for label, card in zip(scales, cards):
            label.next_to(card, DOWN, buff=0.16)
        self.play(LaggedStart(*[FadeIn(card, shift=RIGHT * 0.12) for card in cards], lag_ratio=0.17), FadeIn(arrows), run_time=1.15)
        self.play(FadeIn(scales), run_time=0.45)
        panel = self.code_panel(["void solve(int n) {", "  if (n == 1) return;", "  solve(n - 1);", "}"])
        panel.next_to(cards, DOWN, buff=0.62)
        self.play(FadeIn(panel, shift=UP * 0.12), run_time=0.65)
        self.play(cards[-1][0].animate.set_fill(GREEN).set_stroke(GREEN_LIGHT, width=3), run_time=0.38)
        footer = self.note("相似子问题 + 规模变小 + 最小任务 = 可终止的递归")
        self.play(FadeIn(footer, shift=UP * 0.1), run_time=0.5)
        self.wait(1.2)


class RecursionBaseCaseVisualization(RecursionScene):
    def construct(self):
        self.intro("递归算法：递归出口", "出口让压栈停止，让返回开始")
        bad = VGroup(*[self.card(f"solve({n})", width=1.7, fill="#7f1d1d", stroke="#fca5a5", size=21) for n in [3, 2, 1, 0, -1]])
        bad.arrange(UP, buff=0.12).to_edge(LEFT, buff=0.72).shift(DOWN * 0.15)
        bad_title = Text("没有可达出口", font=FONT, font_size=24, color="#fca5a5").next_to(bad, UP, buff=0.2)
        warning = Text("还在继续……", font=FONT, font_size=20, color=ORANGE_LIGHT).next_to(bad, DOWN, buff=0.18)
        self.play(FadeIn(bad_title), LaggedStart(*[FadeIn(card, shift=UP * 0.1) for card in bad], lag_ratio=0.1), FadeIn(warning), run_time=1.1)

        good = VGroup(*[self.card(f"solve({n})", width=1.7, fill=BLUE, stroke=BLUE_LIGHT, size=21) for n in [3, 2, 1]])
        good.arrange(UP, buff=0.12).to_edge(RIGHT, buff=0.72).shift(DOWN * 0.05)
        good[-1][0].set_fill(GREEN).set_stroke(GREEN_LIGHT)
        good_title = Text("n == 1：直接返回", font=FONT, font_size=24, color=GREEN_LIGHT).next_to(good, UP, buff=0.2)
        returns = VGroup(*[Arrow(good[i + 1].get_left(), good[i].get_left(), path_arc=-0.6, buff=0.1, color=GREEN_LIGHT) for i in range(2)])
        self.play(FadeIn(good_title), LaggedStart(*[FadeIn(card) for card in good], lag_ratio=0.12), run_time=0.8)
        self.play(Create(returns), run_time=0.6)
        footer = self.note("先处理最小问题：if (n == 1) return;")
        self.play(FadeIn(footer), run_time=0.45)
        self.wait(1.2)


class RecursionParameterVisualization(RecursionScene):
    def construct(self):
        self.intro("递归算法：参数变化", "每一层都要更靠近出口")
        route = VGroup(*[self.card(str(n), width=1.0, height=0.72, fill=PURPLE, stroke=PURPLE_LIGHT) for n in [5, 4, 3, 2, 1]])
        route.arrange(RIGHT, buff=0.64).shift(UP * 0.55)
        arrows = VGroup(*[Arrow(route[i].get_right(), route[i + 1].get_left(), buff=0.07, color=PURPLE_LIGHT) for i in range(4)])
        self.play(LaggedStart(*[FadeIn(card, shift=RIGHT * 0.1) for card in route], lag_ratio=0.12), Create(arrows), run_time=1.0)
        measure = Text("规模：5 → 4 → 3 → 2 → 1", font=FONT, font_size=29, color=WHITE)
        measure.next_to(route, DOWN, buff=0.5)
        self.play(Write(measure), run_time=0.6)
        bad = self.card("solve(n)", width=2.3, fill="#7f1d1d", stroke="#fca5a5")
        bad.next_to(measure, DOWN, buff=0.46).shift(LEFT * 1.4)
        bad_note = Text("参数不变：原地打转", font=FONT, font_size=21, color="#fca5a5").next_to(bad, DOWN, buff=0.15)
        good = self.card("solve(n - 1)", width=2.8, fill=GREEN, stroke=GREEN_LIGHT)
        good.next_to(measure, DOWN, buff=0.46).shift(RIGHT * 1.4)
        good_note = Text("严格变小：走向出口", font=FONT, font_size=21, color=GREEN_LIGHT).next_to(good, DOWN, buff=0.15)
        self.play(FadeIn(bad), FadeIn(bad_note), FadeIn(good), FadeIn(good_note), run_time=0.65)
        footer = self.note("调试第一步：手写前三层参数，确认它真的在前进")
        self.play(FadeIn(footer), run_time=0.45)
        self.wait(1.2)


class RecursionCallStackVisualization(RecursionScene):
    def construct(self):
        self.intro("递归算法：调用栈压入与弹出", "先后进，后先出；返回值逐层向上")
        frames = VGroup(*[self.card(f"sum({n})", width=2.3, fill=BLUE, stroke=BLUE_LIGHT) for n in [4, 3, 2, 1]])
        frames.arrange(UP, buff=0.1).to_edge(LEFT, buff=1.15).shift(DOWN * 0.2)
        stack_label = Text("调用栈", font=FONT, font_size=25, color=MUTED).next_to(frames, DOWN, buff=0.2)
        self.play(FadeIn(stack_label), LaggedStart(*[FadeIn(frame, shift=UP * 0.25) for frame in frames], lag_ratio=0.17), run_time=1.25)
        equations = VGroup(
            Text("sum(1) = 1", font=MONO_FONT, font_size=25, color=GREEN_LIGHT),
            Text("sum(2) = 2 + 1 = 3", font=MONO_FONT, font_size=25, color=WHITE),
            Text("sum(3) = 3 + 3 = 6", font=MONO_FONT, font_size=25, color=WHITE),
            Text("sum(4) = 4 + 6 = 10", font=MONO_FONT, font_size=25, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.65)
        self.play(LaggedStart(*[FadeIn(line, shift=UP * 0.08) for line in equations], lag_ratio=0.17), run_time=1.1)
        for frame in reversed(frames):
            self.play(frame[0].animate.set_fill(GREEN).set_stroke(GREEN_LIGHT), run_time=0.2)
        footer = self.note("每层保存自己的 n；最深层先返回，父层再完成计算")
        self.play(FadeIn(footer), run_time=0.45)
        self.wait(1.2)


class RecursionFactorialVisualization(RecursionScene):
    def construct(self):
        self.intro("递归展开与回收：阶乘", "展开时留下乘法，回收时得到结果")
        expand = VGroup(
            *[Text(text, font=MONO_FONT, font_size=28, color=BLUE_LIGHT) for text in ["5!", "5 × 4!", "5 × 4 × 3!", "5 × 4 × 3 × 2!", "5 × 4 × 3 × 2 × 1"]]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(LEFT, buff=0.62).shift(DOWN * 0.1)
        expand_title = Text("展开", font=FONT, font_size=24, color=MUTED).next_to(expand, UP, buff=0.2)
        self.play(FadeIn(expand_title), LaggedStart(*[FadeIn(line, shift=DOWN * 0.08) for line in expand], lag_ratio=0.13), run_time=1.05)
        returns = VGroup(
            *[Text(text, font=MONO_FONT, font_size=28, color=GREEN_LIGHT) for text in ["1", "2", "6", "24", "120"]]
        ).arrange(UP, buff=0.22).to_edge(RIGHT, buff=1.25).shift(DOWN * 0.1)
        return_title = Text("回收", font=FONT, font_size=24, color=MUTED).next_to(returns, UP, buff=0.2)
        self.play(FadeIn(return_title), LaggedStart(*[FadeIn(value, shift=UP * 0.1) for value in returns], lag_ratio=0.13), run_time=1.0)
        bridge = Arrow(expand[-1].get_right(), returns[0].get_left(), buff=0.15, color=GREEN_LIGHT)
        self.play(Create(bridge), run_time=0.45)
        footer = self.note("return n * factorial(n - 1)：子问题与合并方式写在同一行")
        self.play(FadeIn(footer), run_time=0.45)
        self.wait(1.2)


class RecursionFibonacciVisualization(RecursionScene):
    def construct(self):
        self.intro("递归算法：Fibonacci 递归树", "双分支很直观，重复计算也很明显")
        labels = {
            "root": self.card("fib(5)", width=1.7, fill=PURPLE, stroke=PURPLE_LIGHT, size=22),
            "l": self.card("fib(4)", width=1.6, fill=BLUE, stroke=BLUE_LIGHT, size=20),
            "r": self.card("fib(3)", width=1.6, fill=ORANGE, stroke=ORANGE_LIGHT, size=20),
            "ll": self.card("fib(3)", width=1.5, fill=ORANGE, stroke=ORANGE_LIGHT, size=19),
            "lr": self.card("fib(2)", width=1.5, fill=SLATE, stroke=SLATE_LIGHT, size=19),
            "rl": self.card("fib(2)", width=1.5, fill=SLATE, stroke=SLATE_LIGHT, size=19),
            "rr": self.card("fib(1)", width=1.5, fill=GREEN, stroke=GREEN_LIGHT, size=19),
        }
        labels["root"].move_to(UP * 1.65)
        labels["l"].move_to(LEFT * 2.1 + UP * 0.35)
        labels["r"].move_to(RIGHT * 2.1 + UP * 0.35)
        labels["ll"].move_to(LEFT * 3.3 + DOWN * 1.15)
        labels["lr"].move_to(LEFT * 1.1 + DOWN * 1.15)
        labels["rl"].move_to(RIGHT * 1.1 + DOWN * 1.15)
        labels["rr"].move_to(RIGHT * 3.3 + DOWN * 1.15)
        edges = VGroup()
        for parent, child in [("root", "l"), ("root", "r"), ("l", "ll"), ("l", "lr"), ("r", "rl"), ("r", "rr")]:
            edges.add(Line(labels[parent].get_bottom(), labels[child].get_top(), color=SLATE_LIGHT, stroke_width=2.5))
        self.play(FadeIn(labels["root"]), run_time=0.35)
        self.play(Create(edges[:2]), FadeIn(labels["l"]), FadeIn(labels["r"]), run_time=0.6)
        self.play(Create(edges[2:]), *[FadeIn(labels[key]) for key in ["ll", "lr", "rl", "rr"]], run_time=0.8)
        repeated = VGroup(labels["r"], labels["ll"])
        self.play(*[card[0].animate.set_stroke("#facc15", width=5) for card in repeated], run_time=0.45)
        duplicate = Text("同一个 fib(3) 被重复展开", font=FONT, font_size=25, color="#fde68a").to_edge(DOWN, buff=0.55)
        self.play(FadeIn(duplicate), run_time=0.45)
        footer = self.note("保存已经算过的结果，就能从朴素递归走向记忆化", color=GREEN_LIGHT)
        self.play(ReplacementTransform(duplicate, footer), run_time=0.5)
        self.wait(1.2)


class RecursionHanoiVisualization(RecursionScene):
    def construct(self):
        self.intro("递归算法：汉诺塔", "n 个盘子的任务，固定拆成三步")
        steps = VGroup(
            self.card("① 移 n-1：A → B", width=4.0, fill=BLUE, stroke=BLUE_LIGHT, size=23, font=FONT),
            self.card("② 移最大盘：A → C", width=4.0, fill=ORANGE, stroke=ORANGE_LIGHT, size=23, font=FONT),
            self.card("③ 移 n-1：B → C", width=4.0, fill=GREEN, stroke=GREEN_LIGHT, size=23, font=FONT),
        ).arrange(DOWN, buff=0.28).to_edge(LEFT, buff=0.58).shift(DOWN * 0.12)
        self.play(LaggedStart(*[FadeIn(step, shift=RIGHT * 0.12) for step in steps], lag_ratio=0.18), run_time=1.0)

        bases = VGroup(*[Line(DOWN * 1.5, UP * 1.25, color=SLATE_LIGHT, stroke_width=5) for _ in range(3)])
        bases.arrange(RIGHT, buff=1.45).to_edge(RIGHT, buff=0.72).shift(DOWN * 0.1)
        names = VGroup(*[Text(name, font=MONO_FONT, font_size=26, color=WHITE).next_to(base, DOWN, buff=0.16) for name, base in zip("ABC", bases)])
        disks = VGroup()
        for index, width in enumerate([1.6, 1.25, 0.9]):
            disk = RoundedRectangle(width=width, height=0.28, corner_radius=0.08, stroke_width=0, fill_color=[ORANGE, BLUE, PURPLE][index], fill_opacity=1)
            disk.move_to(bases[0].get_bottom() + UP * (0.22 + index * 0.3))
            disks.add(disk)
        self.play(FadeIn(bases), FadeIn(names), LaggedStart(*[FadeIn(disk) for disk in disks], lag_ratio=0.12), run_time=0.8)
        self.play(disks[-1].animate.move_to(bases[2].get_bottom() + UP * 0.22), run_time=0.55)
        footer = self.note("hanoi(n-1, from, to, aux) → 移最大盘 → hanoi(n-1, aux, from, to)")
        self.play(FadeIn(footer), run_time=0.45)
        self.wait(1.2)


class RecursionTreeTraversalVisualization(RecursionScene):
    def construct(self):
        self.intro("递归算法：树形递归输出", "visit 放在哪里，决定遍历顺序")
        positions = [UP * 1.25, LEFT * 2.0, RIGHT * 2.0, LEFT * 3.1 + DOWN * 1.45, LEFT * 0.9 + DOWN * 1.45, RIGHT * 0.9 + DOWN * 1.45, RIGHT * 3.1 + DOWN * 1.45]
        values = ["1", "2", "3", "4", "5", "6", "7"]
        nodes = VGroup()
        for value, position in zip(values, positions):
            circle = Circle(radius=0.36, stroke_width=2.5, stroke_color=BLUE_LIGHT, fill_color=BLUE, fill_opacity=1)
            label = Text(value, font=MONO_FONT, weight="BOLD", font_size=24, color=WHITE).move_to(circle)
            nodes.add(VGroup(circle, label).move_to(position))
        edges = VGroup()
        for parent, child in [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]:
            edges.add(Line(nodes[parent].get_center(), nodes[child].get_center(), color=SLATE_LIGHT, stroke_width=2.5).set_z_index(-1))
        self.play(Create(edges), LaggedStart(*[FadeIn(node) for node in nodes], lag_ratio=0.08), run_time=0.9)
        order = [0, 1, 3, 4, 2, 5, 6]
        for index in order:
            self.play(nodes[index][0].animate.set_fill(ORANGE).set_stroke(ORANGE_LIGHT), run_time=0.16)
        sequence = Text("前序：1  2  4  5  3  6  7", font=MONO_FONT, font_size=27, color=ORANGE_LIGHT)
        sequence.to_edge(DOWN, buff=0.64)
        self.play(FadeIn(sequence), run_time=0.42)
        footer = self.note("根在前：前序　根在中：中序　根在后：后序")
        self.play(ReplacementTransform(sequence, footer), run_time=0.5)
        self.wait(1.2)


class RecursionDebugVisualization(RecursionScene):
    def construct(self):
        self.intro("递归算法：递归调试方法", "用缩进日志把调用栈变成可读轨迹")
        logs = [
            ("enter 3", 0, BLUE_LIGHT),
            ("enter 2", 1, BLUE_LIGHT),
            ("enter 1", 2, BLUE_LIGHT),
            ("leave 1", 2, GREEN_LIGHT),
            ("leave 2", 1, GREEN_LIGHT),
            ("leave 3", 0, GREEN_LIGHT),
        ]
        lines = VGroup()
        for text, depth, color in logs:
            prefix = "│  " * depth
            lines.add(Text(prefix + text, font=MONO_FONT, font_size=27, color=color))
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(LEFT, buff=1.0).shift(DOWN * 0.08)
        self.play(LaggedStart(*[FadeIn(line, shift=RIGHT * 0.1) for line in lines], lag_ratio=0.14), run_time=1.2)
        checklist = VGroup(
            self.card("① 参数是否变化", width=3.45, fill=SLATE, stroke=BLUE_LIGHT, size=22, font=FONT),
            self.card("② 出口是否命中", width=3.45, fill=SLATE, stroke=GREEN_LIGHT, size=22, font=FONT),
            self.card("③ 返回值流向哪里", width=3.45, fill=SLATE, stroke=ORANGE_LIGHT, size=22, font=FONT),
        ).arrange(DOWN, buff=0.26).to_edge(RIGHT, buff=0.78).shift(DOWN * 0.08)
        self.play(LaggedStart(*[FadeIn(item, shift=LEFT * 0.1) for item in checklist], lag_ratio=0.14), run_time=0.9)
        footer = self.note("进入时打印参数，返回时打印结果；先看最小样例，再看分支样例")
        self.play(FadeIn(footer), run_time=0.45)
        self.wait(1.2)
