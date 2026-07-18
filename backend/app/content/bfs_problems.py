from dataclasses import dataclass


@dataclass(frozen=True)
class TestCase:
    input: str
    output: str
    hidden: bool = False


@dataclass(frozen=True)
class Problem:
    id: str
    title: str
    difficulty: str
    tags: list[str]
    statement: str
    input_format: str
    output_format: str
    constraints: str
    samples: list[TestCase]
    tests: list[TestCase]
    time_limit_ms: int = 2000
    memory_limit_mb: int = 128


def make_problem(problem_id, title, difficulty, tags, statement, input_format,
                 output_format, constraints, sample_input, sample_output, hidden_cases):
    sample = TestCase(sample_input, sample_output)
    return Problem(
        id=problem_id, title=title, difficulty=difficulty, tags=["BFS", *tags],
        statement=statement, input_format=input_format, output_format=output_format,
        constraints=constraints, samples=[sample],
        tests=[sample, *(TestCase(data, answer, hidden=True) for data, answer in hidden_cases)],
    )


BFS_PROBLEMS: dict[str, Problem] = {
    "bfs-queue-commands": make_problem(
        "bfs-queue-commands", "队列指令模拟", "入门", ["队列", "FIFO"],
        "维护整数队列。push x 入队；pop 输出并删除队首，队空输出 EMPTY；size 输出元素个数。",
        "第一行 q，之后 q 行各一条指令。", "按指令逐行输出。", "1 <= q <= 100000。",
        "7\npush 3\npush 8\nsize\npop\npush 5\npop\npop\n", "2\n3\n8\n5\n",
        [("3\npop\nsize\npop\n", "EMPTY\n0\nEMPTY\n"), ("4\npush -1\npop\npush 0\nsize\n", "-1\n1\n")]),
    "bfs-round-robin": make_problem(
        "bfs-round-robin", "轮转队列", "基础", ["队列", "模拟"],
        "n 个任务依次入队，每轮处理队首至多 quantum 时间；未完成就回到队尾。输出完成顺序。",
        "第一行 n 和 quantum；第二行 n 个处理时间。", "输出 1-based 任务编号。", "1 <= n <= 100000。",
        "4 3\n5 2 7 3\n", "2 4 1 3\n", [("1 5\n12\n", "1\n"), ("4 10\n1 2 3 4\n", "1 2 3 4\n")]),
    "bfs-graph-distances": make_problem(
        "bfs-graph-distances", "无权图单源距离", "基础", ["无权图", "距离"],
        "输出无向无权图中起点到每个节点的最少边数，不可达输出 -1。",
        "第一行 n、m、start；之后 m 行为边。", "输出 n 个距离。", "1 <= n <= 200000。",
        "6 5 1\n1 2\n1 3\n2 4\n3 5\n5 6\n", "0 1 1 2 2 3\n", [("1 0 1\n", "0\n"), ("4 1 2\n1 2\n", "1 0 -1 -1\n")]),
    "bfs-level-counts": make_problem(
        "bfs-level-counts", "统计 BFS 各层节点数", "基础", ["层序", "计数"],
        "从无向图 1 号点 BFS，输出距离 0 到最大可达距离的节点数。",
        "第一行 n、m，之后 m 行为边。", "输出每层节点数。", "1 <= n <= 200000。",
        "7 6\n1 2\n1 3\n2 4\n2 5\n3 6\n6 7\n", "1 2 3 1\n", [("1 0\n", "1\n"), ("5 2\n1 2\n2 3\n", "1 1 1\n")]),
    "bfs-maze-shortest": make_problem(
        "bfs-maze-shortest", "迷宫最短步数", "基础", ["网格", "最短路"],
        "在 . 和 # 网格中上下左右移动，求左上到右下的最少步数，不可达输出 -1。",
        "第一行 n、m，之后 n 行网格。", "输出最少步数。", "1 <= n,m <= 1000。",
        "3 4\n....\n.##.\n....\n", "5\n", [("1 1\n.\n", "0\n"), ("2 2\n.#\n#.\n", "-1\n"), ("1 3\n#..\n", "-1\n")]),
    "bfs-grid-reachable-count": make_problem(
        "bfs-grid-reachable-count", "统计可达格子", "入门", ["网格", "访问标记"],
        "从左上角出发，只走 . 格，统计上下左右可达格数；起点为墙输出 0。",
        "第一行 n、m，之后 n 行网格。", "输出可达格数。", "1 <= n,m <= 1000。",
        "3 4\n..#.\n.##.\n....\n", "9\n", [("1 1\n#\n", "0\n"), ("2 3\n...\n...\n", "6\n"), ("3 3\n.#.\n###\n...\n", "1\n")]),
    "bfs-number-line-shortest": make_problem(
        "bfs-number-line-shortest", "数轴最少操作", "基础", ["隐式图", "最短步数"],
        "整数 x 每步变为 x-1、x+1 或 2*x，状态限于 [0,100000]，求最少步数。",
        "一行 start 和 target。", "输出最少步数。", "0 <= start,target <= 100000。",
        "5 17\n", "4\n", [("10 10\n", "0\n"), ("0 3\n", "3\n"), ("20 3\n", "17\n")]),
    "bfs-modulo-shortest": make_problem(
        "bfs-modulo-shortest", "模环上的最少操作", "进阶", ["状态图", "取模"],
        "状态 x 每步变为 (x+1)%m 或 (2*x)%m，求 start 到 target 的最少步数。",
        "一行 m、start、target。", "输出最少步数。", "1 <= m <= 1000000。",
        "10 3 8\n", "2\n", [("1 0 0\n", "0\n"), ("7 0 6\n", "4\n"), ("8 1 4\n", "2\n")]),
    "bfs-maze-path": make_problem(
        "bfs-maze-path", "还原迷宫最短路径", "进阶", ["网格", "前驱"],
        "从左上到右下按上、下、左、右扩展，输出确定的最短路径，不可达输出 -1。",
        "第一行 n、m，之后 n 行网格。", "先输出步数，再逐行输出 1-based 坐标。", "1 <= n,m <= 500。",
        "2 2\n..\n..\n", "2\n1 1\n2 1\n2 2\n", [("1 1\n.\n", "0\n1 1\n"), ("2 2\n.#\n#.\n", "-1\n")]),
    "bfs-graph-path": make_problem(
        "bfs-graph-path", "还原图中最短路径", "基础", ["无权图", "前驱"],
        "无向图按边输入顺序扩展，输出从 1 到 n 的 BFS 最短路径，不可达输出 -1。",
        "第一行 n、m，之后 m 行为边。", "先输出步数，再输出路径。", "1 <= n <= 200000。",
        "5 5\n1 2\n1 3\n2 4\n3 4\n4 5\n", "3\n1 2 4 5\n", [("1 0\n", "0\n1\n"), ("3 1\n1 2\n", "-1\n")]),
    "bfs-infection-time": make_problem(
        "bfs-infection-time", "全部感染的最短时间", "基础", ["多源", "扩散"],
        "网格中 1 是初始感染点，每分钟感染上下左右相邻的 0，求全部感染所需时间。",
        "第一行 n、m，之后 n 行为 01 串。", "输出最少分钟数。", "1 <= n,m <= 1000，至少一个 1。",
        "3 4\n1000\n0000\n0001\n", "3\n", [("1 1\n1\n", "0\n"), ("1 5\n00100\n", "2\n")]),
    "bfs-nearest-source": make_problem(
        "bfs-nearest-source", "每格到最近源的距离", "基础", ["多源", "距离矩阵"],
        "对 01 网格每个格输出到最近 1 格的曼哈顿距离。",
        "第一行 n、m，之后 n 行为 01 串。", "输出距离矩阵。", "1 <= n,m <= 1000，至少一个 1。",
        "3 3\n000\n010\n000\n", "2 1 2\n1 0 1\n2 1 2\n", [("1 4\n1001\n", "0 1 1 0\n"), ("2 2\n11\n11\n", "0 0\n0 0\n")]),
    "bfs-knight-shortest": make_problem(
        "bfs-knight-shortest", "骑士最少步数", "基础", ["骑士", "棋盘"],
        "骑士按国际象棋规则移动，求起点到终点的最少步数，不可达输出 -1。",
        "一行 n、sx、sy、tx、ty，坐标从 1 开始。", "输出最少步数。", "1 <= n <= 1000。",
        "8 1 1 8 8\n", "6\n", [("1 1 1 1 1\n", "0\n"), ("2 1 1 2 2\n", "-1\n"), ("3 1 1 2 3\n", "1\n")]),
    "bfs-knight-reachable": make_problem(
        "bfs-knight-reachable", "骑士恰好 k 步可达格数", "进阶", ["骑士", "层统计"],
        "统计 n*n 棋盘上从给定位置出发，最短距离恰好为 k 的格子数。",
        "一行 n、sx、sy、k。", "输出格子数。", "1 <= n <= 1000。",
        "8 1 1 1\n", "2\n", [("1 1 1 0\n", "1\n"), ("3 2 2 1\n", "0\n"), ("4 1 1 2\n", "5\n")]),
    "bfs-integer-transform": make_problem(
        "bfs-integer-transform", "整数最少变换", "基础", ["状态", "隐式图"],
        "整数 x 每步执行 x+1、x-1 或 2*x，状态限定在 [0,100000]，求最少操作数。",
        "一行 start 和 target。", "输出最少操作数。", "0 <= start,target <= 100000。",
        "4 15\n", "3\n", [("7 7\n", "0\n"), ("1 8\n", "3\n"), ("9 2\n", "7\n")]),
    "bfs-lock-four-digits": make_problem(
        "bfs-lock-four-digits", "四位密码锁", "进阶", ["字符串状态", "禁用状态"],
        "四位密码每步将任一位循环加减 1（0 与 9 相邻），不能进入禁用状态，求最少步数。",
        "第一行起点和终点；第二行 k；之后 k 行为禁用密码。", "输出最少步数，不可达为 -1。", "0 <= k <= 10000。",
        "0000 0009\n0\n", "1\n", [("0000 0000\n0\n", "0\n"), ("0000 0001\n1\n0001\n", "-1\n"), ("0000 0011\n0\n", "2\n")]),
    "bfs-unweighted-shortest": make_problem(
        "bfs-unweighted-shortest", "无权图最少边数", "入门", ["BFS 与 DFS", "最短路"],
        "输出无向无权图从 1 到 n 的最少边数，不可达输出 -1。",
        "第一行 n、m，之后 m 行为边。", "输出一个整数。", "1 <= n <= 200000。",
        "5 5\n1 2\n2 5\n1 3\n3 4\n4 5\n", "2\n", [("1 0\n", "0\n"), ("4 1\n1 2\n", "-1\n")]),
    "bfs-method-signals": make_problem(
        "bfs-method-signals", "搜索方法判断信号", "基础", ["BFS 与 DFS", "方法选择"],
        "信号为 SHORTEST、LEVEL、REACH、ENUM、BACKTRACK。前三类优先 BFS，后两类优先 DFS，统计 BFS 类数量。",
        "第一行 n；之后 n 行为信号。", "输出 BFS 类任务数。", "1 <= n <= 100000。",
        "5\nSHORTEST\nENUM\nLEVEL\nBACKTRACK\nREACH\n", "3\n", [("1\nENUM\n", "0\n"), ("3\nSHORTEST\nLEVEL\nREACH\n", "3\n")]),
}
