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


def make_problem(
    problem_id: str,
    title: str,
    difficulty: str,
    tags: list[str],
    statement: str,
    input_format: str,
    output_format: str,
    constraints: str,
    sample_input: str,
    sample_output: str,
    hidden_cases: list[tuple[str, str]],
) -> Problem:
    sample = TestCase(sample_input, sample_output)
    return Problem(
        id=problem_id,
        title=title,
        difficulty=difficulty,
        tags=["搜索与回溯", *tags],
        statement=statement,
        input_format=input_format,
        output_format=output_format,
        constraints=constraints,
        samples=[sample],
        tests=[sample, *(TestCase(data, answer, hidden=True) for data, answer in hidden_cases)],
    )


SEARCH_PROBLEMS: dict[str, Problem] = {
    "search-binary-strings": make_problem(
        "search-binary-strings", "枚举所有二进制串", "入门", ["DFS", "搜索树"],
        "给定长度 n，请按字典序输出所有长度为 n 的二进制串。",
        "一行一个整数 n。", "每行一个二进制串，按字典序从小到大输出。", "1 <= n <= 10。",
        "3\n", "000\n001\n010\n011\n100\n101\n110\n111\n",
        [("1\n", "0\n1\n"), ("2\n", "00\n01\n10\n11\n")],
    ),
    "search-tree-level-count": make_problem(
        "search-tree-level-count", "计算搜索树各层节点数", "基础", ["DFS", "搜索树", "深度"],
        "二进制串搜索树从深度 0 的根开始，每个非叶子都有 0、1 两个子节点。用 DFS 统计深度 0 到 n 每层的节点数。",
        "一行一个整数 n。", "输出 n+1 个整数，表示各层节点数。", "0 <= n <= 20。",
        "4\n", "1 2 4 8 16\n",
        [("0\n", "1\n"), ("1\n", "1 2\n"), ("10\n", "1 2 4 8 16 32 64 128 256 512 1024\n")],
    ),
    "search-dfs-sequences": make_problem(
        "search-dfs-sequences", "DFS 枚举定长序列", "入门", ["DFS", "递归出口", "枚举"],
        "长度为 n 的序列每个位置都可以填 1 到 m。请按字典序输出所有序列。",
        "一行两个整数 n 和 m。", "每行一个序列，数字之间用一个空格分隔。", "1 <= n,m <= 6，m^n <= 50000。",
        "2 2\n", "1 1\n1 2\n2 1\n2 2\n",
        [("1 3\n", "1\n2\n3\n"), ("3 1\n", "1 1 1\n")],
    ),
    "search-dfs-leaf-count": make_problem(
        "search-dfs-leaf-count", "统计 DFS 叶子数", "基础", ["DFS", "叶子", "计数"],
        "长度为 n 的序列每个位置有 m 种选择。用 DFS 枚举决策过程，只在递归出口累加叶子数。",
        "一行两个整数 n 和 m。", "输出 DFS 搜索树的叶子数。", "0 <= n <= 12，1 <= m <= 8。",
        "3 2\n", "8\n",
        [("0 5\n", "1\n"), ("4 3\n", "81\n"), ("10 2\n", "1024\n")],
    ),
    "search-fixed-weight-binary": make_problem(
        "search-fixed-weight-binary", "枚举恰有 k 个 1 的二进制串", "基础", ["回溯", "撤销选择", "二进制串"],
        "给定 n 和 k，请按字典序输出所有长度为 n、恰好包含 k 个 1 的二进制串。",
        "一行两个整数 n 和 k。", "每行一个符合条件的二进制串。", "1 <= n <= 15，0 <= k <= n。",
        "4 2\n", "0011\n0101\n0110\n1001\n1010\n1100\n",
        [("3 2\n", "011\n101\n110\n"), ("4 0\n", "0000\n"), ("4 4\n", "1111\n")],
    ),
    "search-balanced-parentheses": make_problem(
        "search-balanced-parentheses", "生成合法括号序列", "进阶", ["回溯", "括号", "剪枝"],
        "给定括号对数 n，请按字典序输出所有由 n 对小括号组成的合法序列。",
        "一行一个整数 n。", "每行一个合法括号序列。", "1 <= n <= 9。",
        "3\n", "((()))\n(()())\n(())()\n()(())\n()()()\n",
        [("1\n", "()\n"), ("2\n", "(())\n()()\n")],
    ),
    "search-permutation-basic": make_problem(
        "search-permutation-basic", "输出 1 到 n 的全排列", "基础", ["回溯", "全排列", "used 数组"],
        "给定 n，请按字典序输出 1,2,...,n 的所有全排列。",
        "一行一个整数 n。", "每行一个排列，数字之间用一个空格分隔。", "1 <= n <= 8。",
        "3\n", "1 2 3\n1 3 2\n2 1 3\n2 3 1\n3 1 2\n3 2 1\n",
        [("1\n", "1\n"), ("2\n", "1 2\n2 1\n")],
    ),
    "search-permutation-kth": make_problem(
        "search-permutation-kth", "第 k 个全排列", "进阶", ["回溯", "全排列", "提前停止"],
        "按字典序枚举 1,2,...,n 的全排列，请输出第 k 个排列，k 从 1 开始。",
        "一行两个整数 n 和 k。", "输出第 k 个排列。", "1 <= n <= 9，1 <= k <= n!。",
        "3 4\n", "2 3 1\n",
        [("1 1\n", "1\n"), ("3 1\n", "1 2 3\n"), ("4 24\n", "4 3 2 1\n")],
    ),
    "search-combinations-basic": make_problem(
        "search-combinations-basic", "输出 1 到 n 中的 k 数组合", "基础", ["回溯", "组合", "start 起点"],
        "从 1,2,...,n 中选出 k 个不同的数。请按字典序输出所有组合，每个组合内部递增。",
        "一行两个整数 n 和 k。", "每行一个组合。", "1 <= k <= n <= 15。",
        "4 2\n", "1 2\n1 3\n1 4\n2 3\n2 4\n3 4\n",
        [("3 1\n", "1\n2\n3\n"), ("3 3\n", "1 2 3\n")],
    ),
    "search-combination-sum-k": make_problem(
        "search-combination-sum-k", "k 数组合求和", "进阶", ["回溯", "组合", "目标和"],
        "从 1,2,...,n 中选出 k 个不同的数，统计和恰好等于 target 的组合数。",
        "一行三个整数 n、k 和 target。", "输出符合条件的组合数。", "1 <= k <= n <= 25，1 <= target <= 1000。",
        "5 2 5\n", "2\n",
        [("5 3 9\n", "2\n"), ("6 1 7\n", "0\n"), ("6 6 21\n", "1\n")],
    ),
    "search-subsets-basic": make_problem(
        "search-subsets-basic", "枚举 1 到 n 的所有子集", "基础", ["回溯", "子集", "选或不选"],
        "对 1,2,...,n 的每个元素，按“不选”后“选”的顺序 DFS，输出所有叶子对应的子集。",
        "一行一个整数 n。", "每行一个子集，空集输出 {}。", "1 <= n <= 15。",
        "2\n", "{}\n2\n1\n1 2\n",
        [("1\n", "{}\n1\n"), ("3\n", "{}\n3\n2\n2 3\n1\n1 3\n1 2\n1 2 3\n")],
    ),
    "search-subset-sum-count": make_problem(
        "search-subset-sum-count", "统计子集和等于 target 的方案", "进阶", ["回溯", "子集和", "计数"],
        "给定 n 个正整数，每个数可选或不选。统计元素和恰好等于 target 的子集数，不同下标视为不同选择。",
        "第一行 n 和 target；第二行 n 个正整数。", "输出方案数，target=0 时空集也计一个方案。", "1 <= n <= 25，0 <= target <= 1000。",
        "4 5\n1 2 3 4\n", "2\n",
        [("3 0\n1 2 3\n", "1\n"), ("4 4\n2 2 2 2\n", "6\n"), ("5 20\n1 2 3 4 5\n", "0\n")],
    ),
    "search-maze-reachable": make_problem(
        "search-maze-reachable", "迷宫是否可达", "基础", ["DFS", "迷宫", "visited"],
        "给定迷宫，'.' 表示可通过，'#' 表示墙。每次可向上下左右移动一格，判断能否从左上角到达右下角。",
        "第一行 n 和 m；接下来 n 行是迷宫。", "可达输出 YES，否则输出 NO。", "1 <= n,m <= 50。",
        "3 3\n...\n.#.\n...\n", "YES\n",
        [("1 1\n.\n", "YES\n"), ("1 1\n#\n", "NO\n"), ("3 4\n..#.\n#...\n...#\n", "NO\n")],
    ),
    "search-maze-path-count": make_problem(
        "search-maze-path-count", "统计迷宫简单路径", "进阶", ["回溯", "迷宫", "恢复现场"],
        "统计从左上角到右下角的简单路径数。每次可向上下左右移动，同一条路径中不能重复走同一格。",
        "第一行 n 和 m；接下来 n 行是迷宫。", "输出简单路径数。", "1 <= n,m <= 7，可通过格子不超过 24 个。",
        "2 2\n..\n..\n", "2\n",
        [("1 1\n.\n", "1\n"), ("2 3\n...\n##.\n", "1\n"), ("3 3\n...\n###\n...\n", "0\n"), ("3 3\n.#.\n...\n.#.\n", "1\n")],
    ),
    "search-pruned-subset-sum": make_problem(
        "search-pruned-subset-sum", "剪枝统计目标子集和", "进阶", ["回溯", "剪枝", "后缀和"],
        "给定 n 个正整数，统计和为 target 的子集数。使用“当前和已超标”与“所有剩余数全选也不足”两类剪枝。",
        "第一行 n 和 target；第二行 n 个正整数。", "输出和为 target 的子集数。", "1 <= n <= 35，0 <= target <= 100000。",
        "5 7\n1 2 3 4 5\n", "3\n",
        [("3 0\n1 2 3\n", "1\n"), ("5 10\n2 2 2 2 2\n", "1\n"), ("6 6\n1 1 1 1 1 1\n", "1\n"), ("4 100\n10 20 30 40\n", "1\n")],
    ),
    "search-knapsack-backtrack": make_problem(
        "search-knapsack-backtrack", "回溯求背包最大价值", "进阶", ["回溯", "剪枝", "0/1 背包"],
        "有 n 件物品，每件有重量和价值，每件最多选一次。用回溯在总重量不超过 capacity 时最大化总价值。",
        "第一行 n 和 capacity；接下来 n 行是重量和价值。", "输出最大总价值。", "1 <= n <= 30。",
        "4 7\n2 6\n3 10\n4 12\n5 13\n", "22\n",
        [("1 3\n4 100\n", "0\n"), ("3 10\n2 3\n3 4\n5 10\n", "17\n"), ("5 5\n1 2\n1 2\n1 2\n1 2\n1 2\n", "10\n")],
    ),
    "search-n-queens-count": make_problem(
        "search-n-queens-count", "统计 N 皇后方案数", "进阶", ["回溯", "N 皇后", "对角线约束"],
        "在 n*n 棋盘上放置 n 个皇后，使任意两个皇后都不在同一行、同一列或同一条对角线上。输出合法方案数。",
        "一行一个整数 n。", "输出合法方案数。", "1 <= n <= 12。",
        "4\n", "2\n",
        [("1\n", "1\n"), ("2\n", "0\n"), ("5\n", "10\n"), ("8\n", "92\n")],
    ),
    "search-n-queens-first": make_problem(
        "search-n-queens-first", "输出第一个 N 皇后方案", "进阶", ["回溯", "N 皇后", "提前停止"],
        "按行从上到下放置皇后，每行按列从左到右尝试。输出 DFS 找到的第一个合法方案。",
        "一行一个整数 n。", "有解输出 n 个 1-based 列号，无解输出 NONE。", "1 <= n <= 12。",
        "4\n", "2 4 1 3\n",
        [("1\n", "1\n"), ("2\n", "NONE\n"), ("3\n", "NONE\n"), ("5\n", "1 3 5 2 4\n")],
    ),
    "search-budget-check": make_problem(
        "search-budget-check", "搜索规模是否超预算", "基础", ["复杂度", "分支因子", "溢出判断"],
        "搜索每层最多 b 个分支，深度为 d，叶子上界是 b^d。判断这个上界是否不超过 limit，计算时不能溢出。",
        "一行三个非负整数 b、d 和 limit。", "b^d <= limit 输出 YES，否则输出 NO。", "1 <= b,limit <= 10^18，0 <= d <= 10^18。",
        "3 10 59048\n", "NO\n",
        [("2 10 1024\n", "YES\n"), ("10 18 1000000000000000000\n", "YES\n"), ("10 19 1000000000000000000\n", "NO\n"), ("999999999999999999 0 1\n", "YES\n")],
    ),
    "search-full-tree-node-count": make_problem(
        "search-full-tree-node-count", "计算完整搜索树节点数", "基础", ["复杂度", "搜索树", "等比累加"],
        "完整搜索树每个非叶子都有 b 个子节点，根深度为 0，叶子深度为 d。输出所有层的节点总数。",
        "一行两个整数 b 和 d。", "输出 1+b+b^2+...+b^d。", "1 <= b <= 20，0 <= d <= 15，答案不超过 long long。",
        "2 3\n", "15\n",
        [("1 0\n", "1\n"), ("1 5\n", "6\n"), ("3 2\n", "13\n"), ("10 4\n", "11111\n")],
    ),
}
