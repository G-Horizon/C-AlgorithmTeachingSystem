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


def p(
    problem_id: str,
    title: str,
    difficulty: str,
    tags: list[str],
    statement: str,
    input_format: str,
    output_format: str,
    constraints: str,
    cases: list[tuple[str, str]],
) -> Problem:
    tests = [TestCase(data, answer, hidden=i > 0) for i, (data, answer) in enumerate(cases)]
    return Problem(problem_id, title, difficulty, ["动态规划", *tags], statement, input_format,
                   output_format, constraints, [tests[0]], tests)


DP_PROBLEMS: dict[str, Problem] = {}


def add(*args) -> None:
    item = p(*args)
    DP_PROBLEMS[item.id] = item


add("dp-fibonacci-memo", "记忆化 Fibonacci", "入门", ["记忆化", "Fibonacci"],
    "定义 F(0)=0、F(1)=1、F(n)=F(n-1)+F(n-2)，使用记忆化递归求 F(n)。",
    "一行一个整数 n。", "输出 F(n)。", "0 <= n <= 90。",
    [("10\n", "55\n"), ("0\n", "0\n"), ("50\n", "12586269025\n")])
add("dp-fibonacci-bottom-up", "自底向上 Fibonacci", "基础", ["自底向上", "Fibonacci"],
    "按照 F(0)、F(1) 到 F(n) 的顺序填表，求 F(n)。", "一行 n。", "输出 F(n)。", "0 <= n <= 90。",
    [("20\n", "6765\n"), ("2\n", "1\n"), ("90\n", "2880067194370816120\n")])
add("dp-min-cost-stairs", "到达末级台阶的最小代价", "基础", ["状态定义", "最小值"],
    "有 n 级台阶，第 i 级代价为 cost[i]。可从地面踏上第 1 或第 2 级，之后每次向上 1 或 2 级，求到达第 n 级的最小总代价。",
    "第一行 n，第二行 n 个非负整数。", "输出最小总代价。", "1 <= n <= 100000。",
    [("5\n4 2 7 1 3\n", "6\n"), ("1\n8\n", "8\n"), ("4\n1 100 1 1\n", "3\n")])
add("dp-state-table-query", "查询台阶 DP 状态", "入门", ["状态表", "输出"],
    "按最小代价台阶规则，输出 dp[1] 到 dp[n]，dp[i] 表示到达第 i 级的最小总代价。",
    "第一行 n，第二行 n 个代价。", "输出 n 个状态值。", "1 <= n <= 100000。",
    [("5\n4 2 7 1 3\n", "4 2 9 3 6\n"), ("1\n8\n", "8\n"), ("4\n1 100 1 1\n", "1 100 2 3\n")])
add("dp-house-robber", "不相邻元素最大和", "基础", ["状态转移", "选或不选"],
    "选择若干个互不相邻的非负元素，使总和最大。", "第一行 n，第二行 n 个整数。", "输出最大和。", "1 <= n <= 100000。",
    [("6\n2 7 9 3 1 5\n", "16\n"), ("1\n8\n", "8\n"), ("5\n5 1 1 5 1\n", "10\n")])
add("dp-max-sum-no-adjacent-trace", "输出不相邻最大和状态表", "基础", ["状态转移", "调试"],
    "令 dp[i] 为前 i 个元素中选择互不相邻元素的最大和，输出 dp[1..n]。",
    "第一行 n，第二行 n 个非负整数。", "输出 n 个状态值。", "1 <= n <= 100000。",
    [("6\n2 7 9 3 1 5\n", "2 7 11 11 12 16\n"), ("1\n0\n", "0\n"), ("4\n5 1 1 5\n", "5 5 6 10\n")])
add("dp-grid-paths", "网格路径计数", "入门", ["二维 DP", "计数"],
    "从 n 行 m 列网格左上角出发，每次向下或向右，求到右下角的路径数。",
    "一行 n、m。", "输出路径数。", "1 <= n,m <= 20。",
    [("3 4\n", "10\n"), ("1 1\n", "1\n"), ("5 5\n", "70\n")])
