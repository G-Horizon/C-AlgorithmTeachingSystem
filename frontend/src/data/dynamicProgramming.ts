import type { Lesson, Problem } from "./curriculum";

const problem = (
  id: string,
  title: string,
  difficulty: Problem["difficulty"],
  focus: string,
  starterCode: string,
): Problem => ({ id, title, difficulty, focus, status: "ready", starterCode });

const lesson = (
  id: string,
  title: string,
  summary: string,
  concepts: string[],
  steps: string[],
  code: string,
  problems: Problem[],
): Lesson => ({ id, title, summary, duration: "讲义约 10 分钟", concepts, steps, code, problems });

const fibonacciMemoCode = `#include <iostream>
#include <vector>
using namespace std;

vector<long long> memo;
long long fib(int n) {
    if (n <= 1) return n;
    if (memo[n] != -1) return memo[n];
    return memo[n] = fib(n - 1) + fib(n - 2);
}

int main() {
    int n;
    cin >> n;
    memo.assign(n + 1, -1);
    cout << fib(n);
    return 0;
}`;

const minCostCode = `#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> cost(n + 1), dp(n + 1);
    for (int i = 1; i <= n; i++) cin >> cost[i];
    // dp[i]：到达第 i 级台阶的最小总代价
    dp[1] = cost[1];
    if (n >= 2) dp[2] = cost[2];
    for (int i = 3; i <= n; i++) {
        dp[i] = min(dp[i - 1], dp[i - 2]) + cost[i];
    }
    cout << dp[n];
    return 0;
}`;

const houseRobberCode = `#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> value(n + 1), dp(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> value[i];
    dp[1] = value[1];
    for (int i = 2; i <= n; i++) {
        dp[i] = max(dp[i - 1], dp[i - 2] + value[i]);
    }
    cout << dp[n];
    return 0;
}`;

const gridPathsCode = `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<long long>> dp(n + 1, vector<long long>(m + 1, 0));
    dp[1][1] = 1;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (i == 1 && j == 1) continue;
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
        }
    }
    cout << dp[n][m];
    return 0;
}`;

const numberTriangleCode = `#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<vector<long long>> a(n + 2, vector<long long>(n + 2));
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= i; j++) cin >> a[i][j];
    for (int i = n - 1; i >= 1; i--)
        for (int j = 1; j <= i; j++)
            a[i][j] += max(a[i + 1][j], a[i + 1][j + 1]);
    cout << a[1][1];
    return 0;
}`;

const knapsack2dCode = `#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, capacity;
    cin >> n >> capacity;
    vector<int> weight(n + 1), value(n + 1);
    for (int i = 1; i <= n; i++) cin >> weight[i] >> value[i];
    vector<vector<long long>> dp(n + 1, vector<long long>(capacity + 1, 0));
    for (int i = 1; i <= n; i++) {
        for (int j = 0; j <= capacity; j++) {
            dp[i][j] = dp[i - 1][j];
            if (j >= weight[i])
                dp[i][j] = max(dp[i][j], dp[i - 1][j - weight[i]] + value[i]);
        }
    }
    cout << dp[n][capacity];
    return 0;
}`;

const knapsack1dCode = `#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, capacity;
    cin >> n >> capacity;
    vector<long long> dp(capacity + 1, 0);
    for (int i = 1; i <= n; i++) {
        int weight, value;
        cin >> weight >> value;
        for (int j = capacity; j >= weight; j--)
            dp[j] = max(dp[j], dp[j - weight] + value);
    }
    cout << dp[capacity];
    return 0;
}`;

const lisCode = `#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n), dp(n, 1);
    for (int& x : a) cin >> x;
    int answer = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < i; j++)
            if (a[j] < a[i]) dp[i] = max(dp[i], dp[j] + 1);
        answer = max(answer, dp[i]);
    }
    cout << answer;
    return 0;
}`;

