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
  sorting: {
    chapterId: "sorting",
    title: "第二章总结测验：数据排序",
    summary:
      "排序不只是把数字排整齐，更重要的是看懂每种算法怎样组织比较和移动，并能根据数据规模、值域与稳定性要求作出选择。",
    checklist: [
      "能指出冒泡、选择、插入排序中已排序区如何变化，并写对循环边界。",
      "能解释交换次数、右移次数和逆序对之间的联系。",
      "能判断计数排序是否适合当前值域，并用 offset 处理负数。",
      "能独立写出合并两个有序段和快速排序 partition。",
      "能比较 O(n²)、O(n log n)、O(n + K)，并说明稳定性什么时候有用。",
      "能用快速选择只处理包含第 k 小元素的一侧。",
    ],
    questions: [
      {
        id: "bubble-final-position",
        prompt: "升序冒泡排序完成一整轮从左到右的相邻比较后，哪一项一定成立？",
        options: [
          { id: "A", text: "当前未排序区的最大值到达最右侧。" },
          { id: "B", text: "当前未排序区的最小值到达最右侧。" },
          { id: "C", text: "整个数组一定已经有序。" },
          { id: "D", text: "每一对相邻元素都发生过交换。" },
        ],
        answer: "A",
        explanation: "较大的元素会在相邻比较中不断向右移动，因此每轮至少确定未排序区中的一个最大值。",
        relatedProblemIds: ["bubble-sort-basic", "bubble-sort-count", "bubble-sort-flag"],
      },
      {
        id: "selection-swap-time",
        prompt: "选择排序为什么要在内层扫描结束后再交换，而不是每发现一个更小值就交换？",
        options: [
          { id: "A", text: "先用 minIndex 记住全局最小位置，一轮只需完成一次最终放置。" },
          { id: "B", text: "因为 C++ 的 swap 只能在循环外调用。" },
          { id: "C", text: "因为内层循环不能访问 a[i]。" },
          { id: "D", text: "为了让选择排序变成稳定排序。" },
        ],
        answer: "A",
        explanation: "扫描阶段负责寻找，扫描完成后才知道这一轮真正的最小值在哪里；频繁交换既多余，也模糊了选择排序的核心。",
        relatedProblemIds: ["selection-sort-basic", "selection-sort-trace"],
      },
      {
        id: "insertion-stability",
        prompt: "升序插入排序想保持相等元素的原相对顺序，右移条件应当是什么？",
        options: [
          { id: "A", text: "a[j] > key" },
          { id: "B", text: "a[j] >= key" },
          { id: "C", text: "a[j] < key" },
          { id: "D", text: "a[j] == key" },
        ],
        answer: "A",
        explanation: "只移动严格大于 key 的元素，遇到相等元素就停下，新元素会放在原有相等元素之后，因此相对顺序不变。",
        relatedProblemIds: ["insertion-sort-basic", "insertion-sort-shifts"],
      },
      {
        id: "counting-applicability",
        prompt: "有 1000 个整数，取值范围是 -20 到 20。哪种方案最能利用这个条件？",
        options: [
          { id: "A", text: "建立 41 个计数桶，并用 value - (-20) 映射下标。" },
          { id: "B", text: "建立 1000 个桶，下标直接使用原值。" },
          { id: "C", text: "必须使用冒泡排序。" },
          { id: "D", text: "把负数全部改成 0 后计数。" },
        ],
        answer: "A",
        explanation: "值域很小，计数排序可用 O(n + K) 完成；负数通过减去最小值映射到从 0 开始的桶下标。",
        relatedProblemIds: ["counting-sort-basic", "counting-sort-frequency", "counting-sort-offset"],
      },
      {
        id: "merge-inversion-count",
        prompt: "归并两个有序段时，如果 a[i] > a[j] 并先取右段的 a[j]，会新增多少个逆序对？",
        options: [
          { id: "A", text: "mid - i + 1" },
          { id: "B", text: "j - mid" },
          { id: "C", text: "right - j + 1" },
          { id: "D", text: "固定新增 1 个" },
        ],
        answer: "A",
        explanation: "左段已经有序，a[i] 及其后直到 a[mid] 的所有元素都大于 a[j]，所以一次新增 mid-i+1 个逆序对。",
        relatedProblemIds: ["merge-two-sorted-arrays", "merge-sort-inversions"],
      },
      {
        id: "quick-select-branch",
        prompt: "partition 返回 pos 后，快速选择的目标下标 target < pos，下一步应当怎么做？",
        options: [
          { id: "A", text: "只处理 [left, pos - 1]。" },
          { id: "B", text: "只处理 [pos + 1, right]。" },
          { id: "C", text: "左右两边都完整排序。" },
          { id: "D", text: "直接返回 a[pos]。" },
        ],
        answer: "A",
        explanation: "pivot 已经位于最终排名 pos；target 在它左边时，右侧不可能包含答案，可以整段跳过。",
        relatedProblemIds: ["quick-sort-partition", "quick-select-kth"],
      },
    ],
    reviewPlan: [
      {
        title: "基础动作",
        description: "复盘比较、交换、选择和插入三个最直观的排序动作。",
        problemIds: ["bubble-sort-count", "selection-sort-trace", "insertion-sort-shifts"],
      },
      {
        title: "换一种组织方式",
        description: "从值域、双指针和分区三个角度突破只会双重循环的阶段。",
        problemIds: ["counting-sort-offset", "merge-two-sorted-arrays", "quick-sort-partition"],
      },
      {
        title: "综合挑战",
        description: "练习排序中的经典扩展：逆序对与第 k 小。",
        problemIds: ["merge-sort-inversions", "quick-select-kth"],
      },
    ],
  },
  recurrence: {
    chapterId: "recurrence",
    title: "第三章总结测验：递推算法",
    summary:
      "递推的核心是把大问题拆成一张有方向的状态表：先说明每个格子记录什么，再准备最小状态，最后沿着依赖方向把未知逐个变成已知。",
    checklist: [
      "能用一句完整的话解释 f[i] 或 dp[i][j] 的含义，并指出最终答案落在哪个状态。",
      "能根据依赖关系写出递推式，并确定循环方向和第一个未知状态。",
      "能区分 0-based 与 1-based 数列定义，正确设置初值和循环起点。",
      "能在只依赖少量旧状态时使用滚动变量，并保证更新顺序不覆盖旧值。",
      "能处理二维递推的首行、首列、三角形边缘、障碍和数塔底层。",
      "能用 n=0、n=1、单行、单列等极小输入检查数组边界和初始化。",
    ],
    questions: [
      {
        id: "state-sentence",
        prompt: "写递推程序时，最应该先明确哪件事？",
        options: [
          { id: "A", text: "每个状态表示什么，以及原问题对应哪个状态。" },
          { id: "B", text: "数组必须使用全局变量。" },
          { id: "C", text: "所有递推都从下标 1 开始。" },
          { id: "D", text: "先把循环写成两层再补公式。" },
        ],
        answer: "A",
        explanation: "状态含义决定初值、转移和答案位置。没有这句话，公式即使看起来熟悉，也可能回答了另一个问题。",
        relatedProblemIds: ["recurrence-state-table", "recurrence-domino-tiling"],
      },
      {
        id: "first-unknown",
        prompt: "已知 f[1]=1、f[2]=2，且 f[i]=f[i-1]+f[i-2]。循环应从哪里开始？",
        options: [
          { id: "A", text: "i = 0" },
          { id: "B", text: "i = 1" },
          { id: "C", text: "i = 2" },
          { id: "D", text: "i = 3" },
        ],
        answer: "D",
        explanation: "f[1]、f[2] 已经是已知区，第一个需要由递推式计算的未知状态是 f[3]。",
        relatedProblemIds: ["recurrence-known-to-unknown-sequence", "recurrence-new-state-log"],
      },
      {
        id: "fibonacci-indexing",
        prompt: "题目定义 F(0)=0、F(1)=1。输入 n=2 时，正确输出是什么？",
        options: [
          { id: "A", text: "0" },
          { id: "B", text: "1" },
          { id: "C", text: "2" },
          { id: "D", text: "3" },
        ],
        answer: "B",
        explanation: "这是 0-based 定义：F(2)=F(1)+F(0)=1。若误套 1-based 下标，整张表会整体错位。",
        relatedProblemIds: ["recurrence-fibonacci-zero-based", "recurrence-fibonacci-index-table"],
      },
      {
        id: "rolling-update",
        prompt: "滚动计算 c=a+b 后，哪组更新能让 a、b 继续表示相邻两项？",
        options: [
          { id: "A", text: "a=b; b=c;" },
          { id: "B", text: "b=a; a=c;" },
          { id: "C", text: "a=c; b=a;" },
          { id: "D", text: "a=a+b; b=a+b;" },
        ],
        answer: "A",
        explanation: "先用旧 a、旧 b 算出 c，再让 a 接住旧 b、b 接住新 c，窗口才会向前移动一格。",
        relatedProblemIds: ["recurrence-rolling-fibonacci", "recurrence-rolling-trace"],
      },
      {
        id: "grid-source",
        prompt: "机器人只能向右或向下走时，内部格 dp[i][j] 的路径数来自哪里？",
        options: [
          { id: "A", text: "上方和左方之和。" },
          { id: "B", text: "左上方和右上方之和。" },
          { id: "C", text: "下方和右方之和。" },
          { id: "D", text: "只来自上方。" },
        ],
        answer: "A",
        explanation: "进入当前格的最后一步只可能从上方向下走，或从左方向右走，所以两类路径相加。",
        relatedProblemIds: ["recurrence-grid-paths-basic", "recurrence-grid-paths-obstacle"],
      },
      {
        id: "tower-direction",
        prompt: "状态 f[i][j] 表示从数塔第 i 行第 j 个位置走到底层的最大和。最自然的初始化和遍历方向是什么？",
        options: [
          { id: "A", text: "初始化顶端，再从上向下。" },
          { id: "B", text: "初始化底层，再从下向上。" },
          { id: "C", text: "所有状态初始化为 1，再从左向右。" },
          { id: "D", text: "不需要初值，直接输出顶端。" },
        ],
        answer: "B",
        explanation: "当前格依赖下一层的左下和右下，因此要先让底层成为已知，再让 i 从 n-1 倒着走到 1。",
        relatedProblemIds: ["recurrence-number-tower-basic", "recurrence-number-tower-table"],
      },
      {
        id: "boundary-start",
        prompt: "转移会读取 f[i-1] 和 f[i-2]。如果循环从 i=1 开始，最直接的风险是什么？",
        options: [
          { id: "A", text: "会读取不存在的 f[-1]。" },
          { id: "B", text: "会自动变成二维递推。" },
          { id: "C", text: "数组会被自动扩容。" },
          { id: "D", text: "答案一定多 1。" },
        ],
        answer: "A",
        explanation: "i=1 时 i-2=-1。循环应从第一个依赖下标都合法、并且尚未初始化的状态开始。",
        relatedProblemIds: ["recurrence-boundary-climb-stairs", "recurrence-boundary-state-table"],
      },
    ],
    reviewPlan: [
      {
        title: "状态与方向",
        description: "先把状态含义、已知区和递推方向说清楚，再开始写循环。",
        problemIds: [
          "recurrence-state-table",
          "recurrence-known-to-unknown-sequence",
          "recurrence-climb-stairs-source-trace",
        ],
      },
      {
        title: "一维与空间优化",
        description: "对照数组版、不同下标定义和滚动变量版，练稳初始化与更新顺序。",
        problemIds: [
          "recurrence-fibonacci-index-table",
          "recurrence-rolling-trace",
          "recurrence-boundary-state-table",
        ],
      },
      {
        title: "二维综合",
        description: "集中处理二维表的边缘、障碍、哨兵初值与最值方向。",
        problemIds: [
          "recurrence-pascal-triangle-query",
          "recurrence-grid-paths-obstacle",
          "recurrence-number-tower-min",
          "recurrence-boundary-grid-sentinel",
        ],
      },
    ],
  },
  greedy: {
    chapterId: "greedy",
    title: "第六章总结测验：贪心算法",
    summary:
      "贪心不是‘每次挑最大的’，而是把候选集、选择规则和不后悔的理由连成一条完整证据链，再用排序、双指针或优先队列实现。",
    checklist: [
      "能明确写出候选对象、选择规则、选择后维护的状态和结束条件。",
      "能解释为什么很多贪心算法先排序，再做一次线性扫描。",
      "能区分活动选择、区间覆盖与最少点覆盖三种不同的区间策略。",
      "能使用双指针完成轻重配对，并使用优先队列实现延迟决策。",
      "能用交换论证或‘不变差’直觉说明策略可靠，而不只凭样例猜测。",
      "会主动构造零钱反例，知道贪心策略成立需要题目结构保证。",
    ],
    questions: [
      {
        id: "greedy-first-question",
        prompt: "准备使用贪心前，最应该先写清楚什么？",
        options: [
          { id: "A", text: "候选是什么、按什么规则选，以及为什么选后不用反悔。" },
          { id: "B", text: "固定使用从大到小排序。" },
          { id: "C", text: "一定使用双指针。" },
          { id: "D", text: "先把所有样例硬编码进程序。" },
        ],
        answer: "A",
        explanation: "贪心策略必须同时包含可执行的选择规则和正确性理由；排序、双指针只是可能的实现手段。",
        relatedProblemIds: ["greedy-select-k-largest", "greedy-max-affordable-count"],
      },
      {
        id: "activity-key",
        prompt: "想选择最多个互不冲突活动，应优先选择哪一个？",
        options: [
          { id: "A", text: "持续时间最长的活动。" },
          { id: "B", text: "开始时间最早的活动。" },
          { id: "C", text: "结束时间最早的活动。" },
          { id: "D", text: "编号最小的活动。" },
        ],
        answer: "C",
        explanation: "结束越早，留给后续活动的时间空间越大；这个选择还能通过交换论证替换进某个最优方案。",
        relatedProblemIds: ["greedy-activity-count", "greedy-activity-ids"],
      },
      {
        id: "interval-cover-key",
        prompt: "连续覆盖 [L,R] 时，在所有左端点不超过当前 cover 的区间中应选择什么？",
        options: [
          { id: "A", text: "右端点最远的区间。" },
          { id: "B", text: "长度最短的区间。" },
          { id: "C", text: "左端点最大的区间。" },
          { id: "D", text: "编号最小的区间。" },
        ],
        answer: "A",
        explanation: "当前步使用一个区间后，把连续可达位置推得越远，剩余待覆盖目标就不会更大。",
        relatedProblemIds: ["greedy-interval-cover-count", "greedy-interval-point-cover"],
      },
      {
        id: "boat-heavy-person",
        prompt: "救生艇双指针算法中，为什么每轮都让当前最重的人上船？",
        options: [
          { id: "A", text: "最重者之后不可能由更轻的人替代其占用的船，必须在本轮处理。" },
          { id: "B", text: "最重者一定能和第二重的人同行。" },
          { id: "C", text: "最重者的编号一定最大。" },
          { id: "D", text: "这样可以省略限重判断。" },
        ],
        answer: "A",
        explanation: "最重者无论如何都需要一条船；若连最轻者也不能与其配对，他就只能单独走。",
        relatedProblemIds: ["greedy-boats-count", "greedy-boats-pair-solo"],
      },
      {
        id: "coin-counterexample",
        prompt: "币值为 1、3、4，金额为 6 时，从大面额开始的贪心结果与最优结果分别是多少枚？",
        options: [
          { id: "A", text: "贪心 3 枚，最优 2 枚。" },
          { id: "B", text: "贪心 2 枚，最优 3 枚。" },
          { id: "C", text: "都是 2 枚。" },
          { id: "D", text: "都无法凑出。" },
        ],
        answer: "A",
        explanation: "贪心取 4+1+1 共 3 枚，而全局最优是 3+3 共 2 枚，这说明任意币制都用贪心是错误的。",
        relatedProblemIds: ["greedy-standard-change", "greedy-coin-greedy-vs-optimal"],
      },
      {
        id: "delayed-decision",
        prompt: "最少加油次数中，暂时不在每个加油站立即加油，而把路过站点的油量放入大根堆，体现了什么？",
        options: [
          { id: "A", text: "延迟决策：真正走不动时，再从已路过候选中选最大补给。" },
          { id: "B", text: "动态规划状态压缩。" },
          { id: "C", text: "二分答案。" },
          { id: "D", text: "深度优先搜索。" },
        ],
        answer: "A",
        explanation: "把决定推迟到必须加油时，可以从全部已可用候选里拿最大油量，让一次加油后的可达范围最远。",
        relatedProblemIds: ["greedy-min-refuels", "greedy-deadline-max-tasks"],
      },
    ],
    reviewPlan: [
      {
        title: "规则入门",
        description: "从排序后直接选择开始，练习把局部规则写成代码。",
        problemIds: ["greedy-select-k-largest", "greedy-max-affordable-count", "greedy-water-total-wait"],
      },
      {
        title: "区间与双指针",
        description: "集中辨析区间选择、覆盖、落点与轻重配对。",
        problemIds: ["greedy-activity-count", "greedy-interval-cover-count", "greedy-boats-count"],
      },
      {
        title: "证明与反例",
        description: "用交换直觉、延迟决策和反例检查策略边界。",
        problemIds: ["greedy-coin-greedy-vs-optimal", "greedy-deadline-max-tasks", "greedy-min-refuels"],
      },
    ],
  },
  recursion: {
    chapterId: "recursion",
    title: "第四章总结测验：递归算法",
    summary:
      "递归的核心不是背函数模板，而是看清当前任务、规模更小的同类子问题、可达出口，以及返回值怎样沿调用栈逐层合并。",
    checklist: [
      "能为递归函数说清参数含义，并证明每次调用都更靠近出口。",
      "能区分压栈阶段与回收阶段，读懂先递归后输出的执行顺序。",
      "能写出阶乘、Fibonacci 与汉诺塔的子问题和合并方式。",
      "能识别树形递归中的重复计算，并用记忆化保存子问题答案。",
      "能通过 visit 的位置区分前序、中序和后序遍历。",
      "能用 depth、进入日志和返回日志调试递归参数与边界。",
    ],
    questions: [
      {
        id: "recursion-three-parts",
        prompt: "一个递归函数能够正确终止，最关键的组合是什么？",
        options: [
          { id: "A", text: "同类子问题、规模严格变小、可直接处理的出口。" },
          { id: "B", text: "全局变量、while 循环和排序。" },
          { id: "C", text: "两个 return 和一个数组。" },
          { id: "D", text: "每次都使用相同参数调用自己。" },
        ],
        answer: "A",
        explanation: "递归必须把任务交给更小的同类问题，并保证参数最终能到达可直接回答的出口。",
        relatedProblemIds: ["recursion-countdown", "recursion-sum-to-n"],
      },
      {
        id: "recursion-output-order",
        prompt: "函数先调用 solve(n-1)，再输出 n；当 n=4 时，输出顺序是什么？",
        options: [
          { id: "A", text: "1 2 3 4" },
          { id: "B", text: "4 3 2 1" },
          { id: "C", text: "1 4 2 3" },
          { id: "D", text: "没有输出" },
        ],
        answer: "A",
        explanation: "输出语句位于子调用之后，要等最深层先返回，因此发生在回收阶段。",
        relatedProblemIds: ["recursion-print-up", "recursion-reverse-string"],
      },
      {
        id: "recursion-stack-order",
        prompt: "调用栈中哪一层最先返回？",
        options: [
          { id: "A", text: "最后压入、命中出口的最深层。" },
          { id: "B", text: "最早压入的第一层。" },
          { id: "C", text: "参数最大的层。" },
          { id: "D", text: "所有层同时返回。" },
        ],
        answer: "A",
        explanation: "调用栈后进先出，最深层先弹出，父层拿到子结果后才能继续。",
        relatedProblemIds: ["recursion-enter-leave", "recursion-sum-stack"],
      },
      {
        id: "recursion-fibonacci-repeat",
        prompt: "朴素递归 Fibonacci 在 n 较大时很慢，主要原因是什么？",
        options: [
          { id: "A", text: "相同的 fib(k) 会在不同分支被重复计算。" },
          { id: "B", text: "整数加法不能在递归中使用。" },
          { id: "C", text: "出口太多。" },
          { id: "D", text: "数组下标必须从 1 开始。" },
        ],
        answer: "A",
        explanation: "递归树包含大量相同子树；记忆化让每个 fib(k) 只计算一次。",
        relatedProblemIds: ["recursion-fibonacci-calls", "recursion-fibonacci-memo"],
      },
      {
        id: "recursion-hanoi-split",
        prompt: "把 n 个汉诺塔盘子从 A 移到 C 的标准三步中，中间一步是什么？",
        options: [
          { id: "A", text: "把第 n 个最大盘从 A 移到 C。" },
          { id: "B", text: "把所有盘子从 B 移回 A。" },
          { id: "C", text: "交换任意两个小盘。" },
          { id: "D", text: "删除最大的盘子。" },
        ],
        answer: "A",
        explanation: "先移走上面的 n-1 个盘子，最大盘才能直接到目标柱，再处理第二个 n-1 子任务。",
        relatedProblemIds: ["recursion-hanoi-moves", "recursion-hanoi-count"],
      },
      {
        id: "recursion-tree-visit",
        prompt: "二叉树中序遍历的访问顺序是什么？",
        options: [
          { id: "A", text: "左子树、根、右子树。" },
          { id: "B", text: "根、左子树、右子树。" },
          { id: "C", text: "左子树、右子树、根。" },
          { id: "D", text: "只访问叶子。" },
        ],
        answer: "A",
        explanation: "递归骨架相同，中序只需把访问根节点放在左右两次子调用之间。",
        relatedProblemIds: ["recursion-tree-inorder", "recursion-tree-postorder"],
      },
    ],
    reviewPlan: [
      {
        title: "结构入门",
        description: "先稳住出口、参数变化和调用栈顺序。",
        problemIds: ["recursion-countdown", "recursion-print-up", "recursion-enter-leave"],
      },
      {
        title: "返回值与分支",
        description: "练习单分支合并、双分支递归与重复计算优化。",
        problemIds: ["recursion-factorial-trace", "recursion-combination", "recursion-fibonacci-memo"],
      },
      {
        title: "结构化挑战",
        description: "综合汉诺塔、树遍历与参数轨迹调试。",
        problemIds: ["recursion-hanoi-disk-counts", "recursion-tree-postorder", "recursion-euclid-trace"],
      },
    ],
  },
  "search-backtracking": {
    chapterId: "search-backtracking",
    title: "第五章总结测验：搜索与回溯",
    summary:
      "搜索与回溯的核心是把所有可能组织成决策树，再用选择、递归和撤销系统走完必要分支。",
    checklist: [
      "能说清 pos、path 和递归出口分别表示什么。",
      "能把一次选择与对应撤销成对写出，不让状态污染兄弟分支。",
      "能用 used 数组写全排列，用 start 去除组合的顺序重复。",
      "能区分子集的选/不选分支与排列的候选循环。",
      "能在迷宫中写对边界、墙和 visited，并根据任务决定是否撤销访问标记。",
      "能证明一个剪枝条件不会漏解，并估算分支因子与搜索深度。",
    ],
    questions: [
      {
        id: "dfs-exit",
        prompt: "用 dfs(pos) 填长度为 n 的 path 时，什么时候应输出一个完整方案？",
        options: [
          { id: "A", text: "pos == n 时。" },
          { id: "B", text: "pos == 0 时。" },
          { id: "C", text: "每次进入 for 循环时。" },
          { id: "D", text: "path 还是空时。" },
        ],
        answer: "A",
        explanation: "pos==n 说明 0 到 n-1 的所有决策位已填好，当前节点是一个完整叶子。",
        relatedProblemIds: ["search-binary-strings", "search-dfs-sequences"],
      },
      {
        id: "undo-purpose",
        prompt: "path.push_back(choice); dfs(...); 之后为什么要执行 path.pop_back()？",
        options: [
          { id: "A", text: "恢复进入该分支前的现场，供下一个兄弟分支使用。" },
          { id: "B", text: "为了让递归深度加一。" },
          { id: "C", text: "为了自动排序 path。" },
          { id: "D", text: "因为 vector 不能保存多个元素。" },
        ],
        answer: "A",
        explanation: "子树搜完后要撤销本层选择，否则上一个分支的状态会污染后续分支。",
        relatedProblemIds: ["search-fixed-weight-binary", "search-balanced-parentheses"],
      },
      {
        id: "permutation-used",
        prompt: "全排列中 used[value] 的作用是什么？",
        options: [
          { id: "A", text: "避免同一个值在当前路径中被重复使用。" },
          { id: "B", text: "记录 value 在所有排列中总共出现多少次。" },
          { id: "C", text: "保证数组自动降序。" },
          { id: "D", text: "代替递归出口。" },
        ],
        answer: "A",
        explanation: "一个排列中每个值只能出现一次，used 表示它是否已经在当前 path 中。",
        relatedProblemIds: ["search-permutation-basic", "search-permutation-kth"],
      },
      {
        id: "combination-start",
        prompt: "组合搜索选了 value 后，下一层为什么从 value + 1 开始？",
        options: [
          { id: "A", text: "保证路径递增，避免同一组数因顺序不同被重复枚举。" },
          { id: "B", text: "因为 value 之前的数一定比较大。" },
          { id: "C", text: "为了将组合变成全排列。" },
          { id: "D", text: "为了允许 value 被重复选择。" },
        ],
        answer: "A",
        explanation: "start 限制后续只向右选，因此 {1,2} 不会再以 {2,1} 的形式出现。",
        relatedProblemIds: ["search-combinations-basic", "search-combination-sum-k"],
      },
      {
        id: "maze-visited-undo",
        prompt: "哪种迷宫任务必须在回退时撤销 visited[x][y]？",
        options: [
          { id: "A", text: "统计所有不重复走格子的简单路径。" },
          { id: "B", text: "只判断起点和终点是否连通。" },
          { id: "C", text: "读入迷宫字符串。" },
          { id: "D", text: "检查坐标是否越界。" },
        ],
        answer: "A",
        explanation: "路径计数中 visited 描述的是“当前路径”，兄弟分支可以从其他方向使用该格，所以离开时要撤销。",
        relatedProblemIds: ["search-maze-reachable", "search-maze-path-count"],
      },
      {
        id: "safe-pruning",
        prompt: "子集和搜索中，使用 if (sum > target) return 的安全前提是什么？",
        options: [
          { id: "A", text: "剩余可选数都不为负，后续选择不可能让 sum 变小。" },
          { id: "B", text: "target 必须是奇数。" },
          { id: "C", text: "数组必须严格递减。" },
          { id: "D", text: "搜索深度必须等于 2。" },
        ],
        answer: "A",
        explanation: "若后续存在负数，当前超过 target 后仍可能被负数拉回，直接剪掉会漏解。",
        relatedProblemIds: ["search-pruned-subset-sum", "search-budget-check"],
      },
    ],
    reviewPlan: [
      {
        title: "框架入门",
        description: "先稳住搜索树、递归出口和选择撤销。",
        problemIds: ["search-binary-strings", "search-dfs-sequences", "search-fixed-weight-binary"],
      },
      {
        title: "经典枚举",
        description: "对比排列、组合和子集的状态与去重方式。",
        problemIds: ["search-permutation-basic", "search-combinations-basic", "search-subsets-basic"],
      },
      {
        title: "约束挑战",
        description: "在网格、剪枝和棋盘约束中综合运用回溯。",
        problemIds: ["search-maze-path-count", "search-pruned-subset-sum", "search-n-queens-count"],
      },
    ],
  },
  "dynamic-programming": {
    chapterId: "dynamic-programming",
    title: "第九章总结测验：动态规划",
    summary: "动态规划的主线是先说清状态含义，再沿依赖关系完成初始化、转移和遍历；表格只是把这些关系保存下来的载体。",
    checklist: [
      "能识别重叠子问题，并在记忆化递归与自底向上 DP 之间转换。",
      "能用完整句子定义 dp[i] 或 dp[i][j]，明确下标范围与答案位置。",
      "能从最后一步列出来源状态，写出计数、最值或可行性转移。",
      "能根据依赖箭头确定初始化与遍历顺序。",
      "能解释 01 背包一维优化为什么必须倒序枚举容量。",
      "能写出 LIS、LCS 和基础区间 DP，并用小表格调试。",
    ],
    questions: [
      {
        id: "dp-state-first",
        prompt: "开始写动态规划代码前，最应该先确定什么？",
        options: [
          { id: "A", text: "每个 dp 状态的完整含义、范围和答案位置。" },
          { id: "B", text: "数组必须开成二维。" },
          { id: "C", text: "所有状态都初始化为 0。" },
          { id: "D", text: "循环一律从大到小。" },
        ],
        answer: "A",
        explanation: "状态定义决定了初值、转移与最终答案；维数和循环方向都应由依赖关系决定。",
        relatedProblemIds: ["dp-min-cost-stairs", "dp-state-table-query"],
      },
      {
        id: "dp-knapsack-order",
        prompt: "01 背包压缩成一维数组后，为什么容量要倒序更新？",
        options: [
          { id: "A", text: "保证来源还是上一轮旧值，避免同一物品被重复使用。" },
          { id: "B", text: "让数组下标不越界。" },
          { id: "C", text: "使时间复杂度变成 O(log n)。" },
          { id: "D", text: "因为物品重量按降序输入。" },
        ],
        answer: "A",
        explanation: "正序会读到本轮刚更新的 dp[j-weight]，等价于允许当前物品再次被选。",
        relatedProblemIds: ["dp-knapsack-01", "dp-knapsack-01-rolling"],
      },
      {
        id: "dp-lis-state",
        prompt: "经典 O(n²) LIS 中 dp[i] 的含义是什么？",
        options: [
          { id: "A", text: "以 a[i] 结尾的最长上升子序列长度。" },
          { id: "B", text: "前 i 个数的总和。" },
          { id: "C", text: "从 a[i] 开始的连续上升段长度。" },
          { id: "D", text: "a[i] 左侧比它大的元素数量。" },
        ],
        answer: "A",
        explanation: "固定结尾后，才能枚举左侧所有更小的前驱并使用 dp[j]+1 转移。",
        relatedProblemIds: ["dp-lis-length", "dp-lis-nondecreasing"],
      },
      {
        id: "dp-lcs-equal",
        prompt: "LCS 中两个前缀末尾字符相等时，当前状态从哪里转移？",
        options: [
          { id: "A", text: "左上状态加 1。" },
          { id: "B", text: "上方状态加 1。" },
          { id: "C", text: "左方状态加 1。" },
          { id: "D", text: "当前状态固定为 1。" },
        ],
        answer: "A",
        explanation: "相等字符可以接在两个都删去末尾后的公共子序列后，因此是 dp[i-1][j-1]+1。",
        relatedProblemIds: ["dp-lcs-length", "dp-lcs-table"],
      },
      {
        id: "dp-interval-order",
        prompt: "区间 DP 为什么通常按区间长度从小到大计算？",
        options: [
          { id: "A", text: "长区间要依赖分割得到的更短子区间。" },
          { id: "B", text: "这样不需要初始化。" },
          { id: "C", text: "区间长度就是最终答案。" },
          { id: "D", text: "可以省略分割点循环。" },
        ],
        answer: "A",
        explanation: "枚举分割点时，左右两段都比当前区间短，必须先得到它们的答案。",
        relatedProblemIds: ["dp-stone-merge", "dp-palindrome-subsequence"],
      },
      {
        id: "dp-debug-first-error",
        prompt: "程序 DP 表与手算表不同，最有效的定位方式是什么？",
        options: [
          { id: "A", text: "找到遍历顺序中的第一个错误状态并检查其来源。" },
          { id: "B", text: "只查看最后答案。" },
          { id: "C", text: "把所有初值改成 0。" },
          { id: "D", text: "随机交换循环顺序。" },
        ],
        answer: "A",
        explanation: "第一个错误状态的来源通常仍正确，最容易把问题缩小到定义、边界或当前转移。",
        relatedProblemIds: ["dp-fibonacci-table", "dp-transition-audit"],
      },
    ],
    reviewPlan: [
      { title: "状态与转移", description: "先稳定一维状态、边界和最值转移。", problemIds: ["dp-fibonacci-bottom-up", "dp-min-cost-stairs", "dp-house-robber"] },
      { title: "表格与背包", description: "练习二维依赖、选或不选与空间压缩。", problemIds: ["dp-grid-paths-obstacles", "dp-knapsack-01", "dp-knapsack-01-rolling"] },
      { title: "序列与区间", description: "完成 LIS、LCS 与区间合并综合训练。", problemIds: ["dp-lis-length", "dp-lcs-length", "dp-stone-merge"] },
    ],
  },
  "divide-conquer": {
    chapterId: "divide-conquer",
    title: "第七章总结测验：分治算法",
    summary:
      "分治的核心是让子问题保持同类且规模严格缩小，并把正确性落实到递归出口、子问题答案和合并规则上；二分、归并、快排与快速幂只是这一骨架的不同落点。",
    checklist: [
      "能用区间参数写清分解位置、递归出口和左右答案的合并方式。",
      "能区分闭区间二分与半开区间边界二分，并保证每轮区间严格缩小。",
      "能独立写出两个有序段的双指针合并，再嵌入归并排序。",
      "能解释 pivot 分区后的不变量，并处理快排中的重复值与退化风险。",
      "能用指数二进制位解释快速幂，并在乘法过程中安全取模。",
      "能在归并时批量统计跨区间逆序对，并用递归树估算 O(n log n)。",
    ],
    questions: [
      {
        id: "divide-three-steps",
        prompt: "一个正确的分治递归最关键的三个结构是什么？",
        options: [
          { id: "A", text: "规模严格缩小的分解、可直接回答的出口、能由子答案得到当前答案的合并。" },
          { id: "B", text: "固定分成三个子问题、使用全局变量、最后排序。" },
          { id: "C", text: "只要调用自己两次即可。" },
          { id: "D", text: "必须使用 while 循环代替递归。" },
        ],
        answer: "A",
        explanation: "没有出口会无限递归，规模不缩小无法到达出口，没有正确合并则子问题答案不能形成原问题答案。",
        relatedProblemIds: ["divide-range-sum", "divide-range-maximum"],
      },
      {
        id: "binary-discard-half",
        prompt: "在严格递增数组中，若 a[mid] < target，闭区间二分下一步应怎样更新？",
        options: [
          { id: "A", text: "left = mid + 1。" },
          { id: "B", text: "right = mid。" },
          { id: "C", text: "left = mid。" },
          { id: "D", text: "同时令 left 和 right 等于 mid。" },
        ],
        answer: "A",
        explanation: "mid 及其左侧都不可能等于更大的 target，因此应完整排除 [left,mid]。",
        relatedProblemIds: ["divide-binary-search-index", "divide-binary-search-comparisons"],
      },
      {
        id: "lower-bound-continue",
        prompt: "查找第一个大于等于 target 的位置时，a[mid] 已满足条件，为什么仍不能立即返回？",
        options: [
          { id: "A", text: "mid 左侧可能还有更早的满足位置。" },
          { id: "B", text: "因为 mid 一定越界。" },
          { id: "C", text: "因为数组必须先逆序。" },
          { id: "D", text: "因为 target 必须出现两次。" },
        ],
        answer: "A",
        explanation: "边界二分寻找的是满足单调条件的第一个位置，命中条件只说明 mid 是候选上界。",
        relatedProblemIds: ["divide-lower-bound-index", "divide-number-range"],
      },
      {
        id: "merge-linear",
        prompt: "两个有序段为什么能在线性时间内合并？",
        options: [
          { id: "A", text: "每次只比较两个段的当前最小未处理元素，并让至少一个指针前进。" },
          { id: "B", text: "因为每个元素会与所有其他元素比较。" },
          { id: "C", text: "因为临时数组会自动排序。" },
          { id: "D", text: "因为递归深度恒为 1。" },
        ],
        answer: "A",
        explanation: "两个指针总共只前进 n+m 次，已有序性保证较小的当前元素就是全局下一个元素。",
        relatedProblemIds: ["divide-merge-two-sorted", "divide-merge-sort"],
      },
      {
        id: "fast-power-bit",
        prompt: "二进制快速幂中，什么时候把当前 base 乘入 answer？",
        options: [
          { id: "A", text: "当前 exponent 的最低位为 1 时。" },
          { id: "B", text: "每轮都无条件乘入。" },
          { id: "C", text: "只有 exponent 为偶数时。" },
          { id: "D", text: "base 等于 1 时。" },
        ],
        answer: "A",
        explanation: "最低位为 1 表示当前 2^k 次幂对指数有贡献；随后 base 平方、exponent 右移。",
        relatedProblemIds: ["divide-fast-power-mod", "divide-fast-power-steps"],
      },
      {
        id: "inversion-batch",
        prompt: "合并两个有序段时，若 left[i] > right[j]，新增多少个跨区间逆序对？",
        options: [
          { id: "A", text: "左段从 i 到末尾的元素个数。" },
          { id: "B", text: "固定增加 1。" },
          { id: "C", text: "右段剩余元素个数。" },
          { id: "D", text: "当前递归深度。" },
        ],
        answer: "A",
        explanation: "左段有序，left[i] 之后的元素都不小于 left[i]，因此都大于 right[j]。",
        relatedProblemIds: ["divide-cross-inversions", "divide-inversion-count"],
      },
    ],
    reviewPlan: [
      {
        title: "分治与二分基础",
        description: "先稳定递归出口、区间缩小和普通二分，再过渡到边界查找。",
        problemIds: ["divide-range-sum", "divide-binary-search-index", "divide-lower-bound-index"],
      },
      {
        title: "排序与合并",
        description: "对比归并的先递归后合并与快排的先分区后递归。",
        problemIds: ["divide-merge-two-sorted", "divide-merge-sort", "divide-lomuto-partition", "divide-quick-sort"],
      },
      {
        title: "计数与复杂度挑战",
        description: "把快速幂、逆序对和递归树串成对数层数的综合训练。",
        problemIds: ["divide-fast-power-mod", "divide-cross-inversions", "divide-inversion-count", "divide-level-work"],
      },
    ],
  },
  "bfs": {
    chapterId: "bfs",
    title: "第八章总结测验：广度优先搜索",
    summary: "这一章的核心是用队列按距离层扩展状态，并把网格、图、数字和字符串统一看成无权状态图。",
    checklist: [
      "能解释队列为什么保证近层状态先于远层状态处理。",
      "能写出入队即标记的 BFS 主循环，避免重复入队。",
      "能处理网格边界、障碍、方向数组和不可达状态。",
      "能用前驱数组还原路径，用多源初始化计算最近源距离。",
      "能判断普通 BFS 只直接适用于等权边最短路，并区分 BFS 与 DFS 的任务信号。",
    ],
    questions: [
      { id: "bfs-mark-time", prompt: "BFS 中通常应在什么时候把新状态标记为已访问？", options: [{ id: "A", text: "入队时。" }, { id: "B", text: "出队后。" }, { id: "C", text: "队列清空后。" }, { id: "D", text: "找到终点后。" }], answer: "A", explanation: "入队即标记可阻止同一状态在出队前被多个父状态重复加入队列。", relatedProblemIds: ["bfs-graph-distances", "bfs-grid-reachable-count"] },
      { id: "bfs-first-shortest", prompt: "无权图中一个节点第一次被 BFS 发现时，为什么距离已经最短？", options: [{ id: "A", text: "队列按非递减距离扩展状态。" }, { id: "B", text: "所有节点编号递增。" }, { id: "C", text: "DFS 已提前检查过。" }, { id: "D", text: "每个节点只有一条入边。" }], answer: "A", explanation: "更短路径必然来自更近的一层，而那一层会更早处理。", relatedProblemIds: ["bfs-number-line-shortest", "bfs-unweighted-shortest"] },
      { id: "bfs-multi-source-init", prompt: "多源 BFS 的正确初始化方式是什么？", options: [{ id: "A", text: "所有源距离设为 0，并在开始时全部入队。" }, { id: "B", text: "逐个源完整运行 BFS 后只保留最后结果。" }, { id: "C", text: "只选择编号最小的源。" }, { id: "D", text: "把源的距离依次设为 0、1、2。" }], answer: "A", explanation: "可把所有源连接到一个虚拟超级源，所有源因此处在同一第 0 层。", relatedProblemIds: ["bfs-infection-time", "bfs-nearest-source"] },
      { id: "bfs-path-data", prompt: "若要输出一条 BFS 最短路径，除距离外还应记录什么？", options: [{ id: "A", text: "每个状态第一次到达时的前驱。" }, { id: "B", text: "每层队列容量。" }, { id: "C", text: "所有可能路径字符串。" }, { id: "D", text: "节点的出度排序。" }], answer: "A", explanation: "从终点沿前驱回到起点，再反转即可得到路径。", relatedProblemIds: ["bfs-maze-path", "bfs-graph-path"] },
      { id: "bfs-use-case", prompt: "下面哪类任务最明确地优先考虑普通 BFS？", options: [{ id: "A", text: "无权图最少边数。" }, { id: "B", text: "枚举所有排列。" }, { id: "C", text: "带负权边最短路。" }, { id: "D", text: "递归生成全部子集。" }], answer: "A", explanation: "普通 BFS 的按层性质正好对应等权边的最少边数。", relatedProblemIds: ["bfs-unweighted-shortest", "bfs-method-signals"] },
    ],
    reviewPlan: [
      { title: "队列与基础层序", description: "先稳固 FIFO、入队标记和距离数组。", problemIds: ["bfs-queue-commands", "bfs-graph-distances", "bfs-level-counts"] },
      { title: "网格最短路", description: "集中练习方向数组、边界、前驱与多源初始化。", problemIds: ["bfs-maze-shortest", "bfs-maze-path", "bfs-infection-time", "bfs-nearest-source"] },
      { title: "状态建模挑战", description: "把骑士、数字和密码锁转成有限无权状态图。", problemIds: ["bfs-knight-shortest", "bfs-number-line-shortest", "bfs-lock-four-digits"] },
    ],
  },
};

