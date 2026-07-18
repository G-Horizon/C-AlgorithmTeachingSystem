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
        tags=["分治", *tags],
        statement=statement,
        input_format=input_format,
        output_format=output_format,
        constraints=constraints,
        samples=[sample],
        tests=[sample, *(TestCase(data, answer, hidden=True) for data, answer in hidden_cases)],
    )


DIVIDE_CONQUER_PROBLEMS: dict[str, Problem] = {
    "divide-range-sum": make_problem(
        "divide-range-sum", "分治求区间总和", "入门", ["分解与合并", "递归"],
        "用分治递归计算数组所有元素之和：长度为 1 时直接返回，其他区间拆成左右两半并合并答案。",
        "第一行 n；第二行 n 个整数。", "输出数组元素总和。",
        "1 <= n <= 200000，元素绝对值不超过 10^9。",
        "5\n2 -1 4 3 7\n", "15\n",
        [("1\n-9\n", "-9\n"), ("4\n0 0 0 0\n", "0\n"), ("6\n1000000000 1000000000 -1 -2 -3 -4\n", "1999999990\n")],
    ),
    "divide-range-maximum": make_problem(
        "divide-range-maximum", "分治求数组最大值", "基础", ["分解与合并", "最大值"],
        "用分治递归求数组最大值。左右子问题返回后，用 max 合并当前区间答案。",
        "第一行 n；第二行 n 个整数。", "输出数组最大值。",
        "1 <= n <= 200000，元素绝对值不超过 10^18。",
        "6\n-8 3 9 1 9 2\n", "9\n",
        [("1\n-100\n", "-100\n"), ("5\n-5 -2 -9 -3 -7\n", "-2\n"), ("4\n8 8 8 8\n", "8\n")],
    ),
    "divide-binary-search-index": make_problem(
        "divide-binary-search-index", "二分查找目标下标", "入门", ["二分查找", "闭区间"],
        "在严格递增数组中用二分查找 target，找到则输出 0-based 下标，否则输出 -1。",
        "第一行 n 和 target；第二行 n 个严格递增整数。", "输出目标下标或 -1。",
        "1 <= n <= 200000。",
        "7 11\n1 3 5 7 9 11 13\n", "5\n",
        [("1 4\n4\n", "0\n"), ("5 0\n1 2 3 4 5\n", "-1\n"), ("6 8\n-10 -3 0 8 20 99\n", "3\n")],
    ),
    "divide-binary-search-comparisons": make_problem(
        "divide-binary-search-comparisons", "统计二分比较次数", "基础", ["二分查找", "过程统计"],
        "按闭区间二分模板查找 target。每次读取 a[mid] 记一次比较，找到或区间为空后输出比较次数。",
        "第一行 n 和 target；第二行 n 个严格递增整数。", "输出读取并比较中点元素的次数。",
        "1 <= n <= 200000。",
        "7 6\n1 2 3 4 5 6 7\n", "2\n",
        [("1 9\n9\n", "1\n"), ("7 8\n1 2 3 4 5 6 7\n", "3\n"), ("8 1\n1 2 3 4 5 6 7 8\n", "3\n")],
    ),
    "divide-lower-bound-index": make_problem(
        "divide-lower-bound-index", "第一个大于等于 target", "基础", ["边界二分", "lower_bound"],
        "在非递减数组中找到第一个大于等于 target 的元素下标。若所有元素都小于 target，输出 n。",
        "第一行 n 和 target；第二行 n 个非递减整数。", "输出 0-based 下标，末尾插入位置为 n。",
        "1 <= n <= 200000。",
        "7 4\n1 2 4 4 4 8 10\n", "2\n",
        [("5 0\n1 2 3 4 5\n", "0\n"), ("5 9\n1 2 3 4 5\n", "5\n"), ("4 3\n3 3 3 3\n", "0\n")],
    ),
    "divide-number-range": make_problem(
        "divide-number-range", "数的起止范围", "进阶", ["边界二分", "重复元素"],
        "在非递减数组中输出 target 第一次和最后一次出现的 0-based 下标；不存在时输出 -1 -1。",
        "第一行 n 和 target；第二行 n 个非递减整数。", "输出 first last。",
        "1 <= n <= 200000。",
        "8 4\n1 2 4 4 4 4 7 9\n", "2 5\n",
        [("5 3\n1 2 4 5 6\n", "-1 -1\n"), ("4 7\n7 7 7 7\n", "0 3\n"), ("6 9\n1 2 3 4 5 9\n", "5 5\n")],
    ),
    "divide-merge-sort": make_problem(
        "divide-merge-sort", "实现归并排序", "基础", ["归并排序", "双指针"],
        "使用归并排序将数组按非递减顺序排列。",
        "第一行 n；第二行 n 个整数。", "一行输出排序后的 n 个整数。",
        "1 <= n <= 200000。",
        "7\n5 2 9 1 5 6 3\n", "1 2 3 5 5 6 9\n",
        [("1\n-2\n", "-2\n"), ("5\n5 4 3 2 1\n", "1 2 3 4 5\n"), ("6\n0 -1 0 -3 2 2\n", "-3 -1 0 0 2 2\n")],
    ),
    "divide-merge-two-sorted": make_problem(
        "divide-merge-two-sorted", "合并两个有序数组", "入门", ["归并", "双指针"],
        "给定两个非递减数组，用双指针把它们合并成一个非递减数组。",
        "第一行 n 和 m；第二、三行分别为两个数组。", "输出合并后的 n+m 个整数。",
        "1 <= n,m <= 200000，n+m <= 300000。",
        "4 5\n1 3 3 9\n2 3 5 8 10\n", "1 2 3 3 3 5 8 9 10\n",
        [("1 1\n1\n2\n", "1 2\n"), ("3 2\n4 5 6\n-2 10\n", "-2 4 5 6 10\n"), ("2 3\n1 1\n1 1 1\n", "1 1 1 1 1\n")],
    ),
    "divide-quick-sort": make_problem(
        "divide-quick-sort", "实现快速排序", "基础", ["快速排序", "partition"],
        "使用快速排序将数组按非递减顺序排列。实现时要保证重复值情况下区间仍严格缩小。",
        "第一行 n；第二行 n 个整数。", "一行输出排序后的数组。",
        "1 <= n <= 200000。",
        "7\n4 2 8 4 1 9 3\n", "1 2 3 4 4 8 9\n",
        [("1\n6\n", "6\n"), ("5\n2 2 2 2 2\n", "2 2 2 2 2\n"), ("6\n-1 8 0 -5 8 3\n", "-5 -1 0 3 8 8\n")],
    ),
    "divide-lomuto-partition": make_problem(
        "divide-lomuto-partition", "完成一次 pivot 分区", "基础", ["快速排序", "Lomuto 分区"],
        "取最后一个元素为 pivot。从左向右扫描，把小于等于 pivot 的元素稳定地交换到边界左侧，最后让 pivot 就位。输出 pivot 的 0-based 下标与分区后的数组。",
        "第一行 n；第二行 n 个整数。", "第一行 pivot 下标；第二行分区后的数组。",
        "1 <= n <= 200000。",
        "6\n7 2 5 1 8 5\n", "3\n2 5 1 5 8 7\n",
        [("1\n9\n", "0\n9\n"), ("5\n1 2 3 4 9\n", "4\n1 2 3 4 9\n"), ("5\n9 8 7 6 1\n", "0\n1 8 7 6 9\n")],
    ),
    "divide-fast-power-mod": make_problem(
        "divide-fast-power-mod", "快速幂取模", "基础", ["快速幂", "模运算"],
        "计算 base^exponent mod mod。指数可以很大，必须使用二进制快速幂。",
        "一行三个非负整数 base、exponent、mod。", "输出取模结果。",
        "0 <= base <= 10^18，0 <= exponent <= 10^18，1 <= mod <= 10^18。",
        "2 10 1000\n", "24\n",
        [("7 0 13\n", "1\n"), ("10 9 1\n", "0\n"), ("123456789 2 1000000007\n", "643499475\n")],
    ),
    "divide-fast-power-steps": make_problem(
        "divide-fast-power-steps", "快速幂轮数与乘入次数", "入门", ["快速幂", "二进制"],
        "模拟快速幂处理指数的过程。输出 exponent 变为 0 需要的右移轮数，以及其中最低位为 1、会把 base 乘入答案的轮数。指数 0 输出 0 0。",
        "一行一个非负整数 exponent。", "输出 rounds multiplyRounds。",
        "0 <= exponent <= 10^18。",
        "13\n", "4 3\n",
        [("0\n", "0 0\n"), ("16\n", "5 1\n"), ("15\n", "4 4\n")],
    ),
    "divide-inversion-count": make_problem(
        "divide-inversion-count", "统计数组逆序对", "进阶", ["归并排序", "逆序对"],
        "统计满足 i<j 且 a[i]>a[j] 的下标对数量。答案可能很大，请使用 long long。",
        "第一行 n；第二行 n 个整数。", "输出逆序对数量。",
        "1 <= n <= 200000。",
        "5\n2 3 8 6 1\n", "5\n",
        [("1\n9\n", "0\n"), ("5\n1 2 3 4 5\n", "0\n"), ("5\n5 4 3 2 1\n", "10\n"), ("4\n2 2 1 1\n", "4\n")],
    ),
    "divide-cross-inversions": make_problem(
        "divide-cross-inversions", "统计两个有序段的跨区间逆序对", "基础", ["归并", "跨区间贡献"],
        "给定两个各自非递减的数组 left 和 right，且 left 中元素在原数组的下标都更小。统计 left[i] > right[j] 的数对数量。",
        "第一行 n 和 m；第二、三行是两个非递减数组。", "输出跨区间逆序对数量。",
        "1 <= n,m <= 200000。",
        "4 3\n1 4 6 9\n2 5 8\n", "6\n",
        [("2 2\n1 2\n3 4\n", "0\n"), ("3 2\n5 5 5\n1 5\n", "3\n"), ("3 3\n7 8 9\n1 2 3\n", "9\n")],
    ),
    "divide-level-work": make_problem(
        "divide-level-work", "估算分治层数与总工作", "基础", ["递归树", "复杂度"],
        "一个规模 n 的问题每轮把子问题规模向上折半，直到规模 1。根为第 0 层。输出拆分轮数 levels；若递归树每一层的总工作都记作 n，再输出包括叶子层在内的总工作 n*(levels+1)。",
        "一行一个正整数 n。", "输出 levels totalWork。",
        "1 <= n <= 10^12。",
        "8\n", "3 32\n",
        [("1\n", "0 1\n"), ("5\n", "3 20\n"), ("16\n", "4 80\n")],
    ),
    "divide-full-tree-nodes": make_problem(
        "divide-full-tree-nodes", "完整二叉递归树节点数", "入门", ["递归树", "节点计数"],
        "一棵完整二叉递归树有 leaves 个叶子，leaves 保证是 2 的幂。输出整棵树的节点总数。",
        "一行一个 leaves。", "输出节点总数。",
        "1 <= leaves <= 2^50，且 leaves 是 2 的幂。",
        "8\n", "15\n",
        [("1\n", "1\n"), ("2\n", "3\n"), ("16\n", "31\n")],
    ),
}
