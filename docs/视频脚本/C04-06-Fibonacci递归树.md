# C04-06 Fibonacci 递归树

## 制作目标

- 学习目标：理解双分支递归、返回值合并与重复计算。
- 核心结论：递归树能解释执行结构，也能暴露朴素 Fibonacci 的指数级重复。
- 输出视频：`media/videos/recursion_chapter_scenes/1080p60/RecursionFibonacciVisualization.mp4`
- 预览图：`media/previews/recursion_fibonacci_preview.png`

## 分镜与旁白

| 镜头 | 画面 | 旁白 |
| --- | --- | --- |
| 1 | `fib(5)` 分裂为 `fib(4)` 与 `fib(3)`。 | 当前问题需要两个更小子问题，因此调用结构开始分叉。 |
| 2 | 第二层继续展开。 | 每个非出口节点都会继续请求前两项，形成二叉递归树。 |
| 3 | 两个 `fib(3)` 用相同颜色与描边突出。 | 相同子问题在不同分支被重新计算，这是朴素递归慢的原因。 |
| 4 | 叶子返回，父节点相加。 | 左右子结果都返回后，父节点才完成自己的加法。 |
| 5 | 出现“保存已算结果”。 | 给每个下标增加缓存，就能把重复展开变成一次计算。 |

## 练习衔接

- `recursion-fibonacci-basic`：写出双分支递归。
- `recursion-fibonacci-calls`：统计整棵递归树的节点数。
- `recursion-fibonacci-memo`：用缓存剪掉重复子树。