export const problemGuides: Record<string, ProblemGuide> = {
  "recursion-countdown": guide(
    ["出口设为 n==0。", "当前层先输出 n，再调用 countdown(n-1)。"],
    ["处理空格后输出当前值。", "递归处理严格更小的 n-1。"],
    ["调用参数不变会无限递归。", "在递归之后输出会得到 1 到 n。"],
  ),
  "recursion-sum-to-n": guide(
    ["把答案拆成当前 n 与 1 到 n-1 的和。", "n==0 时空区间之和为 0。"],
    ["返回 n + sumTo(n-1)。"],
    ["忘记返回子调用结果会得到未定义值。", "累加结果使用 long long。"],
  ),
  "recursion-power-two": guide(
    ["2^0 是递归出口。", "每减少一次指数，回收时乘一次 2。"],
    ["n==0 返回 1，否则返回 2*powerTwo(n-1)。"],
    ["出口返回 0 会让所有结果都变成 0。"],
  ),
  "recursion-print-up": guide(
    ["要让较小数字先输出，因此输出语句放在递归之后。", "n==0 时直接返回。"],
    ["先 printUp(n-1)，再输出 n。"],
    ["空格要放在当前数字之前或统一允许行尾空格，避免 1 和 2 粘在一起。"],
  ),
  "recursion-digit-sum": guide(
    ["n%10 是当前个位。", "n/10 会去掉当前个位并缩小问题。"],
    ["n==0 返回 0，否则返回 n%10+digitSum(n/10)。"],
    ["不要把出口写成 n<10 后返回 0。"],
  ),
  "recursion-gcd": guide(
    ["第二个参数是余数推进器。", "b==0 时第一个参数就是答案。"],
    ["返回 gcdRecursive(b, a%b)。"],
    ["写成 gcd(a%b,b) 不保证第二个参数走向 0。"],
  ),
  "recursion-print-range": guide(
    ["current 表示当前待输出整数。", "current>right 时区间为空。"],
    ["输出 current，再调用 current+1。"],
    ["出口写 current==right 会漏掉 right 或多调用一层，取决于输出位置。"],
  ),
  "recursion-reverse-string": guide(
    ["先让 index 走到字符串末尾。", "回收阶段会按下标从大到小执行输出。"],
    ["index==s.size() 返回；递归后输出 s[index]。"],
    ["在递归之前输出只会得到原字符串。"],
  ),
  "recursion-palindrome": guide(
    ["区间长度小于等于 1 时天然回文。", "两端不同可以立即返回 false。"],
    ["两端相同后检查 left+1、right-1。"],
    ["只移动一侧会多做工作并可能错过正确出口。"],
  ),
  "recursion-sum-stack": guide(
    ["每层的 n 保存在自己的栈帧中。", "子调用返回后再完成当前加法。"],
    ["用 child 保存 recursiveSum(n-1)，返回 n+child。"],
    ["递归出口至少要覆盖 n==1。"],
  ),
  "recursion-enter-leave": guide(
    ["enter 在递归调用前输出。", "leave 在递归调用后输出。"],
    ["n>1 时进入 visit(n-1)，然后输出 leave。"],
    ["n==1 仍要同时输出 enter 和 leave。"],
  ),
  "recursion-array-max": guide(
    ["最后一个元素是最小子问题。", "其余位置与后缀最大值比较。"],
    ["返回 max(a[index], arrayMax(a,index+1))。"],
    ["不能把出口默认成 0，数组元素可能全为负数。"],
  ),
  "recursion-factorial-basic": guide(
    ["0! 和 1! 都等于 1。", "回收时乘上当前 n。"],
    ["n<=1 返回 1，否则返回 1LL*n*factorial(n-1)。"],
    ["结果应使用 long long，且 n 不可超过题目范围。"],
  ),
  "recursion-factorial-trace": guide(
    ["轨迹要在子调用返回之后打印。", "出口层先输出 1!=1。"],
    ["保存 child，算出 answer=n*child，再输出 n!=answer。"],
    ["在展开阶段打印会得到 n 到 1 的顺序。"],
  ),
  "recursion-combination": guide(
    ["k==0 或 k==n 时只有一种选法。", "其余情况分成选当前元素和不选当前元素。"],
    ["返回 C(n-1,k-1)+C(n-1,k)。"],
    ["朴素递归只适合本题给定的小 n。"],
  ),
  "recursion-fibonacci-basic": guide(
    ["F(0)=0、F(1)=1 是两个出口。", "当前项来自前两项。"],
    ["n<=1 返回 n，否则返回 fib(n-1)+fib(n-2)。"],
    ["朴素递归对大 n 会产生大量重复调用。"],
  ),
  "recursion-fibonacci-calls": guide(
    ["函数一进入就把 calls 加一，出口调用也包含在内。", "返回值计算仍按普通 Fibonacci。"],
    ["把 calls++ 放在所有 if 之前。"],
    ["只在非出口节点计数会漏掉递归树的叶子。"],
  ),
  "recursion-fibonacci-memo": guide(
    ["memo[k]!=-1 表示已经计算过。", "出口结果也可以写入缓存。"],
    ["先查缓存，未命中时递归相加并保存。"],
    ["memo 要初始化为不会与合法答案冲突的 -1。"],
  ),
  "recursion-hanoi-moves": guide(
    ["先把 n-1 个盘子移到辅助柱。", "移动第 n 个盘子后，再处理第二个 n-1 子任务。"],
    ["三根柱子在两个子调用中的角色不同，按 from、auxiliary、to 仔细传参。"],
    ["只交换柱名、不交换参数位置会产生非法步骤。"],
  ),
  "recursion-hanoi-count": guide(
    ["两个 n-1 子任务次数相同。", "中间移动最大盘恰好一次。"],
    ["T(0)=0，T(n)=2*T(n-1)+1。"],
    ["n=0 时不能返回 1。"],
  ),
  "recursion-hanoi-disk-counts": guide(
    ["每次执行中间动作时，被移动的是当前编号 n 的盘子。", "两个子任务都处理 1 到 n-1。"],
    ["递归 hanoi(n-1)，counts[n]++，再递归 hanoi(n-1)。"],
    ["盘子编号 1 表示最小盘，不要反向输出。"],
  ),
  "recursion-tree-preorder": guide(
    ["数组下标 i 的孩子是 2*i 和 2*i+1。", "越界或值为 0 时返回。"],
    ["先输出当前根，再递归左右孩子。"],
    ["遇到空节点后不能继续访问它的孩子。"],
  ),
  "recursion-tree-inorder": guide(
    ["递归骨架与前序相同，只移动 visit 的位置。", "当前根在左右子树之间输出。"],
    ["递归左孩子，输出根，递归右孩子。"],
    ["不要把数组中的 0 当普通节点输出。"],
  ),
  "recursion-tree-postorder": guide(
    ["根必须等左右子树都处理完才输出。", "空节点出口仍放在函数开头。"],
    ["递归左、递归右、最后输出根。"],
    ["把输出放在两个子调用之间会变成中序。"],
  ),
  "recursion-depth-trace": guide(
    ["下一层传 depth+1。", "进入和返回使用同一个 depth 缩进。"],
    ["先打印 enter，递归，再打印 leave。"],
    ["不要在返回前修改当前层 depth。"],
  ),
  "recursion-binary-search-trace": guide(
    ["left>right 时返回 -1，不再输出 mid。", "每个有效调用先计算并输出 mid。"],
    ["目标较小搜索 left..mid-1，较大搜索 mid+1..right。"],
    ["子区间再次包含 mid 会导致区间不缩小。"],
  ),
  "recursion-euclid-trace": guide(
    ["每层先输出 depth:a,b。", "b==0 的出口层也需要出现在轨迹里。"],
    ["出口返回 a，否则递归 gcdTrace(b,a%b,depth+1)。"],
    ["最终 gcd= 应由 main 在递归全部返回后输出。"],
  ),
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
  "bubble-sort-basic": guide(
    [
      "把右侧看作逐轮扩大的已排序区；第 i 轮只需扫描到 n - 1 - i。",
      "每次只比较 a[j] 和 a[j + 1]。",
      "左边更大时才交换，这样较大的值会持续向右移动。",
    ],
    ["外层循环控制轮数，内层 j 从 0 扫描到 j + 1 < n - i。", "若 a[j] > a[j + 1]，调用 swap；最后按顺序输出数组。"],
    ["内层循环写到 j < n 会访问 a[n]。", "把比较方向写反会得到降序结果。"],
  ),
  "bubble-sort-count": guide(
    [
      "交换次数只在两个元素真正调用 swap 时增加。",
      "一次相邻交换会消除一个逆序对，可以用这个性质检查结果。",
      "计数变量要放在两层循环外，避免每轮清零。",
    ],
    ["按普通冒泡排序完成双重循环。", "在 if (a[j] > a[j + 1]) 内先交换，再执行 swaps++。"],
    ["比较一次不等于交换一次。", "不要把 swaps 写在 if 外面，否则会统计所有比较。"],
  ),
  "bubble-sort-flag": guide(
    [
      "每一轮开始时先假设不会交换：changed = false。",
      "一旦发生交换就把 changed 设为 true。",
      "整轮结束仍为 false，说明所有相邻元素已经有序，可以 break。",
    ],
    ["在外层循环内初始化 changed。", "完成内层扫描后检查 if (!changed) break。"],
    ["changed 放在外层循环外会保留上一轮状态。", "不能在第一次没有交换的相邻比较后立刻退出，要等整轮结束。"],
  ),
  "selection-sort-basic": guide(
    [
      "第 i 轮要把区间 [i, n - 1] 的最小值放到 a[i]。",
      "先设 minIndex = i，再让 j 从 i + 1 开始扫描。",
      "扫描中只更新下标，扫描结束后再交换一次。",
    ],
    ["若 a[j] < a[minIndex]，令 minIndex = j。", "内层循环结束后 swap(a[i], a[minIndex])。"],
    ["不要把 minIndex 初始化为 0，否则会重新碰已排序区。", "边扫描边交换会偏离选择排序的一轮一次选择。"],
  ),
  "selection-sort-trace": guide(
    [
      "chosen 记录的是每轮扫描结束后的 minIndex。",
      "要在 swap 之前保存下标，因为交换后元素的位置已经改变。",
      "通常只需要 n - 1 轮，最后一个位置自然有序。",
    ],
    ["每轮完成最小值扫描后 chosen.push_back(minIndex)。", "随后交换 a[i] 与 a[minIndex]，最后分别输出数组和 chosen。"],
    ["记录最小值本身而不是下标会与题意不符。", "每次 minIndex 更新都记录会多出中间过程。"],
  ),
  "selection-sort-desc": guide(
    [
      "降序时，左侧已排序区应放当前最大值。",
      "把 minIndex 的含义改成 maxIndex 会更容易读懂。",
      "更新条件从小于改成大于。",
    ],
    ["第 i 轮在 [i, n - 1] 扫描最大值下标。", "扫描结束后把最大值交换到 a[i]。"],
    ["只改变量名而没有改比较方向，结果仍是升序。", "输出阶段不要再次反转数组。"],
  ),
  "insertion-sort-basic": guide(
    [
      "循环开始时，[0, i - 1] 已经有序，先保存 key = a[i]。",
      "比 key 大的元素向右移动，空位随 j 向左移动。",
      "循环结束后，真正的插入位置是 j + 1。",
    ],
    ["设置 j = i - 1，while (j >= 0 && a[j] > key) 不断执行 a[j + 1] = a[j]。", "退出 while 后令 a[j + 1] = key。"],
    ["不先保存 key 会在右移时覆盖待插入元素。", "把 key 写到 a[j] 会在 j=-1 时越界。"],
  ),
  "insertion-sort-shifts": guide(
    [
      "只统计已有元素向右腾位置的动作。",
      "每执行一次 a[j + 1] = a[j]，shifts 就增加一次。",
      "最后把 key 放回空位不算右移。",
    ],
    ["复用插入排序的 while 循环。", "在移动赋值语句之后执行 shifts++，循环外插入 key。"],
    ["比较次数和右移次数不是一回事。", "不要把 a[j + 1] = key 也计入 shifts。"],
  ),
  "insertion-sort-desc": guide(
    [
      "降序有序区要求前面的值更大。",
      "当 a[j] < key 时，a[j] 才应该向右移动。",
      "其他步骤和升序插入排序完全一致。",
    ],
    ["保存 key，令 j=i-1。", "while (j >= 0 && a[j] < key) 右移，最后写入 a[j + 1]。"],
    ["比较符号仍写 > 会继续得到升序。", "相等元素无需移动，否则会破坏稳定性。"],
  ),
  "counting-sort-basic": guide(
    [
      "先根据题目给出的最大值确定 count 数组大小。",
      "数值 x 直接对应桶 count[x]。",
      "还原时从小到大枚举 value，并输出 count[value] 次。",
    ],
    ["扫描输入执行 count[x]++。", "双层还原：外层枚举 value，内层按出现次数输出 value。"],
    ["count 的大小必须覆盖最大可能值。", "只输出一次出现过的值会丢失重复元素。"],
  ),
  "counting-sort-frequency": guide(
    [
      "这题只需要统计，不需要再构造有序数组。",
      "读到 x 时，对应位置就是 count[x]。",
      "即使某个值没出现，也要输出它的 0。",
    ],
    ["建立 m + 1 个桶，对每个输入执行 count[x]++。", "按 0 到 m 的顺序输出全部桶。"],
    ["数组大小写成 m 会缺少值 m 的桶。", "不要按输入顺序输出计数。"],
  ),
  "counting-sort-offset": guide(
    [
      "真实值范围 [minValue, maxValue] 一共有 maxValue - minValue + 1 个桶。",
      "值 x 映射到下标 x - minValue。",
      "桶下标 index 还原为真实值 index + minValue。",
    ],
    ["先读完整个数组并求最小值、最大值，再创建 count。", "统计 count[x-minValue]，最后按桶顺序重复输出 index+minValue。"],
    ["忘记 +1 会让最大值映射到数组外。", "输出桶下标而不加回 minValue 会改变原数据。"],
  ),
  "merge-sort-basic": guide(
    [
      "递归出口是 left >= right，长度 0 或 1 的区间天然有序。",
      "先分别排序 [left, mid] 和 [mid + 1, right]。",
      "合并时用两个指针读取左右有序段，再把 temp 复制回原区间。",
    ],
    ["写好 mergeSort 的拆分与递归调用。", "合并阶段处理左右都未结束、左侧剩余、右侧剩余三种情况。"],
    ["合并后忘记复制回 a，会让上层递归看到旧数据。", "边界混用左闭右开和左右闭区间容易漏元素。"],
  ),
  "merge-two-sorted-arrays": guide(
    [
      "i、j 分别指向两个数组当前还没使用的最小元素。",
      "两边都有元素时，把较小者放入 result，并移动对应指针。",
      "一边用完后，把另一边剩余元素全部追加。",
    ],
    ["先写 while (i < n && j < m) 完成主合并。", "再分别用两个 while 收尾。"],
    ["每轮只能移动被选中一侧的指针。", "漏掉收尾循环会丢失较长数组末尾的数据。"],
  ),
  "merge-sort-inversions": guide(
    [
      "左右子区间内部的逆序对由递归返回值统计。",
      "合并时若 a[i] <= a[j]，先取左侧，不产生跨区间逆序对。",
      "若 a[i] > a[j]，左侧从 i 到 mid 都与 a[j] 构成逆序对。",
    ],
    ["在普通归并排序上累加两个子区间答案。", "取右侧元素时执行 answer += mid - i + 1，完成合并和复制。"],
    ["答案可能超过 int，要使用 long long。", "相等元素不构成严格逆序对，比较应使用 <= 先取左侧。"],
  ),
  "quick-sort-basic": guide(
    [
      "先让 partition 把 pivot 放到最终位置，并返回 pos。",
      "pos 左边都不大于 pivot，右边都大于 pivot。",
      "递归只处理 [left, pos - 1] 和 [pos + 1, right]。",
    ],
    ["递归出口写 left >= right。", "调用 partition 后递归左右两段，不再把 pos 包含进去。"],
    ["递归区间再次包含 pos 可能导致无限递归。", "partition 只能保证分区，不代表左右两段已经有序。"],
  ),
  "quick-sort-partition": guide(
    [
      "pivot 取 a[right]，i 表示当前小于等于 pivot 区域的右边界。",
      "j 扫描到 right - 1，遇到 a[j] <= pivot 就先 i++ 再交换。",
      "扫描结束后，pivot 应与 a[i + 1] 交换。",
    ],
    ["初始化 i = left - 1，完成 j 的单次扫描。", "交换 a[i+1] 与 a[right]，返回 i+1。"],
    ["j 扫到 right 会把 pivot 自己重复参与扫描。", "最后不移动 pivot，返回的位置就没有最终排名含义。"],
  ),
  "quick-select-kth": guide(
    [
      "题目中的第 k 小通常对应 0-based 的 target = k - 1。",
      "partition 后若 pos == target，答案就是 a[pos]。",
      "target 在哪一侧就只进入哪一侧，另一侧可以整体忽略。",
    ],
    ["循环或递归执行 partition。", "根据 target 与 pos 的大小缩小 left/right，直到找到目标位置。"],
    ["把 k 直接当数组下标会偏一位。", "快速选择不要求把整个数组排好，别无条件递归两边。"],
  ),
  "recurrence-climb-stairs-basic": guide(
    [
      "先把 f[i] 读成“走到第 i 阶的方法数”。",
      "最后一步不是走 1 阶，就是走 2 阶，所以来源互不重复。",
      "按题意保留 f[0]=1，并从 i=2 开始计算。",
    ],
    ["创建至少 n+2 个状态，写入 f[0]=1、f[1]=1。", "循环计算 f[i]=f[i-1]+f[i-2]，输出 f[n]。"],
    ["把 f[0] 设为 0 会让后续整条状态链偏小。", "n=0 时仍去访问不存在的小数组位置会越界。"],
  ),
  "recurrence-state-table": guide(
    [
      "这题不仅要答案，还要保留每个中间状态。",
      "初值 f[0]、f[1] 也是状态表的一部分。",
      "输出范围是 0 到 n，共 n+1 项。",
    ],
    ["先按爬楼梯递推填完整个 f 数组。", "从 i=0 到 n 输出，使用 if(i) 控制空格。"],
    ["只输出 f[2] 之后会漏掉初始状态。", "把循环写成 i<n 会漏掉最终答案 f[n]。"],
  ),
  "recurrence-domino-tiling": guide(
    [
      "观察最右侧：可以放一块竖骨牌，或上下两块横骨牌。",
      "两种结尾分别留下 2×(n-1) 和 2×(n-2) 的子问题。",
      "因此状态转移与爬楼梯相同，但要按矩形覆盖解释。",
    ],
    ["定义 f[i] 为覆盖 2×i 矩形的方法数。", "设 f[0]=1、f[1]=1，递推到 f[n]。"],
    ["横骨牌必须上下成对出现。", "不要因为题目背景不同就机械改掉正确的初值。"],
  ),
  "recurrence-known-to-unknown-sequence": guide(
    [
      "f[1]、f[2] 已经给出，是已知区。",
      "第一个未知状态是 f[3]，它的两个来源都已知。",
      "每算出一项，已知区就向右扩展一格。",
    ],
    ["建立能访问到 n 的数组并写入两个初值。", "从 i=3 到 n 计算 f[i]，最后输出 f[n]。"],
    ["循环从 2 开始会覆盖题目给定的 f[2]。", "n=1、n=2 时应直接保留初值。"],
  ),
  "recurrence-new-state-log": guide(
    [
      "只输出递推新算出的状态，不输出 f[1]、f[2]。",
      "计算和输出可以放在同一轮循环里。",
      "n<3 时没有新状态，程序不应输出多余数字。",
    ],
    ["从 i=3 开始填 f[i]。", "每次计算后输出 f[i]，用 first 标记或 i>3 控制空格。"],
    ["先输出初值会与题目要求不符。", "空输出情形不要额外打印 0 或提示文字。"],
  ),
  "recurrence-third-order-sequence": guide(
    [
      "当前项依赖前三项，所以要先准备三个初值。",
      "第一个未知状态是 f[4]。",
      "每轮读取 i-1、i-2、i-3 三个合法位置。",
    ],
    ["写入 f[1]=1、f[2]=1、f[3]=2。", "从 i=4 到 n 求三项之和，输出 f[n]。"],
    ["仍从 i=3 开始会覆盖第三个初值。", "数组只开 n+1 时需确认能访问下标 n，且小 n 也安全。"],
  ),
  "recurrence-climb-stairs-transition": guide(
    [
      "按最后一步分类：最后走 1 阶来自 i-1，最后走 2 阶来自 i-2。",
      "两类方案的最后一步不同，不会重复，可以直接相加。",
      "f[i] 的含义必须始终是到达 i 的方法数。",
    ],
    ["先设置 f[0]=1、f[1]=1。", "按 f[i]=f[i-1]+f[i-2] 递推并输出 f[n]。"],
    ["把“来自哪里”写反不影响加法，但会妨碍复杂变式理解。", "不要额外把当前台阶算成一种方案。"],
  ),
  "recurrence-climb-stairs-transition-table": guide(
    [
      "输出的是新算状态 f[2] 到 f[n]。",
      "f[0]、f[1] 只负责启动递推，不在输出中。",
      "每个新值必须在输出前先完成计算。",
    ],
    ["初始化后从 i=2 循环。", "循环内计算并输出 f[i]，正确控制状态之间的空格。"],
    ["输出整张 f[0..n] 会多两项。", "n<2 时不要输出未计算状态。"],
  ),
  "recurrence-climb-stairs-source-trace": guide(
    [
      "每行的 a、b、c 分别是旧 f[i-1]、旧 f[i-2] 和新 f[i]。",
      "先计算 c，再按题面拼出 i:a+b=c。",
      "输出格式中的冒号、加号和等号都必须精确。",
    ],
    ["初始化 f[0]、f[1] 后，从 i=2 开始循环。", "用 cout 依次输出 i、来源值和结果，每个状态占一行。"],
    ["输出下标 i-1、i-2 而不是对应数值会答非所问。", "不要在最后多打印解释性文字。"],
  ),
  "recurrence-fibonacci-zero-based": guide(
    [
      "0-based 定义明确给出 F(0)=0、F(1)=1。",
      "F(2) 才是第一个由递推式计算的状态。",
      "先单独确认 n=0 的答案是否正确。",
    ],
    ["创建 f 数组并写入 0、1 两个初值。", "从 i=2 递推到 n，输出 f[n]。"],
    ["套用 1-based 的 F(1)=1、F(2)=1 会整体错位。", "循环从 1 开始会读取 f[-1] 或覆盖初值。"],
  ),
  "recurrence-fibonacci-one-based": guide(
    [
      "这题的第一项和第二项都为 1。",
      "输入 n 表示 1-based 的第 n 项，不存在 F(0) 查询。",
      "第一个未知状态是 F[3]。",
    ],
    ["设置 f[1]=1、f[2]=1。", "从 i=3 到 n 递推，输出 f[n]。"],
    ["把 n 当 0-based 下标会多算或少算一项。", "n=1 时数组仍要允许安全设置 f[2]。"],
  ),
  "recurrence-fibonacci-index-table": guide(
    [
      "0-based 的 f[k] 应与 1-based 的 F[k+1] 对照。",
      "两套数组分别按各自初值和起点生成。",
      "先手算 k=0、1、2 的两列检查偏移。",
    ],
    ["填出 f[0..n] 和 F[1..n+1]。", "对每个 k 输出 k、f[k]、F[k+1] 规定的字段。"],
    ["把 F[k] 与 f[k] 直接对齐会产生下标偏移。", "只复用一套数组时别忘了换算 k+1。"],
  ),
  "recurrence-rolling-fibonacci": guide(
    [
      "a、b 分别保存相邻两项 F(0)、F(1)。",
      "每轮先用旧 a、旧 b 算 c。",
      "更新顺序固定为 a=b，再 b=c。",
    ],
    ["先处理 n=0，直接输出 0。", "从 i=2 到 n 滚动更新，循环结束输出 b。"],
    ["先执行 b=c 再计算 a 会丢掉旧 b。", "n=1 时不进入循环，b 本身就是答案。"],
  ),
  "recurrence-rolling-climb-stairs": guide(
    [
      "这里的两个起点是 f[0]=1、f[1]=1。",
      "滚动结构与 Fibonacci 相同，但状态含义和 n=0 答案不同。",
      "a、b 应始终对应当前 i 的前两项。",
    ],
    ["初始化 a=1、b=1。", "从 i=2 到 n 计算 c 并滚动，n=0 时输出 a 或统一返回 1。"],
    ["照搬 Fibonacci 的 n=0 输出 0 会错。", "初始化 a=0、b=1 会算成另一条数列。"],
  ),
  "recurrence-rolling-trace": guide(
    [
      "题目要求先输出本轮的旧 a、旧 b 和新 c。",
      "输出完成后才能让窗口向前滚动。",
      "第 i 行格式是 i:a+b=c。",
    ],
    ["每轮执行 c=a+b，立即输出 trace。", "随后执行 a=b、b=c，再进入下一轮。"],
    ["更新后再输出会把旧值覆盖掉。", "使用数组值代替变量也能算对，但要确保 trace 顺序一致。"],
  ),
  "recurrence-pascal-triangle-row": guide(
    [
      "第 i 行合法列号是 1 到 i。",
      "两端 f[i][1]、f[i][i] 固定为 1。",
      "内部格才从左上和正上方相加。",
    ],
    ["逐行设置边界，再让 j 从 2 到 i-1 填内部。", "最后输出第 n 行的 1..n。"],
    ["内部循环写到 j<=i 会覆盖右边界。", "访问 f[i-1][j] 前要保证 j<i。"],
  ),
  "recurrence-pascal-triangle-table": guide(
    [
      "必须按行从上向下填，因为第 i 行依赖第 i-1 行。",
      "每行先写两端 1，再处理中间。",
      "输出第 i 行时只输出前 i 个有效位置。",
    ],
    ["双重循环构造前 n 行。", "每完成或全部完成后，按三角形范围输出每一行。"],
    ["输出 n×n 矩阵会多出大量无效 0。", "第一行左右边界其实是同一个格，重复赋值没问题。"],
  ),
  "recurrence-pascal-triangle-query": guide(
    [
      "只需要保证构造到第 n 行。",
      "k 是 1-based 列号，答案直接在 f[n][k]。",
      "k=1 或 k=n 时答案应由边界初始化得到 1。",
    ],
    ["按标准杨辉三角递推填到 n。", "输出 f[n][k]，也可用一维滚动数组优化。"],
    ["把 k 减 1 后又访问 1-based 数组会偏一位。", "忘记设置两端边界会让边缘查询输出 0。"],
  ),
  "recurrence-grid-paths-basic": guide(
    [
      "dp[i][j] 表示走到当前格的方法数。",
      "内部格最后一步来自上方或左方。",
      "没有障碍时，第一行和第一列都只有一种走法。",
    ],
    ["初始化 dp[i][1]=1、dp[1][j]=1。", "从 i=2、j=2 开始累加上方与左方，输出 dp[n][m]。"],
    ["把行列下标写反会在非正方形网格出错。", "1×m 或 n×1 不应进入内部循环，但答案仍是 1。"],
  ),
  "recurrence-grid-paths-table": guide(
    [
      "先把第一行和第一列填成边界状态。",
      "每个内部格都依赖已经算好的上方与左方。",
      "输出必须覆盖 n 行、每行 m 列。",
    ],
    ["按行优先填完整张 dp 表。", "双重循环输出 dp[1..n][1..m]，精确控制空格和换行。"],
    ["只输出右下角会漏掉题目要求的表。", "输出下标 0 的哨兵行列会多一圈 0。"],
  ),
  "recurrence-grid-paths-obstacle": guide(
    [
      "障碍格的 dp 必须保持 0，不能从邻居累加。",
      "起点若可走，先设 dp[0][0]=1；若是障碍则保持 0。",
      "非障碍格再分别检查上方和左方是否存在。",
    ],
    ["逐格扫描，遇到 # 就 continue。", "对普通格累加合法的上、左状态，输出终点 dp。"],
    ["先累加再判断障碍会让路径穿过墙。", "无条件把起点设为 1 会使起点是障碍时仍有路径。"],
  ),
  "recurrence-number-tower-basic": guide(
    [
      "定义 f[i][j] 为从当前格走到底层的最大和。",
      "底层没有后续选择，直接等于原数字。",
      "当前格取左下、右下两种后续最大和中的较大者。",
    ],
    ["先复制底层到 f[n][j]。", "让 i 从 n-1 倒到 1，计算 a[i][j]+max(...)，输出 f[1][1]。"],
    ["从上向下填与当前状态定义的依赖方向相反。", "只比较下一格原数字会忽略它后面的整条路径。"],
  ),
  "recurrence-number-tower-table": guide(
    [
      "整张 f 表仍按自底向上计算。",
      "第 i 行只存在 j=1..i 的有效格。",
      "计算完成后按原三角形形状从上到下输出。",
    ],
    ["初始化底层并倒序填完所有上层。", "输出第 i 行的 f[i][1..i]。"],
    ["只输出顶端答案不满足题意。", "输出矩形区域会带出无效位置的 0。"],
  ),
  "recurrence-number-tower-min": guide(
    [
      "状态含义改成从当前格走到底层的最小和。",
      "初始化与遍历方向和最大路径题相同。",
      "唯一核心变化是 max 改为 min。",
    ],
    ["底层 f[n][j]=a[n][j]。", "自底向上执行 a[i][j]+min(左下,右下)，输出顶端。"],
    ["把所有 f 初始为 0 后从上向下取 min 会被虚假的 0 干扰。", "只改题目文字却忘记改 max 会继续输出最大和。"],
  ),
  "recurrence-boundary-climb-stairs": guide(
    [
      "题目明确 n=0 的答案为 1，先让程序覆盖这个最小输入。",
      "数组至少要能安全写入 f[0] 和 f[1]。",
      "依赖 i-1、i-2，所以第一个未知状态是 f[2]。",
    ],
    ["使用 n+2 大小的数组，初始化 f[0]=f[1]=1。", "从 i=2 递推到 n，输出 f[n]。"],
    ["数组只开 n+1 时，n=0 再写 f[1] 会越界。", "循环从 i=1 开始会读取 f[-1]。"],
  ),
  "recurrence-boundary-state-table": guide(
    [
      "这道题的初值是 2 和 3，不能套用 Fibonacci 的 0 和 1。",
      "n=0 时只应输出 f[0]。",
      "状态表范围是闭区间 0..n。",
    ],
    ["设置 f[0]=2、f[1]=3，从 i=2 开始递推。", "按 i=0..n 输出完整状态表。"],
    ["无条件输出 f[1] 会在 n=0 时多输出一项。", "把输出循环写成 i<n 会漏掉 f[n]。"],
  ),
  "recurrence-boundary-grid-sentinel": guide(
    [
      "多开第 0 行和第 0 列，所有位置默认是 0。",
      "把 dp[0][1] 设为 1，能让 dp[1][1] 从上方自然得到 1。",
      "随后每个有效格都统一使用 dp[i-1][j]+dp[i][j-1]。",
    ],
    ["创建 (n+1)×(m+1) 的 0 表并设置唯一哨兵 dp[0][1]=1。", "从 i=1..n、j=1..m 统一递推，输出 dp[n][m]。"],
    ["同时再把第一行、第一列设为 1 会重复设计边界。", "哨兵写成 dp[0][0]=1 时，左上角读取的上、左都仍为 0。"],
  ),
  "greedy-select-k-largest": guide(
    ["恰好选 k 个数时，负数也不能跳过。", "把所有数降序排列后，答案就是前 k 项之和。", "总和使用 long long。"],
    ["降序排序。", "累加下标 0 到 k-1 的元素，复杂度 O(n log n)。"],
    ["只累加正数会违反‘恰好 k 个’。", "用 int 保存总和可能溢出。"],
  ),
  "greedy-coin-greedy-vs-optimal": guide(
    ["贪心部分按币值降序取整。", "最优部分令 dp[x] 表示凑出 x 的最少硬币数。", "无法凑出的状态保持 INF。"],
    ["分别算 greedy 和 dp[amount]。", "剩余金额不为 0 或 dp 为 INF 时输出 -1。"],
    ["把贪心结果误当成最优结果。", "从 INF 加 1 会产生错误状态。"],
  ),
  "greedy-max-affordable-count": guide(
    ["目标是件数而非价值，因此优先买最便宜的。", "排序后逐件扣除预算。", "遇到第一件买不起时，后面更贵的也买不起。"],
    ["价格升序排序。", "能支付就扣预算并计数，否则结束。"],
    ["按原顺序购买不一定最多。", "把预算和价格和放进 int 可能溢出。"],
  ),
  "greedy-select-k-values": guide(
    ["重复值要保留。", "降序排序后输出前 k 个。", "用是否为首项控制空格。"],
    ["sort(a.rbegin(), a.rend())。", "循环 i=0..k-1 输出。"],
    ["用 set 会错误去重。", "最后多余空格通常可接受，但不要多输出行或元素。"],
  ),
  "greedy-min-dot-product": guide(
    ["让一个序列升序，另一个降序。", "这样大数与小数配对。", "乘积和使用 long long。"],
    ["分别做相反方向排序。", "逐位置相乘累加，复杂度 O(n log n)。"],
    ["两个序列都升序会得到较大的点积。", "负数存在时仍可使用同一交换结论。"],
  ),
  "greedy-smallest-concatenation": guide(
    ["不能直接按字符串字典序排序。", "比较 x 在 y 前还是后，要看 x+y 与 y+x。", "数字可能很长，不要转整数。"],
    ["自定义比较器 return x+y < y+x。", "排序后原样依次拼接。"],
    ["比较 x<y 会在 3 和 30 上出错。", "擅自把全零结果压缩成一个 0 会违反本题保留规则。"],
  ),
  "greedy-activity-count": guide(
    ["按结束时间最早排序。", "用 lastEnd 记录上一个已选活动结束时刻。", "半开区间允许 start==lastEnd。"],
    ["排序后扫描。", "满足 start>=lastEnd 时选择并更新 lastEnd。"],
    ["按持续时间最短选不保证最优。", "把 >= 写成 > 会漏掉首尾相接的活动。"],
  ),
  "greedy-activity-ids": guide(
    ["读取时保存原编号。", "结束时间相同按编号小者优先。", "选择规则与基础活动选择相同。"],
    ["按 (end,id) 排序。", "记录所选 id，先输出数量再输出编号。"],
    ["排序后直接输出数组下标会丢失原编号。", "没有处理并列规则会让输出不确定。"],
  ),
  "greedy-interval-cover-count": guide(
    ["先按左端点排序。", "每轮枚举所有 left<=cover 的区间。", "从这些候选中取最大的 right。"],
    ["维护扫描指针 i、当前 cover 和 farthest。", "若 farthest 没推进则输出 -1。"],
    ["只选择第一个能接上的区间不一定最少。", "候选无法推进时继续循环会死循环。"],
  ),
  "greedy-interval-point-cover": guide(
    ["按右端点升序。", "遇到尚未覆盖的区间，就在它的右端点落点。", "闭区间中 point==left 仍算覆盖。"],
    ["维护最近一次选择的 point。", "若 point<left，则 point=right 并计数。"],
    ["按左端点落点可能无法覆盖尽量多的后续区间。", "使用 point<=left 会把端点相等误判为未覆盖。"],
  ),
  "greedy-water-total-wait": guide(
    ["短任务排前。", "第 i 项会让后面的 n-i-1 人等待。", "也可以维护前缀等待逐人累加。"],
    ["升序排序时间。", "累加 time[i]*(n-i-1)。"],
    ["把本人接水时间计入本人的等待。", "贡献乘法使用 int 会溢出。"],
  ),
  "greedy-water-order-average": guide(
    ["为每个人保存 (time,id)。", "并列时间按编号升序。", "平均等待是 total/n，不是总完成时间平均。"],
    ["稳定排序后输出编号。", "维护 prefix，把每个人到来前的 prefix 加入 total，最后保留两位小数。"],
    ["先做整数除法会丢失小数。", "把接水时间本身加入当前人的等待。"],
  ),
  "greedy-standard-change": guide(
    ["固定币值从大到小。", "当前币值使用 amount/coin 枚。", "再令 amount%=coin。"],
    ["依次处理 100、50、20、10、5、1。", "累加每种硬币数量。"],
    ["把这一结论推广到任意币制。", "漏掉面额 1 会使部分金额无法处理。"],
  ),
  "greedy-boats-count": guide(
    ["排序后最重者每轮一定离开。", "若最轻者能与最重者配对，就同时移动左指针。", "每轮都减少右指针并增加船数。"],
    ["升序排序并维护 left、right。", "循环到 left>right。"],
    ["只尝试最重与次重会浪费轻重配对机会。", "只剩一人时仍访问两个不同下标会越界。"],
  ),
  "greedy-boats-pair-solo": guide(
    ["双人船对应一次成功的轻重配对。", "配对失败时最重者单独乘船。", "指针相遇表示最后一人单独乘船。"],
    ["沿用最少救生艇双指针。", "分别累加 pairs 和 solo。"],
    ["把船数当成双人船数。", "指针相遇时误计为一对。"],
  ),
  "greedy-fractional-knapsack": guide(
    ["物品可分割，因此按 value/weight 的单位价值降序。", "每次取 min(capacity,weight)。", "答案使用 double。"],
    ["排序后依次装入。", "取部分物品时按比例增加价值，并把结果保留两位。"],
    ["用整数除法计算单位价值。", "把可分割背包的贪心套到不可分割 0/1 背包。"],
  ),
  "greedy-deadline-max-tasks": guide(
    ["按截止时间升序考虑任务。", "先把当前任务加入已选集合。", "若超时，删掉已选任务里耗时最长的一个。"],
    ["用大根堆维护已选耗时。", "每次 used>deadline 时弹出堆顶，最终堆大小即答案。"],
    ["超时时直接丢弃当前任务，可能不如删掉更早但更耗时的任务。", "只按耗时排序不能同时满足各自截止时间。"],
  ),
  "greedy-min-refuels": guide(
    ["把当前可达范围内经过的加油站油量放入大根堆。", "只有 reach<target 时才需要加油。", "走不动时选择最大油量让新可达范围最远。"],
    ["按位置排序并维护扫描指针。", "堆空且仍未到终点时输出 -1，否则弹堆顶并计数。"],
    ["到站就立即加油会增加不必要次数。", "未先把所有可达站点入堆就做选择会漏候选。"],
  ),
  "greedy-merge-interval-groups": guide(
    ["按左端点升序。", "维护当前合并段最远右端点。", "left<=currentRight 时与当前段相交或相接。"],
    ["遇到断开区间时新增一组。", "否则更新 currentRight=max(currentRight,right)。"],
    ["把端点相接误判成两段。", "合并时直接令 currentRight=right 可能让覆盖范围倒退。"],
  ),
  "search-binary-strings": guide(
    ["pos 表示当前要填的位置。", "先走 0 分支再走 1 分支，输出就是字典序。", "pos==n 时 path 才是完整方案。"],
    ["在 dfs(pos) 中分别 push '0'、'1' 并进入 pos+1。", "每个分支返回后都 pop 末尾字符。"],
    ["只 push 不 pop 会让 path 越来越长。", "在 pos==n-1 就输出会少一位。"],
  ),
  "search-tree-level-count": guide(
    ["进入 dfs(depth) 就说明当前层有一个节点被访问。", "先执行 levelCount[depth]++。", "depth==n 是叶子，不再向下递归。"],
    ["每个非叶子分别调用两次 dfs(depth+1)。", "最后输出下标 0..n。"],
    ["只统计叶子会少掉中间层。", "depth==n 后仍递归会越界。"],
  ),
  "search-dfs-sequences": guide(
    ["每一层都有 1..m 这 m 个候选。", "path.size() 应与 pos 保持一致。", "候选从小到大枚举才是字典序。"],
    ["pos==n 时输出 path 并 return。", "for choice=1..m：push、dfs(pos+1)、pop。"],
    ["把当前 choice 当成 pos。", "忘记 return 会让叶子继续进入候选循环。"],
  ),
  "search-dfs-leaf-count": guide(
    ["这题无需保存 path。", "pos==n 时累加 leaves 并 return。", "非叶子仍需进入 m 个分支。"],
    ["写出与定长序列相同的 DFS 层级。", "只把叶子输出换成 leaves++。"],
    ["在每个节点都计数会得到总节点数。", "n=0 时根本身就是唯一叶子。"],
  ),
  "search-fixed-weight-binary": guide(
    ["ones 记录 path 中已有多少个 1。", "ones>k 后不可能恢复，可直接返回。", "ones+(n-pos)<k 表示剩余位全填 1 也不够。"],
    ["先搜索 0 分支，ones 不变。", "1 分支调用 dfs(pos+1,ones+1)，两边都要 pop。"],
    ["只在叶子判断不会错，但会走很多无效分支。", "把字符 '1' 与整数 1 混用。"],
  ),
  "search-balanced-parentheses": guide(
    ["left 和 right 分别是已放置的左、右括号数。", "left<n 才能继续放 '('。", "right<left 才能放 ')'，否则前缀已经非法。"],
    ["path.size()==2*n 时输出。", "先搜索左括号分支，再搜索右括号分支，每次都撤销。"],
    ["允许 right>left 会生成非法前缀。", "只检查最终左右数量相等不够。"],
  ),
  "search-permutation-basic": guide(
    ["used[value] 表示 value 是否已在当前路径中。", "path.size()==n 时输出。", "候选从 1 到 n 枚举。"],
    ["跳过 used 为 true 的值。", "选择时设标记并 push，返回后 pop 并恢复标记。"],
    ["只恢复 path 不恢复 used 会漏排列。", "used 数组若只开 n 位，访问 used[n] 会越界。"],
  ),
  "search-permutation-kth": guide(
    ["按从小到大枚举候选，叶子顺序就是字典序。", "只在 path.size()==n 时增加 visitedLeaves。", "找到第 k 个后设 found，后续调用立即返回。"],
    ["叶子处先 ++visitedLeaves，再与 k 比较。", "将 found 传回每层，避免继续枚举无用分支。"],
    ["k 从 1 开始，不是数组下标。", "在非叶子增加计数会让排名错位。"],
  ),
  "search-combinations-basic": guide(
    ["start 是本层最小可选值。", "选 value 后下一层从 value+1 开始。", "need=k-path.size() 可用来缩小循环上界。"],
    ["path.size()==k 时输出并 return。", "for value=start..n-need+1，执行 push、dfs(value+1)、pop。"],
    ["下一层仍从 start 开始会重复使用数字。", "像排列一样从 1 重新枚举会产生顺序重复。"],
  ),
  "search-combination-sum-k": guide(
    ["chosen 是已选数量，sum 是已选数字和。", "chosen==k 时才检查 sum==target。", "数都为正，sum>target 后可提前返回。"],
    ["从 start 枚举 value，递归传入 value+1、chosen+1、sum+value。", "对符合条件的叶子累加 answer。"],
    ["只判断 sum 而不限制 chosen 会把不同长度算进来。", "选了 value 后仍从 value 开始会重复选它。"],
  ),
  "search-subsets-basic": guide(
    ["dfs(value) 决定的是 value 选不选。", "先不选后选才能得到题目约定顺序。", "value==n+1 时输出，path 可能为空。"],
    ["不选分支直接 dfs(value+1)。", "选择分支 push value，递归后 pop。"],
    ["漏掉空集会少一个方案。", "改变两个分支顺序会导致输出顺序不符题意。"],
  ),
  "search-subset-sum-count": guide(
    ["index 表示正在决定 numbers[index]。", "不选分支传 sum，选分支传 sum+numbers[index]。", "index==n 时再检查 sum。"],
    ["两个分支都进入 index+1。", "sum==target 时 answer++，因此 target=0 会计入空集。"],
    ["一旦 sum==target 就提前 return 会漏掉包含后续 0 的情形；本题虽为正整数，仍建议在出口统一判断。", "把相同数值当成同一个下标会少算方案。"],
  ),
  "search-maze-reachable": guide(
    ["先检查起点和终点是否为墙。", "新坐标要依次检查越界、墙和 visited。", "只判断连通性时，已访问格无需撤销。"],
    ["进入 dfs(x,y) 后标记 visited[x][y]。", "任意相邻格返回 true 时立即向上返回 true。"],
    ["不记 visited 会在相邻格之间无限递归。", "访问 grid[nx][ny] 前必须先确认坐标在边界内。"],
  ),
  "search-maze-path-count": guide(
    ["visited 描述的是当前这一条路径。", "进入当前格时设 true，离开函数前恢复 false。", "到达终点时累加后立即 return。"],
    ["对四个合法且未访问的相邻格继续 DFS。", "搜完全部邻居后撤销当前格标记。"],
    ["不撤销 visited 会把不同路径互相屏蔽。", "到达终点后继续走会重复统计。"],
  ),
  "search-pruned-subset-sum": guide(
    ["本题数字都为正，sum>target 后可安全剪枝。", "suffixSum[index] 是剩余数全选时的最大增量。", "sum+suffixSum[index]<target 时不可能追上目标。"],
    ["先构建后缀和。", "DFS 前部先写两个剪枝，然后再处理 index==n 与选/不选分支。"],
    ["输入有负数时 sum>target 不再安全。", "suffixSum 下标若少开一位，index==n 会越界。"],
  ),
  "search-knapsack-backtrack": guide(
    ["totalWeight>capacity 时当前分支非法。", "suffixValue[index] 是忽略重量后剩余物品能提供的价值上界。", "totalValue+suffixValue[index]<=best 时无法刷新答案。"],
    ["每到一个合法状态就用 totalValue 更新 best。", "然后分别搜索不选和选当前物品。"],
    ["价值上界剪枝使用 < 或 <= 都不影响最优值，但别把方向写反。", "先访问 weight[index] 再检查 index==n 会越界。"],
  ),
  "search-n-queens-count": guide(
    ["每层只放第 row 行，因此无需检查行冲突。", "主对角线下标是 row-col+n-1。", "副对角线下标是 row+col。"],
    ["列与两条对角线都未占用时才能放。", "进入下一行前同时标记三组约束，返回后同时恢复。"],
    ["忘记给 row-col 加偏移会出现负下标。", "对角线数组需要 2*n-1 位。"],
  ),
  "search-n-queens-first": guide(
    ["让 dfs(row) 返回是否已找到解。", "列从小到大尝试，第一个解就是题目要求的顺序。", "row==n 时返回 true。"],
    ["放置后记录 queenColumn[row]=col 并进入下一行。", "子问题返回 true 时不再撤销，直接向上传递 true。"],
    ["找到解后仍恢复并继续搜索会丢失第一个方案。", "输出要把 0-based 列号加 1。"],
  ),
  "search-budget-check": guide(
    ["目标是比较 b^d 与 limit，不必真的算到超大值。", "每次乘 b 前检查 leaves>limit/b。", "d==0 时 b^0=1。"],
    ["从 leaves=1 开始执行 d 次乘法。", "一旦乘法必定超过 limit 就输出 NO，完成全部次数则输出 YES。"],
    ["先执行 leaves*=b 可能已经溢出，之后比较不可信。", "循环次数应是 d，不是 d+1。"],
  ),
  "search-full-tree-node-count": guide(
    ["第 0 层有 1 个根节点。", "从一层到下一层，nodesOnLevel 乘以 b。", "需要累加第 0 层到第 d 层，共 d+1 层。"],
    ["初始 nodesOnLevel=1、total=0。", "循环 level=0..d：先累加当层，再乘 b 准备下一层。"],
    ["只输出 b^d 得到的是叶子数，不是总节点。", "d=0 时仍要包含根节点。"],
  ),
  "divide-range-sum": guide(
    ["让函数回答闭区间 [left,right] 的和。", "left==right 时直接返回唯一元素。"],
    ["取 mid 后分别递归 [left,mid] 与 [mid+1,right]。", "当前答案是两个返回值之和。"],
    ["递归区间重叠会重复计算。", "总和要使用 long long。"],
  ),
  "divide-range-maximum": guide(
    ["分解方式与分治求和完全相同。", "只需把合并规则换成 max。"],
    ["叶子返回 a[left]。", "返回 max(leftAnswer,rightAnswer)。"],
    ["最大值初值写成 0 会在全负数数组上出错。"],
  ),
  "divide-binary-search-index": guide(
    ["维护答案仍可能出现的闭区间。", "a[mid]<target 时 mid 也能排除。"],
    ["循环条件写 left<=right。", "向右令 left=mid+1，向左令 right=mid-1。"],
    ["写 left=mid 可能在只剩两个元素时死循环。", "未找到要输出 -1。"],
  ),
  "divide-binary-search-comparisons": guide(
    ["每进入一轮循环并读取 a[mid] 就计数一次。", "命中这一轮也要计数。"],
    ["comparisons 在比较前增加。", "随后按普通闭区间二分更新或退出。"],
    ["把左右两次关系判断算成两次会偏大；题目统计的是中点元素比较轮数。"],
  ),
  "divide-lower-bound-index": guide(
    ["使用半开区间 [left,right)，初始 right=n。", "条件是 a[mid]>=target。"],
    ["满足时 right=mid，保留候选。", "不满足时 left=mid+1，最终 left==right。"],
    ["所有元素都小时答案 n，不应输出 -1。", "循环条件应为 left<right。"],
  ),
  "divide-number-range": guide(
    ["first 是第一个 >=target 的位置。", "last 可由第一个 >target 的位置减 1 得到。"],
    ["先求 lower_bound 并判断是否真的等于 target。", "再求 upper_bound-1。"],
    ["只找到任意一次出现位置后向两边线性扫，最坏会退化为 O(n)。"],
  ),
  "divide-merge-sort": guide(
    ["先保证左右两段各自有序，再做 combine。", "临时数组下标与原区间对齐最容易写。"],
    ["递归 [left,mid]、[mid+1,right]。", "双指针合并，补完剩余元素后写回。"],
    ["漏写回原数组会让上层拿到未排序子段。", "相等时优先取左段可保持稳定。"],
  ),
  "divide-merge-two-sorted": guide(
    ["i、j 分别指向两个数组第一个未处理元素。", "某一段耗尽后只能取另一段。"],
    ["每轮取 a[i] 与 b[j] 中较小者。", "直到两个指针都到末尾。"],
    ["只写双指针同时未越界的循环会漏掉尾部。"],
  ),
  "divide-quick-sort": guide(
    ["选中间值作 pivot 可降低已有序输入的退化风险。", "重复值时交换后两个指针都必须移动。"],
    ["先分区到 i>j。", "递归 [left,j] 和 [i,right]，且调用前检查区间有效。"],
    ["交换后不移动指针会在等于 pivot 的元素上死循环。", "递归区间若未缩小会栈溢出。"],
  ),
  "divide-lomuto-partition": guide(
    ["pivot 固定取原数组最后一个元素。", "boundary 表示下一个小于等于 pivot 元素应放的位置。"],
    ["扫描到 <=pivot 时与 a[boundary] 交换并递增 boundary。", "扫描结束把 pivot 交换到 boundary。"],
    ["扫描范围不要包含最后的 pivot。", "比较符号必须符合题目规定的 <=。"],
  ),
  "divide-fast-power-mod": guide(
    ["answer 初始为 1%mod，兼顾 mod=1。", "exponent 的当前位为 1 才乘入。"],
    ["每轮依次处理当前位、base 平方、exponent 右移。", "每次乘法立刻取模。"],
    ["64 位数相乘可能在取模前溢出，可用 __int128 保存中间积。", "0 次幂应返回 1 mod mod。"],
  ),
  "divide-fast-power-steps": guide(
    ["右移轮数就是正指数的二进制位数。", "乘入次数就是二进制中 1 的个数。"],
    ["while exponent>0，每轮 rounds++。", "最低位为 1 时 multiplyRounds++，然后右移。"],
    ["exponent=0 时一轮也不执行。"],
  ),
  "divide-inversion-count": guide(
    ["答案分为左段内部、右段内部、跨左右段三部分。", "跨区间贡献只在归并时统计。"],
    ["left[i]>right[j] 时增加 mid-i+1。", "计数后仍完成合并并写回。"],
    ["相等元素不构成逆序对，应优先取左值。", "答案最多接近 n²/2，要用 long long。"],
  ),
  "divide-cross-inversions": guide(
    ["两个输入段已经有序，不需要递归。", "left[i]>right[j] 时，left[i..n-1] 都能配对。"],
    ["满足 left[i]<=right[j] 时移动 i。", "否则答案加 n-i 并移动 j。"],
    ["相等不算逆序对。", "逐对枚举会超时。"],
  ),
  "divide-level-work": guide(
    ["非 2 的幂要用 (size+1)/2 向上折半。", "根层也有一份 n 的工作。"],
    ["从 size=n 开始，size>1 时折半并增加 levels。", "总层数为 levels+1。"],
    ["只乘 levels 会漏掉根层或叶子层。"],
  ),
  "divide-full-tree-nodes": guide(
    ["完整二叉树每层节点数翻倍。", "叶子层也要计入总数。"],
    ["从 levelNodes=1 开始逐层累加，直到该层节点数等于 leaves。", "也可使用 2*leaves-1。"],
    ["输出 leaves 得到的只是叶子数。"],
  ),
  "bfs-queue-commands": guide(["分别维护队首、队尾语义。", "pop 前必须检查 empty。"], ["逐条读取操作。", "push 入队；pop 输出队首后删除；size 直接查询。"], ["queue::pop 不返回元素。", "空队列调用 front 会产生未定义行为。"]),
  "bfs-round-robin": guide(["队列元素同时保存编号和剩余时间。", "未完成任务要回到队尾。"], ["每轮弹出队首并扣除 quantum。", "剩余量大于 0 则重新入队，否则记录编号。"], ["不要在原位置等待任务完成。", "处理时间用 long long。"]),
  "bfs-graph-distances": guide(["dist=-1 可同时表示未访问。", "起点距离为 0。"], ["起点入队。", "每次把未访问邻居距离设为 dist[u]+1 后立即入队。"], ["无向边要加入两个邻接表。", "入队后才标记会导致重复。"]),
  "bfs-level-counts": guide(["先求每个可达点的 dist。", "最大层只考虑可达点。"], ["完成 BFS 后按距离累加计数数组。", "输出 0 到最大距离。"], ["不可达点不能统计到 -1 层。"]),
  "bfs-maze-shortest": guide(["用四方向数组生成邻格。", "起点或终点为墙时不可达。"], ["建立 n*m 的 dist=-1。", "通过边界、墙和访问检查后赋距离并入队。"], ["先访问 grid[nx][ny] 再判越界会越界。", "答案是步数而非路径格数。"]),
  "bfs-grid-reachable-count": guide(["只要关心是否第一次到达，不必保存完整路径。", "起点入队时计数 1。"], ["每个新格第一次入队时累加。", "队列清空后输出计数。"], ["不能把所有 . 都直接计入，它们可能不连通。"]),
  "bfs-number-line-shortest": guide(["整数就是节点，三种操作就是边。", "限定状态边界保证搜索有限。"], ["从 start BFS。", "生成 x-1、x+1、2*x 并过滤越界与已访问。"], ["target 小于 start 时仍可统一 BFS。", "数组上界必须包含 100000。"]),
  "bfs-modulo-shortest": guide(["取模后状态只有 m 个。", "两个操作都可能回到已访问状态。"], ["dist[start]=0。", "扩展 (x+1)%m 与 (2*x)%m。"], ["m=1 时起终点只能是 0。", "不要在无限整数域搜索。"]),
  "bfs-maze-path": guide(["首次发现邻格时记录其前驱。", "扩展顺序决定多条最短路中输出哪一条。"], ["BFS 填 pre。", "从终点沿 pre 回溯到起点，再 reverse。"], ["输出步数是 path.size()-1。", "不可达时不能回溯未初始化前驱。"]),
  "bfs-graph-path": guide(["邻接表保留输入顺序可让输出确定。", "pre[start] 使用特殊值。"], ["BFS 时记录 pre[v]=u。", "从 n 回溯到 1 并反转。"], ["n=1 时路径长度为 0。", "不要输出发现顺序代替路径。"]),
  "bfs-infection-time": guide(["所有初始 1 都属于第 0 层。", "最后感染时间是最大距离。"], ["扫描网格，把所有 1 同时入队。", "执行一次多源 BFS 并取最大 dist。"], ["逐个感染源独立 BFS 会重复工作。"]),
  "bfs-nearest-source": guide(["每个 1 都是距离 0 的源。", "第一次到达来自某个最近源。"], ["多源初始化后按普通网格 BFS。", "逐行输出距离矩阵。"], ["不能只从第一个 1 出发。", "输出行列空格要准确。"]),
  "bfs-knight-shortest": guide(["列出八种 (dx,dy)。", "小棋盘可能不可达。"], ["起点距离设 0。", "对八个候选统一判边界与访问状态。"], ["输入坐标从 1 开始，数组通常从 0 开始。", "起终点相同答案为 0。"]),
  "bfs-knight-reachable": guide(["题目统计最短距离等于 k，而不是任意走 k 步。", "仍需完整距离数组。"], ["骑士 BFS 求所有最短距离。", "扫描棋盘统计 dist==k。"], ["重复绕路能走 k 步不代表最短距离是 k。"]),
  "bfs-integer-transform": guide(["完整状态只需当前整数。", "操作生成邻居，无需显式建图。"], ["在安全范围内进行 BFS。", "target 第一次发现或出队时得到最短步数。"], ["缺少 visited 会在 x+1 与 x-1 间循环。"]),
  "bfs-lock-four-digits": guide(["10000 个密码可编码为 0 到 9999。", "每位都可循环加减。"], ["先标记所有禁用状态。", "每次生成 8 个邻居并做 BFS。"], ["0 减 1 应变成 9。", "起点或终点禁用时应不可达。"]),
  "bfs-unweighted-shortest": guide(["每条边代价都为 1，这是普通 BFS 的适用信号。", "只需输出到 n 的距离。"], ["从 1 执行 BFS。", "返回 dist[n]，未访问自然为 -1。"], ["用 DFS 找到的第一条路径不保证最短。"]),
  "bfs-method-signals": guide(["SHORTEST、LEVEL、REACH 计入 BFS 类。", "ENUM、BACKTRACK 不计入。"], ["逐个读取字符串。", "匹配前三个信号时增加答案。"], ["这里是在识别题意信号，不需要真的运行搜索。"]),
};

