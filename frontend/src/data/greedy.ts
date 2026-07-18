import type { Lesson, Problem } from "./curriculum";

const cpp = (body: string) => `#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>
using namespace std;

int main() {
${body}
    return 0;
}`;

const problem = (
  id: string,
  title: string,
  difficulty: Problem["difficulty"],
  focus: string,
  starterCode: string,
): Problem => ({ id, title, difficulty, focus, status: "ready", starterCode });

const selectKLargestCode = cpp(`    int n, k;
    cin >> n >> k;
    vector<long long> a(n);
    for (long long& x : a) cin >> x;

    sort(a.rbegin(), a.rend());
    long long answer = 0;
    for (int i = 0; i < k; i++) answer += a[i];
    cout << answer;`);

const maxAffordableCountCode = cpp(`    int n;
    long long budget;
    cin >> n >> budget;
    vector<long long> cost(n);
    for (long long& x : cost) cin >> x;

    sort(cost.begin(), cost.end());
    int count = 0;
    for (long long x : cost) {
        if (x > budget) break;
        budget -= x;
        count++;
    }
    cout << count;`);

const minDotProductCode = cpp(`    int n;
    cin >> n;
    vector<long long> a(n), b(n);
    for (long long& x : a) cin >> x;
    for (long long& x : b) cin >> x;

    sort(a.begin(), a.end());
    sort(b.rbegin(), b.rend());
    long long answer = 0;
    for (int i = 0; i < n; i++) answer += a[i] * b[i];
    cout << answer;`);

const smallestConcatenationCode = `#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<string> a(n);
    for (string& s : a) cin >> s;

    sort(a.begin(), a.end(), [](const string& x, const string& y) {
        return x + y < y + x;
    });
    for (const string& s : a) cout << s;
    return 0;
}`;

const activityCountCode = cpp(`    int n;
    cin >> n;
    vector<pair<int, int>> activities(n);
    for (auto& [start, end] : activities) cin >> start >> end;

    sort(activities.begin(), activities.end(), [](auto a, auto b) {
        return a.second != b.second ? a.second < b.second : a.first < b.first;
    });
    int count = 0;
    int lastEnd = -1000000000;
    for (auto [start, end] : activities) {
        if (start >= lastEnd) {
            count++;
            lastEnd = end;
        }
    }
    cout << count;`);

const activityIdsCode = `#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

struct Activity { int start, end, id; };

int main() {
    int n;
    cin >> n;
    vector<Activity> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i].start >> a[i].end;
        a[i].id = i + 1;
    }
    sort(a.begin(), a.end(), [](const Activity& x, const Activity& y) {
        return x.end != y.end ? x.end < y.end : x.id < y.id;
    });
    int lastEnd = -1000000000;
    vector<int> answer;
    for (const Activity& item : a) {
        if (item.start >= lastEnd) {
            answer.push_back(item.id);
            lastEnd = item.end;
        }
    }
    cout << answer.size() << '\\n';
    for (int i = 0; i < (int)answer.size(); i++) {
        if (i) cout << ' ';
        cout << answer[i];
    }
    return 0;
}`;

const intervalCoverCode = `#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    long long L, R;
    cin >> n >> L >> R;
    vector<pair<long long, long long>> seg(n);
    for (auto& [left, right] : seg) cin >> left >> right;
    sort(seg.begin(), seg.end());

    int used = 0, i = 0;
    long long cover = L;
    while (cover < R) {
        long long farthest = cover;
        while (i < n && seg[i].first <= cover) {
            farthest = max(farthest, seg[i].second);
            i++;
        }
        if (farthest == cover) {
            cout << -1;
            return 0;
        }
        cover = farthest;
        used++;
    }
    cout << used;
    return 0;
}`;

const intervalPointsCode = cpp(`    int n;
    cin >> n;
    vector<pair<int, int>> seg(n);
    for (auto& [left, right] : seg) cin >> left >> right;
    sort(seg.begin(), seg.end(), [](auto a, auto b) { return a.second < b.second; });

    int count = 0;
    int point = -1000000000;
    for (auto [left, right] : seg) {
        if (point < left) {
            point = right;
            count++;
        }
    }
    cout << count;`);

const waterWaitCode = cpp(`    int n;
    cin >> n;
    vector<long long> time(n);
    for (long long& x : time) cin >> x;
    sort(time.begin(), time.end());

    long long total = 0;
    for (int i = 0; i < n; i++) total += time[i] * (n - i - 1);
    cout << total;`);

