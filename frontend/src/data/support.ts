export type ProblemGuide = {
  hints: string[];
  solution: string[];
  pitfalls: string[];
};

export type ChapterQuizOption = {
  id: string;
  text: string;
};

export type ChapterQuizQuestion = {
  id: string;
  prompt: string;
  options: ChapterQuizOption[];
  answer: string;
  explanation: string;
  relatedProblemIds: string[];
};

export type ChapterReviewPack = {
  title: string;
  description: string;
  problemIds: string[];
};

export type ChapterSummaryQuiz = {
  chapterId: string;
  title: string;
  summary: string;
  checklist: string[];
  questions: ChapterQuizQuestion[];
  reviewPlan: ChapterReviewPack[];
};

const guide = (hints: string[], solution: string[], pitfalls: string[]): ProblemGuide => ({
  hints,
  solution,
  pitfalls,
});

export const chapterSummaryQuizzes: Record<string, ChapterSummaryQuiz> = {
  "big-integer": {
    chapterId: "big-integer",
    title: "第一章总结测验：高精度计算",
    summary:
      "这一章的目标不是背模板，而是看懂普通数字装不下时，怎样把一个大整数拆成可控的一位一位来处理。",
    checklist: [
      "能解释为什么大整数要用 string 读入，而不是直接放进 long long。",
      "能把数字字符转成整数数字，并知道什么时候要正向、什么时候要反向存储。",
      "能用 carry、borrow、remainder 分别描述加法、减法、乘法和除法中的状态。",
      "能在每个高精度函数结束前整理前导零，并保留真正的 0。",
      "能把高精度函数放进循环或递推中，解决阶乘、幂、Fibonacci 等综合题。",
    ],
    questions: [
      {
        id: "storage-direction",
        prompt: "做高精度加法时，为什么常把个位放在数组下标 0？",
        options: [
          { id: "A", text: "因为竖式从个位开始，循环下标从 0 开始正好对齐。" },
          { id: "B", text: "因为 vector 只能从下标 0 保存个位。" },
          { id: "C", text: "因为这样可以避免所有进位。" },
          { id: "D", text: "因为字符串必须倒序读入才不会溢出。" },
        ],
        answer: "A",
        explanation: "反向存储的核心好处是让 a[0]、b[0]、c[0] 都表示个位，逐位计算时下标自然递增。",
        relatedProblemIds: ["big-integer-reverse-store", "big-integer-add-basic"],
      },
      {
        id: "carry-meaning",
        prompt: "在高精度加法里，t = carry + a[i] + b[i] 之后，当前位和下一轮进位分别是什么？",
        options: [
          { id: "A", text: "当前位是 t / 10，下一轮进位是 t % 10。" },
          { id: "B", text: "当前位是 t % 10，下一轮进位是 t / 10。" },
          { id: "C", text: "当前位和进位都直接保存 t。" },
          { id: "D", text: "只要 t 大于 9，就丢弃当前位。" },
        ],
        answer: "B",
        explanation: "十进制里一列只能留下个位，所以 c.push_back(t % 10)，多出来的十位交给下一列。",
        relatedProblemIds: ["big-integer-add-basic", "big-integer-add-trace"],
      },
      {
        id: "borrow-zero",
        prompt: "高精度减法得到结果数组后，为什么要 while(c.size() > 1 && c.back() == 0) c.pop_back()？",
        options: [
          { id: "A", text: "为了删掉低位的 0。" },
          { id: "B", text: "为了删掉多余最高位 0，同时避免把数字 0 删空。" },
          { id: "C", text: "为了让数组变成正向存储。" },
          { id: "D", text: "为了修复 borrow 的值。" },
        ],
        answer: "B",
        explanation: "反向数组的 back 是最高位。必须清理多余最高位 0，但 c.size() > 1 保证结果 0 仍保留一位。",
        relatedProblemIds: ["big-integer-sub-basic", "big-integer-normalize-array"],
      },
      {
        id: "multiply-index",
        prompt: "高精度乘高精度中，反向数组 a[i] 和 b[j] 的乘积应该先累加到哪里？",
        options: [
          { id: "A", text: "c[i + j]" },
          { id: "B", text: "c[i * j]" },
          { id: "C", text: "c[max(i, j)]" },
          { id: "D", text: "c[a[i] + b[j]]" },
        ],
        answer: "A",
        explanation: "第 i 位乘第 j 位会贡献到 10^(i+j) 这一列，所以先累加到 c[i+j]，再统一处理进位。",
        relatedProblemIds: ["big-integer-mul-big-basic", "big-integer-mul-big-grid-trace"],
      },
      {
        id: "division-direction",
        prompt: "高精度除低精度为什么通常从最高位往最低位扫描？",
        options: [
          { id: "A", text: "因为长除法需要先确定高位商，并把余数带到下一位。" },
          { id: "B", text: "因为除法不能处理反向数组。" },
          { id: "C", text: "因为余数永远等于当前数字。" },
          { id: "D", text: "因为这样可以不处理商的前导零。" },
        ],
        answer: "A",
        explanation: "每落下一位都要 r = r * 10 + digit，再写出这一位商，新的余数继续参与下一位。",
        relatedProblemIds: ["big-integer-div-small-basic", "big-integer-div-small-trace"],
      },
      {
        id: "reuse-functions",
        prompt: "做高精度阶乘或 Fibonacci 时，最推荐的结构是什么？",
        options: [
          { id: "A", text: "在主函数里重写所有进位细节。" },
          { id: "B", text: "先封装 add、multiplySmall 等函数，主流程只负责循环和状态更新。" },
          { id: "C", text: "把大整数转成 double 后再计算。" },
          { id: "D", text: "只保存最后 9 位，其他位忽略。" },
        ],
        answer: "B",
        explanation: "综合题的重点是复用稳定的高精度函数，让外层循环、递推状态和边界处理都清楚可查。",
        relatedProblemIds: ["big-integer-factorial-small", "big-integer-fibonacci", "big-integer-factorial-sum"],
      },
    ],
    reviewPlan: [
      {
        title: "入门复盘",
        description: "确认大整数读入、拆位和反向存储已经扎稳。",
        problemIds: ["big-integer-type-range", "big-integer-digit-split", "big-integer-reverse-store"],
      },
      {
        title: "竖式核心",
        description: "集中练 carry、borrow、乘法贡献位和除法余数。",
        problemIds: [
          "big-integer-add-trace",
          "big-integer-sub-borrow-count",
          "big-integer-mul-big-grid-trace",
          "big-integer-div-small-trace",
        ],
      },
      {
        title: "综合挑战",
        description: "把封装好的高精度函数放进循环、批处理和递推。",
        problemIds: ["big-integer-add-multiple", "big-integer-normalized-calculator", "big-integer-factorial-sum"],
      },
    ],
  },
};

