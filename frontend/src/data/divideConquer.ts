import type { Lesson, Problem } from "./curriculum";

const problem = (
  id: string,
  title: string,
  difficulty: Problem["difficulty"],
  focus: string,
  starterCode: string,
): Problem => ({ id, title, difficulty, focus, status: "ready", starterCode });

const rangeSumCode = `#include <iostream>
#include <vector>
using namespace std;

long long rangeSum(const vector<long long>& a, int left, int right) {
    if (left == right) return a[left];
    int mid = left + (right - left) / 2;
    return rangeSum(a, left, mid) + rangeSum(a, mid + 1, right);
}

int main() {
    int n;
    cin >> n;
    vector<long long> a(n);
    for (long long& x : a) cin >> x;
    cout << rangeSum(a, 0, n - 1);
    return 0;
}`;

const rangeMaximumCode = `#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

long long rangeMaximum(const vector<long long>& a, int left, int right) {
    if (left == right) return a[left];
    int mid = left + (right - left) / 2;
    long long leftAnswer = rangeMaximum(a, left, mid);
    long long rightAnswer = rangeMaximum(a, mid + 1, right);
    return max(leftAnswer, rightAnswer);
}

int main() {
    int n;
    cin >> n;
    vector<long long> a(n);
    for (long long& x : a) cin >> x;
    cout << rangeMaximum(a, 0, n - 1);
    return 0;
}`;

const binarySearchCode = `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    long long target;
    cin >> n >> target;
    vector<long long> a(n);
    for (long long& x : a) cin >> x;

    int left = 0, right = n - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (a[mid] == target) {
            cout << mid;
            return 0;
        }
        if (a[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    cout << -1;
    return 0;
}`;

const binaryComparisonsCode = `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    long long target;
    cin >> n >> target;
    vector<long long> a(n);
    for (long long& x : a) cin >> x;

    int left = 0, right = n - 1, comparisons = 0;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        comparisons++;
        if (a[mid] == target) break;
        if (a[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    cout << comparisons;
    return 0;
}`;

const lowerBoundCode = `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    long long target;
    cin >> n >> target;
    vector<long long> a(n);
    for (long long& x : a) cin >> x;

    int left = 0, right = n;
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (a[mid] >= target) right = mid;
        else left = mid + 1;
    }
    cout << left;
    return 0;
}`;

const numberRangeCode = `#include <iostream>
#include <vector>
using namespace std;

int lowerBound(const vector<long long>& a, long long target) {
    int left = 0, right = a.size();
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (a[mid] >= target) right = mid;
        else left = mid + 1;
    }
    return left;
}

int upperBound(const vector<long long>& a, long long target) {
    int left = 0, right = a.size();
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (a[mid] > target) right = mid;
        else left = mid + 1;
    }
    return left;
}

int main() {
    int n;
    long long target;
    cin >> n >> target;
    vector<long long> a(n);
    for (long long& x : a) cin >> x;
    int first = lowerBound(a, target);
    if (first == n || a[first] != target) cout << "-1 -1";
    else cout << first << ' ' << upperBound(a, target) - 1;
    return 0;
}`;

const mergeSortCode = `#include <iostream>
#include <vector>
using namespace std;

void mergeSort(vector<long long>& a, vector<long long>& temp, int left, int right) {
    if (left >= right) return;
    int mid = left + (right - left) / 2;
    mergeSort(a, temp, left, mid);
    mergeSort(a, temp, mid + 1, right);
    int i = left, j = mid + 1, k = left;
    while (i <= mid && j <= right) {
        if (a[i] <= a[j]) temp[k++] = a[i++];
        else temp[k++] = a[j++];
    }
    while (i <= mid) temp[k++] = a[i++];
    while (j <= right) temp[k++] = a[j++];
    for (int p = left; p <= right; p++) a[p] = temp[p];
}

int main() {
    int n;
    cin >> n;
    vector<long long> a(n), temp(n);
    for (long long& x : a) cin >> x;
    mergeSort(a, temp, 0, n - 1);
    for (int i = 0; i < n; i++) cout << (i ? " " : "") << a[i];
    return 0;
}`;