const waterOrderCode = `#include <algorithm>
#include <iomanip>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<pair<int, int>> people(n);
    for (int i = 0; i < n; i++) {
        cin >> people[i].first;
        people[i].second = i + 1;
    }
    stable_sort(people.begin(), people.end());
    long long prefix = 0, total = 0;
    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << people[i].second;
        total += prefix;
        prefix += people[i].first;
    }
    cout << '\\n' << fixed << setprecision(2) << (double)total / n;
    return 0;
}`;

const coinCountCode = cpp(`    int amount;
    cin >> amount;
    vector<int> coins = {100, 50, 20, 10, 5, 1};
    int count = 0;
    for (int coin : coins) {
        count += amount / coin;
        amount %= coin;
    }
    cout << count;`);

const coinCompareCode = `#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, amount;
    cin >> n >> amount;
    vector<int> coins(n);
    for (int& coin : coins) cin >> coin;
    sort(coins.rbegin(), coins.rend());

    int left = amount, greedy = 0;
    for (int coin : coins) {
        greedy += left / coin;
        left %= coin;
    }

    const int INF = 1000000000;
    vector<int> dp(amount + 1, INF);
    dp[0] = 0;
    for (int value = 1; value <= amount; value++) {
        for (int coin : coins) {
            if (value >= coin && dp[value - coin] != INF) {
                dp[value] = min(dp[value], dp[value - coin] + 1);
            }
        }
    }
    cout << (left == 0 ? greedy : -1) << ' ' << (dp[amount] == INF ? -1 : dp[amount]);
    return 0;
}`;

const boatsCode = cpp(`    int n, limit;
    cin >> n >> limit;
    vector<int> weight(n);
    for (int& x : weight) cin >> x;
    sort(weight.begin(), weight.end());

    int left = 0, right = n - 1, boats = 0;
    while (left <= right) {
        if (left < right && weight[left] + weight[right] <= limit) left++;
        right--;
        boats++;
    }
    cout << boats;`);

const boatPairCountCode = cpp(`    int n, limit;
    cin >> n >> limit;
    vector<int> weight(n);
    for (int& x : weight) cin >> x;
    sort(weight.begin(), weight.end());

    int left = 0, right = n - 1, pairs = 0, solo = 0;
    while (left <= right) {
        if (left == right) {
            solo++;
        } else if (weight[left] + weight[right] <= limit) {
            left++;
            pairs++;
        } else {
            solo++;
        }
        right--;
    }
    cout << pairs << ' ' << solo;`);

const fractionalKnapsackCode = `#include <algorithm>
#include <iomanip>
#include <iostream>
#include <vector>
using namespace std;

struct Item { double weight, value; };

int main() {
    int n;
    double capacity;
    cin >> n >> capacity;
    vector<Item> items(n);
    for (Item& item : items) cin >> item.weight >> item.value;
    sort(items.begin(), items.end(), [](const Item& a, const Item& b) {
        return a.value / a.weight > b.value / b.weight;
    });

    double answer = 0;
    for (const Item& item : items) {
        double take = min(capacity, item.weight);
        answer += take * item.value / item.weight;
        capacity -= take;
        if (capacity == 0) break;
    }
    cout << fixed << setprecision(2) << answer;
    return 0;
}`;

const deadlineTasksCode = `#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<pair<int, int>> tasks(n); // duration, deadline
    for (auto& [duration, deadline] : tasks) cin >> duration >> deadline;
    sort(tasks.begin(), tasks.end(), [](auto a, auto b) { return a.second < b.second; });

    priority_queue<int> chosen;
    long long used = 0;
    for (auto [duration, deadline] : tasks) {
        used += duration;
        chosen.push(duration);
        if (used > deadline) {
            used -= chosen.top();
            chosen.pop();
        }
    }
    cout << chosen.size();
    return 0;
}`;

const refuelCode = cpp(`    int n, target, fuel;
    cin >> n >> target >> fuel;
    vector<pair<int, int>> station(n);
    for (auto& [position, supply] : station) cin >> position >> supply;
    sort(station.begin(), station.end());

    priority_queue<int> passed;
    int i = 0, stops = 0, reach = fuel;
    while (reach < target) {
        while (i < n && station[i].first <= reach) passed.push(station[i++].second);
        if (passed.empty()) {
            cout << -1;
            return 0;
        }
        reach += passed.top();
        passed.pop();
        stops++;
    }
    cout << stops;`);

const mergeIntervalsCode = cpp(`    int n;
    cin >> n;
    vector<pair<int, int>> seg(n);
    for (auto& [left, right] : seg) cin >> left >> right;
    sort(seg.begin(), seg.end());

    int groups = 0;
    int currentRight = -1000000000;
    for (auto [left, right] : seg) {
        if (groups == 0 || left > currentRight) {
            groups++;
            currentRight = right;
        } else {
            currentRight = max(currentRight, right);
        }
    }
    cout << groups;`);