add("dp-grid-paths-obstacles", "带障碍的网格路径", "基础", ["二维 DP", "障碍"],
    "网格中 '.' 可通行、'#' 是障碍。从左上角出发，每次向下或向右，求到右下角的路径数。",
    "第一行 n、m，随后 n 行网格。", "输出路径数。", "1 <= n,m <= 20。",
    [("3 4\n....\n.#..\n....\n", "4\n"), ("1 1\n.\n", "1\n"), ("2 2\n.#\n#.\n", "0\n")])
add("dp-number-triangle-max", "数字三角形最大路径和", "基础", ["路径 DP", "自底向上"],
    "从数字三角形顶部出发，每步走左下或右下，求到底边的最大路径和。",
    "第一行 n，随后第 i 行 i 个整数。", "输出最大路径和。", "1 <= n <= 500。",
    [("4\n7\n3 8\n8 1 0\n2 7 4 4\n", "25\n"), ("1\n-5\n", "-5\n"), ("3\n1\n2 3\n4 5 6\n", "10\n")])
add("dp-number-triangle-min", "数字三角形最小路径和", "基础", ["路径 DP", "最小值"],
    "从数字三角形顶部出发，每步走左下或右下，求到底边的最小路径和。",
    "第一行 n，随后第 i 行 i 个整数。", "输出最小路径和。", "1 <= n <= 500。",
    [("4\n7\n3 8\n8 1 0\n2 7 4 4\n", "15\n"), ("1\n-5\n", "-5\n"), ("3\n1\n2 3\n4 5 6\n", "7\n")])
add("dp-knapsack-01", "01 背包最大价值", "基础", ["01 背包", "二维 DP"],
    "每件物品最多选一次，在总重量不超过容量时求最大总价值。",
    "第一行 n、capacity；随后 n 行 weight、value。", "输出最大价值。", "1 <= n <= 100，capacity <= 10000。",
    [("4 7\n2 6\n3 10\n4 12\n5 13\n", "22\n"), ("1 1\n2 9\n", "0\n"), ("3 5\n1 2\n2 4\n3 4\n", "8\n")])
add("dp-knapsack-exact", "恰好装满的 01 背包", "进阶", ["01 背包", "不可达状态"],
    "每件物品最多选一次，求总重量恰好等于容量时的最大价值；无法装满输出 -1。",
    "第一行 n、capacity；随后 n 行 weight、value。", "输出最大价值或 -1。", "1 <= n <= 100，capacity <= 10000。",
    [("4 7\n2 6\n3 10\n4 12\n5 13\n", "22\n"), ("2 5\n2 9\n4 20\n", "-1\n"), ("3 5\n1 2\n2 4\n3 4\n", "8\n")])
add("dp-knapsack-01-rolling", "一维 01 背包", "基础", ["01 背包", "空间优化"],
    "使用一维状态和倒序容量完成 01 背包。", "第一行 n、capacity；随后 n 行物品。", "输出最大价值。", "n <= 1000，capacity <= 10000。",
    [("4 7\n2 6\n3 10\n4 12\n5 13\n", "22\n"), ("1 6\n3 5\n", "5\n"), ("3 3\n1 2\n1 3\n2 4\n", "7\n")])
add("dp-knapsack-count", "01 背包装满方案数", "进阶", ["01 背包", "计数"],
    "每个重量最多选一次，统计总重量恰好等于 capacity 的选择方案数。",
    "第一行 n、capacity；第二行 n 个重量。", "输出方案数。", "1 <= n <= 40，capacity <= 1000。",
    [("5 5\n1 2 3 4 5\n", "3\n"), ("3 0\n1 2 3\n", "1\n"), ("4 4\n2 2 2 2\n", "6\n")])
add("dp-lis-length", "最长严格上升子序列长度", "基础", ["LIS", "序列 DP"],
    "求整数序列的最长严格上升子序列长度，子序列不要求连续。",
    "第一行 n，第二行 n 个整数。", "输出长度。", "1 <= n <= 3000。",
    [("8\n10 9 2 5 3 7 101 18\n", "4\n"), ("1\n5\n", "1\n"), ("5\n5 4 3 2 1\n", "1\n")])