Object.assign(problemGuides, {
  "dp-fibonacci-memo": guide(
    ["先处理 n<=1。", "memo[n] 不是 -1 时直接返回。"],
    ["递归计算两个子问题。", "返回前把和保存到 memo[n]。"],
    ["只读取缓存却不写回会继续重复计算。", "n=0 时数组也要有一个位置。"],
  ),
  "dp-fibonacci-bottom-up": guide(
    ["先初始化 F(0) 与 F(1)。", "循环从 2 开始。"],
    ["按下标递增填写 dp[i]。", "最终输出 dp[n]。"],
    ["n=0 时不能访问 dp[1]。", "结果使用 long long。"],
  ),
  "dp-min-cost-stairs": guide(
    ["dp[i] 表示踏上第 i 级后的最小总代价。", "第 1、2 级都可直接从地面到达。"],
    ["dp[i]=min(dp[i-1],dp[i-2])+cost[i]。"],
    ["不要把题目误解为越过第 n 级。", "单级台阶要单独处理。"],
  ),
  "dp-state-table-query": guide(
    ["转移与最小代价台阶相同。", "本题要求输出所有状态。"],
    ["依次计算后输出 dp[1..n]。"],
    ["状态之间只输出一个空格。", "不要只输出最终答案。"],
  ),
  "dp-house-robber": guide(
    ["当前元素只有选与不选两种决策。", "选择当前时只能接 dp[i-2]。"],
    ["dp[i]=max(dp[i-1],dp[i-2]+a[i])。"],
    ["把 dp[i-1]+a[i] 当候选会选到相邻元素。"],
  ),
  "dp-max-sum-no-adjacent-trace": guide(
    ["先把最终值算法写对。", "每计算一项就保留状态。"],
    ["输出 dp[1] 到 dp[n]。"],
    ["不要输出额外说明文字。", "n=1 时仍要输出一个状态。"],
  ),
  "dp-grid-paths": guide(
    ["dp[1][1]=1。", "其余格从上方和左方累加。"],
    ["按行或按列从左上填到右下。"],
    ["不要再次转移起点。", "首行首列缺失来源按 0 处理。"],
  ),
  "dp-grid-paths-obstacles": guide(
    ["障碍格的状态始终为 0。", "先检查起点和终点。"],
    ["只为可通行格累加上方与左方。"],
    ["不能先算路径再把障碍清零后继续错误传播。"],
  ),
  "dp-number-triangle-max": guide(
    ["从底边向上更容易初始化。", "每格只看下一行两个孩子。"],
    ["a[i][j]+=max(a[i+1][j],a[i+1][j+1])。"],
    ["数字可能为负，答案初值不能固定为 0。"],
  ),
  "dp-number-triangle-min": guide(
    ["结构与最大路径和完全相同。", "合并候选时改用 min。"],
    ["从倒数第二行更新到顶部。"],
    ["不要同时改变遍历方向和比较方向。"],
  ),
  "dp-knapsack-01": guide(
    ["dp[i][j] 只使用前 i 件物品。", "容量不足时只能不选。"],
    ["比较 dp[i-1][j] 与 dp[i-1][j-w]+v。"],
    ["选择来源必须来自上一行。", "容量 0 也属于合法状态。"],
  ),
  "dp-knapsack-exact": guide(
    ["只有 dp[0][0]=0 可达。", "其余初值设为负无穷。"],
    ["只从可达状态进行选或不选转移。"],
    ["普通背包的全 0 初值会把不可达容量当成合法。"],
  ),
  "dp-knapsack-01-rolling": guide(
    ["每件物品处理一次。", "容量从 capacity 倒序到 weight。"],
    ["用 dp[j-weight]+value 更新 dp[j]。"],
    ["正序循环会把同一物品使用多次。"],
  ),
  "dp-knapsack-count": guide(
    ["dp[j] 表示恰好得到重量 j 的方案数。", "空集使 dp[0]=1。"],
    ["对每个物品倒序执行 dp[j]+=dp[j-weight]。"],
    ["相同重量的不同物品仍是不同选择。"],
  ),
  "dp-lis-length": guide(
    ["dp[i] 表示以 a[i] 结尾。", "每个元素自身给出初值 1。"],
    ["枚举 j<i 且 a[j]<a[i]，用 dp[j]+1 更新。"],
    ["答案是所有 dp[i] 的最大值，不一定在最后。"],
  ),
  "dp-lis-nondecreasing": guide(
    ["允许相等元素相接。", "状态定义仍是以 a[i] 结尾。"],
    ["把连接条件写成 a[j]<=a[i]。"],
    ["误用严格小于会在重复值数据上变短。"],
  ),
  "dp-lcs-length": guide(
    ["dp[i][j] 使用两个字符串的前缀。", "第 0 行和第 0 列为 0。"],
    ["字符相等从左上加 1，否则取上、左最大值。"],
    ["字符串字符下标是 i-1 与 j-1。"],
  ),
  "dp-lcs-table": guide(
    ["先正确填完整表格。", "输出时跳过用于空前缀的第 0 行列。"],
    ["按 i=1..n、j=1..m 输出。"],
    ["每行末尾不要输出题目未要求的说明。"],
  ),
  "dp-stone-merge": guide(
    ["dp[l][r] 表示合并该闭区间的最小代价。", "用前缀和快速取得区间总量。"],
    ["按长度递增，枚举 k 分成左右两段。"],
    ["每层合并都要加一次整个区间的石子总数。"],
  ),
  "dp-palindrome-subsequence": guide(
    ["长度为 1 的区间答案为 1。", "从短区间向长区间计算。"],
    ["两端相等时接内部状态加 2，否则丢一端取最大。"],
    ["长度为 2 且两端相等时内部是空区间。"],
  ),
  "dp-fibonacci-table": guide(
    ["本题规定 F(0)=F(1)=1。", "输出从下标 0 开始。"],
    ["逐项转移并依次输出。"],
    ["不要套用 F(0)=0 的另一种定义。"],
  ),
  "dp-transition-audit": guide(
    ["先检查下标 0，再检查下标 1。", "后续正确值应由你重算。"],
    ["按下标递增输出第一个差异，全部相同输出 OK。"],
    ["不能用候选表中的错误前项继续推出所谓正确值。"],
  ),
  "dp-coin-min": guide(
    ["dp[0]=0，其余为 INF。", "每种币可重复使用。"],
    ["对每个金额枚举所有不超过它的币值。"],
    ["不可达来源不能加 1。", "任意币制不能默认贪心正确。"],
  ),
  "dp-method-classifier": guide(
    ["先检查 greedyProven。", "再同时检查 overlap 与 stateable。"],
    ["优先级依次为 GREEDY、DP、SEARCH。"],
    ["只存在一个 DP 特征不足以确定使用 DP。"],
  ),
} satisfies Record<string, ProblemGuide>);

export function getChapterSummaryQuiz(chapterId: string) {
  return chapterSummaryQuizzes[chapterId];
}

export function getProblemGuide(problemId: string) {
  return problemGuides[problemId];
}