const lcsCode = `#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    string a, b;
    cin >> a >> b;
    vector<vector<int>> dp(a.size() + 1, vector<int>(b.size() + 1, 0));
    for (int i = 1; i <= (int)a.size(); i++) {
        for (int j = 1; j <= (int)b.size(); j++) {
            if (a[i - 1] == b[j - 1]) dp[i][j] = dp[i - 1][j - 1] + 1;
            else dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
        }
    }
    cout << dp[a.size()][b.size()];
    return 0;
}`;

const intervalMergeCode = `#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> a(n + 1), prefix(n + 1, 0);
    for (int i = 1; i <= n; i++) { cin >> a[i]; prefix[i] = prefix[i - 1] + a[i]; }
    const long long INF = (1LL << 60);
    vector<vector<long long>> dp(n + 1, vector<long long>(n + 1, 0));
    for (int len = 2; len <= n; len++) {
        for (int left = 1; left + len - 1 <= n; left++) {
            int right = left + len - 1;
            dp[left][right] = INF;
            for (int k = left; k < right; k++)
                dp[left][right] = min(dp[left][right], dp[left][k] + dp[k + 1][right]);
            dp[left][right] += prefix[right] - prefix[left - 1];
        }
    }
    cout << dp[1][n];
    return 0;
}`;

const printDpCode = `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> dp(n + 1, 0);
    dp[0] = 1;
    if (n >= 1) dp[1] = 1;
    for (int i = 2; i <= n; i++) dp[i] = dp[i - 1] + dp[i - 2];
    for (int i = 0; i <= n; i++) {
        if (i) cout << ' ';
        cout << dp[i];
    }
    return 0;
}`;

const coinMinCode = `#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, amount;
    cin >> n >> amount;
    vector<int> coins(n);
    for (int& coin : coins) cin >> coin;
    const int INF = 1000000000;
    vector<int> dp(amount + 1, INF);
    dp[0] = 0;
    for (int value = 1; value <= amount; value++)
        for (int coin : coins)
            if (value >= coin && dp[value - coin] != INF)
                dp[value] = min(dp[value], dp[value - coin] + 1);
    cout << (dp[amount] == INF ? -1 : dp[amount]);
    return 0;
}`;

const todo = (comment: string) => `#include <iostream>\n#include <vector>\nusing namespace std;\n\nint main() {\n    ${comment}\n    return 0;\n}`;

