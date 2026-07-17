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


PROBLEMS: dict[str, Problem] = {
    "big-integer-type-range": Problem(
        id="big-integer-type-range",
        title="判断最小可用整数类型",
        difficulty="入门",
        tags=["高精度", "整型范围", "字符串比较"],
        statement=(
            "给定一个非负整数 x，它可能超过 long long 的范围。请判断能保存它的最小类型："
            "如果 x <= 2147483647，输出 int；否则如果 x <= 9223372036854775807，输出 long long；"
            "否则输出 big integer。"
        ),
        input_format="一行一个非负整数 x。",
        output_format="输出 int、long long 或 big integer。",
        constraints="1 <= len(x) <= 100。输入不含多余前导零，数字 0 例外。",
        samples=[
            TestCase(input="2147483648\n", output="long long\n"),
        ],
        tests=[
            TestCase(input="0\n", output="int\n"),
            TestCase(input="2147483647\n", output="int\n", hidden=True),
            TestCase(input="2147483648\n", output="long long\n"),
            TestCase(input="9223372036854775807\n", output="long long\n", hidden=True),
            TestCase(input="9223372036854775808\n", output="big integer\n", hidden=True),
            TestCase(input="100000000000000000000\n", output="big integer\n", hidden=True),
        ],
    ),
    "big-integer-raw-echo": Problem(
        id="big-integer-raw-echo",
        title="原样读入并输出大整数",
        difficulty="入门",
        tags=["高精度", "字符串", "读入输出"],
        statement="给定若干个非负大整数，请用字符串读入并按原样输出。数字可能远远超过 long long 的范围。",
        input_format="第一行一个整数 n。接下来 n 行，每行一个非负大整数。",
        output_format="按输入顺序输出这 n 个大整数，每个占一行。",
        constraints="1 <= n <= 20，单个数字长度不超过 200。输入不含多余前导零，数字 0 例外。",
        samples=[
            TestCase(input="3\n0\n12345678901234567890\n100000000000000000000\n", output="0\n12345678901234567890\n100000000000000000000\n"),
        ],
        tests=[
            TestCase(input="3\n0\n12345678901234567890\n100000000000000000000\n", output="0\n12345678901234567890\n100000000000000000000\n"),
            TestCase(input="1\n999999999999999999999999999999\n", output="999999999999999999999999999999\n", hidden=True),
            TestCase(input="4\n1\n22\n333\n4444\n", output="1\n22\n333\n4444\n", hidden=True),
        ],
    ),
    "big-integer-overflow-count": Problem(
        id="big-integer-overflow-count",
        title="统计超出 long long 的数字",
        difficulty="基础",
        tags=["高精度", "整型范围", "批量判断"],
        statement="给定 n 个非负整数，请统计其中有多少个严格大于 9223372036854775807，因此不能用 long long 保存。",
        input_format="第一行一个整数 n。接下来 n 行，每行一个非负整数。",
        output_format="输出超出 long long 范围的数字个数。",
        constraints="1 <= n <= 100，单个数字长度不超过 200。输入不含多余前导零，数字 0 例外。",
        samples=[
            TestCase(input="4\n1\n9223372036854775807\n9223372036854775808\n100000000000000000000\n", output="2\n"),
        ],
        tests=[
            TestCase(input="4\n1\n9223372036854775807\n9223372036854775808\n100000000000000000000\n", output="2\n"),
            TestCase(input="3\n0\n9\n123456789\n", output="0\n", hidden=True),
            TestCase(input="5\n9223372036854775808\n9223372036854775809\n99999999999999999999\n10\n11\n", output="3\n", hidden=True),
            TestCase(input="2\n9223372036854775806\n9223372036854775807\n", output="0\n", hidden=True),
        ],
    ),
    "big-integer-digit-split": Problem(
        id="big-integer-digit-split",
        title="把大整数拆成数字",
        difficulty="入门",
        tags=["高精度", "字符串", "数组", "字符转换"],
        statement="给定一个非负大整数，请把它的每一位转换成数字，并按从高位到低位的顺序输出。",
        input_format="一行一个非负整数 s。",
        output_format="输出每一位数字，数字之间用一个空格分隔。",
        constraints="1 <= len(s) <= 1000。输入不含多余前导零，数字 0 例外。",
        samples=[
            TestCase(input="724105\n", output="7 2 4 1 0 5\n"),
        ],
        tests=[
            TestCase(input="724105\n", output="7 2 4 1 0 5\n"),
            TestCase(input="0\n", output="0\n", hidden=True),
            TestCase(input="9876543210\n", output="9 8 7 6 5 4 3 2 1 0\n", hidden=True),
        ],
    ),
    "big-integer-digit-sum": Problem(
        id="big-integer-digit-sum",
        title="大整数各位数字和",
        difficulty="入门",
        tags=["高精度", "字符串", "字符转换", "累加"],
        statement="给定一个非负大整数，请输出它所有数位上的数字之和。",
        input_format="一行一个非负整数 s。",
        output_format="输出各位数字和。",
        constraints="1 <= len(s) <= 10000。输入不含多余前导零，数字 0 例外。",
        samples=[
            TestCase(input="724105\n", output="19\n"),
        ],
        tests=[
            TestCase(input="724105\n", output="19\n"),
            TestCase(input="0\n", output="0\n", hidden=True),
            TestCase(input="999999\n", output="54\n", hidden=True),
            TestCase(input="12345678901234567890\n", output="90\n", hidden=True),
        ],
    ),
    "big-integer-digit-frequency": Problem(
        id="big-integer-digit-frequency",
        title="统计每个数字出现次数",
        difficulty="基础",
        tags=["高精度", "字符串", "计数数组"],
        statement="给定一个非负大整数，请统计数字 0 到 9 各出现了多少次。",
        input_format="一行一个非负整数 s。",
        output_format="输出 10 个整数，依次表示 0、1、2、...、9 的出现次数，数字之间用一个空格分隔。",
        constraints="1 <= len(s) <= 10000。输入不含多余前导零，数字 0 例外。",
        samples=[
            TestCase(input="1002003000\n", output="7 1 1 1 0 0 0 0 0 0\n"),
        ],
        tests=[
            TestCase(input="1002003000\n", output="7 1 1 1 0 0 0 0 0 0\n"),
            TestCase(input="0\n", output="1 0 0 0 0 0 0 0 0 0\n", hidden=True),
            TestCase(input="9876543210\n", output="1 1 1 1 1 1 1 1 1 1\n", hidden=True),
            TestCase(input="111222333444555666777888999\n", output="0 3 3 3 3 3 3 3 3 3\n", hidden=True),
        ],
    ),
    "big-integer-reverse-store": Problem(
        id="big-integer-reverse-store",
        title="反向存储大整数",
        difficulty="入门",
        tags=["高精度", "反向存储", "数组"],
        statement="给定一个非负大整数，请把它按反向数组存储，并输出数组内容。也就是先输出个位，再输出十位、百位。",
        input_format="一行一个非负整数 s。",
        output_format="输出反向数组中的数字，数字之间用一个空格分隔。",
        constraints="1 <= len(s) <= 1000。输入不含多余前导零，数字 0 例外。",
        samples=[
            TestCase(input="98765\n", output="5 6 7 8 9\n"),
        ],
        tests=[
            TestCase(input="98765\n", output="5 6 7 8 9\n"),
            TestCase(input="0\n", output="0\n", hidden=True),
            TestCase(input="1000\n", output="0 0 0 1\n", hidden=True),
            TestCase(input="1234567890\n", output="0 9 8 7 6 5 4 3 2 1\n", hidden=True),
        ],
    ),
    "big-integer-reverse-restore": Problem(
        id="big-integer-reverse-restore",
        title="反向数组还原大整数",
        difficulty="基础",
        tags=["高精度", "反向存储", "倒序输出"],
        statement="给定一个反向存储的大整数数组，其中第 0 个元素是个位。请把它还原成正常顺序的大整数输出。",
        input_format="第一行一个整数 n。第二行 n 个数字，表示反向数组。",
        output_format="输出正常顺序的大整数。",
        constraints="1 <= n <= 1000。最高位可以为 0，但输出时不要删除数组内部代表数值的位。",
        samples=[
            TestCase(input="5\n5 6 7 8 9\n", output="98765\n"),
        ],
        tests=[
            TestCase(input="5\n5 6 7 8 9\n", output="98765\n"),
            TestCase(input="1\n0\n", output="0\n", hidden=True),
            TestCase(input="4\n0 0 0 1\n", output="1000\n", hidden=True),
            TestCase(input="10\n0 9 8 7 6 5 4 3 2 1\n", output="1234567890\n", hidden=True),
        ],
    ),
    "big-integer-low-position-query": Problem(
        id="big-integer-low-position-query",
        title="查询从低位数的第 k 位",
        difficulty="基础",
        tags=["高精度", "反向存储", "下标"],
        statement=(
            "给定一个非负大整数 s 和 q 次询问。每次给出 k，请输出从低位开始数的第 k 位数字，k 从 0 开始。"
            "如果 k 超出数字长度，输出 0。"
        ),
        input_format="第一行包含一个非负整数 s 和一个整数 q。第二行包含 q 个非负整数 k。",
        output_format="输出 q 个数字，数字之间用一个空格分隔。",
        constraints="1 <= len(s) <= 1000，1 <= q <= 100，0 <= k <= 2000。输入不含多余前导零，数字 0 例外。",
        samples=[
            TestCase(input="98765 5\n0 1 4 5 10\n", output="5 6 9 0 0\n"),
        ],
        tests=[
            TestCase(input="98765 5\n0 1 4 5 10\n", output="5 6 9 0 0\n"),
            TestCase(input="0 3\n0 1 2\n", output="0 0 0\n", hidden=True),
            TestCase(input="1000 4\n0 1 2 3\n", output="0 0 0 1\n", hidden=True),
            TestCase(input="1234567890 6\n0 2 4 6 8 10\n", output="0 8 6 4 2 0\n", hidden=True),
        ],
    ),
    "big-integer-add-basic": Problem(
        id="big-integer-add-basic",
        title="大整数加法",
        difficulty="入门",
        tags=["高精度", "加法", "字符串", "数组"],
        statement="给定两个非负大整数 a 和 b，请输出它们的和。数字可能远远超过 long long 的范围。",
        input_format="一行两个非负整数 a 和 b。",
        output_format="输出 a + b 的结果，不要输出多余的前导零。",
        constraints="1 <= len(a), len(b) <= 1000。输入不含多余前导零，数字 0 例外。",
        samples=[
            TestCase(
                input="98765 8765\n",
                output="107530\n",
            )
        ],
        tests=[
            TestCase(input="98765 8765\n", output="107530\n"),
            TestCase(input="99999999999999999999 1\n", output="100000000000000000000\n", hidden=True),
            TestCase(input="0 0\n", output="0\n", hidden=True),
            TestCase(
                input="12345678901234567890 98765432109876543210\n",
                output="111111111011111111100\n",
                hidden=True,
            ),
            TestCase(input="500 500\n", output="1000\n", hidden=True),
        ],
    ),
    "big-integer-add-trace": Problem(
        id="big-integer-add-trace",
        title="输出逐位计算轨迹",
        difficulty="基础",
        tags=["高精度", "加法", "进位", "过程追踪"],
        statement=(
            "给定两个非负大整数 a 和 b，请用反向数组模拟高精度加法。"
            "第一行输出最终和；第二行按从低位到高位的顺序，输出每一轮计算得到的临时值 t。"
            "这里 t = carry + 当前位 a + 当前位 b，缺失的一位按 0 处理。"
        ),
        input_format="一行两个非负整数 a 和 b。",
        output_format="第一行输出 a + b；第二行输出每一轮的 t，数字之间用一个空格分隔。",
        constraints="1 <= len(a), len(b) <= 1000。第二行只输出主循环中的 t，不额外输出最后的 carry。",
        samples=[
            TestCase(
                input="98765 8765\n",
                output="107530\n10 13 15 17 10\n",
            )
        ],
        tests=[
            TestCase(input="98765 8765\n", output="107530\n10 13 15 17 10\n"),
            TestCase(input="999 1\n", output="1000\n10 10 10\n", hidden=True),
            TestCase(input="123 456\n", output="579\n9 7 5\n", hidden=True),
            TestCase(input="9999 9999\n", output="19998\n18 19 19 19\n", hidden=True),
            TestCase(input="0 0\n", output="0\n0\n", hidden=True),
        ],
    ),
    "big-integer-add-multiple": Problem(
        id="big-integer-add-multiple",
        title="多个大整数求和",
        difficulty="进阶",
        tags=["高精度", "加法", "函数封装", "循环"],
        statement="给定 n 个非负大整数，请输出它们的总和。建议先封装两个大整数相加的函数，再在循环中反复调用。",
        input_format="第一行一个整数 n。接下来 n 行，每行一个非负大整数。",
        output_format="输出所有数字的总和，不要输出多余的前导零。",
        constraints="1 <= n <= 100，单个数字长度不超过 500。输入不含多余前导零，数字 0 例外。",
        samples=[
            TestCase(
                input="3\n999\n1\n1\n",
                output="1001\n",
            )
        ],
        tests=[
            TestCase(input="3\n999\n1\n1\n", output="1001\n"),
            TestCase(
                input="4\n12345678901234567890\n98765432109876543210\n10\n90\n",
                output="111111111011111111200\n",
                hidden=True,
            ),
            TestCase(input="5\n0\n0\n0\n0\n0\n", output="0\n", hidden=True),
            TestCase(
                input="3\n99999999999999999999\n1\n1\n",
                output="100000000000000000001\n",
                hidden=True,
            ),
        ],
    ),
    "big-integer-sub-basic": Problem(
        id="big-integer-sub-basic",
        title="大整数减法",
        difficulty="入门",
        tags=["高精度", "减法", "借位", "字符串", "数组"],
        statement="给定两个非负大整数 a 和 b，且保证 a >= b，请输出 a - b 的结果。",
        input_format="一行两个非负整数 a 和 b。",
        output_format="输出 a - b 的结果，不要输出多余的前导零。",
        constraints="1 <= len(a), len(b) <= 1000。输入不含多余前导零，数字 0 例外，并保证 a >= b。",
        samples=[
            TestCase(
                input="1000 999\n",
                output="1\n",
            )
        ],
        tests=[
            TestCase(input="1000 999\n", output="1\n"),
            TestCase(input="12345678901234567890 12345678901234567889\n", output="1\n", hidden=True),
            TestCase(input="99999999999999999999 1\n", output="99999999999999999998\n", hidden=True),
            TestCase(input="500 500\n", output="0\n", hidden=True),
            TestCase(input="100000000000000000000 99999999999999999999\n", output="1\n", hidden=True),
        ],
    ),
    "big-integer-sub-borrow-count": Problem(
        id="big-integer-sub-borrow-count",
        title="统计借位次数",
        difficulty="基础",
        tags=["高精度", "减法", "借位", "过程追踪"],
        statement=(
            "给定两个非负大整数 a 和 b，且保证 a >= b。请用反向数组模拟高精度减法。"
            "第一行输出最终差；第二行输出借位次数。这里每当某一位计算出的 t < 0，就记一次借位。"
        ),
        input_format="一行两个非负整数 a 和 b。",
        output_format="第一行输出 a - b；第二行输出借位次数。",
        constraints="1 <= len(a), len(b) <= 1000。输入不含多余前导零，数字 0 例外，并保证 a >= b。",
        samples=[
            TestCase(
                input="1000 999\n",
                output="1\n3\n",
            )
        ],
        tests=[
            TestCase(input="1000 999\n", output="1\n3\n"),
            TestCase(input="9320 4785\n", output="4535\n3\n", hidden=True),
            TestCase(input="12345 12345\n", output="0\n0\n", hidden=True),
            TestCase(input="10000 1\n", output="9999\n4\n", hidden=True),
            TestCase(input="500 123\n", output="377\n2\n", hidden=True),
        ],
    ),
    "big-integer-sub-ledger": Problem(
        id="big-integer-sub-ledger",
        title="连续扣款",
        difficulty="进阶",
        tags=["高精度", "减法", "函数封装", "循环"],
        statement=(
            "给定一个非负大整数余额 balance 和 n 笔扣款。请按顺序扣除每一笔金额，输出最终余额。"
            "题目保证任意时刻余额都不会小于当前扣款。"
        ),
        input_format="第一行包含一个非负大整数 balance 和一个整数 n。接下来 n 行，每行一个非负大整数 cost。",
        output_format="输出扣完所有金额后的最终余额，不要输出多余的前导零。",
        constraints="1 <= n <= 100，balance 和每个 cost 的长度不超过 500。输入不含多余前导零，数字 0 例外。",
        samples=[
            TestCase(
                input="1000 3\n333\n333\n334\n",
                output="0\n",
            )
        ],
        tests=[
            TestCase(input="1000 3\n333\n333\n334\n", output="0\n"),
            TestCase(
                input="100000000000000000000 2\n1\n99999999999999999999\n",
                output="0\n",
                hidden=True,
            ),
            TestCase(input="5000 3\n4999\n0\n1\n", output="0\n", hidden=True),
            TestCase(
                input="12345678901234567890 2\n12345678901234560000\n7890\n",
                output="0\n",
                hidden=True,
            ),
        ],
    ),
    "big-integer-compare": Problem(
        id="big-integer-compare",
        title="比较两个大整数",
        difficulty="入门",
        tags=["高精度", "比较", "字符串"],
        statement=(
            "给定两个非负大整数 a 和 b，请比较它们的大小。由于数字可能超过 long long，"
            "请用字符串长度和从高位到低位的字符比较来完成。"
        ),
        input_format="一行两个非负整数 a 和 b。",
        output_format="如果 a > b 输出 >；如果 a < b 输出 <；如果相等输出 =。",
        constraints="1 <= len(a), len(b) <= 1000。输入不含多余前导零，数字 0 例外。",
        samples=[
            TestCase(
                input="12345 987654\n",
                output="<\n",
            )
        ],
        tests=[
            TestCase(input="12345 987654\n", output="<\n"),
            TestCase(input="1000 999\n", output=">\n", hidden=True),
            TestCase(input="12345678901234567890 12345678901234567890\n", output="=\n", hidden=True),
            TestCase(input="99999999999999999999 100000000000000000000\n", output="<\n", hidden=True),
            TestCase(input="700000000000000000001 699999999999999999999\n", output=">\n", hidden=True),
        ],
    ),
    "big-integer-sub-signed": Problem(
        id="big-integer-sub-signed",
        title="任意两个大整数相减",
        difficulty="基础",
        tags=["高精度", "比较", "减法", "负号"],
        statement=(
            "给定两个非负大整数 a 和 b，请输出 a - b。结果可能为负数。"
            "建议先比较 a 和 b 的大小，必要时交换顺序并记录负号，再复用绝对值减法。"
        ),
        input_format="一行两个非负整数 a 和 b。",
        output_format="输出 a - b 的结果；负数需要带一个前导负号，0 不输出负号。",
        constraints="1 <= len(a), len(b) <= 1000。输入不含多余前导零，数字 0 例外。",
        samples=[
            TestCase(
                input="12345 987654\n",
                output="-975309\n",
            )
        ],
        tests=[
            TestCase(input="12345 987654\n", output="-975309\n"),
            TestCase(input="987654 12345\n", output="975309\n", hidden=True),
            TestCase(input="500 500\n", output="0\n", hidden=True),
            TestCase(input="0 99999999999999999999\n", output="-99999999999999999999\n", hidden=True),
            TestCase(input="100000000000000000000 1\n", output="99999999999999999999\n", hidden=True),
        ],
    ),
    "big-integer-sub-sign-batch": Problem(
        id="big-integer-sub-sign-batch",
        title="多组带符号差值",
        difficulty="进阶",
        tags=["高精度", "比较", "减法", "函数封装", "多组输入"],
        statement=(
            "给定 q 组非负大整数 a 和 b，请逐行输出每一组 a - b 的结果。"
            "这一题适合把 compare、subtractAbs 和 subtractSigned 都封装成函数。"
        ),
        input_format="第一行一个整数 q。接下来 q 行，每行两个非负整数 a 和 b。",
        output_format="输出 q 行，第 i 行为第 i 组 a - b 的带符号结果。",
        constraints="1 <= q <= 100；每个数字长度不超过 500。输入不含多余前导零，数字 0 例外。",
        samples=[
            TestCase(
                input="3\n10 3\n3 10\n999 999\n",
                output="7\n-7\n0\n",
            )
        ],
        tests=[
            TestCase(input="3\n10 3\n3 10\n999 999\n", output="7\n-7\n0\n"),
            TestCase(
                input="4\n1000 1\n1 1000\n12345678901234567890 12345678901234567889\n0 0\n",
                output="999\n-999\n1\n0\n",
                hidden=True,
            ),
            TestCase(
                input="2\n100000000000000000000 99999999999999999999\n99999999999999999999 100000000000000000000\n",
                output="1\n-1\n",
                hidden=True,
            ),
            TestCase(
                input="3\n500 123\n123 500\n700000000000000000001 699999999999999999999\n",
                output="377\n-377\n2\n",
                hidden=True,
            ),
        ],
    ),
    "big-integer-mul-small-basic": Problem(
        id="big-integer-mul-small-basic",
        title="大整数乘小整数",
        difficulty="入门",
        tags=["高精度", "乘法", "进位", "字符串", "数组"],
        statement=(
            "给定一个非负大整数 a 和一个非负小整数 b，请输出 a * b。"
            "a 的长度可能远超 long long，需要用反向数组模拟竖式乘法。"
        ),
        input_format="一行包含一个非负大整数 a 和一个非负整数 b。",
        output_format="输出 a * b 的结果，不要输出多余的前导零。",
        constraints="1 <= len(a) <= 1000；0 <= b <= 10000。输入不含多余前导零，数字 0 例外。",
        samples=[
            TestCase(
                input="98765 12\n",
                output="1185180\n",
            )
        ],
        tests=[
            TestCase(input="98765 12\n", output="1185180\n"),
            TestCase(input="999 12\n", output="11988\n", hidden=True),
            TestCase(input="12345678901234567890 9\n", output="111111110111111111010\n", hidden=True),
            TestCase(input="0 9999\n", output="0\n", hidden=True),
            TestCase(input="100000000000000000000 10000\n", output="1000000000000000000000000\n", hidden=True),
        ],
    ),
    "big-integer-mul-small-trace": Problem(
        id="big-integer-mul-small-trace",
        title="输出乘法进位轨迹",
        difficulty="基础",
        tags=["高精度", "乘法", "进位", "过程追踪"],
        statement=(
            "给定一个非负大整数 a 和一个非负小整数 b，请用反向数组完成 a * b。"
            "第一行输出最终乘积；第二行按从低位到高位的顺序，输出主循环每一轮计算出的临时值 t。"
            "这里 t = a[i] * b + carry，第二行不额外输出最后拆分 carry 的过程。"
        ),
        input_format="一行包含一个非负大整数 a 和一个非负整数 b。",
        output_format="第一行输出 a * b；第二行输出每一轮主循环的 t，数字之间用一个空格分隔。",
        constraints="1 <= len(a) <= 1000；0 <= b <= 10000。若 a 只有一位，也仍然输出一项 t。",
        samples=[
            TestCase(
                input="98765 12\n",
                output="1185180\n60 78 91 105 118\n",
            )
        ],
        tests=[
            TestCase(input="98765 12\n", output="1185180\n60 78 91 105 118\n"),
            TestCase(input="999 12\n", output="11988\n108 118 119\n", hidden=True),
            TestCase(input="123 45\n", output="5535\n135 103 55\n", hidden=True),
            TestCase(input="0 10000\n", output="0\n0\n", hidden=True),
            TestCase(input="5005 8\n", output="40040\n40 4 0 40\n", hidden=True),
        ],
    ),
    "big-integer-factorial-small": Problem(
        id="big-integer-factorial-small",
        title="高精度阶乘",
        difficulty="进阶",
        tags=["高精度", "乘法", "函数封装", "循环", "阶乘"],
        statement=(
            "给定一个整数 n，请输出 n!。结果可能非常大，"
            "建议封装“高精度整数乘普通整数”的函数，并在循环中反复更新答案。"
        ),
        input_format="一行一个整数 n。",
        output_format="输出 n! 的十进制表示。",
        constraints="0 <= n <= 200。",
        samples=[
            TestCase(
                input="10\n",
                output="3628800\n",
            )
        ],
        tests=[
            TestCase(input="10\n", output="3628800\n"),
            TestCase(input="0\n", output="1\n", hidden=True),
            TestCase(input="1\n", output="1\n", hidden=True),
            TestCase(input="20\n", output="2432902008176640000\n", hidden=True),
            TestCase(
                input="50\n",
                output="30414093201713378043612608166064768844377641568960512000000000000\n",
                hidden=True,
            ),
        ],
        time_limit_ms=2500,
    ),
    "big-integer-mul-big-basic": Problem(
        id="big-integer-mul-big-basic",
        title="大整数乘大整数",
        difficulty="入门",
        tags=["高精度", "乘法", "双重循环", "字符串", "数组"],
        statement=(
            "给定两个非负大整数 a 和 b，请输出 a * b。两个数都可能远远超过 long long，"
            "需要使用反向数组模拟竖式乘法。"
        ),
        input_format="一行两个非负大整数 a 和 b。",
        output_format="输出 a * b 的结果，不要输出多余的前导零。",
        constraints="1 <= len(a), len(b) <= 500。输入不含多余前导零，数字 0 例外。",
        samples=[
            TestCase(
                input="123 45\n",
                output="5535\n",
            )
        ],
        tests=[
            TestCase(input="123 45\n", output="5535\n"),
            TestCase(input="999 999\n", output="998001\n", hidden=True),
            TestCase(
                input="12345678901234567890 987654321\n",
                output="12193263112482853211126352690\n",
                hidden=True,
            ),
            TestCase(input="0 99999999999999999999\n", output="0\n", hidden=True),
            TestCase(
                input="100000000000000000000 100000000000000000000\n",
                output="10000000000000000000000000000000000000000\n",
                hidden=True,
            ),
        ],
        time_limit_ms=3000,
    ),
    "big-integer-mul-big-grid-trace": Problem(
        id="big-integer-mul-big-grid-trace",
        title="输出乘法网格累加",
        difficulty="基础",
        tags=["高精度", "乘法", "过程追踪", "双重循环", "进位"],
        statement=(
            "给定两个非负大整数 a 和 b，请用反向数组完成 a * b。第一行输出最终乘积；"
            "第二行输出统一进位之前的 raw 数组，也就是执行完所有 raw[i+j] += a[i] * b[j] "
            "之后，从下标 0 到 len(a)+len(b)-1 的每一格数值。"
        ),
        input_format="一行两个非负大整数 a 和 b。",
        output_format=(
            "第一行输出 a * b；第二行输出进位前 raw 数组，数字之间用一个空格分隔。"
        ),
        constraints="1 <= len(a), len(b) <= 200。输入不含多余前导零，数字 0 例外。",
        samples=[
            TestCase(
                input="123 45\n",
                output="5535\n15 22 13 4 0\n",
            )
        ],
        tests=[
            TestCase(input="123 45\n", output="5535\n15 22 13 4 0\n"),
            TestCase(input="99 99\n", output="9801\n81 162 81 0\n", hidden=True),
            TestCase(input="5005 88\n", output="440440\n40 40 0 40 40 0\n", hidden=True),
            TestCase(input="0 12345\n", output="0\n0 0 0 0 0 0\n", hidden=True),
            TestCase(input="314159 2718\n", output="853884162\n72 49 76 86 29 55 18 23 6 0\n", hidden=True),
        ],
        time_limit_ms=3000,
    ),
    "big-integer-power-small": Problem(
        id="big-integer-power-small",
        title="大整数的小指数幂",
        difficulty="进阶",
        tags=["高精度", "乘法", "函数封装", "循环", "幂"],
        statement=(
            "给定一个非负大整数 a 和一个非负整数 n，请输出 a^n。结果可能非常大，"
            "建议封装“高精度乘高精度”函数，并在循环中反复更新答案。约定 0^0 = 1。"
        ),
        input_format="一行包含一个非负大整数 a 和一个非负整数 n。",
        output_format="输出 a^n 的十进制表示。",
        constraints="1 <= len(a) <= 80，0 <= n <= 100。输入不含多余前导零，数字 0 例外。",
        samples=[
            TestCase(
                input="12 3\n",
                output="1728\n",
            )
        ],
        tests=[
            TestCase(input="12 3\n", output="1728\n"),
            TestCase(input="999 2\n", output="998001\n", hidden=True),
            TestCase(input="2 100\n", output="1267650600228229401496703205376\n", hidden=True),
            TestCase(input="12345 0\n", output="1\n", hidden=True),
            TestCase(
                input="123456789 5\n",
                output="28679718602997181072337614380936720482949\n",
                hidden=True,
            ),
        ],
        time_limit_ms=3500,
    ),
    "big-integer-div-small-basic": Problem(
        id="big-integer-div-small-basic",
        title="大整数除小整数",
        difficulty="入门",
        tags=["高精度", "除法", "余数", "字符串"],
        statement=(
            "给定一个非负大整数 a 和一个正整数 b，请输出 a / b 的整数商。"
            "a 可能远远超过 long long 的范围，需要从高位到低位模拟长除法。"
        ),
        input_format="一行包含一个非负大整数 a 和一个正整数 b。",
        output_format="输出 a / b 的整数商，不要输出多余的前导零。",
        constraints="1 <= len(a) <= 1000，1 <= b <= 10000。输入不含多余前导零，数字 0 例外。",
        samples=[
            TestCase(
                input="98765 12\n",
                output="8230\n",
            )
        ],
        tests=[
            TestCase(input="98765 12\n", output="8230\n"),
            TestCase(input="12345678901234567890 9\n", output="1371742100137174210\n", hidden=True),
            TestCase(input="1000 7\n", output="142\n", hidden=True),
            TestCase(input="0 37\n", output="0\n", hidden=True),
            TestCase(input="99999999999999999999 1\n", output="99999999999999999999\n", hidden=True),
        ],
        time_limit_ms=2500,
    ),
    "big-integer-div-small-quot-rem": Problem(
        id="big-integer-div-small-quot-rem",
        title="输出商和余数",
        difficulty="基础",
        tags=["高精度", "除法", "余数", "过程理解"],
        statement=(
            "给定一个非负大整数 a 和一个正整数 b，请用高精度除低精度的方法计算 a / b。"
            "第一行输出整数商，第二行输出余数。"
        ),
        input_format="一行包含一个非负大整数 a 和一个正整数 b。",
        output_format="第一行输出商；第二行输出余数。",
        constraints="1 <= len(a) <= 1000，1 <= b <= 10000。余数必须满足 0 <= r < b。",
        samples=[
            TestCase(
                input="98765 12\n",
                output="8230\n5\n",
            )
        ],
        tests=[
            TestCase(input="98765 12\n", output="8230\n5\n"),
            TestCase(input="12345 37\n", output="333\n24\n", hidden=True),
            TestCase(input="1000 7\n", output="142\n6\n", hidden=True),
            TestCase(input="0 9999\n", output="0\n0\n", hidden=True),
            TestCase(input="99999999999999999999 10\n", output="9999999999999999999\n9\n", hidden=True),
        ],
        time_limit_ms=2500,
    ),
    "big-integer-div-small-trace": Problem(
        id="big-integer-div-small-trace",
        title="输出长除法轨迹",
        difficulty="进阶",
        tags=["高精度", "除法", "余数", "过程追踪"],
        statement=(
            "给定一个非负大整数 a 和一个正整数 b，请模拟高精度除低精度。第一行输出整数商，"
            "第二行输出最终余数；第三行按从高位到低位的顺序，输出每次执行 r = r * 10 + digit "
            "之后、写商之前的临时 r。"
        ),
        input_format="一行包含一个非负大整数 a 和一个正整数 b。",
        output_format=(
            "第一行输出商；第二行输出最终余数；第三行输出每次落下一位后的临时 r，数字之间用一个空格分隔。"
        ),
        constraints="1 <= len(a) <= 500，1 <= b <= 10000。第三行长度应等于 a 的位数。",
        samples=[
            TestCase(
                input="98765 12\n",
                output="8230\n5\n9 98 27 36 5\n",
            )
        ],
        tests=[
            TestCase(input="98765 12\n", output="8230\n5\n9 98 27 36 5\n"),
            TestCase(input="12345 37\n", output="333\n24\n1 12 123 124 135\n", hidden=True),
            TestCase(input="1000 7\n", output="142\n6\n1 10 30 20\n", hidden=True),
            TestCase(input="0 5\n", output="0\n0\n0\n", hidden=True),
            TestCase(input="5005 8\n", output="625\n5\n5 50 20 45\n", hidden=True),
        ],
        time_limit_ms=2500,
    ),
    "big-integer-normalize-array": Problem(
        id="big-integer-normalize-array",
        title="整理倒序结果数组",
        difficulty="入门",
        tags=["高精度", "前导零", "数组", "边界处理"],
        statement=(
            "给定一个高精度计算后的倒序结果数组 c，其中 c[0] 是个位，c[n-1] 是当前最高位。"
            "请删除最高位上多余的 0，但如果整个数就是 0，必须保留一个 0。"
        ),
        input_format="第一行一个整数 n。第二行 n 个数字，按低位到高位的顺序给出。",
        output_format="第一行输出规范化后的数组长度；第二行按低位到高位输出规范化后的数组。",
        constraints="1 <= n <= 1000，0 <= c[i] <= 9。输入数组可能包含多个多余最高位 0。",
        samples=[
            TestCase(
                input="5\n3 2 1 0 0\n",
                output="3\n3 2 1\n",
            )
        ],
        tests=[
            TestCase(input="5\n3 2 1 0 0\n", output="3\n3 2 1\n"),
            TestCase(input="3\n0 0 0\n", output="1\n0\n", hidden=True),
            TestCase(input="4\n0 0 5 0\n", output="3\n0 0 5\n", hidden=True),
            TestCase(input="1\n7\n", output="1\n7\n", hidden=True),
            TestCase(input="8\n9 8 7 0 0 0 0 0\n", output="3\n9 8 7\n", hidden=True),
        ],
        time_limit_ms=2000,
    ),
    "big-integer-trim-string": Problem(
        id="big-integer-trim-string",
        title="整理商字符串",
        difficulty="基础",
        tags=["高精度", "前导零", "字符串", "除法"],
        statement=(
            "高精度除低精度时，商通常从左到右写入字符串，前面可能会出现多余的 0。"
            "给定一个只包含数字的字符串 q，请删除多余前导零；如果 q 表示 0，则输出一个 0。"
        ),
        input_format="一行一个只包含数字的非空字符串 q。",
        output_format="输出删除多余前导零后的字符串。",
        constraints="1 <= len(q) <= 1000。q 可能全由 0 组成。",
        samples=[
            TestCase(
                input="0008230\n",
                output="8230\n",
            )
        ],
        tests=[
            TestCase(input="0008230\n", output="8230\n"),
            TestCase(input="0000\n", output="0\n", hidden=True),
            TestCase(input="123456\n", output="123456\n", hidden=True),
            TestCase(input="000000001\n", output="1\n", hidden=True),
            TestCase(input="000100200\n", output="100200\n", hidden=True),
        ],
        time_limit_ms=2000,
    ),
    "big-integer-normalized-calculator": Problem(
        id="big-integer-normalized-calculator",
        title="边界结果计算器",
        difficulty="进阶",
        tags=["高精度", "前导零", "综合练习", "边界测试"],
        statement=(
            "请实现一个小型高精度计算器，每次操作都输出规范化后的结果。支持四种操作："
            "add 表示 a + b；sub 表示 a - b，保证 a >= b；mul_small 表示 a 乘一个普通非负整数 b；"
            "div_small 表示 a 除以一个普通正整数 b，只输出整数商。输入数字本身也可能带有前导零。"
        ),
        input_format=(
            "第一行一个整数 q。接下来 q 行，每行包含 op、a、b。"
            "op 为 add、sub、mul_small、div_small 之一。"
        ),
        output_format="对每个操作输出一行规范化后的结果，不要输出多余前导零。",
        constraints=(
            "1 <= q <= 30，1 <= len(a), len(b) <= 500。sub 保证 a >= b；"
            "mul_small 的 b 在 int 范围内；div_small 的 b 为正整数。"
        ),
        samples=[
            TestCase(
                input=(
                    "6\n"
                    "add 000999 0001\n"
                    "sub 1000 0999\n"
                    "sub 123456 123456\n"
                    "mul_small 0000 12345\n"
                    "div_small 0005 8\n"
                    "div_small 1000 7\n"
                ),
                output="1000\n1\n0\n0\n0\n142\n",
            )
        ],
        tests=[
            TestCase(
                input=(
                    "6\n"
                    "add 000999 0001\n"
                    "sub 1000 0999\n"
                    "sub 123456 123456\n"
                    "mul_small 0000 12345\n"
                    "div_small 0005 8\n"
                    "div_small 1000 7\n"
                ),
                output="1000\n1\n0\n0\n0\n142\n",
            ),
            TestCase(
                input=(
                    "5\n"
                    "add 0000 0000\n"
                    "add 99999999999999999999 1\n"
                    "mul_small 000123 10\n"
                    "div_small 0001000 10\n"
                    "div_small 7 10\n"
                ),
                output="0\n100000000000000000000\n1230\n100\n0\n",
                hidden=True,
            ),
            TestCase(
                input=(
                    "4\n"
                    "sub 100000000000000000000 1\n"
                    "sub 0000100 0000099\n"
                    "mul_small 99999999999999999999 0\n"
                    "div_small 99999999999999999999 1\n"
                ),
                output="99999999999999999999\n1\n0\n99999999999999999999\n",
                hidden=True,
            ),
            TestCase(
                input=(
                    "4\n"
                    "add 12345678901234567890 98765432109876543210\n"
                    "sub 100000000000000000000 99999999999999999999\n"
                    "mul_small 123456789 9\n"
                    "div_small 12345678901234567890 9\n"
                ),
                output="111111111011111111100\n1\n1111111101\n1371742100137174210\n",
                hidden=True,
            ),
            TestCase(
                input=(
                    "5\n"
                    "add 000001 000009\n"
                    "sub 000999 000999\n"
                    "mul_small 000250 40\n"
                    "div_small 000000 37\n"
                    "div_small 000999 1000\n"
                ),
                output="10\n0\n10000\n0\n0\n",
                hidden=True,
            ),
        ],
        time_limit_ms=3500,
    ),
    "big-integer-fibonacci": Problem(
        id="big-integer-fibonacci",
        title="高精度 Fibonacci",
        difficulty="基础",
        tags=["高精度", "加法", "递推", "Fibonacci", "状态更新"],
        statement=(
            "给定一个非负整数 n，请输出 Fibonacci 数列的第 n 项。约定 F(0)=0，F(1)=1，"
            "F(n)=F(n-1)+F(n-2)。当 n 较大时，结果会超过 long long，需要用高精度加法完成递推。"
        ),
        input_format="一行一个非负整数 n。",
        output_format="输出 F(n) 的十进制表示。",
        constraints="0 <= n <= 5000。",
        samples=[
            TestCase(
                input="10\n",
                output="55\n",
            )
        ],
        tests=[
            TestCase(input="10\n", output="55\n"),
            TestCase(input="0\n", output="0\n", hidden=True),
            TestCase(input="1\n", output="1\n", hidden=True),
            TestCase(input="2\n", output="1\n", hidden=True),
            TestCase(input="100\n", output="354224848179261915075\n", hidden=True),
            TestCase(input="200\n", output="280571172992510140037611932413038677189525\n", hidden=True),
        ],
        time_limit_ms=3000,
    ),
    "big-integer-factorial-sum": Problem(
        id="big-integer-factorial-sum",
        title="阶乘和",
        difficulty="进阶",
        tags=["高精度", "阶乘", "加法", "乘法", "综合练习"],
        statement=(
            "给定一个正整数 n，请输出 1! + 2! + ... + n!。"
            "建议维护当前阶乘 fact 和累计答案 sum：每一轮先更新 fact，再把 fact 加到 sum 中。"
        ),
        input_format="一行一个正整数 n。",
        output_format="输出 1! + 2! + ... + n! 的十进制表示。",
        constraints="1 <= n <= 200。",
        samples=[
            TestCase(
                input="10\n",
                output="4037913\n",
            )
        ],
        tests=[
            TestCase(input="10\n", output="4037913\n"),
            TestCase(input="1\n", output="1\n", hidden=True),
            TestCase(input="3\n", output="9\n", hidden=True),
            TestCase(input="20\n", output="2561327494111820313\n", hidden=True),
            TestCase(
                input="50\n",
                output="31035053229546199656252032972759319953190362094566672920420940313\n",
                hidden=True,
            ),
        ],
        time_limit_ms=3000,
    ),
    "bubble-sort-basic": Problem(
        id="bubble-sort-basic",
        title="手写冒泡排序",
        difficulty="入门",
        tags=["排序", "冒泡排序", "数组"],
        statement="给定 n 个整数，请使用排序算法将它们按从小到大的顺序输出。",
        input_format="第一行一个整数 n。第二行包含 n 个整数。",
        output_format="输出排序后的 n 个整数，数字之间用一个空格分隔。",
        constraints="1 <= n <= 200，整数范围在 [-10000, 10000] 内。",
        samples=[
            TestCase(
                input="5\n5 1 4 2 8\n",
                output="1 2 4 5 8\n",
            )
        ],
        tests=[
            TestCase(input="5\n5 1 4 2 8\n", output="1 2 4 5 8\n"),
            TestCase(input="6\n3 3 2 1 2 1\n", output="1 1 2 2 3 3\n", hidden=True),
            TestCase(input="4\n-1 10 0 -5\n", output="-5 -1 0 10\n", hidden=True),
            TestCase(input="1\n42\n", output="42\n", hidden=True),
        ],
    ),
    "bubble-sort-count": Problem(
        id="bubble-sort-count",
        title="统计交换次数",
        difficulty="基础",
        tags=["排序", "冒泡排序", "计数"],
        statement="给定 n 个整数，请按从小到大排序，并输出冒泡排序过程中发生的交换次数。",
        input_format="第一行一个整数 n。第二行包含 n 个整数。",
        output_format="第一行输出排序后的数组；第二行输出交换次数。",
        constraints="1 <= n <= 200，整数范围在 [-10000, 10000] 内。",
        samples=[
            TestCase(
                input="5\n5 1 4 2 8\n",
                output="1 2 4 5 8\n4\n",
            )
        ],
        tests=[
            TestCase(input="5\n5 1 4 2 8\n", output="1 2 4 5 8\n4\n"),
            TestCase(input="4\n1 2 3 4\n", output="1 2 3 4\n0\n", hidden=True),
            TestCase(input="4\n4 3 2 1\n", output="1 2 3 4\n6\n", hidden=True),
            TestCase(input="6\n3 3 2 1 2 1\n", output="1 1 2 2 3 3\n11\n", hidden=True),
        ],
    ),
    "bubble-sort-flag": Problem(
        id="bubble-sort-flag",
        title="提前结束优化",
        difficulty="进阶",
        tags=["排序", "冒泡排序", "优化"],
        statement="给定 n 个整数，请使用带 changed 标记的冒泡排序优化，并输出排序后的结果。",
        input_format="第一行一个整数 n。第二行包含 n 个整数。",
        output_format="输出排序后的 n 个整数，数字之间用一个空格分隔。",
        constraints="1 <= n <= 2000，整数范围在 [-10000, 10000] 内。",
        samples=[
            TestCase(
                input="5\n1 2 3 5 4\n",
                output="1 2 3 4 5\n",
            )
        ],
        tests=[
            TestCase(input="5\n1 2 3 5 4\n", output="1 2 3 4 5\n"),
            TestCase(input="8\n1 2 3 4 5 6 7 8\n", output="1 2 3 4 5 6 7 8\n", hidden=True),
            TestCase(input="7\n7 1 6 2 5 3 4\n", output="1 2 3 4 5 6 7\n", hidden=True),
        ],
    ),
    "selection-sort-basic": Problem(
        id="selection-sort-basic",
        title="手写选择排序",
        difficulty="入门",
        tags=["排序", "选择排序", "数组"],
        statement="给定 n 个整数，请使用选择排序思想将它们按从小到大的顺序输出。",
        input_format="第一行一个整数 n。第二行包含 n 个整数。",
        output_format="输出排序后的 n 个整数，数字之间用一个空格分隔。",
        constraints="1 <= n <= 200，整数范围在 [-10000, 10000] 内。",
        samples=[
            TestCase(
                input="5\n6 3 5 1 4\n",
                output="1 3 4 5 6\n",
            )
        ],
        tests=[
            TestCase(input="5\n6 3 5 1 4\n", output="1 3 4 5 6\n"),
            TestCase(input="6\n3 3 2 1 2 1\n", output="1 1 2 2 3 3\n", hidden=True),
            TestCase(input="4\n-1 10 0 -5\n", output="-5 -1 0 10\n", hidden=True),
            TestCase(input="1\n42\n", output="42\n", hidden=True),
        ],
    ),
    "selection-sort-trace": Problem(
        id="selection-sort-trace",
        title="记录每轮最小值下标",
        difficulty="基础",
        tags=["排序", "选择排序", "过程追踪"],
        statement=(
            "给定 n 个整数，请按从小到大选择排序。第一行输出排序结果；"
            "第二行输出每一轮扫描结束后最终选中的 minIndex。若 n=1，第二行输出空行。"
        ),
        input_format="第一行一个整数 n。第二行包含 n 个整数。",
        output_format="第一行输出排序后的数组；第二行输出每一轮选择的 minIndex。",
        constraints="1 <= n <= 200。选择最小值时只在 a[j] < a[minIndex] 时更新，遇到相等元素不更新。",
        samples=[
            TestCase(
                input="5\n5 1 4 2 8\n",
                output="1 2 4 5 8\n1 3 2 3\n",
            )
        ],
        tests=[
            TestCase(input="5\n5 1 4 2 8\n", output="1 2 4 5 8\n1 3 2 3\n"),
            TestCase(input="4\n4 3 2 1\n", output="1 2 3 4\n3 2 2\n", hidden=True),
            TestCase(input="6\n2 2 1 1 3 0\n", output="0 1 1 2 2 3\n5 2 3 3 5\n", hidden=True),
            TestCase(input="1\n9\n", output="9\n\n", hidden=True),
        ],
    ),
    "selection-sort-desc": Problem(
        id="selection-sort-desc",
        title="选择排序降序版",
        difficulty="进阶",
        tags=["排序", "选择排序", "降序"],
        statement="给定 n 个整数，请使用选择排序思想将它们按从大到小的顺序输出。",
        input_format="第一行一个整数 n。第二行包含 n 个整数。",
        output_format="输出降序排序后的 n 个整数，数字之间用一个空格分隔。",
        constraints="1 <= n <= 200，整数范围在 [-10000, 10000] 内。",
        samples=[
            TestCase(
                input="5\n6 3 5 1 4\n",
                output="6 5 4 3 1\n",
            )
        ],
        tests=[
            TestCase(input="5\n6 3 5 1 4\n", output="6 5 4 3 1\n"),
            TestCase(input="6\n3 3 2 1 2 1\n", output="3 3 2 2 1 1\n", hidden=True),
            TestCase(input="4\n-1 10 0 -5\n", output="10 0 -1 -5\n", hidden=True),
            TestCase(input="1\n42\n", output="42\n", hidden=True),
        ],
    ),
    "insertion-sort-basic": Problem(
        id="insertion-sort-basic",
        title="手写插入排序",
        difficulty="入门",
        tags=["排序", "插入排序", "数组"],
        statement="给定 n 个整数，请使用插入排序思想将它们按从小到大的顺序输出。",
        input_format="第一行一个整数 n。第二行包含 n 个整数。",
        output_format="输出排序后的 n 个整数，数字之间用一个空格分隔。",
        constraints="1 <= n <= 200，整数范围在 [-10000, 10000] 内。",
        samples=[
            TestCase(
                input="5\n5 1 4 2 8\n",
                output="1 2 4 5 8\n",
            )
        ],
        tests=[
            TestCase(input="5\n5 1 4 2 8\n", output="1 2 4 5 8\n"),
            TestCase(input="6\n3 3 2 1 2 1\n", output="1 1 2 2 3 3\n", hidden=True),
            TestCase(input="4\n-1 10 0 -5\n", output="-5 -1 0 10\n", hidden=True),
            TestCase(input="1\n42\n", output="42\n", hidden=True),
        ],
    ),
    "insertion-sort-shifts": Problem(
        id="insertion-sort-shifts",
        title="统计右移次数",
        difficulty="基础",
        tags=["排序", "插入排序", "计数"],
        statement="给定 n 个整数，请按从小到大插入排序，并输出排序过程中元素向右移动的次数。",
        input_format="第一行一个整数 n。第二行包含 n 个整数。",
        output_format="第一行输出排序后的数组；第二行输出右移次数。",
        constraints="1 <= n <= 200。只有执行 a[j + 1] = a[j] 时才计入一次右移；相等元素不右移。",
        samples=[
            TestCase(
                input="5\n5 1 4 2 8\n",
                output="1 2 4 5 8\n4\n",
            )
        ],
        tests=[
            TestCase(input="5\n5 1 4 2 8\n", output="1 2 4 5 8\n4\n"),
            TestCase(input="4\n1 2 3 4\n", output="1 2 3 4\n0\n", hidden=True),
            TestCase(input="4\n4 3 2 1\n", output="1 2 3 4\n6\n", hidden=True),
            TestCase(input="6\n3 3 2 1 2 1\n", output="1 1 2 2 3 3\n11\n", hidden=True),
        ],
    ),
    "insertion-sort-desc": Problem(
        id="insertion-sort-desc",
        title="插入排序降序版",
        difficulty="进阶",
        tags=["排序", "插入排序", "降序"],
        statement="给定 n 个整数，请使用插入排序思想将它们按从大到小的顺序输出。",
        input_format="第一行一个整数 n。第二行包含 n 个整数。",
        output_format="输出降序排序后的 n 个整数，数字之间用一个空格分隔。",
        constraints="1 <= n <= 200，整数范围在 [-10000, 10000] 内。",
        samples=[
            TestCase(
                input="5\n5 1 4 2 8\n",
                output="8 5 4 2 1\n",
            )
        ],
        tests=[
            TestCase(input="5\n5 1 4 2 8\n", output="8 5 4 2 1\n"),
            TestCase(input="6\n3 3 2 1 2 1\n", output="3 3 2 2 1 1\n", hidden=True),
            TestCase(input="4\n-1 10 0 -5\n", output="10 0 -1 -5\n", hidden=True),
            TestCase(input="1\n42\n", output="42\n", hidden=True),
        ],
    ),
    "counting-sort-basic": Problem(
        id="counting-sort-basic",
        title="小值域计数排序",
        difficulty="入门",
        tags=["排序", "计数排序", "数组"],
        statement="给定 n 个非负整数，请使用计数排序思想，将它们按从小到大的顺序输出。",
        input_format="第一行一个整数 n。第二行包含 n 个非负整数。",
        output_format="输出排序后的 n 个整数，数字之间用一个空格分隔。",
        constraints="1 <= n <= 1000，0 <= ai <= 1000。",
        samples=[
            TestCase(
                input="6\n3 1 2 3 0 2\n",
                output="0 1 2 2 3 3\n",
            )
        ],
        tests=[
            TestCase(input="6\n3 1 2 3 0 2\n", output="0 1 2 2 3 3\n"),
            TestCase(input="5\n4 4 0 1 4\n", output="0 1 4 4 4\n", hidden=True),
            TestCase(input="1\n0\n", output="0\n", hidden=True),
            TestCase(input="8\n9 1 9 0 5 5 2 1\n", output="0 1 1 2 5 5 9 9\n", hidden=True),
        ],
    ),
    "counting-sort-frequency": Problem(
        id="counting-sort-frequency",
        title="输出频率表",
        difficulty="基础",
        tags=["排序", "计数排序", "频率表"],
        statement="给定 n 个范围在 0 到 m 之间的整数，请输出每个数值出现的次数。",
        input_format="第一行两个整数 n 和 m。第二行包含 n 个整数，每个整数 x 满足 0 <= x <= m。",
        output_format="输出 m + 1 个整数，第 i 个数表示数值 i 出现的次数。",
        constraints="1 <= n <= 1000，0 <= m <= 1000。",
        samples=[
            TestCase(
                input="6 3\n3 1 2 3 0 2\n",
                output="1 1 2 2\n",
            )
        ],
        tests=[
            TestCase(input="6 3\n3 1 2 3 0 2\n", output="1 1 2 2\n"),
            TestCase(input="5 4\n4 4 0 1 4\n", output="1 1 0 0 3\n", hidden=True),
            TestCase(input="1 0\n0\n", output="1\n", hidden=True),
            TestCase(
                input="8 9\n9 1 9 0 5 5 2 1\n",
                output="1 2 1 0 0 2 0 0 0 2\n",
                hidden=True,
            ),
        ],
    ),
    "counting-sort-offset": Problem(
        id="counting-sort-offset",
        title="带负数的计数排序",
        difficulty="进阶",
        tags=["排序", "计数排序", "下标映射"],
        statement=(
            "给定 n 个整数，数值可能为负数。请使用计数排序思想和 offset 映射，"
            "将它们按从小到大的顺序输出。"
        ),
        input_format="第一行一个整数 n。第二行包含 n 个整数。",
        output_format="输出排序后的 n 个整数，数字之间用一个空格分隔。",
        constraints="1 <= n <= 1000，-1000 <= ai <= 1000。",
        samples=[
            TestCase(
                input="7\n-2 3 0 -2 1 3 -1\n",
                output="-2 -2 -1 0 1 3 3\n",
            )
        ],
        tests=[
            TestCase(input="7\n-2 3 0 -2 1 3 -1\n", output="-2 -2 -1 0 1 3 3\n"),
            TestCase(input="5\n-5 -1 -3 -5 0\n", output="-5 -5 -3 -1 0\n", hidden=True),
            TestCase(input="6\n2 -2 2 -2 0 1\n", output="-2 -2 0 1 2 2\n", hidden=True),
            TestCase(input="1\n-7\n", output="-7\n", hidden=True),
        ],
    ),
    "merge-sort-basic": Problem(
        id="merge-sort-basic",
        title="手写归并排序",
        difficulty="基础",
        tags=["排序", "归并排序", "分治"],
        statement="给定 n 个整数，请使用归并排序思想，将它们按从小到大的顺序输出。",
        input_format="第一行一个整数 n。第二行包含 n 个整数。",
        output_format="输出排序后的 n 个整数，数字之间用一个空格分隔。",
        constraints="1 <= n <= 200000，整数范围在 [-1000000000, 1000000000] 内。",
        samples=[
            TestCase(
                input="6\n6 3 5 1 4 2\n",
                output="1 2 3 4 5 6\n",
            )
        ],
        tests=[
            TestCase(input="6\n6 3 5 1 4 2\n", output="1 2 3 4 5 6\n"),
            TestCase(input="6\n3 3 2 1 2 1\n", output="1 1 2 2 3 3\n", hidden=True),
            TestCase(input="5\n-1 10 0 -5 10\n", output="-5 -1 0 10 10\n", hidden=True),
            TestCase(input="1\n42\n", output="42\n", hidden=True),
        ],
        time_limit_ms=2500,
    ),
    "merge-two-sorted-arrays": Problem(
        id="merge-two-sorted-arrays",
        title="合并两个有序数组",
        difficulty="入门",
        tags=["排序", "归并排序", "双指针"],
        statement="给定两个已经按非降序排列的数组，请用双指针将它们合并为一个新的非降序数组。",
        input_format="第一行两个整数 n 和 m。第二行包含 n 个整数，第三行包含 m 个整数，两个数组均已按非降序排列。",
        output_format="输出合并后的 n + m 个整数，数字之间用一个空格分隔。",
        constraints="1 <= n, m <= 100000，整数范围在 [-1000000000, 1000000000] 内。",
        samples=[
            TestCase(
                input="3 3\n3 5 6\n1 2 4\n",
                output="1 2 3 4 5 6\n",
            )
        ],
        tests=[
            TestCase(input="3 3\n3 5 6\n1 2 4\n", output="1 2 3 4 5 6\n"),
            TestCase(input="4 3\n1 2 2 5\n2 3 4\n", output="1 2 2 2 3 4 5\n", hidden=True),
            TestCase(input="2 4\n-5 10\n-6 -5 0 10\n", output="-6 -5 -5 0 10 10\n", hidden=True),
            TestCase(input="1 1\n7\n7\n", output="7 7\n", hidden=True),
        ],
        time_limit_ms=2000,
    ),
    "merge-sort-inversions": Problem(
        id="merge-sort-inversions",
        title="归并排序数逆序对",
        difficulty="进阶",
        tags=["排序", "归并排序", "逆序对"],
        statement=(
            "给定 n 个整数，请输出数组中的逆序对数量。若 i < j 且 a[i] > a[j]，"
            "则 (i, j) 是一个逆序对。可以在归并排序的合并过程中统计答案。"
        ),
        input_format="第一行一个整数 n。第二行包含 n 个整数。",
        output_format="输出一个整数，表示逆序对数量。",
        constraints="1 <= n <= 200000，整数范围在 [-1000000000, 1000000000] 内，答案可能超过 int 范围。",
        samples=[
            TestCase(
                input="5\n2 4 1 3 5\n",
                output="3\n",
            )
        ],
        tests=[
            TestCase(input="5\n2 4 1 3 5\n", output="3\n"),
            TestCase(input="5\n1 2 3 4 5\n", output="0\n", hidden=True),
            TestCase(input="5\n5 4 3 2 1\n", output="10\n", hidden=True),
            TestCase(input="6\n3 3 2 1 2 1\n", output="11\n", hidden=True),
        ],
        time_limit_ms=2500,
    ),
    "quick-sort-basic": Problem(
        id="quick-sort-basic",
        title="手写快速排序",
        difficulty="基础",
        tags=["排序", "快速排序", "分治"],
        statement="给定 n 个整数，请使用快速排序思想，将它们按从小到大的顺序输出。",
        input_format="第一行一个整数 n。第二行包含 n 个整数。",
        output_format="输出排序后的 n 个整数，数字之间用一个空格分隔。",
        constraints="1 <= n <= 2000，整数范围在 [-1000000000, 1000000000] 内。",
        samples=[
            TestCase(
                input="7\n5 2 7 3 6 1 4\n",
                output="1 2 3 4 5 6 7\n",
            )
        ],
        tests=[
            TestCase(input="7\n5 2 7 3 6 1 4\n", output="1 2 3 4 5 6 7\n"),
            TestCase(input="6\n3 3 2 1 2 1\n", output="1 1 2 2 3 3\n", hidden=True),
            TestCase(input="5\n-1 10 0 -5 10\n", output="-5 -1 0 10 10\n", hidden=True),
            TestCase(input="4\n1 2 3 4\n", output="1 2 3 4\n", hidden=True),
        ],
        time_limit_ms=2000,
    ),
    "quick-sort-partition": Problem(
        id="quick-sort-partition",
        title="完成一次分区",
        difficulty="入门",
        tags=["排序", "快速排序", "分区"],
        statement=(
            "给定 n 个整数，请以最后一个元素作为 pivot，对整个数组执行一次 Lomuto 分区。"
            "输出分区后的数组，以及 pivot 的最终下标。"
        ),
        input_format="第一行一个整数 n。第二行包含 n 个整数。",
        output_format="第一行输出分区后的数组；第二行输出 pivot 的最终下标，使用 0-based 下标。",
        constraints="1 <= n <= 2000。分区时若 a[j] <= pivot，就交换进左侧小区间。",
        samples=[
            TestCase(
                input="7\n5 2 7 3 6 1 4\n",
                output="2 3 1 4 6 7 5\n3\n",
            )
        ],
        tests=[
            TestCase(input="7\n5 2 7 3 6 1 4\n", output="2 3 1 4 6 7 5\n3\n"),
            TestCase(input="4\n4 1 3 2\n", output="1 2 3 4\n1\n", hidden=True),
            TestCase(input="4\n1 2 3 4\n", output="1 2 3 4\n3\n", hidden=True),
            TestCase(input="5\n3 1 3 2 3\n", output="3 1 3 2 3\n4\n", hidden=True),
        ],
        time_limit_ms=2000,
    ),
    "quick-select-kth": Problem(
        id="quick-select-kth",
        title="快速选择第 k 小",
        difficulty="进阶",
        tags=["排序", "快速排序", "快速选择"],
        statement=(
            "给定 n 个整数和 k，请输出第 k 小的数。可以借用快速排序的分区思想，"
            "每次只递归进入包含第 k 小元素的一侧。"
        ),
        input_format="第一行两个整数 n 和 k。第二行包含 n 个整数。",
        output_format="输出第 k 小的整数。k 使用 1-based 排名。",
        constraints="1 <= k <= n <= 2000，整数范围在 [-1000000000, 1000000000] 内。",
        samples=[
            TestCase(
                input="7 4\n5 2 7 3 6 1 4\n",
                output="4\n",
            )
        ],
        tests=[
            TestCase(input="7 4\n5 2 7 3 6 1 4\n", output="4\n"),
            TestCase(input="6 3\n3 1 2 2 5 4\n", output="2\n", hidden=True),
            TestCase(input="5 2\n-1 10 0 -5 3\n", output="-1\n", hidden=True),
            TestCase(input="5 5\n5 4 3 2 1\n", output="5\n", hidden=True),
        ],
        time_limit_ms=2000,
    ),
    "recurrence-climb-stairs-basic": Problem(
        id="recurrence-climb-stairs-basic",
        title="爬楼梯方法数",
        difficulty="入门",
        tags=["递推", "状态定义", "爬楼梯", "一维状态"],
        statement=(
            "有一条楼梯，你一次可以走 1 阶或 2 阶。请输出从第 0 阶走到第 n 阶的方法数。"
            "本题约定 f[0] = 1，表示什么都不走也是一种到达第 0 阶的方法。"
        ),
        input_format="一行一个整数 n。",
        output_format="输出走到第 n 阶的方法数。",
        constraints="0 <= n <= 45。答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="5\n",
                output="8\n",
            )
        ],
        tests=[
            TestCase(input="5\n", output="8\n"),
            TestCase(input="0\n", output="1\n", hidden=True),
            TestCase(input="1\n", output="1\n", hidden=True),
            TestCase(input="2\n", output="2\n", hidden=True),
            TestCase(input="10\n", output="89\n", hidden=True),
            TestCase(input="45\n", output="1836311903\n", hidden=True),
        ],
    ),
    "recurrence-state-table": Problem(
        id="recurrence-state-table",
        title="输出状态表",
        difficulty="基础",
        tags=["递推", "状态表", "爬楼梯", "初始化"],
        statement=(
            "仍然考虑一次走 1 阶或 2 阶的楼梯问题。请输出 f[0] 到 f[n] 的整张状态表，"
            "其中 f[i] 表示走到第 i 阶的方法数。"
        ),
        input_format="一行一个整数 n。",
        output_format="输出 n + 1 个整数，依次为 f[0], f[1], ..., f[n]，数字之间用一个空格分隔。",
        constraints="0 <= n <= 45。答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="5\n",
                output="1 1 2 3 5 8\n",
            )
        ],
        tests=[
            TestCase(input="5\n", output="1 1 2 3 5 8\n"),
            TestCase(input="0\n", output="1\n", hidden=True),
            TestCase(input="1\n", output="1 1\n", hidden=True),
            TestCase(input="2\n", output="1 1 2\n", hidden=True),
            TestCase(input="10\n", output="1 1 2 3 5 8 13 21 34 55 89\n", hidden=True),
        ],
    ),
    "recurrence-domino-tiling": Problem(
        id="recurrence-domino-tiling",
        title="2 x n 骨牌覆盖",
        difficulty="进阶",
        tags=["递推", "状态定义", "骨牌覆盖", "模型转换"],
        statement=(
            "用若干块 2 x 1 的骨牌覆盖一个 2 x n 的矩形，骨牌可以竖着放，也可以横着放。"
            "请输出一共有多少种覆盖方法。"
        ),
        input_format="一行一个整数 n。",
        output_format="输出覆盖 2 x n 矩形的方法数。",
        constraints="0 <= n <= 45。空矩形 n = 0 时，覆盖方法数为 1。",
        samples=[
            TestCase(
                input="5\n",
                output="8\n",
            )
        ],
        tests=[
            TestCase(input="5\n", output="8\n"),
            TestCase(input="0\n", output="1\n", hidden=True),
            TestCase(input="1\n", output="1\n", hidden=True),
            TestCase(input="2\n", output="2\n", hidden=True),
            TestCase(input="8\n", output="34\n", hidden=True),
            TestCase(input="45\n", output="1836311903\n", hidden=True),
        ],
    ),
    "recurrence-known-to-unknown-sequence": Problem(
        id="recurrence-known-to-unknown-sequence",
        title="从已知推出第 n 项",
        difficulty="入门",
        tags=["递推", "已知状态", "循环起点", "一维状态"],
        statement=(
            "已知 f[1] = 1，f[2] = 2。对于 i >= 3，有 f[i] = f[i - 1] + f[i - 2]。"
            "给定 n，请输出 f[n]。"
        ),
        input_format="一行一个整数 n。",
        output_format="输出 f[n] 的值。",
        constraints="1 <= n <= 45。答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="6\n",
                output="13\n",
            )
        ],
        tests=[
            TestCase(input="6\n", output="13\n"),
            TestCase(input="1\n", output="1\n", hidden=True),
            TestCase(input="2\n", output="2\n", hidden=True),
            TestCase(input="3\n", output="3\n", hidden=True),
            TestCase(input="10\n", output="89\n", hidden=True),
            TestCase(input="45\n", output="1836311903\n", hidden=True),
        ],
    ),
    "recurrence-new-state-log": Problem(
        id="recurrence-new-state-log",
        title="输出新状态",
        difficulty="基础",
        tags=["递推", "填表过程", "已知区", "状态输出"],
        statement=(
            "仍然已知 f[1] = 1，f[2] = 2，且 f[i] = f[i - 1] + f[i - 2]。"
            "给定 n，请只输出从 f[3] 到 f[n] 这些新算出的状态值。"
        ),
        input_format="一行一个整数 n。",
        output_format="输出 n - 2 个整数，依次为 f[3], f[4], ..., f[n]，数字之间用一个空格分隔。",
        constraints="3 <= n <= 45。答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="6\n",
                output="3 5 8 13\n",
            )
        ],
        tests=[
            TestCase(input="6\n", output="3 5 8 13\n"),
            TestCase(input="3\n", output="3\n", hidden=True),
            TestCase(input="4\n", output="3 5\n", hidden=True),
            TestCase(input="10\n", output="3 5 8 13 21 34 55 89\n", hidden=True),
            TestCase(input="45\n", output=(
                "3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181 "
                "6765 10946 17711 28657 46368 75025 121393 196418 317811 "
                "514229 832040 1346269 2178309 3524578 5702887 9227465 "
                "14930352 24157817 39088169 63245986 102334155 165580141 "
                "267914296 433494437 701408733 1134903170 1836311903\n"
            ), hidden=True),
        ],
    ),
    "recurrence-third-order-sequence": Problem(
        id="recurrence-third-order-sequence",
        title="前三项推出当前项",
        difficulty="进阶",
        tags=["递推", "三项依赖", "循环起点", "边界"],
        statement=(
            "已知 f[1] = 1，f[2] = 1，f[3] = 2。对于 i >= 4，"
            "有 f[i] = f[i - 1] + f[i - 2] + f[i - 3]。给定 n，请输出 f[n]。"
        ),
        input_format="一行一个整数 n。",
        output_format="输出 f[n] 的值。",
        constraints="1 <= n <= 35。答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="6\n",
                output="13\n",
            )
        ],
        tests=[
            TestCase(input="6\n", output="13\n"),
            TestCase(input="1\n", output="1\n", hidden=True),
            TestCase(input="2\n", output="1\n", hidden=True),
            TestCase(input="3\n", output="2\n", hidden=True),
            TestCase(input="10\n", output="149\n", hidden=True),
            TestCase(input="20\n", output="66012\n", hidden=True),
        ],
    ),
    "recurrence-climb-stairs-transition": Problem(
        id="recurrence-climb-stairs-transition",
        title="最后一步分类求方法数",
        difficulty="入门",
        tags=["递推", "爬楼梯", "状态转移", "最后一步分类"],
        statement=(
            "有一条楼梯，你一次可以走 1 阶或 2 阶。请用最后一步分类的思想求出走到第 n 阶的方法数。"
            "本题约定 f[0] = 1，f[1] = 1，且 f[i] = f[i - 1] + f[i - 2]。"
        ),
        input_format="一行一个整数 n。",
        output_format="输出走到第 n 阶的方法数。",
        constraints="0 <= n <= 45。答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="6\n",
                output="13\n",
            )
        ],
        tests=[
            TestCase(input="6\n", output="13\n"),
            TestCase(input="0\n", output="1\n", hidden=True),
            TestCase(input="1\n", output="1\n", hidden=True),
            TestCase(input="2\n", output="2\n", hidden=True),
            TestCase(input="10\n", output="89\n", hidden=True),
            TestCase(input="45\n", output="1836311903\n", hidden=True),
        ],
    ),
    "recurrence-climb-stairs-transition-table": Problem(
        id="recurrence-climb-stairs-transition-table",
        title="输出转移表",
        difficulty="基础",
        tags=["递推", "爬楼梯", "填表", "一维状态"],
        statement=(
            "仍然考虑一次走 1 阶或 2 阶的楼梯问题。已知 f[0] = 1、f[1] = 1，"
            "请输出从 f[2] 到 f[n] 这些通过递推新算出的状态值。"
        ),
        input_format="一行一个整数 n。",
        output_format="输出 n - 1 个整数，依次为 f[2], f[3], ..., f[n]，数字之间用一个空格分隔。",
        constraints="2 <= n <= 45。答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="6\n",
                output="2 3 5 8 13\n",
            )
        ],
        tests=[
            TestCase(input="6\n", output="2 3 5 8 13\n"),
            TestCase(input="2\n", output="2\n", hidden=True),
            TestCase(input="3\n", output="2 3\n", hidden=True),
            TestCase(input="10\n", output="2 3 5 8 13 21 34 55 89\n", hidden=True),
            TestCase(input="45\n", output=(
                "2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181 "
                "6765 10946 17711 28657 46368 75025 121393 196418 317811 "
                "514229 832040 1346269 2178309 3524578 5702887 9227465 "
                "14930352 24157817 39088169 63245986 102334155 165580141 "
                "267914296 433494437 701408733 1134903170 1836311903\n"
            ), hidden=True),
        ],
    ),
    "recurrence-climb-stairs-source-trace": Problem(
        id="recurrence-climb-stairs-source-trace",
        title="最后一步来源分解",
        difficulty="进阶",
        tags=["递推", "爬楼梯", "转移来源", "调试输出"],
        statement=(
            "已知 f[0] = 1、f[1] = 1，且 f[i] = f[i - 1] + f[i - 2]。"
            "给定 n，请输出每个新状态的来源分解，格式为 i:a+b=c，"
            "表示 f[i] = f[i - 1] + f[i - 2]。"
        ),
        input_format="一行一个整数 n。",
        output_format="从 i = 2 到 n，每行输出一条来源分解：i:a+b=c。",
        constraints="2 <= n <= 20。答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="5\n",
                output="2:1+1=2\n3:2+1=3\n4:3+2=5\n5:5+3=8\n",
            )
        ],
        tests=[
            TestCase(input="5\n", output="2:1+1=2\n3:2+1=3\n4:3+2=5\n5:5+3=8\n"),
            TestCase(input="2\n", output="2:1+1=2\n", hidden=True),
            TestCase(input="3\n", output="2:1+1=2\n3:2+1=3\n", hidden=True),
            TestCase(input="7\n", output=(
                "2:1+1=2\n3:2+1=3\n4:3+2=5\n5:5+3=8\n"
                "6:8+5=13\n7:13+8=21\n"
            ), hidden=True),
            TestCase(input="10\n", output=(
                "2:1+1=2\n3:2+1=3\n4:3+2=5\n5:5+3=8\n"
                "6:8+5=13\n7:13+8=21\n8:21+13=34\n"
                "9:34+21=55\n10:55+34=89\n"
            ), hidden=True),
        ],
    ),
    "recurrence-fibonacci-zero-based": Problem(
        id="recurrence-fibonacci-zero-based",
        title="0-based Fibonacci",
        difficulty="入门",
        tags=["递推", "Fibonacci", "0-based", "初始化"],
        statement=(
            "给定一个非负整数 n，请输出 Fibonacci 数列的第 n 项。"
            "本题约定 F(0) = 0，F(1) = 1，且对 i >= 2 有 F(i) = F(i - 1) + F(i - 2)。"
        ),
        input_format="一行一个整数 n。",
        output_format="输出 F(n) 的值。",
        constraints="0 <= n <= 90。答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="6\n",
                output="8\n",
            )
        ],
        tests=[
            TestCase(input="6\n", output="8\n"),
            TestCase(input="0\n", output="0\n", hidden=True),
            TestCase(input="1\n", output="1\n", hidden=True),
            TestCase(input="2\n", output="1\n", hidden=True),
            TestCase(input="45\n", output="1134903170\n", hidden=True),
            TestCase(input="90\n", output="2880067194370816120\n", hidden=True),
        ],
        time_limit_ms=2000,
    ),
    "recurrence-fibonacci-one-based": Problem(
        id="recurrence-fibonacci-one-based",
        title="1-based Fibonacci",
        difficulty="基础",
        tags=["递推", "Fibonacci", "1-based", "循环起点"],
        statement=(
            "给定一个正整数 n，请输出 Fibonacci 数列的第 n 项。"
            "本题约定 F(1) = 1，F(2) = 1，且对 i >= 3 有 F(i) = F(i - 1) + F(i - 2)。"
        ),
        input_format="一行一个整数 n。",
        output_format="输出 F(n) 的值。",
        constraints="1 <= n <= 90。答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="6\n",
                output="8\n",
            )
        ],
        tests=[
            TestCase(input="6\n", output="8\n"),
            TestCase(input="1\n", output="1\n", hidden=True),
            TestCase(input="2\n", output="1\n", hidden=True),
            TestCase(input="3\n", output="2\n", hidden=True),
            TestCase(input="45\n", output="1134903170\n", hidden=True),
            TestCase(input="90\n", output="2880067194370816120\n", hidden=True),
        ],
        time_limit_ms=2000,
    ),
    "recurrence-fibonacci-index-table": Problem(
        id="recurrence-fibonacci-index-table",
        title="下标对照表",
        difficulty="进阶",
        tags=["递推", "Fibonacci", "下标对照", "状态表"],
        statement=(
            "给定 n，请同时输出 0-based Fibonacci 的 f[k] 和 1-based Fibonacci 的 F[k + 1]。"
            "其中 f[0] = 0，f[1] = 1；F[1] = 1，F[2] = 1。"
            "这张表用来观察同一类数列在不同题目定义下的下标偏移。"
        ),
        input_format="一行一个整数 n。",
        output_format="从 k = 0 到 n，每行输出 k:f[k] F[k+1]，冒号后两个数字之间用一个空格分隔。",
        constraints="0 <= n <= 20。答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="5\n",
                output="0:0 1\n1:1 1\n2:1 2\n3:2 3\n4:3 5\n5:5 8\n",
            )
        ],
        tests=[
            TestCase(input="5\n", output="0:0 1\n1:1 1\n2:1 2\n3:2 3\n4:3 5\n5:5 8\n"),
            TestCase(input="0\n", output="0:0 1\n", hidden=True),
            TestCase(input="1\n", output="0:0 1\n1:1 1\n", hidden=True),
            TestCase(input="10\n", output=(
                "0:0 1\n1:1 1\n2:1 2\n3:2 3\n4:3 5\n5:5 8\n"
                "6:8 13\n7:13 21\n8:21 34\n9:34 55\n10:55 89\n"
            ), hidden=True),
            TestCase(input="20\n", output=(
                "0:0 1\n1:1 1\n2:1 2\n3:2 3\n4:3 5\n5:5 8\n"
                "6:8 13\n7:13 21\n8:21 34\n9:34 55\n10:55 89\n"
                "11:89 144\n12:144 233\n13:233 377\n14:377 610\n"
                "15:610 987\n16:987 1597\n17:1597 2584\n18:2584 4181\n"
                "19:4181 6765\n20:6765 10946\n"
            ), hidden=True),
        ],
        time_limit_ms=2000,
    ),
    "recurrence-rolling-fibonacci": Problem(
        id="recurrence-rolling-fibonacci",
        title="滚动变量求 Fibonacci",
        difficulty="入门",
        tags=["递推", "滚动变量", "Fibonacci", "空间优化"],
        statement=(
            "给定一个非负整数 n，请输出 0-based Fibonacci 的第 n 项。"
            "本题约定 F(0) = 0，F(1) = 1，且 F(i) = F(i - 1) + F(i - 2)。"
            "请尝试只使用少量变量完成递推，而不是保存整张数组表。"
        ),
        input_format="一行一个整数 n。",
        output_format="输出 F(n) 的值。",
        constraints="0 <= n <= 90。答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="6\n",
                output="8\n",
            )
        ],
        tests=[
            TestCase(input="6\n", output="8\n"),
            TestCase(input="0\n", output="0\n", hidden=True),
            TestCase(input="1\n", output="1\n", hidden=True),
            TestCase(input="2\n", output="1\n", hidden=True),
            TestCase(input="45\n", output="1134903170\n", hidden=True),
            TestCase(input="90\n", output="2880067194370816120\n", hidden=True),
        ],
        time_limit_ms=2000,
    ),
    "recurrence-rolling-climb-stairs": Problem(
        id="recurrence-rolling-climb-stairs",
        title="滚动变量求爬楼梯",
        difficulty="基础",
        tags=["递推", "滚动变量", "爬楼梯", "空间优化"],
        statement=(
            "有一条楼梯，你一次可以走 1 阶或 2 阶。"
            "本题约定 f[0] = 1，f[1] = 1，且 f[i] = f[i - 1] + f[i - 2]。"
            "请用滚动变量求走到第 n 阶的方法数。"
        ),
        input_format="一行一个整数 n。",
        output_format="输出走到第 n 阶的方法数。",
        constraints="0 <= n <= 45。答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="6\n",
                output="13\n",
            )
        ],
        tests=[
            TestCase(input="6\n", output="13\n"),
            TestCase(input="0\n", output="1\n", hidden=True),
            TestCase(input="1\n", output="1\n", hidden=True),
            TestCase(input="2\n", output="2\n", hidden=True),
            TestCase(input="10\n", output="89\n", hidden=True),
            TestCase(input="45\n", output="1836311903\n", hidden=True),
        ],
        time_limit_ms=2000,
    ),
    "recurrence-rolling-trace": Problem(
        id="recurrence-rolling-trace",
        title="输出滚动过程",
        difficulty="进阶",
        tags=["递推", "滚动变量", "调试输出", "更新顺序"],
        statement=(
            "从 0-based Fibonacci 开始：F(0) = 0，F(1) = 1。"
            "请用变量 a、b 表示当前窗口里的两个旧状态，"
            "从 i = 2 到 n 输出每一步的计算过程，格式为 i:a+b=c。"
            "输出之后再执行 a = b、b = c。"
        ),
        input_format="一行一个整数 n。",
        output_format="从 i = 2 到 n，每行输出一条滚动过程：i:a+b=c。",
        constraints="2 <= n <= 20。答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="6\n",
                output="2:0+1=1\n3:1+1=2\n4:1+2=3\n5:2+3=5\n6:3+5=8\n",
            )
        ],
        tests=[
            TestCase(input="6\n", output="2:0+1=1\n3:1+1=2\n4:1+2=3\n5:2+3=5\n6:3+5=8\n"),
            TestCase(input="2\n", output="2:0+1=1\n", hidden=True),
            TestCase(input="3\n", output="2:0+1=1\n3:1+1=2\n", hidden=True),
            TestCase(input="10\n", output=(
                "2:0+1=1\n3:1+1=2\n4:1+2=3\n5:2+3=5\n"
                "6:3+5=8\n7:5+8=13\n8:8+13=21\n"
                "9:13+21=34\n10:21+34=55\n"
            ), hidden=True),
            TestCase(input="20\n", output=(
                "2:0+1=1\n3:1+1=2\n4:1+2=3\n5:2+3=5\n"
                "6:3+5=8\n7:5+8=13\n8:8+13=21\n"
                "9:13+21=34\n10:21+34=55\n11:34+55=89\n"
                "12:55+89=144\n13:89+144=233\n14:144+233=377\n"
                "15:233+377=610\n16:377+610=987\n17:610+987=1597\n"
                "18:987+1597=2584\n19:1597+2584=4181\n20:2584+4181=6765\n"
            ), hidden=True),
        ],
        time_limit_ms=2000,
    ),
    "recurrence-pascal-triangle-row": Problem(
        id="recurrence-pascal-triangle-row",
        title="输出杨辉三角第 n 行",
        difficulty="入门",
        tags=["递推", "二维递推", "杨辉三角", "边界条件"],
        statement=(
            "给定一个正整数 n，请输出杨辉三角的第 n 行。"
            "本题使用 1-based 行号：第 1 行是 1，第 2 行是 1 1。"
            "建议用 f[i][j] 表示第 i 行第 j 个数。"
        ),
        input_format="一行一个整数 n。",
        output_format="输出第 n 行的 n 个整数，数字之间用一个空格分隔。",
        constraints="1 <= n <= 60。答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="5\n",
                output="1 4 6 4 1\n",
            )
        ],
        tests=[
            TestCase(input="5\n", output="1 4 6 4 1\n"),
            TestCase(input="1\n", output="1\n", hidden=True),
            TestCase(input="2\n", output="1 1\n", hidden=True),
            TestCase(input="6\n", output="1 5 10 10 5 1\n", hidden=True),
            TestCase(input="10\n", output="1 9 36 84 126 126 84 36 9 1\n", hidden=True),
            TestCase(
                input="20\n",
                output="1 19 171 969 3876 11628 27132 50388 75582 92378 92378 75582 50388 27132 11628 3876 969 171 19 1\n",
                hidden=True,
            ),
        ],
        time_limit_ms=2000,
    ),
    "recurrence-pascal-triangle-table": Problem(
        id="recurrence-pascal-triangle-table",
        title="输出前 n 行杨辉三角",
        difficulty="基础",
        tags=["递推", "二维递推", "杨辉三角", "填表"],
        statement=(
            "给定一个正整数 n，请输出杨辉三角的前 n 行。"
            "每一行两端都是 1，内部格满足 f[i][j] = f[i - 1][j - 1] + f[i - 1][j]。"
        ),
        input_format="一行一个整数 n。",
        output_format="输出 n 行，第 i 行包含 i 个整数，数字之间用一个空格分隔。",
        constraints="1 <= n <= 20。答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="5\n",
                output="1\n1 1\n1 2 1\n1 3 3 1\n1 4 6 4 1\n",
            )
        ],
        tests=[
            TestCase(input="5\n", output="1\n1 1\n1 2 1\n1 3 3 1\n1 4 6 4 1\n"),
            TestCase(input="1\n", output="1\n", hidden=True),
            TestCase(input="2\n", output="1\n1 1\n", hidden=True),
            TestCase(input="6\n", output="1\n1 1\n1 2 1\n1 3 3 1\n1 4 6 4 1\n1 5 10 10 5 1\n", hidden=True),
            TestCase(
                input="10\n",
                output=(
                    "1\n"
                    "1 1\n"
                    "1 2 1\n"
                    "1 3 3 1\n"
                    "1 4 6 4 1\n"
                    "1 5 10 10 5 1\n"
                    "1 6 15 20 15 6 1\n"
                    "1 7 21 35 35 21 7 1\n"
                    "1 8 28 56 70 56 28 8 1\n"
                    "1 9 36 84 126 126 84 36 9 1\n"
                ),
                hidden=True,
            ),
        ],
        time_limit_ms=2000,
    ),
    "recurrence-pascal-triangle-query": Problem(
        id="recurrence-pascal-triangle-query",
        title="查询杨辉三角中的一个数",
        difficulty="进阶",
        tags=["递推", "二维递推", "杨辉三角", "组合数"],
        statement=(
            "给定 n 和 k，请输出杨辉三角第 n 行第 k 个数。"
            "本题使用 1-based 行列号，并保证 1 <= k <= n。"
        ),
        input_format="一行两个整数 n 和 k。",
        output_format="输出第 n 行第 k 个数。",
        constraints="1 <= k <= n <= 60。答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="5 3\n",
                output="6\n",
            )
        ],
        tests=[
            TestCase(input="5 3\n", output="6\n"),
            TestCase(input="1 1\n", output="1\n", hidden=True),
            TestCase(input="6 2\n", output="5\n", hidden=True),
            TestCase(input="10 5\n", output="126\n", hidden=True),
            TestCase(input="20 10\n", output="92378\n", hidden=True),
            TestCase(input="30 15\n", output="77558760\n", hidden=True),
            TestCase(input="60 30\n", output="59132290782430712\n", hidden=True),
        ],
        time_limit_ms=2000,
    ),
    "recurrence-grid-paths-basic": Problem(
        id="recurrence-grid-paths-basic",
        title="走方格路径数",
        difficulty="入门",
        tags=["递推", "二维递推", "路径计数", "网格"],
        statement=(
            "给定一个 n 行 m 列的方格地图。"
            "从左上角出发，每一步只能向右或向下走，"
            "请输出走到右下角一共有多少种不同走法。"
        ),
        input_format="一行两个整数 n 和 m，表示网格有 n 行 m 列。",
        output_format="输出从左上角走到右下角的方法数。",
        constraints="1 <= n, m <= 30。答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="3 4\n",
                output="10\n",
            )
        ],
        tests=[
            TestCase(input="3 4\n", output="10\n"),
            TestCase(input="1 1\n", output="1\n", hidden=True),
            TestCase(input="1 5\n", output="1\n", hidden=True),
            TestCase(input="4 5\n", output="35\n", hidden=True),
            TestCase(input="5 5\n", output="70\n", hidden=True),
            TestCase(input="10 10\n", output="48620\n", hidden=True),
            TestCase(input="30 30\n", output="30067266499541040\n", hidden=True),
        ],
        time_limit_ms=2000,
    ),
    "recurrence-grid-paths-table": Problem(
        id="recurrence-grid-paths-table",
        title="输出路径计数表",
        difficulty="基础",
        tags=["递推", "二维递推", "路径计数", "填表"],
        statement=(
            "给定 n 行 m 列的方格地图。"
            "请输出整张路径计数表，其中 dp[i][j] 表示从左上角走到第 i 行第 j 列的方法数。"
            "本题使用 1-based 行列含义，但输出时只输出数值表。"
        ),
        input_format="一行两个整数 n 和 m。",
        output_format="输出 n 行，每行 m 个整数，数字之间用一个空格分隔。",
        constraints="1 <= n, m <= 12。答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="3 4\n",
                output="1 1 1 1\n1 2 3 4\n1 3 6 10\n",
            )
        ],
        tests=[
            TestCase(input="3 4\n", output="1 1 1 1\n1 2 3 4\n1 3 6 10\n"),
            TestCase(input="1 6\n", output="1 1 1 1 1 1\n", hidden=True),
            TestCase(input="2 2\n", output="1 1\n1 2\n", hidden=True),
            TestCase(input="4 5\n", output="1 1 1 1 1\n1 2 3 4 5\n1 3 6 10 15\n1 4 10 20 35\n", hidden=True),
            TestCase(input="5 3\n", output="1 1 1\n1 2 3\n1 3 6\n1 4 10\n1 5 15\n", hidden=True),
        ],
        time_limit_ms=2000,
    ),
    "recurrence-grid-paths-obstacle": Problem(
        id="recurrence-grid-paths-obstacle",
        title="带障碍的走方格",
        difficulty="进阶",
        tags=["递推", "二维递推", "路径计数", "障碍"],
        statement=(
            "给定一个 n 行 m 列的地图，'.' 表示可以走，'#' 表示障碍。"
            "从左上角出发，每一步只能向右或向下走，不能走进障碍格。"
            "请输出走到右下角的方法数。如果起点或终点是障碍，答案为 0。"
        ),
        input_format="第一行两个整数 n 和 m。接下来 n 行，每行一个长度为 m 的字符串，只包含 '.' 和 '#'。",
        output_format="输出从左上角走到右下角的方法数。",
        constraints="1 <= n, m <= 30。答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="3 4\n....\n.#..\n....\n",
                output="4\n",
            )
        ],
        tests=[
            TestCase(input="3 4\n....\n.#..\n....\n", output="4\n"),
            TestCase(input="1 1\n.\n", output="1\n", hidden=True),
            TestCase(input="1 1\n#\n", output="0\n", hidden=True),
            TestCase(input="3 3\n...\n...\n...\n", output="6\n", hidden=True),
            TestCase(input="3 3\n.#.\n...\n...\n", output="3\n", hidden=True),
            TestCase(input="4 5\n.....\n.##..\n...#.\n.....\n", output="5\n", hidden=True),
            TestCase(input="5 5\n.....\n###..\n.....\n..#..\n.....\n", output="5\n", hidden=True),
        ],
        time_limit_ms=2000,
    ),
    "recurrence-number-tower-basic": Problem(
        id="recurrence-number-tower-basic",
        title="数塔最大路径和",
        difficulty="入门",
        tags=["递推", "二维递推", "数塔", "最值"],
        statement=(
            "给定一个 n 层数塔。"
            "从最顶端出发，每一步只能走到下一层相邻的左下或右下位置。"
            "请输出从顶端走到底层能得到的最大路径和。"
        ),
        input_format="第一行一个整数 n。接下来 n 行，第 i 行有 i 个整数，表示数塔第 i 层。",
        output_format="输出最大路径和。",
        constraints="1 <= n <= 50。每个数字在 0 到 1000000 之间，答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="5\n7\n3 8\n8 1 0\n2 7 4 4\n4 5 2 6 5\n",
                output="30\n",
            )
        ],
        tests=[
            TestCase(input="5\n7\n3 8\n8 1 0\n2 7 4 4\n4 5 2 6 5\n", output="30\n"),
            TestCase(input="1\n42\n", output="42\n", hidden=True),
            TestCase(input="3\n1\n2 3\n4 5 6\n", output="10\n", hidden=True),
            TestCase(input="4\n5\n9 6\n4 6 8\n0 7 1 5\n", output="27\n", hidden=True),
            TestCase(input="4\n0\n0 0\n0 0 0\n0 0 0 0\n", output="0\n", hidden=True),
            TestCase(input="6\n9\n1 2\n3 4 5\n9 1 1 9\n2 8 3 7 4\n6 5 4 3 2 1\n", output="35\n", hidden=True),
        ],
        time_limit_ms=2000,
    ),
    "recurrence-number-tower-table": Problem(
        id="recurrence-number-tower-table",
        title="输出数塔递推表",
        difficulty="基础",
        tags=["递推", "二维递推", "数塔", "填表"],
        statement=(
            "给定一个 n 层数塔。"
            "请按自底向上的方法计算 f 表，其中 f[i][j] 表示从第 i 行第 j 个数走到底层的最大路径和。"
            "输出整张 f 表。"
        ),
        input_format="第一行一个整数 n。接下来 n 行，第 i 行有 i 个整数。",
        output_format="输出 n 行，第 i 行输出 i 个整数，表示 f[i][1] 到 f[i][i]，数字之间用一个空格分隔。",
        constraints="1 <= n <= 30。每个数字在 0 到 1000000 之间，答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="5\n7\n3 8\n8 1 0\n2 7 4 4\n4 5 2 6 5\n",
                output="30\n23 21\n20 13 10\n7 12 10 10\n4 5 2 6 5\n",
            )
        ],
        tests=[
            TestCase(
                input="5\n7\n3 8\n8 1 0\n2 7 4 4\n4 5 2 6 5\n",
                output="30\n23 21\n20 13 10\n7 12 10 10\n4 5 2 6 5\n",
            ),
            TestCase(input="1\n9\n", output="9\n", hidden=True),
            TestCase(input="3\n1\n2 3\n4 5 6\n", output="10\n7 9\n4 5 6\n", hidden=True),
            TestCase(
                input="4\n5\n9 6\n4 6 8\n0 7 1 5\n",
                output="27\n22 19\n11 13 13\n0 7 1 5\n",
                hidden=True,
            ),
        ],
        time_limit_ms=2000,
    ),
    "recurrence-number-tower-min": Problem(
        id="recurrence-number-tower-min",
        title="数塔最小路径和",
        difficulty="进阶",
        tags=["递推", "二维递推", "数塔", "最值"],
        statement=(
            "给定一个 n 层数塔。"
            "从最顶端出发，每一步只能走到下一层相邻的左下或右下位置。"
            "请输出从顶端走到底层能得到的最小路径和。"
        ),
        input_format="第一行一个整数 n。接下来 n 行，第 i 行有 i 个整数。",
        output_format="输出最小路径和。",
        constraints="1 <= n <= 50。每个数字在 0 到 1000000 之间，答案可以用 long long 存储。",
        samples=[
            TestCase(
                input="5\n7\n3 8\n8 1 0\n2 7 4 4\n4 5 2 6 5\n",
                output="17\n",
            )
        ],
        tests=[
            TestCase(input="5\n7\n3 8\n8 1 0\n2 7 4 4\n4 5 2 6 5\n", output="17\n"),
            TestCase(input="1\n42\n", output="42\n", hidden=True),
            TestCase(input="3\n1\n2 3\n4 5 6\n", output="7\n", hidden=True),
            TestCase(input="4\n5\n9 6\n4 6 8\n0 7 1 5\n", output="18\n", hidden=True),
            TestCase(input="4\n0\n0 0\n0 0 0\n0 0 0 0\n", output="0\n", hidden=True),
        ],
        time_limit_ms=2000,
    ),
}


def list_problems() -> list[Problem]:
    return list(PROBLEMS.values())


def get_problem(problem_id: str) -> Problem | None:
    return PROBLEMS.get(problem_id)