add("dp-lis-nondecreasing", "最长不下降子序列", "基础", ["LIS", "不下降"],
    "求最长不下降子序列长度，相邻选择的元素允许相等。", "第一行 n，第二行 n 个整数。", "输出长度。", "1 <= n <= 3000。",
    [("7\n3 1 2 2 5 4 4\n", "5\n"), ("4\n2 2 2 2\n", "4\n"), ("5\n5 4 3 2 1\n", "1\n")])
add("dp-lcs-length", "最长公共子序列长度", "基础", ["LCS", "字符串 DP"],
    "求两个字符串的最长公共子序列长度。", "两行不含空格的字符串。", "输出 LCS 长度。", "字符串长度不超过 1000。",
    [("ABCBDAB\nBDCABA\n", "4\n"), ("A\nB\n", "0\n"), ("ALGORITHM\nRHYTHM\n", "4\n")])
add("dp-lcs-table", "输出 LCS 状态表", "进阶", ["LCS", "状态表"],
    "dp[i][j] 表示两个字符串长度 i、j 的前缀的 LCS 长度，输出 i=1..n、j=1..m 的表格。",
    "两行字符串。", "输出 n 行、每行 m 个整数。", "字符串长度不超过 30。",
    [("ABC\nAC\n", "1 1\n1 1\n1 2\n"), ("A\nB\n", "0\n"), ("AB\nAB\n", "1 1\n1 2\n")])
add("dp-stone-merge", "石子合并最小代价", "进阶", ["区间 DP", "石子合并"],
    "一排石子只能合并相邻两堆，每次代价为两堆石子总数，求合并成一堆的最小总代价。",
    "第一行 n，第二行 n 堆石子数。", "输出最小总代价。", "1 <= n <= 300。",
    [("4\n1 3 5 2\n", "22\n"), ("1\n9\n", "0\n"), ("3\n1 1 1\n", "5\n")])
add("dp-palindrome-subsequence", "最长回文子序列", "进阶", ["区间 DP", "回文"],
    "求字符串的最长回文子序列长度。", "一行字符串。", "输出长度。", "1 <= |s| <= 1000。",
    [("bbbab\n", "4\n"), ("a\n", "1\n"), ("cbbd\n", "2\n")])
add("dp-fibonacci-table", "输出 Fibonacci 状态表", "入门", ["调试", "状态表"],
    "定义 F(0)=F(1)=1、F(i)=F(i-1)+F(i-2)，输出 F(0..n)。", "一行 n。", "输出 n+1 个状态值。", "0 <= n <= 80。",
    [("6\n", "1 1 2 3 5 8 13\n"), ("0\n", "1\n"), ("2\n", "1 1 2\n")])
add("dp-transition-audit", "检查递推表中的首个错误", "基础", ["调试", "状态核对"],
    "候选表应满足 dp[0]=dp[1]=1、dp[i]=dp[i-1]+dp[i-2]。输出首个错误下标；全部正确输出 OK。",
    "第一行 n，第二行 n+1 个候选状态。", "输出下标或 OK。", "1 <= n <= 80。",
    [("6\n1 1 2 3 6 8 13\n", "4\n"), ("4\n1 1 2 3 5\n", "OK\n"), ("2\n0 1 1\n", "0\n")])
add("dp-coin-min", "任意币制最少硬币数", "基础", ["完全背包", "贪心反例"],
    "每种硬币可使用任意次，求凑成 amount 的最少硬币数；无法凑出输出 -1。",
    "第一行 n、amount；第二行 n 个币值。", "输出最少硬币数或 -1。", "n <= 30，amount <= 10000。",
    [("3 6\n1 3 4\n", "2\n"), ("2 7\n2 4\n", "-1\n"), ("3 0\n2 3 5\n", "0\n")])
add("dp-method-classifier", "算法选择判断", "入门", ["算法选择", "方法边界"],
    "输入 overlap、stateable、greedyProven 三个 0/1 特征。greedyProven 为 1 输出 GREEDY；否则前两项均为 1 输出 DP；其余输出 SEARCH。",
    "一行三个 0 或 1。", "输出 GREEDY、DP 或 SEARCH。", "输入只含 0 和 1。",
    [("1 1 0\n", "DP\n"), ("1 1 1\n", "GREEDY\n"), ("0 0 0\n", "SEARCH\n")])