export const dynamicProgrammingLessons: Lesson[] = [
  lesson("dp-recursion-memo", "从递归到记忆化再到 DP", "递归树中的相同子问题可以合并：先缓存答案，再按依赖顺序整理为自底向上的表格。", ["重叠子问题", "记忆化", "自底向上", "Fibonacci"], ["画出递归树并圈出重复节点。", "用 memo 保存第一次计算的结果。", "命中缓存时直接返回。", "观察依赖方向，把递归改成从小到大的循环。", "比较调用次数与空间开销。"], fibonacciMemoCode, [problem("dp-fibonacci-memo", "记忆化 Fibonacci", "入门", "缓存已经计算的 F(n)", fibonacciMemoCode), problem("dp-fibonacci-bottom-up", "自底向上 Fibonacci", "基础", "按 F(0)、F(1) 到 F(n) 的顺序填表", todo("// TODO: 读入 n，自底向上计算并输出 F(n)"))]),
  lesson("dp-state-definition", "状态定义", "先用一句完整的话说明 dp 下标代表的子问题，后面的初始化、转移和答案位置才有共同依据。", ["状态", "下标范围", "子问题", "答案位置"], ["明确原问题要求的目标。", "缩小数据范围得到同类子问题。", "写出 dp[i] 的完整语义。", "检查状态是否包含做决策所需的信息。", "指出最终答案位于哪个状态。"], minCostCode, [problem("dp-min-cost-stairs", "到达末级台阶的最小代价", "基础", "定义 dp[i] 为到达第 i 级的最小代价", minCostCode), problem("dp-state-table-query", "查询台阶 DP 状态", "入门", "输出每一级的最小代价", todo("// TODO: 计算并输出 dp[1..n]"))]),
  lesson("dp-transition", "状态转移", "当前状态只从已经解决的更小状态获得候选答案，再用加法、最值或计数把候选合并。", ["状态转移", "来源状态", "选或不选", "max"], ["固定当前状态并列出最后一步的所有可能。", "为每种选择找到对应的前驱状态。", "写出候选值。", "用 max、min 或求和合并候选。", "确认转移没有遗漏或重复。"], houseRobberCode, [problem("dp-house-robber", "不相邻元素最大和", "基础", "比较不选当前元素与选择当前元素", houseRobberCode), problem("dp-max-sum-no-adjacent-trace", "输出不相邻最大和状态表", "基础", "逐项输出选或不选后的最优值", todo("// TODO: 计算 dp[i]=max(dp[i-1],dp[i-2]+a[i]) 并输出状态表"))]),
  lesson("dp-initialization-order", "初始化与遍历顺序", "初始状态是推导起点；循环顺序必须保证当前格依赖的所有格子已经算好。", ["初始化", "边界", "拓扑顺序", "二维 DP"], ["找出无需转移就能回答的最小问题。", "给不可达状态使用合适的哨兵值。", "为当前格画出所有依赖箭头。", "让循环方向沿箭头从来源走向目标。", "用一行或一列的极小数据检查边界。"], gridPathsCode, [problem("dp-grid-paths", "网格路径计数", "入门", "从上方和左方累加路径数", gridPathsCode), problem("dp-grid-paths-obstacles", "带障碍的网格路径", "基础", "障碍状态保持为 0，其余格从上和左转移", todo("// TODO: 读入网格，计算避开障碍的路径数"))]),
  lesson("dp-number-triangle", "数字三角形 DP", "从底向上把每个位置更新为“自身数字加两个孩子中的较大值”，顶部最终汇总全局最优答案。", ["路径 DP", "自底向上", "原地更新", "最大路径和"], ["定义状态为从当前位置到底边的最大路径和。", "底行天然就是初始状态。", "每个位置比较左下与右下两个孩子。", "按行从下到上更新。", "顶部状态就是答案。"], numberTriangleCode, [problem("dp-number-triangle-max", "数字三角形最大路径和", "基础", "从底向上合并两个孩子", numberTriangleCode), problem("dp-number-triangle-min", "数字三角形最小路径和", "基础", "把 max 改为 min 并保持遍历顺序", todo("// TODO: 自底向上计算最小路径和"))]),
  lesson("dp-knapsack-choice", "01 背包：选或不选", "每件物品最多使用一次；二维状态用上一行同时表达不选当前物品和选择当前物品两种来源。", ["01 背包", "选或不选", "容量", "二维状态"], ["定义 dp[i][j] 为前 i 件物品在容量 j 下的最大价值。", "不选第 i 件时继承 dp[i-1][j]。", "容量足够时才能考虑选择。", "选择后从 dp[i-1][j-weight] 加价值。", "两个候选取最大值。"], knapsack2dCode, [problem("dp-knapsack-01", "01 背包最大价值", "基础", "用二维 DP 比较选或不选", knapsack2dCode), problem("dp-knapsack-exact", "恰好装满的 01 背包", "进阶", "不可达状态设为负无穷，只允许合法来源转移", todo("// TODO: 求恰好装满时的最大价值，不可达输出 -1"))]),
  lesson("dp-knapsack-rolling", "01 背包一维优化", "压缩掉物品维后必须倒序枚举容量，确保来源仍是处理当前物品之前的旧状态。", ["空间优化", "倒序容量", "重复使用", "滚动数组"], ["确认二维转移只依赖上一行。", "把两行压缩成一维数组。", "从大容量向小容量更新。", "解释正序为何会再次读到本轮新值。", "用单件物品的小数据验证只使用一次。"], knapsack1dCode, [problem("dp-knapsack-01-rolling", "一维 01 背包", "基础", "倒序更新容量避免重复选择", knapsack1dCode), problem("dp-knapsack-count", "01 背包装满方案数", "进阶", "倒序累加方案数，dp[0]=1", todo("// TODO: 统计恰好装满 capacity 的选择方案数"))]),
  lesson("dp-lis", "最长上升子序列 LIS", "dp[i] 表示以 a[i] 结尾的最长上升子序列长度，因此只向左寻找更小的前驱。", ["LIS", "以 i 结尾", "前驱", "O(n²)"], ["每个元素单独成序列，所以 dp[i] 初值为 1。", "固定 i，枚举所有 j<i。", "只有 a[j]<a[i] 才能连接。", "用 dp[j]+1 更新 dp[i]。", "所有结尾状态的最大值才是全局答案。"], lisCode, [problem("dp-lis-length", "最长严格上升子序列长度", "基础", "枚举可连接的更小前驱", lisCode), problem("dp-lis-nondecreasing", "最长不下降子序列", "基础", "把可连接条件改为 a[j]<=a[i]", todo("// TODO: 求最长不下降子序列长度"))]),
  lesson("dp-lcs", "最长公共子序列 LCS", "二维状态表示两个字符串前缀的答案：末尾字符相同时接在左上状态后，否则丢弃一个末尾并取较大值。", ["LCS", "字符串前缀", "二维 DP", "左上状态"], ["定义 dp[i][j] 为两个长度分别为 i、j 的前缀的 LCS 长度。", "空前缀对应第 0 行和第 0 列，初值为 0。", "末尾字符相同就从左上加 1。", "不同就比较上方与左方。", "右下角是完整字符串的答案。"], lcsCode, [problem("dp-lcs-length", "最长公共子序列长度", "基础", "按字符相等与否分两类转移", lcsCode), problem("dp-lcs-table", "输出 LCS 状态表", "进阶", "输出每个前缀组合的 LCS 长度", todo("// TODO: 填写并输出完整 LCS 表格"))]),
  lesson("dp-interval", "区间 DP 入门", "先解决短区间，再枚举分割点合并成长区间；三层循环分别负责长度、左端点和分割点。", ["区间 DP", "区间长度", "分割点", "石子合并"], ["定义 dp[l][r] 为合并闭区间的最小代价。", "长度为 1 的区间无需合并，初值为 0。", "按 len 从 2 到 n 枚举。", "枚举 k，把区间分成 [l,k] 与 [k+1,r]。", "子区间代价加本次区间总和并取最小。"], intervalMergeCode, [problem("dp-stone-merge", "石子合并最小代价", "进阶", "按区间长度枚举所有分割点", intervalMergeCode), problem("dp-palindrome-subsequence", "最长回文子序列", "进阶", "由短区间向长区间填表", todo("// TODO: 求字符串的最长回文子序列长度"))]),
  lesson("dp-debug-table", "DP 表调试", "用能手算的小数据打印完整状态表，找到第一个错误格，再沿依赖箭头检查定义、初值、转移和顺序。", ["手填表", "打印状态", "第一个错误", "边界调试"], ["选择规模不超过 5 的代表性输入。", "按状态定义手工填写期望表格。", "让程序临时输出每个状态。", "定位按遍历顺序出现的第一个差异。", "检查它的来源状态和边界后再修正。"], printDpCode, [problem("dp-fibonacci-table", "输出 Fibonacci 状态表", "入门", "输出每个已计算状态用于核对", printDpCode), problem("dp-transition-audit", "检查递推表中的首个错误", "基础", "重算正确状态并输出首个不同下标", todo("// TODO: 读入一张候选状态表，输出首个错误位置或 OK"))]),
  lesson("dp-method-boundary", "DP 与贪心、搜索的边界", "有重叠子问题且状态可完整描述未来时优先考虑 DP；具有可靠局部选择可用贪心，状态难压缩时再考虑搜索与剪枝。", ["算法选择", "最优子结构", "重叠子问题", "贪心反例"], ["先判断题目是计数、可行性还是最优化。", "检查递归分支是否反复遇到相同子问题。", "尝试用少量变量定义完整状态。", "若使用贪心，必须寻找证明或反例。", "用约束估算状态数、转移数和搜索树规模。"], coinMinCode, [problem("dp-coin-min", "任意币制最少硬币数", "基础", "用 DP 避免不可靠的大面额优先", coinMinCode), problem("dp-method-classifier", "算法选择判断", "入门", "根据问题结构输出 DP、GREEDY 或 SEARCH", todo("// TODO: 读取结构特征，按规则输出建议方法"))]),
];