export const problemGuides: Record<string, ProblemGuide> = {
  "big-integer-type-range": guide(
    [
      "不要把输入先转成数字；一旦读入时已经溢出，后面比较就失真了。",
      "先去掉多余前导零，再比较长度；长度不同，长的数更大。",
      "长度相同时再用字符串字典序比较，因为每一位都是数字字符。",
    ],
    [
      "写 stripLeadingZeros，再写 compareNumberString(a, b)。",
      "依次和 2147483647、9223372036854775807 比较，输出 int、long long 或 big integer。",
    ],
    ["忽略前导零会让 0009 被当成长度 4 的大数。", "用 stoll 读取超大数会直接溢出或抛异常。"],
  ),
  "big-integer-raw-echo": guide(
    [
      "每个大整数都应该用 string 保存。",
      "题目要求原样输出，就不要去掉前导零。",
      "循环 n 次，读一个输出一个，注意换行。",
    ],
    ["读入 n 后，用 while 或 for 反复读取 string s。", "输出 s 本身；除非题目要求规范化，否则不要修改它。"],
    ["把大整数读入 long long 会破坏原始内容。", "最后一行多一个空格通常没事，但多余文本会 Wrong Answer。"],
  ),
  "big-integer-overflow-count": guide(
    [
      "复用字符串数字比较函数，而不是尝试转换成整型。",
      "比较前先规范化前导零，否则长度判断会偏大。",
      "只统计严格大于 long long 上界的数字。",
    ],
    ["把上界写成字符串常量 9223372036854775807。", "每读入一个 s，若 compareNumberString(s, limit) > 0 就计数。"],
    ["把等于上界的数也计入会错。", "忘记处理 0000 这类输入会影响长度比较。"],
  ),
  "big-integer-digit-split": guide(
    [
      "字符串中的 '7' 是字符，不是整数 7。",
      "字符数字转整数数字的表达式是 s[i] - '0'。",
      "按照题目要求决定是否在数字之间输出空格。",
    ],
    ["从左到右扫描 s，把每位 digit 放进 vector<int>。", "输出数组时用 if(i) cout << ' '; 控制空格。"],
    ["不要写成 s[i]，那会输出字符的 ASCII 值。", "不要漏掉数字 0，它也是有效的一位。"],
  ),
  "big-integer-digit-sum": guide(
    [
      "这题不需要数组，边扫描边累加即可。",
      "每一位的数值仍然是 s[i] - '0'。",
      "sum 用 int 一般足够，因为每位最多 9，但 long long 也可以。",
    ],
    ["读入 string s，初始化 sum = 0。", "遍历每个字符，sum += ch - '0'，最后输出 sum。"],
    ["把字符直接加到 sum 会加 ASCII 编码。", "不要因为有前导零就提前停止扫描。"],
  ),
  "big-integer-digit-frequency": guide(
    [
      "准备 cnt[10]，下标 0 到 9 正好对应数字。",
      "每读到一位 digit，就 cnt[digit]++。",
      "输出时固定输出 10 个计数。",
    ],
    ["扫描字符串，int d = ch - '0'。", "按 0 到 9 的顺序输出 cnt[d]，中间用空格分隔。"],
    ["数组大小要是 10，不是字符串长度。", "不要只输出出现过的数字，题目通常需要完整 0..9。"],
  ),
  "big-integer-reverse-store": guide(
    [
      "反向存储就是让个位先进入数组。",
      "从 s.size() - 1 往 0 扫描。",
      "a[0] 保存最低位，a[1] 保存十位。",
    ],
    ["for (int i = s.size() - 1; i >= 0; --i) push_back(s[i] - '0')。", "输出数组内容时按下标从小到大输出。"],
    ["i 用 int，避免 size_t 到 0 后继续减导致下溢。", "不要把字符本身 push 进 int 数组。"],
  ),
  "big-integer-reverse-restore": guide(
    [
      "输入数组已经是低位在前。",
      "还原正常数字时要从最高下标往 0 输出。",
      "这题通常不需要再处理进位。",
    ],
    ["读入 n 和数组 a。", "for (int i = n - 1; i >= 0; --i) cout << a[i];"],
    ["从 0 到 n-1 输出会得到反过来的数字。", "数组元素是数字，不要再减 '0'。"],
  ),
  "big-integer-low-position-query": guide(
    [
      "把大整数反向存储后，第 0 位就是个位。",
      "如果题目说第 k 个低位，要看 k 是从 0 还是从 1 开始。",
      "超出长度的位置通常可以按 0 处理，除非题面另有说明。",
    ],
    ["先把 s 反向放入 vector<int> a。", "每次查询按题面换算下标，输出 a[index] 或 0。"],
    ["最常见错误是把第 1 位误当成 a[1]。", "查询很多次时不要每次重新反转字符串。"],
  ),
  "big-integer-add-basic": guide(
    [
      "先把两个字符串都转成反向数组。",
      "循环长度取 max(a.size(), b.size())，短的那边缺位按 0。",
      "每一轮只留下 t % 10，把 t / 10 作为下一轮 carry。",
    ],
    ["初始化 carry = 0，逐位计算 t = carry + a[i] + b[i]。", "循环结束后如果 carry > 0，把它追加到结果最高位。"],
    ["漏掉最后一个 carry 会让 999+1 输出 000。", "输出结果时要从 c.back() 倒序到 c[0]。"],
  ),
  "big-integer-add-trace": guide(
    [
      "trace 记录的是每轮还没拆分前的 t。",
      "先把 t 放入 trace，再更新当前位和 carry。",
      "trace 的顺序应该和低位到高位的计算顺序一致。",
    ],
    ["在加法循环内计算 t 后 trace.push_back(t)。", "c.push_back(t % 10)，carry = t / 10，最后处理剩余 carry。"],
    ["不要把 c[i] 放进 trace，题目要的是临时总和 t。", "最后 carry 形成的新位通常不需要再额外记一轮 t，按题面样例确认。"],
  ),
  "big-integer-add-multiple": guide(
    [
      "先把两数相加封装成函数。",
      "answer 初始为 0，每读一个数就 answer = add(answer, 当前数)。",
      "多组累加时，函数返回值要已经是规范的反向数组。",
    ],
    ["实现 toDigits 和 addBigInteger。", "循环 n 次读入 s，将 toDigits(s) 加到 answer 上。"],
    ["不要把所有数字拼接成一个字符串。", "answer 每轮要更新，不能只加最后一个数。"],
  ),
  "big-integer-sub-basic": guide(
    [
      "题目保证 x >= y，可以先不处理负号。",
      "t = a[i] - borrow - b[i]；如果 t < 0，就 t += 10 且 borrow = 1。",
      "如果 t >= 0，本轮不需要继续借位，borrow = 0。",
    ],
    ["按低位到高位逐位相减，缺位按 0。", "生成结果后删除最高位多余 0，再倒序输出。"],
    ["忘记把 borrow 清回 0 会连续错误借位。", "相等相减时要输出 0，而不是空字符串。"],
  ),
  "big-integer-sub-borrow-count": guide(
    [
      "每次 t < 0 都对应一次真实借位。",
      "借位计数应该发生在 t += 10 之前或同时。",
      "结果规范化和借位计数是两件事。",
    ],
    ["照普通高精度减法写循环。", "if (t < 0) 中执行 borrowCount++，最后输出差值和计数。"],
    ["不要把 borrow == 1 的轮数简单累计，关键是本轮是否新发生 t < 0。", "不要因为结果有前导零就删掉 trace 或计数。"],
  ),
  "big-integer-sub-ledger": guide(
    [
      "这题是重复调用高精度减法。",
      "余额 answer 一直用反向数组保存。",
      "每次读入 cost，把它转换成反向数组后执行 answer = subtract(answer, cost)。",
    ],
    ["实现 subtractBigInteger(a, b)，保证返回规范结果。", "主循环中不断更新 answer，最后倒序输出。"],
    ["不要每次都从原始 balance 扣款。", "如果题目保证余额够用，就不需要额外处理负数。"],
  ),
  "big-integer-compare": guide(
    [
      "比较大整数先看有效长度。",
      "长度相同再从最高位向最低位比较。",
      "如果全部相同才返回相等。",
    ],
    ["可先写 trim 函数去掉多余前导零。", "compareBigInteger 返回 1、-1、0，再映射成 >、<、=。"],
    ["字符串字典序只适合长度相同的情况。", "不要让 0012 大于 12。"],
  ),
  "big-integer-sub-signed": guide(
    [
      "先比较 a 和 b 的大小。",
      "如果 a < b，就交换两数做绝对值减法，并记录需要输出负号。",
      "如果相等，直接输出 0。",
    ],
    ["复用 compareBigInteger 和 subtractAbs。", "输出时先判断 negative，再倒序输出差值。"],
    ["不要在结果为 0 时输出 -0。", "交换操作数后别忘了负号标记。"],
  ),
  "big-integer-sub-sign-batch": guide(
    [
      "把单次 signed subtract 封装成函数，批量输入只负责调用。",
      "函数内部完成比较、交换、绝对值减法、符号拼接。",
      "返回 string 会比直接在函数里 cout 更方便测试。",
    ],
    ["写 subtractSigned(a, b) 返回 a-b。", "主函数读 q 组，每组输出一行 subtractSigned 的结果。"],
    ["不要让函数依赖全局临时数组残留。", "每组数据之间要重置 borrow、结果数组和符号。"],
  ),
  "big-integer-mul-small-basic": guide(
    [
      "大整数用反向数组，小整数 b 直接作为 int 或 long long。",
      "每轮 t = a[i] * b + carry。",
      "主循环结束后，carry 可能还有多位，需要 while(carry) 拆完。",
    ],
    ["逐位写 c.push_back(t % 10)，carry = t / 10。", "如果 b 为 0，规范化后结果应为 0。"],
    ["只追加一次 carry 会在 carry >= 10 时出错。", "t 建议用 long long，避免 a[i] * b 溢出 int。"],
  ),
  "big-integer-mul-small-trace": guide(
    [
      "trace 记录每轮 a[i] * b + carry 的临时值。",
      "先记录 t，再拆当前位和新 carry。",
      "剩余 carry 拆位时一般不继续记录 trace，按题意只追踪主循环。",
    ],
    ["照乘低精度模板写主循环并 trace.push_back(t)。", "最后拆分 carry、规范化、倒序输出。"],
    ["把 carry 本身写入 trace 会和样例不一致。", "b 为 0 时结果要整理成单个 0。"],
  ),
  "big-integer-factorial-small": guide(
    [
      "阶乘不是直接乘两个超大数；每轮只是 answer 乘当前普通整数 i。",
      "answer 初始为 1。",
      "循环 i 从 2 到 n，不断 answer = multiplySmall(answer, i)。",
    ],
    ["先实现 multiplySmall(vector<int>, int)。", "主循环更新 answer，最后倒序输出。"],
    ["0! 和 1! 都应该输出 1。", "不要把阶乘值放进 long long 再转换。"],
  ),
  "big-integer-mul-big-basic": guide(
    [
      "两个数都反向存储。",
      "a[i] * b[j] 先加到 c[i+j]。",
      "所有贡献累加完，再从低到高统一进位。",
    ],
    ["初始化 c 长度为 a.size() + b.size()，全 0。", "双重循环累加后，处理 c[i+1] += c[i]/10，c[i] %= 10。"],
    ["不要在双重循环里立即覆盖 c[i+j]。", "结果为 0 时要保留一个 0。"],
  ),
  "big-integer-mul-big-grid-trace": guide(
    [
      "raw 表示统一进位前每个格子的贡献总和。",
      "先完成 raw[i+j] += a[i] * b[j]。",
      "再复制 raw 到 c，对 c 做进位处理。",
    ],
    ["双重循环填 raw。", "输出最终乘积后，再按低位到高位输出 raw 数组。"],
    ["不要在 raw 上直接进位，否则轨迹会被破坏。", "raw 的长度通常是 a.size()+b.size()。"],
  ),
  "big-integer-power-small": guide(
    [
      "把底数转换成反向数组 base。",
      "answer 初始为 1，循环 n 次乘 base。",
      "约定 0^0 = 1 时，n=0 直接保持 answer=1。",
    ],
    ["实现 multiplyBigInteger(a, b)。", "for 循环执行 answer = multiplyBigInteger(answer, base)。"],
    ["不要用 pow 或 double。", "每次乘完都要规范化，否则高位 0 会越积越多。"],
  ),
  "big-integer-div-small-basic": guide(
    [
      "除法从字符串最高位开始扫描。",
      "维护余数 r：r = r * 10 + 当前数字。",
      "当前商位是 r / b，新余数是 r % b。",
    ],
    ["把商逐位追加到 string q。", "扫描结束后删掉 q 左侧多余 0，输出商。"],
    ["不要把被除数反向后从低位开始除。", "商为 0 时仍要输出一个 0。"],
  ),
  "big-integer-div-small-quot-rem": guide(
    [
      "这题同时输出商和最终余数。",
      "余数 r 每轮更新后会带到下一位。",
      "最终循环结束时的 r 就是整体余数。",
    ],
    ["按长除法生成 q 和 r。", "整理 q 的前导零后，第一行输出 q，第二行输出 r。"],
    ["不要把每轮临时 r 当最终余数输出。", "q 可能一开始有很多 0。"],
  ),
  "big-integer-div-small-trace": guide(
    [
      "trace 记录的是落下一位之后、除以 b 之前的临时 r。",
      "顺序应该和从左到右扫描的数字顺序一致。",
      "记录后再写商位、更新余数。",
    ],
    ["每轮先 r = r * 10 + digit，再 trace.push_back(r)。", "接着 q.push_back(r / b + '0')，r %= b。"],
    ["不要记录更新后的余数。", "整理商的前导零不应该影响 trace。"],
  ),
  "big-integer-normalize-array": guide(
    [
      "反向数组的最高位在 back()。",
      "只删除最高位多余 0。",
      "条件必须包含 c.size() > 1，保护数字 0。",
    ],
    ["while (c.size() > 1 && c.back() == 0) c.pop_back();", "输出新长度和数组内容。"],
    ["把所有 0 都删掉会让 0 变成空数组。", "不要删除低位 0，例如 100 的反向数组是 0 0 1。"],
  ),
  "big-integer-trim-string": guide(
    [
      "商字符串是正向存储，前导零在左侧。",
      "start 从 0 往右移动。",
      "最多移动到最后一个字符之前，保证保留一个 0。",
    ],
    ["while (start + 1 < q.size() && q[start] == '0') start++;", "输出 q.substr(start)。"],
    ["不要用空字符串表示 0。", "不要删除中间或末尾的 0。"],
  ),
  "big-integer-normalized-calculator": guide(
    [
      "先把 add、sub、mul_small、div_small 分别拆成函数。",
      "每个函数返回前都做 normalize。",
      "主循环只负责读操作名、分发调用、输出结果。",
    ],
    ["用 vector<int> 处理加减乘，用 string 或 vector 处理除法都可以。", "根据 op 分支调用对应函数，统一把结果转成字符串输出。"],
    ["不要在某个分支忘记规范化。", "sub、div_small 的题面通常会给出非负结果和合法除数，仍要处理结果为 0。"],
  ),
  "big-integer-fibonacci": guide(
    [
      "Fibonacci 是状态更新题，不是公式题。",
      "用两个高精度数组保存相邻两项。",
      "每轮 c = add(a, b)，然后 a = b，b = c。",
    ],
    ["先处理 n=0 输出 0。", "从第 2 项开始循环更新到 n，最后输出 b。"],
    ["不要把 F(n) 放进 long long。", "更新顺序错会把 a、b 都变成同一个值。"],
  ),
  "big-integer-factorial-sum": guide(
    [
      "同时维护当前阶乘 fact 和累计和 sum。",
      "第 i 轮先让 fact 表示 i!，再 sum = sum + fact。",
      "乘法用 multiplySmall，加法用 addBigInteger。",
    ],
    ["fact 初始 1，sum 初始 0。", "循环 i=1..n：fact = multiplySmall(fact, i)，sum = add(sum, fact)。"],
    ["不要每次从头重新计算 i!，会更慢也更容易错。", "1! 要被加入总和。"],
  ),
};

export function getChapterSummaryQuiz(chapterId: string) {
  return chapterSummaryQuizzes[chapterId];
}

export function getProblemGuide(problemId: string) {
  return problemGuides[problemId];
}