const lesson = (
  id: string,
  title: string,
  summary: string,
  concepts: string[],
  steps: string[],
  code: string,
  problems: Problem[],
): Lesson => ({ id, title, summary, duration: "约 8 分钟", concepts, steps, code, problems });

export const greedyLessons: Lesson[] = [
  lesson(
    "greedy-local-global",
    "局部最优与全局最优",
    "认识贪心的核心：每一步做当前最有利且不可撤销的选择；同时用反例提醒自己，局部最优并不自动推出全局最优。",
    ["局部最优", "全局最优", "不可撤销", "反例", "贪心选择性质"],
    ["先写清候选对象和最终目标。", "把当前选择规则写成一句可执行的话。", "检查选择后剩余问题是否仍是同类问题。", "主动寻找一个能让策略失败的小数据。", "只有规则经得住证明或充分验证，才进入编码。"],
    selectKLargestCode,
    [
      problem("greedy-select-k-largest", "选择 k 个数的最大和", "入门", "每次选择当前最大的剩余元素", selectKLargestCode),
      problem("greedy-coin-greedy-vs-optimal", "贪心找零与最优找零", "进阶", "用动态规划构造反例，比较局部选择与全局最优", coinCompareCode),
    ],
  ),
  lesson(
    "greedy-candidate-set",
    "贪心策略的候选集",
    "把“能选什么、选完删掉什么、状态怎样缩小”写清楚，避免只凭感觉挑选。",
    ["候选集", "可行性", "选择函数", "问题缩减", "预算约束"],
    ["候选集只保留当前仍然可选的对象。", "选择前先检查约束，而不是选完再补救。", "被选对象进入答案，失效对象离开候选集。", "维护最少但足够的状态，例如剩余预算。", "循环在候选为空或目标完成时结束。"],
    maxAffordableCountCode,
    [
      problem("greedy-max-affordable-count", "预算内购买最多物品", "入门", "按价格从低到高选择，维护剩余预算", maxAffordableCountCode),
      problem("greedy-select-k-values", "输出最大的 k 个数", "基础", "排序后明确候选区与答案区", cpp(`    int n, k; cin >> n >> k;\n    vector<int> a(n); for (int& x : a) cin >> x;\n    // TODO: 排序后输出最大的 k 个数（从大到小）`)),
    ],
  ),
  lesson(
    "greedy-sort-then-scan",
    "排序后贪心",
    "很多贪心题先用排序建立一个可靠的决策顺序，再用一次线性扫描完成选择。",
    ["排序", "比较器", "线性扫描", "决策顺序", "相邻交换"],
    ["先判断应按哪个关键量排序。", "比较器必须表达稳定、传递的先后关系。", "排序后只维护扫描所需状态。", "用相邻交换思考：逆序的一对交换后会不会更差。", "整体复杂度通常由排序决定，为 O(n log n)。"],
    minDotProductCode,
    [
      problem("greedy-min-dot-product", "最小点积", "基础", "一个升序、一个降序，用交换直觉最小化乘积和", minDotProductCode),
      problem("greedy-smallest-concatenation", "拼接最小数", "进阶", "使用 x+y 与 y+x 定义贪心排序规则", smallestConcatenationCode),
    ],
  ),
  lesson(
    "greedy-activity-selection",
    "活动选择",
    "按结束时间最早选择活动，为后续活动留下尽可能大的时间空间。",
    ["区间选择", "最早结束", "不相交", "lastEnd", "交换论证"],
    ["把每个活动表示为 [start, end)。", "按 end 从小到大排序。", "若 start >= lastEnd，就选择该活动。", "选择后更新 lastEnd = end。", "最早结束的活动可以替换任意最优方案的第一个活动而不变差。"],
    activityCountCode,
    [
      problem("greedy-activity-count", "最多不冲突活动", "入门", "按结束时间排序并统计选择数", activityCountCode),
      problem("greedy-activity-ids", "输出被选择的活动编号", "基础", "保留原编号并处理相同结束时间", activityIdsCode),
    ],
  ),
  lesson(
    "greedy-interval-cover",
    "区间覆盖",
    "覆盖连续目标时，在所有能接上当前覆盖点的区间中，选择右端点最远的一个。",
    ["区间覆盖", "最远右端点", "扫描指针", "不可达", "最少区间"],
    ["先按左端点排序。", "cover 表示已经连续覆盖到的位置。", "扫描所有 left <= cover 的候选，记录最远 right。", "若最远端点没有推进，说明目标无法覆盖。", "每推进一次计入一个区间，直到 cover >= R。"],
    intervalCoverCode,
    [
      problem("greedy-interval-cover-count", "最少区间覆盖目标线段", "基础", "在可衔接候选中选择延伸最远的区间", intervalCoverCode),
      problem("greedy-interval-point-cover", "最少点覆盖所有区间", "进阶", "按右端点排序，在未覆盖区间的右端点落点", intervalPointsCode),
    ],
  ),
  lesson(
    "greedy-water-queue",
    "排队接水",
    "短任务优先能让较短的处理时间被更多后续人共享，从而最小化总等待时间。",
    ["短作业优先", "总等待时间", "前缀和", "稳定排序", "平均等待"],
    ["按接水时间从小到大排队。", "第 i 个人的时间会计入其后每个人的等待。", "可用 time[i] * (n-i-1) 直接累加总等待。", "相同时间按原编号排列，保证输出确定。", "平均等待时间等于总等待除以人数。"],
    waterWaitCode,
    [
      problem("greedy-water-total-wait", "最小总等待时间", "入门", "短任务优先并计算等待贡献", waterWaitCode),
      problem("greedy-water-order-average", "接水顺序与平均等待", "基础", "稳定排序后输出编号和平均等待时间", waterOrderCode),
    ],
  ),
  lesson(
    "greedy-coins-counterexample",
    "零钱问题与反例",
    "标准币制中从大面额开始很自然，但币制改变后可能失效；学会把“策略有效范围”写进结论。",
    ["找零", "大面额优先", "反例", "动态规划对照", "策略边界"],
    ["对标准币制按面额从大到小取整。", "每次更新剩余金额。", "在币值 1、3、4 和金额 6 上测试：贪心得到 4+1+1。", "全局最优是 3+3，说明只看大面额会失败。", "题目未保证币制性质时，不能默认使用贪心。"],
    coinCountCode,
    [
      problem("greedy-standard-change", "标准币制最少找零", "入门", "在固定标准币制中从大面额向下取", coinCountCode),
      problem("greedy-coin-greedy-vs-optimal", "比较贪心与最优硬币数", "进阶", "输出贪心结果和动态规划最优结果", coinCompareCode),
    ],
  ),
  lesson(
    "greedy-boats",
    "船载人问题",
    "最重的人必须占用一条船；尝试让他与当前最轻的人同行，形成排序加双指针的经典贪心。",
    ["双指针", "最重优先", "轻重配对", "容量约束", "最少船数"],
    ["先将体重升序排序。", "右指针指向当前最重的人，他本轮一定上船。", "若最轻与最重不超重，同时移动左指针。", "无论能否配对，都移动右指针并增加一条船。", "指针相遇后算法结束。"],
    boatsCode,
    [
      problem("greedy-boats-count", "最少救生艇", "基础", "排序加双指针完成轻重配对", boatsCode),
      problem("greedy-boats-pair-solo", "统计双人船与单人船", "基础", "记录每次最重者是否成功配对", boatPairCountCode),
    ],
  ),
  lesson(
    "greedy-exchange-proof",
    "贪心正确性直觉：交换",
    "从一个最优方案出发，把它的第一处不同选择替换为贪心选择；若合法且不变差，就能逐步得到贪心方案。",
    ["交换论证", "不变差", "可行方案", "单位价值", "删去最差选择"],
    ["假设存在一个最优方案。", "找到它与贪心方案的第一处不同。", "把原选择换成贪心选择。", "分别检查方案仍合法、目标值不变差。", "重复交换，直到最优方案变成贪心方案。"],
    fractionalKnapsackCode,
    [
      problem("greedy-fractional-knapsack", "可分割背包", "基础", "按单位重量价值排序并允许取一部分", fractionalKnapsackCode),
      problem("greedy-deadline-max-tasks", "截止时间内完成最多任务", "进阶", "超时就删去当前已选任务中耗时最长者", deadlineTasksCode),
    ],
  ),
  lesson(
    "greedy-self-check",
    "贪心自检清单",
    "用“候选是什么、规则是什么、为什么不后悔、反例是什么”四问完成从读题到实现的闭环。",
    ["候选集", "选择规则", "正确性理由", "边界", "复杂度", "反例"],
    ["候选：这一刻有哪些对象合法可选？", "规则：用哪个关键量比较候选？", "状态：选择后需要维护哪些信息？", "不后悔：能否用交换、领先或结构性质解释？", "反例：换一组小数据，规则是否仍成立？", "实现：最后再决定排序、双指针或优先队列。"],
    refuelCode,
    [
      problem("greedy-min-refuels", "最少加油次数", "进阶", "在已路过加油站中选择油量最大的一个补给", refuelCode),
      problem("greedy-merge-interval-groups", "合并区间后的段数", "基础", "排序后维护当前最远右端点", mergeIntervalsCode),
    ],
  ),
];