const mergeTwoCode = `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<long long> a(n), b(m), answer;
    for (long long& x : a) cin >> x;
    for (long long& x : b) cin >> x;
    int i = 0, j = 0;
    while (i < n || j < m) {
        if (j == m || (i < n && a[i] <= b[j])) answer.push_back(a[i++]);
        else answer.push_back(b[j++]);
    }
    for (int k = 0; k < (int)answer.size(); k++) cout << (k ? " " : "") << answer[k];
    return 0;
}`;

const quickSortCode = `#include <iostream>
#include <vector>
using namespace std;

void quickSort(vector<long long>& a, int left, int right) {
    if (left >= right) return;
    long long pivot = a[left + (right - left) / 2];
    int i = left, j = right;
    while (i <= j) {
        while (a[i] < pivot) i++;
        while (a[j] > pivot) j--;
        if (i <= j) swap(a[i++], a[j--]);
    }
    if (left < j) quickSort(a, left, j);
    if (i < right) quickSort(a, i, right);
}

int main() {
    int n;
    cin >> n;
    vector<long long> a(n);
    for (long long& x : a) cin >> x;
    quickSort(a, 0, n - 1);
    for (int i = 0; i < n; i++) cout << (i ? " " : "") << a[i];
    return 0;
}`;

const partitionCode = `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> a(n);
    for (long long& x : a) cin >> x;
    long long pivot = a[n - 1];
    int boundary = 0;
    for (int i = 0; i + 1 < n; i++) {
        if (a[i] <= pivot) swap(a[boundary++], a[i]);
    }
    swap(a[boundary], a[n - 1]);
    cout << boundary << '\\n';
    for (int i = 0; i < n; i++) cout << (i ? " " : "") << a[i];
    return 0;
}`;

const fastPowerCode = `#include <iostream>
using namespace std;

int main() {
    long long base, exponent, mod;
    cin >> base >> exponent >> mod;
    base %= mod;
    long long answer = 1 % mod;
    while (exponent > 0) {
        if (exponent & 1) answer = (__int128)answer * base % mod;
        base = (__int128)base * base % mod;
        exponent >>= 1;
    }
    cout << answer;
    return 0;
}`;

const fastPowerStepsCode = `#include <iostream>
using namespace std;

int main() {
    unsigned long long exponent;
    cin >> exponent;
    int rounds = 0, multiplyRounds = 0;
    while (exponent > 0) {
        rounds++;
        if (exponent & 1) multiplyRounds++;
        exponent >>= 1;
    }
    cout << rounds << ' ' << multiplyRounds;
    return 0;
}`;

const inversionCode = `#include <iostream>
#include <vector>
using namespace std;

long long countInversions(vector<long long>& a, vector<long long>& temp, int left, int right) {
    if (left >= right) return 0;
    int mid = left + (right - left) / 2;
    long long answer = countInversions(a, temp, left, mid)
                     + countInversions(a, temp, mid + 1, right);
    int i = left, j = mid + 1, k = left;
    while (i <= mid && j <= right) {
        if (a[i] <= a[j]) temp[k++] = a[i++];
        else {
            temp[k++] = a[j++];
            answer += mid - i + 1;
        }
    }
    while (i <= mid) temp[k++] = a[i++];
    while (j <= right) temp[k++] = a[j++];
    for (int p = left; p <= right; p++) a[p] = temp[p];
    return answer;
}

int main() {
    int n;
    cin >> n;
    vector<long long> a(n), temp(n);
    for (long long& x : a) cin >> x;
    cout << countInversions(a, temp, 0, n - 1);
    return 0;
}`;

const crossInversionCode = `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<long long> left(n), right(m);
    for (long long& x : left) cin >> x;
    for (long long& x : right) cin >> x;
    long long answer = 0;
    int i = 0, j = 0;
    while (i < n && j < m) {
        if (left[i] <= right[j]) i++;
        else {
            answer += n - i;
            j++;
        }
    }
    cout << answer;
    return 0;
}`;

const levelWorkCode = `#include <iostream>
using namespace std;

int main() {
    unsigned long long n;
    cin >> n;
    int levels = 0;
    unsigned long long size = n;
    while (size > 1) {
        size = (size + 1) / 2;
        levels++;
    }
    cout << levels << ' ' << n * (levels + 1);
    return 0;
}`;

const recursionNodesCode = `#include <iostream>
using namespace std;

int main() {
    unsigned long long leaves;
    cin >> leaves;
    unsigned long long nodes = 0, levelNodes = 1;
    while (levelNodes < leaves) {
        nodes += levelNodes;
        levelNodes *= 2;
    }
    nodes += levelNodes;
    cout << nodes;
    return 0;
}`;

export const divideConquerLessons: Lesson[] = [
  {
    id: "divide-conquer-framework",
    title: "分解、解决、合并",
    summary: "分治把一个大区间拆成更小的同类区间，递归解决后再合并答案；出口、规模缩小和合并规则缺一不可。",
    duration: "10 分钟",
    concepts: ["divide", "solve", "combine", "递归出口", "区间参数"],
    steps: ["用 [left,right] 描述当前任务。", "在 mid 处分成两个规模更小的同类问题。", "长度为 1 时直接回答。", "把左右答案按题目规则合并。"],
    code: rangeSumCode,
    problems: [
      problem("divide-range-sum", "分治求区间总和", "入门", "用左右子区间之和合并当前答案", rangeSumCode),
      problem("divide-range-maximum", "分治求数组最大值", "基础", "把合并规则从加法改为 max", rangeMaximumCode),
    ],
  },
  {
    id: "divide-binary-search",
    title: "二分查找",
    summary: "二分查找利用有序性：比较中点后，能证明目标不在其中一半，于是搜索区间每轮至少缩小一半。",
    duration: "11 分钟",
    concepts: ["有序数组", "闭区间", "中点", "排除一半", "O(log n)"],
    steps: ["维护仍可能包含答案的闭区间 [left,right]。", "用安全写法计算 mid。", "根据比较结果保留唯一可能的一半。", "left > right 表示查找失败。"],
    code: binarySearchCode,
    problems: [
      problem("divide-binary-search-index", "二分查找目标下标", "入门", "维护闭区间并输出任意命中的下标", binarySearchCode),
      problem("divide-binary-search-comparisons", "统计二分比较次数", "基础", "在区间变化过程中准确计数", binaryComparisonsCode),
    ],
  },
  {
    id: "divide-binary-boundary",
    title: "查找边界：第一个大于等于",
    summary: "边界二分不是遇到满足条件就停止，而是把它记作候选答案，继续向左逼近第一个满足条件的位置。",
    duration: "12 分钟",
    concepts: ["半开区间", "lower_bound", "upper_bound", "单调条件", "插入位置"],
    steps: ["把搜索范围写成 [left,right)。", "a[mid] 满足条件时保留 mid 并向左收缩。", "不满足时令 left=mid+1。", "用两个边界得到重复值范围。"],
    code: lowerBoundCode,
    problems: [
      problem("divide-lower-bound-index", "第一个大于等于 target", "基础", "返回合法下标或末尾插入位置 n", lowerBoundCode),
      problem("divide-number-range", "数的起止范围", "进阶", "组合 lower_bound 与 upper_bound", numberRangeCode),
    ],
  },
  {
    id: "divide-merge-sort",
    title: "归并排序的分治视角",
    summary: "归并排序先把区间拆到长度 1，再利用两个子区间已经有序的条件，在线性时间内完成合并。",
    duration: "13 分钟",
    concepts: ["有序子区间", "双指针合并", "临时数组", "稳定排序", "O(n log n)"],
    steps: ["递归排序左右两半。", "双指针比较两段当前元素。", "较小元素进入临时数组。", "把合并结果写回原区间。"],
    code: mergeSortCode,
    problems: [
      problem("divide-merge-sort", "实现归并排序", "基础", "写完整的拆分、递归与合并", mergeSortCode),
      problem("divide-merge-two-sorted", "合并两个有序数组", "入门", "独立练习归并排序的 combine 阶段", mergeTwoCode),
    ],
  },
  {
    id: "divide-quick-sort",
    title: "快速排序的分治视角",
    summary: "快速排序先用 pivot 完成分区，再递归处理两个互不干扰的区间；分区平衡程度决定递归树高度。",
    duration: "13 分钟",
    concepts: ["pivot", "partition", "原地交换", "独立子区间", "最坏 O(n²)"],
    steps: ["选取 pivot。", "移动指针并交换放错区域的元素。", "确认递归区间都严格缩小。", "对左右区间分别快速排序。"],
    code: quickSortCode,
    problems: [
      problem("divide-quick-sort", "实现快速排序", "基础", "正确处理重复值与递归边界", quickSortCode),
      problem("divide-lomuto-partition", "完成一次 pivot 分区", "基础", "观察 pivot 就位后的下标与数组", partitionCode),
    ],
  },
  {
    id: "divide-fast-power",
    title: "快速幂",
    summary: "快速幂按指数的二进制位处理乘方：底数不断平方，当前位为 1 时才乘入答案，把线性次乘法降为对数轮。",
    duration: "11 分钟",
    concepts: ["指数折半", "二进制位", "平方", "模运算", "O(log b)"],
    steps: ["令 answer 表示已处理二进制位的贡献。", "最低位为 1 时乘入当前 base。", "base 每轮平方。", "exponent 右移直到 0。"],
    code: fastPowerCode,
    problems: [
      problem("divide-fast-power-mod", "快速幂取模", "基础", "边乘边取模并避免中间乘法溢出", fastPowerCode),
      problem("divide-fast-power-steps", "快速幂轮数与乘入次数", "入门", "把指数位数和二进制 1 的数量对应到流程", fastPowerStepsCode),
    ],
  },
  {
    id: "divide-inversion-count",
    title: "归并统计逆序对",
    summary: "合并两个有序段时，若左侧当前值大于右侧当前值，左段从当前位置到末尾的所有数都与这个右值构成逆序对。",
    duration: "13 分钟",
    concepts: ["逆序对", "跨区间贡献", "批量计数", "归并", "long long"],
    steps: ["递归统计左右区间内部答案。", "在合并阶段统计跨区间答案。", "右值较小时一次增加 mid-i+1。", "继续归并以维持有序性。"],
    code: inversionCode,
    problems: [
      problem("divide-inversion-count", "统计数组逆序对", "进阶", "把计数嵌入归并排序", inversionCode),
      problem("divide-cross-inversions", "统计两个有序段的跨区间逆序对", "基础", "单独掌握批量增加 n-i", crossInversionCode),
    ],
  },
  {
    id: "divide-recursion-tree",
    title: "递归树复杂度",
    summary: "分治复杂度要同时看递归树高度和每层总工作量：平衡二分通常有 log n 层，若每层线性工作便得到 O(n log n)。",
    duration: "10 分钟",
    concepts: ["递归树", "树高", "每层工作量", "O(n log n)", "平衡分割"],
    steps: ["画出子问题规模随层数的变化。", "计算到达规模 1 需要多少层。", "横向相加得到每层工作量。", "用层数乘每层工作量并辨别最坏退化。"],
    code: levelWorkCode,
    problems: [
      problem("divide-level-work", "估算分治层数与总工作", "基础", "处理非 2 的幂时的向上折半", levelWorkCode),
      problem("divide-full-tree-nodes", "完整二叉递归树节点数", "入门", "区分叶子数、层数与总节点数", recursionNodesCode),
    ],
  },
];
