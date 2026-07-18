import type { LucideIcon } from "lucide-react";
import {
  Binary,
  BrainCircuit,
  Braces,
  Compass,
  GitBranch,
  Grid3X3,
  Layers3,
  Repeat2,
  SortAsc,
} from "lucide-react";
import { greedyLessons } from "./greedy";
import { divideConquerLessons } from "./divideConquer";
import { dynamicProgrammingLessons } from "./dynamicProgramming";
import { bfsLessons } from "./bfs";

export type Problem = {
  id: string;
  title: string;
  difficulty: "入门" | "基础" | "进阶";
  focus: string;
  status: "ready" | "planned";
  starterCode: string;
};

export type Lesson = {
  id: string;
  title: string;
  summary: string;
  videoUrl?: string;
  previewImage?: string;
  duration: string;
  concepts: string[];
  steps: string[];
  code: string;
  problems: Problem[];
};

export type Chapter = {
  id: string;
  order: number;
  title: string;
  subtitle: string;
  status: "ready" | "building" | "planned";
  icon: LucideIcon;
  lessons: Lesson[];
};

const bigIntegerOverflowCode = `#include <iostream>
#include <string>
using namespace std;

string stripLeadingZeros(string s) {
    int pos = 0;
    while (pos + 1 < (int)s.size() && s[pos] == '0') pos++;
    return s.substr(pos);
}

int compareNumberString(string a, string b) {
    a = stripLeadingZeros(a);
    b = stripLeadingZeros(b);
    if (a.size() != b.size()) return a.size() > b.size() ? 1 : -1;
    if (a == b) return 0;
    return a > b ? 1 : -1;
}

int main() {
    string x;
    cin >> x;

    if (compareNumberString(x, "2147483647") <= 0) {
        cout << "int";
    } else if (compareNumberString(x, "9223372036854775807") <= 0) {
        cout << "long long";
    } else {
        cout << "big integer";
    }
    return 0;
}`;

const bigIntegerStorageCode = `#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    string s;
    cin >> s;

    vector<int> digits;
    int sum = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        int digit = s[i] - '0';
        digits.push_back(digit);
        sum += digit;
    }

    for (int i = 0; i < (int)digits.size(); i++) {
        if (i) cout << ' ';
        cout << digits[i];
    }
    cout << '\\n' << sum;
    return 0;
}`;

const bigIntegerReverseStorageCode = `#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    string s;
    cin >> s;

    vector<int> digits;
    for (int i = (int)s.size() - 1; i >= 0; i--) {
        digits.push_back(s[i] - '0');
    }

    for (int i = 0; i < (int)digits.size(); i++) {
        if (i) cout << ' ';
        cout << digits[i];
    }
    cout << '\\n';

    for (int i = (int)digits.size() - 1; i >= 0; i--) {
        cout << digits[i];
    }
    return 0;
}`;

const bigIntegerAdditionCode = `#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

vector<int> toDigits(const string& s) {
    vector<int> digits;
    for (int i = (int)s.size() - 1; i >= 0; i--) {
        digits.push_back(s[i] - '0');
    }
    return digits;
}

vector<int> addBigInteger(const vector<int>& a, const vector<int>& b) {
    vector<int> c;
    int carry = 0;
    int n = max(a.size(), b.size());

    for (int i = 0; i < n; i++) {
        int t = carry;
        if (i < (int)a.size()) t += a[i];
        if (i < (int)b.size()) t += b[i];
        c.push_back(t % 10);
        carry = t / 10;
    }

    if (carry) c.push_back(carry);
    return c;
}

void printBigInteger(const vector<int>& digits) {
    for (int i = (int)digits.size() - 1; i >= 0; i--) {
        cout << digits[i];
    }
}

int main() {
    string x, y;
    cin >> x >> y;

    vector<int> a = toDigits(x);
    vector<int> b = toDigits(y);
    vector<int> answer = addBigInteger(a, b);

    printBigInteger(answer);
    return 0;
}`;

const bigIntegerSubtractionCode = `#include <iostream>
#include <string>
#include <vector>
using namespace std;

vector<int> toDigits(const string& s) {
    vector<int> digits;
    for (int i = (int)s.size() - 1; i >= 0; i--) {
        digits.push_back(s[i] - '0');
    }
    return digits;
}

vector<int> subtractBigInteger(const vector<int>& a, const vector<int>& b) {
    vector<int> c;
    int borrow = 0;

    for (int i = 0; i < (int)a.size(); i++) {
        int t = a[i] - borrow;
        if (i < (int)b.size()) t -= b[i];

        if (t < 0) {
            t += 10;
            borrow = 1;
        } else {
            borrow = 0;
        }
        c.push_back(t);
    }

    while (c.size() > 1 && c.back() == 0) {
        c.pop_back();
    }
    return c;
}

void printBigInteger(const vector<int>& digits) {
    for (int i = (int)digits.size() - 1; i >= 0; i--) {
        cout << digits[i];
    }
}

int main() {
    string x, y;
    cin >> x >> y; // 本课先保证 x >= y

    vector<int> a = toDigits(x);
    vector<int> b = toDigits(y);
    vector<int> answer = subtractBigInteger(a, b);

    printBigInteger(answer);
    return 0;
}`;

const bigIntegerCompareCode = `#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int compareBigInteger(const string& a, const string& b) {
    if (a.size() != b.size()) {
        return a.size() > b.size() ? 1 : -1;
    }
    for (int i = 0; i < (int)a.size(); i++) {
        if (a[i] != b[i]) return a[i] > b[i] ? 1 : -1;
    }
    return 0;
}

vector<int> toDigits(const string& s) {
    vector<int> digits;
    for (int i = (int)s.size() - 1; i >= 0; i--) {
        digits.push_back(s[i] - '0');
    }
    return digits;
}

vector<int> subtractAbs(const vector<int>& a, const vector<int>& b) {
    vector<int> c;
    int borrow = 0;

    for (int i = 0; i < (int)a.size(); i++) {
        int t = a[i] - borrow;
        if (i < (int)b.size()) t -= b[i];

        if (t < 0) {
            t += 10;
            borrow = 1;
        } else {
            borrow = 0;
        }
        c.push_back(t);
    }

    while (c.size() > 1 && c.back() == 0) c.pop_back();
    return c;
}

string toString(const vector<int>& digits) {
    string result;
    for (int i = (int)digits.size() - 1; i >= 0; i--) {
        result.push_back(char('0' + digits[i]));
    }
    return result;
}

int main() {
    string x, y;
    cin >> x >> y;

    int order = compareBigInteger(x, y);
    if (order == 0) {
        cout << 0 << '\\n';
        return 0;
    }

    bool negative = false;
    if (order < 0) {
        swap(x, y);
        negative = true;
    }

    vector<int> answer = subtractAbs(toDigits(x), toDigits(y));
    if (negative) cout << '-';
    cout << toString(answer) << '\\n';
    return 0;
}`;

const bigIntegerMultiplySmallCode = `#include <iostream>
#include <string>
#include <vector>
using namespace std;

vector<int> toDigits(const string& s) {
    vector<int> digits;
    for (int i = (int)s.size() - 1; i >= 0; i--) {
        digits.push_back(s[i] - '0');
    }
    return digits;
}

vector<int> multiplyBigInteger(const vector<int>& a, int b) {
    vector<int> c;
    long long carry = 0;

    for (int i = 0; i < (int)a.size(); i++) {
        long long t = 1LL * a[i] * b + carry;
        c.push_back((int)(t % 10));
        carry = t / 10;
    }

    while (carry > 0) {
        c.push_back((int)(carry % 10));
        carry /= 10;
    }

    while (c.size() > 1 && c.back() == 0) {
        c.pop_back();
    }
    return c;
}

void printBigInteger(const vector<int>& digits) {
    for (int i = (int)digits.size() - 1; i >= 0; i--) {
        cout << digits[i];
    }
}

int main() {
    string x;
    int b;
    cin >> x >> b;

    vector<int> a = toDigits(x);
    vector<int> answer = multiplyBigInteger(a, b);

    printBigInteger(answer);
    return 0;
}`;

const bigIntegerMultiplyBigCode = `#include <iostream>
#include <string>
#include <vector>
using namespace std;

vector<int> toDigits(const string& s) {
    vector<int> digits;
    for (int i = (int)s.size() - 1; i >= 0; i--) {
        digits.push_back(s[i] - '0');
    }
    return digits;
}

vector<int> multiplyBigInteger(const vector<int>& a, const vector<int>& b) {
    vector<int> c(a.size() + b.size(), 0);

    for (int i = 0; i < (int)a.size(); i++) {
        for (int j = 0; j < (int)b.size(); j++) {
            c[i + j] += a[i] * b[j];
        }
    }

    for (int i = 0; i < (int)c.size(); i++) {
        if (c[i] >= 10) {
            if (i + 1 == (int)c.size()) c.push_back(0);
            c[i + 1] += c[i] / 10;
            c[i] %= 10;
        }
    }

    while (c.size() > 1 && c.back() == 0) {
        c.pop_back();
    }
    return c;
}

void printBigInteger(const vector<int>& digits) {
    for (int i = (int)digits.size() - 1; i >= 0; i--) {
        cout << digits[i];
    }
}

int main() {
    string x, y;
    cin >> x >> y;

    vector<int> a = toDigits(x);
    vector<int> b = toDigits(y);
    vector<int> answer = multiplyBigInteger(a, b);

    printBigInteger(answer);
    return 0;
}`;

const bigIntegerDivideSmallCode = `#include <iostream>
#include <string>
using namespace std;

string divideBigInteger(const string& a, int b, int& remainder) {
    string q;
    long long r = 0;

    for (int i = 0; i < (int)a.size(); i++) {
        r = r * 10 + (a[i] - '0');
        q.push_back(char('0' + r / b));
        r %= b;
    }

    int start = 0;
    while (start + 1 < (int)q.size() && q[start] == '0') {
        start++;
    }

    remainder = (int)r;
    return q.substr(start);
}

int main() {
    string x;
    int b;
    cin >> x >> b;

    int remainder = 0;
    string quotient = divideBigInteger(x, b, remainder);

    cout << quotient;
    return 0;
}`;

const bigIntegerNormalizeCode = `#include <iostream>
#include <string>
#include <vector>
using namespace std;

vector<int> toDigits(const string& s) {
    vector<int> digits;
    for (int i = (int)s.size() - 1; i >= 0; i--) {
        digits.push_back(s[i] - '0');
    }
    return digits;
}

void normalize(vector<int>& digits) {
    while (digits.size() > 1 && digits.back() == 0) {
        digits.pop_back();
    }
}

string toString(const vector<int>& digits) {
    string answer;
    for (int i = (int)digits.size() - 1; i >= 0; i--) {
        answer.push_back(char('0' + digits[i]));
    }
    return answer;
}

string trimLeadingZeros(const string& s) {
    int start = 0;
    while (start + 1 < (int)s.size() && s[start] == '0') {
        start++;
    }
    return s.substr(start);
}

int main() {
    string raw;
    cin >> raw;

    vector<int> digits = toDigits(raw);
    normalize(digits);

    cout << toString(digits) << '\\n';
    cout << trimLeadingZeros(raw) << '\\n';
    return 0;
}`;

const bigIntegerCompositeCode = `#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

void normalize(vector<int>& digits) {
    while (digits.size() > 1 && digits.back() == 0) {
        digits.pop_back();
    }
}

vector<int> addBigInteger(const vector<int>& a, const vector<int>& b) {
    vector<int> c;
    int carry = 0;
    int n = max(a.size(), b.size());

    for (int i = 0; i < n; i++) {
        int t = carry;
        if (i < (int)a.size()) t += a[i];
        if (i < (int)b.size()) t += b[i];
        c.push_back(t % 10);
        carry = t / 10;
    }

    if (carry) c.push_back(carry);
    return c;
}

vector<int> multiplySmall(const vector<int>& a, int b) {
    vector<int> c;
    long long carry = 0;

    for (int i = 0; i < (int)a.size(); i++) {
        long long t = 1LL * a[i] * b + carry;
        c.push_back((int)(t % 10));
        carry = t / 10;
    }

    while (carry > 0) {
        c.push_back((int)(carry % 10));
        carry /= 10;
    }

    normalize(c);
    return c;
}

string toString(const vector<int>& digits) {
    string answer;
    for (int i = (int)digits.size() - 1; i >= 0; i--) {
        answer.push_back(char('0' + digits[i]));
    }
    return answer;
}

vector<int> factorial(int n) {
    vector<int> answer(1, 1);
    for (int i = 2; i <= n; i++) {
        answer = multiplySmall(answer, i);
    }
    return answer;
}

vector<int> fibonacci(int n) {
    if (n == 0) return vector<int>(1, 0);
    vector<int> a(1, 0), b(1, 1);
    for (int i = 2; i <= n; i++) {
        vector<int> c = addBigInteger(a, b);
        a = b;
        b = c;
    }
    return b;
}

int main() {
    int n;
    cin >> n;

    cout << toString(factorial(n)) << '\\n';
    cout << toString(fibonacci(n)) << '\\n';
    return 0;
}`;

const bubbleSortCode = `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    for (int i = 0; i < n - 1; i++) {
        bool changed = false;
        for (int j = 0; j < n - i - 1; j++) {
            if (a[j] > a[j + 1]) {
                swap(a[j], a[j + 1]);
                changed = true;
            }
        }
        if (!changed) break;
    }

    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << a[i];
    }
    return 0;
}`;

const selectionSortCode = `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    for (int i = 0; i < n - 1; i++) {
        int minIndex = i;
        for (int j = i + 1; j < n; j++) {
            if (a[j] < a[minIndex]) {
                minIndex = j;
            }
        }
        swap(a[i], a[minIndex]);
    }

    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << a[i];
    }
    return 0;
}`;

const insertionSortCode = `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    for (int i = 1; i < n; i++) {
        int key = a[i];
        int j = i - 1;
        while (j >= 0 && a[j] > key) {
            a[j + 1] = a[j];
            j--;
        }
        a[j + 1] = key;
    }

    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << a[i];
    }
    return 0;
}`;

const countingSortCode = `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    int maxValue = 0;
    for (int i = 0; i < n; i++) {
        cin >> a[i];
        if (a[i] > maxValue) maxValue = a[i];
    }

    vector<int> count(maxValue + 1, 0);
    for (int x : a) {
        count[x]++;
    }

    bool first = true;
    for (int value = 0; value <= maxValue; value++) {
        while (count[value] > 0) {
            if (!first) cout << ' ';
            cout << value;
            first = false;
            count[value]--;
        }
    }
    return 0;
}`;

const mergeSortCode = `#include <iostream>
#include <vector>
using namespace std;

void mergeSort(vector<int>& a, int left, int right, vector<int>& temp) {
    if (left >= right) return;

    int mid = (left + right) / 2;
    mergeSort(a, left, mid, temp);
    mergeSort(a, mid + 1, right, temp);

    int i = left;
    int j = mid + 1;
    int k = left;

    while (i <= mid && j <= right) {
        if (a[i] <= a[j]) {
            temp[k++] = a[i++];
        } else {
            temp[k++] = a[j++];
        }
    }
    while (i <= mid) temp[k++] = a[i++];
    while (j <= right) temp[k++] = a[j++];

    for (int p = left; p <= right; p++) {
        a[p] = temp[p];
    }
}

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    vector<int> temp(n);
    mergeSort(a, 0, n - 1, temp);

    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << a[i];
    }
    return 0;
}`;

const quickSortCode = `#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int partition(vector<int>& a, int left, int right) {
    int pivot = a[right];
    int i = left - 1;

    for (int j = left; j < right; j++) {
        if (a[j] <= pivot) {
            i++;
            swap(a[i], a[j]);
        }
    }
    swap(a[i + 1], a[right]);
    return i + 1;
}

void quickSort(vector<int>& a, int left, int right) {
    if (left >= right) return;

    int pos = partition(a, left, right);
    quickSort(a, left, pos - 1);
    quickSort(a, pos + 1, right);
}

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    quickSort(a, 0, n - 1);

    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << a[i];
    }
    return 0;
}`;

const recurrenceStateCode = `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    // f[i] 表示走到第 i 阶的方法数
    vector<long long> f(n + 2, 0);
    f[0] = 1;
    f[1] = 1;

    for (int i = 2; i <= n; i++) {
        f[i] = f[i - 1] + f[i - 2];
    }

    // 原问题“到第 n 阶”对应答案 f[n]
    cout << f[n];
    return 0;
}`;

const recurrenceKnownToUnknownCode = `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    // 已知起点：前两个格子已经确定
    vector<long long> f(n + 3, 0);
    f[1] = 1;
    f[2] = 2;

    // 从第一个未知格 f[3] 开始，向右推出答案
    for (int i = 3; i <= n; i++) {
        f[i] = f[i - 1] + f[i - 2];
    }

    cout << f[n];
    return 0;
}`;

const recurrenceClimbStairsCode = `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    // f[i] 表示走到第 i 阶的方法数
    vector<long long> f(n + 2, 0);
    f[0] = 1;
    f[1] = 1;

    // 最后一步来自 i - 1 或 i - 2
    for (int i = 2; i <= n; i++) {
        f[i] = f[i - 1] + f[i - 2];
    }

    cout << f[n];
    return 0;
}`;

const recurrenceFibonacciZeroBasedCode = `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    // 题目定义：F(0) = 0, F(1) = 1
    vector<long long> f(n + 2, 0);
    f[0] = 0;
    f[1] = 1;

    // 第一个未知格是 f[2]
    for (int i = 2; i <= n; i++) {
        f[i] = f[i - 1] + f[i - 2];
    }

    cout << f[n];
    return 0;
}`;

const recurrenceRollingFibonacciCode = `#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;

    // 题目定义：F(0) = 0, F(1) = 1
    if (n == 0) {
        cout << 0;
        return 0;
    }

    long long a = 0; // f[i - 2]
    long long b = 1; // f[i - 1]

    for (int i = 2; i <= n; i++) {
        long long c = a + b;
        a = b;
        b = c;
    }

    cout << b;
    return 0;
}`;

const recurrencePascalTriangleCode = `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    // f[i][j] 表示杨辉三角第 i 行第 j 个数
    vector<vector<long long>> f(n + 1, vector<long long>(n + 1, 0));

    for (int i = 1; i <= n; i++) {
        f[i][1] = f[i][i] = 1;
        for (int j = 2; j < i; j++) {
            f[i][j] = f[i - 1][j - 1] + f[i - 1][j];
        }
    }

    for (int j = 1; j <= n; j++) {
        if (j > 1) cout << ' ';
        cout << f[n][j];
    }
    return 0;
}`;

const recurrenceGridPathsCode = `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;

    // dp[i][j] 表示走到第 i 行第 j 列的方法数
    vector<vector<long long>> dp(n + 1, vector<long long>(m + 1, 0));

    for (int i = 1; i <= n; i++) dp[i][1] = 1;
    for (int j = 1; j <= m; j++) dp[1][j] = 1;

    for (int i = 2; i <= n; i++) {
        for (int j = 2; j <= m; j++) {
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
        }
    }

    cout << dp[n][m];
    return 0;
}`;

const recurrenceNumberTowerCode = `#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    // a[i][j] 是数塔原始数字，f[i][j] 是从这里走到底的最大和
    vector<vector<long long>> a(n + 1, vector<long long>(n + 2, 0));
    vector<vector<long long>> f(n + 2, vector<long long>(n + 2, 0));

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) {
            cin >> a[i][j];
        }
    }

    for (int j = 1; j <= n; j++) {
        f[n][j] = a[n][j];
    }

    for (int i = n - 1; i >= 1; i--) {
        for (int j = 1; j <= i; j++) {
            f[i][j] = a[i][j] + max(f[i + 1][j], f[i + 1][j + 1]);
        }
    }

    cout << f[1][1];
    return 0;
}`;

const recursionSelfCallCode = `#include <iostream>
using namespace std;

void countdown(int n) {
    // 出口：最小任务已经处理完
    if (n == 0) return;

    cout << n;
    if (n > 1) cout << ' ';

    // 把规模更小的任务交给下一层
    countdown(n - 1);
}

int main() {
    int n;
    cin >> n;
    countdown(n);
    return 0;
}`;

const recursionBaseCaseCode = `#include <iostream>
using namespace std;

void printUp(int n) {
    if (n == 0) return; // 出口必须先判断
    printUp(n - 1);
    if (n > 1) cout << ' ';
    cout << n;
}

int main() {
    int n;
    cin >> n;
    printUp(n);
    return 0;
}`;

const recursionParameterCode = `#include <iostream>
using namespace std;

void printRange(int current, int right) {
    if (current > right) return;
    cout << current;
    if (current < right) cout << ' ';
    printRange(current + 1, right);
}

int main() {
    int left, right;
    cin >> left >> right;
    printRange(left, right);
    return 0;
}`;

const recursionCallStackCode = `#include <iostream>
using namespace std;

long long recursiveSum(int n) {
    if (n == 1) return 1;
    long long child = recursiveSum(n - 1);
    return n + child;
}

int main() {
    int n;
    cin >> n;
    cout << recursiveSum(n);
    return 0;
}`;

const recursionFactorialCode = `#include <iostream>
using namespace std;

long long factorial(int n) {
    if (n <= 1) return 1;
    return 1LL * n * factorial(n - 1);
}

int main() {
    int n;
    cin >> n;
    cout << factorial(n);
    return 0;
}`;

const recursionFibonacciCode = `#include <iostream>
using namespace std;

long long fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main() {
    int n;
    cin >> n;
    cout << fibonacci(n);
    return 0;
}`;

const recursionHanoiCode = `#include <iostream>
using namespace std;

void hanoi(int n, char from, char auxiliary, char to) {
    if (n == 0) return;
    hanoi(n - 1, from, to, auxiliary);
    cout << from << "->" << to << '\\n';
    hanoi(n - 1, auxiliary, from, to);
}

int main() {
    int n;
    cin >> n;
    hanoi(n, 'A', 'B', 'C');
    return 0;
}`;

const recursionTreeTraversalCode = `#include <iostream>
#include <vector>
using namespace std;

vector<int> tree;

void preorder(int index) {
    if (index >= (int)tree.size() || tree[index] == 0) return;
    cout << tree[index] << ' ';
    preorder(index * 2);
    preorder(index * 2 + 1);
}

int main() {
    int n;
    cin >> n;
    tree.resize(n + 1);
    for (int i = 1; i <= n; i++) cin >> tree[i];
    preorder(1);
    return 0;
}`;

const recursionDebugCode = `#include <iostream>
#include <string>
using namespace std;

void trace(int n, int depth) {
    string indent(depth, '-');
    cout << indent << "enter " << n << '\\n';
    if (n > 1) trace(n - 1, depth + 1);
    cout << indent << "leave " << n << '\\n';
}

int main() {
    int n;
    cin >> n;
    trace(n, 0);
    return 0;
}`;

const searchBinaryTreeCode = `#include <iostream>
#include <string>
using namespace std;

int n;
string path;

void dfs(int pos) {
    if (pos == n) {
        cout << path << '\\n';
        return;
    }

    path.push_back('0');
    dfs(pos + 1);
    path.pop_back();

    path.push_back('1');
    dfs(pos + 1);
    path.pop_back();
}

int main() {
    cin >> n;
    dfs(0);
    return 0;
}`;

const recurrenceInitialBoundaryCode = `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    // 数组要覆盖 f[0] 到 f[n]，并给小规模输入留出 f[1]
    vector<long long> f(n + 2, 0);

    // 先把最小状态变成已知
    f[0] = 1;
    f[1] = 1;

    // f[i] 依赖 i - 1 和 i - 2，所以从 i = 2 开始
    for (int i = 2; i <= n; i++) {
        f[i] = f[i - 1] + f[i - 2];
    }

    cout << f[n];
    return 0;
}`;

const searchDfsFrameworkCode = `#include <iostream>
#include <vector>
using namespace std;

int n, m;
vector<int> path;

void dfs(int pos) {
    if (pos == n) {
        for (int i = 0; i < n; i++) {
            if (i) cout << ' ';
            cout << path[i];
        }
        cout << '\\n';
        return;
    }

    for (int choice = 1; choice <= m; choice++) {
        path.push_back(choice);
        dfs(pos + 1);
        path.pop_back();
    }
}

int main() {
    cin >> n >> m;
    dfs(0);
    return 0;
}`;

const searchChooseUndoCode = `#include <iostream>
#include <string>
using namespace std;

int n, k;
string path;

void dfs(int pos, int ones) {
    if (ones > k || ones + (n - pos) < k) return;
    if (pos == n) {
        cout << path << '\\n';
        return;
    }

    path.push_back('0');
    dfs(pos + 1, ones);
    path.pop_back();

    path.push_back('1');
    dfs(pos + 1, ones + 1);
    path.pop_back();
}

int main() {
    cin >> n >> k;
    dfs(0, 0);
    return 0;
}`;

const searchPermutationCode = `#include <iostream>
#include <vector>
using namespace std;

int n;
vector<int> path;
vector<bool> used;

void dfs() {
    if ((int)path.size() == n) {
        for (int i = 0; i < n; i++) {
            if (i) cout << ' ';
            cout << path[i];
        }
        cout << '\\n';
        return;
    }

    for (int value = 1; value <= n; value++) {
        if (used[value]) continue;
        used[value] = true;
        path.push_back(value);
        dfs();
        path.pop_back();
        used[value] = false;
    }
}

int main() {
    cin >> n;
    used.assign(n + 1, false);
    dfs();
    return 0;
}`;

const searchCombinationCode = `#include <iostream>
#include <vector>
using namespace std;

int n, k;
vector<int> path;

void dfs(int start) {
    if ((int)path.size() == k) {
        for (int i = 0; i < k; i++) {
            if (i) cout << ' ';
            cout << path[i];
        }
        cout << '\\n';
        return;
    }

    int need = k - (int)path.size();
    for (int value = start; value <= n - need + 1; value++) {
        path.push_back(value);
        dfs(value + 1);
        path.pop_back();
    }
}

int main() {
    cin >> n >> k;
    dfs(1);
    return 0;
}`;

const searchSubsetCode = `#include <iostream>
#include <vector>
using namespace std;

int n;
vector<int> path;

void dfs(int value) {
    if (value == n + 1) {
        if (path.empty()) {
            cout << "{}";
        } else {
            for (int i = 0; i < (int)path.size(); i++) {
                if (i) cout << ' ';
                cout << path[i];
            }
        }
        cout << '\\n';
        return;
    }

    dfs(value + 1);
    path.push_back(value);
    dfs(value + 1);
    path.pop_back();
}

int main() {
    cin >> n;
    dfs(1);
    return 0;
}`;

const searchMazeCode = `#include <iostream>
#include <string>
#include <vector>
using namespace std;

int n, m;
vector<string> grid;
vector<vector<bool>> visited;
int dx[4] = {1, 0, -1, 0};
int dy[4] = {0, 1, 0, -1};

bool dfs(int x, int y) {
    if (x == n - 1 && y == m - 1) return true;
    visited[x][y] = true;

    for (int dir = 0; dir < 4; dir++) {
        int nx = x + dx[dir];
        int ny = y + dy[dir];
        if (nx < 0 || nx >= n || ny < 0 || ny >= m) continue;
        if (grid[nx][ny] == '#' || visited[nx][ny]) continue;
        if (dfs(nx, ny)) return true;
    }
    return false;
}

int main() {
    cin >> n >> m;
    grid.resize(n);
    for (string& row : grid) cin >> row;
    visited.assign(n, vector<bool>(m, false));

    if (grid[0][0] == '#' || grid[n - 1][m - 1] == '#') {
        cout << "NO";
    } else {
        cout << (dfs(0, 0) ? "YES" : "NO");
    }
    return 0;
}`;

const searchPruningCode = `#include <iostream>
#include <vector>
using namespace std;

int n, target;
long long answer = 0;
vector<int> numbers;
vector<int> suffixSum;

void dfs(int index, int sum) {
    if (sum > target) return;
    if (sum + suffixSum[index] < target) return;
    if (index == n) {
        if (sum == target) answer++;
        return;
    }

    dfs(index + 1, sum);
    dfs(index + 1, sum + numbers[index]);
}

int main() {
    cin >> n >> target;
    numbers.resize(n);
    suffixSum.assign(n + 1, 0);
    for (int& value : numbers) cin >> value;
    for (int i = n - 1; i >= 0; i--) {
        suffixSum[i] = suffixSum[i + 1] + numbers[i];
    }
    dfs(0, 0);
    cout << answer;
    return 0;
}`;

const searchNQueensCode = `#include <iostream>
#include <vector>
using namespace std;

int n;
long long answer = 0;
vector<bool> columnUsed;
vector<bool> diagonalDown;
vector<bool> diagonalUp;

void dfs(int row) {
    if (row == n) {
        answer++;
        return;
    }

    for (int col = 0; col < n; col++) {
        int down = row - col + n - 1;
        int up = row + col;
        if (columnUsed[col] || diagonalDown[down] || diagonalUp[up]) continue;

        columnUsed[col] = diagonalDown[down] = diagonalUp[up] = true;
        dfs(row + 1);
        columnUsed[col] = diagonalDown[down] = diagonalUp[up] = false;
    }
}

int main() {
    cin >> n;
    columnUsed.assign(n, false);
    diagonalDown.assign(2 * n - 1, false);
    diagonalUp.assign(2 * n - 1, false);
    dfs(0);
    cout << answer;
    return 0;
}`;

const searchComplexityCode = `#include <iostream>
using namespace std;

int main() {
    unsigned long long b, d, limit;
    cin >> b >> d >> limit;

    unsigned long long leaves = 1;
    bool withinBudget = true;
    for (unsigned long long level = 0; level < d; level++) {
        if (b != 0 && leaves > limit / b) {
            withinBudget = false;
            break;
        }
        leaves *= b;
        if (leaves > limit) {
            withinBudget = false;
            break;
        }
    }

    cout << (withinBudget ? "YES" : "NO");
    return 0;
}`;

export const chapters: Chapter[] = [
  {
    id: "big-integer",
    order: 1,
    title: "高精度计算",
    subtitle: "把很大的数拆成一位一位处理",
    status: "ready",
    icon: Binary,
    lessons: [
      {
        id: "big-integer-overflow",
        title: "普通整数为什么不够用",
        summary: "普通整型只是容量有限的容器；当输入超过 long long 范围时，必须先用 string 完整保存，再逐位处理。",
        videoUrl: "/videos/big_integer_intro_scenes/1080p60/BigIntegerOverflowVisualization.mp4",
        previewImage: "/previews/big_integer_overflow_preview.png",
        duration: "约 15 秒",
        concepts: ["int 范围", "long long 范围", "溢出", "字符串读入", "逐位处理"],
        steps: [
          "先把 int 和 long long 看成容量有限的盒子，而不是无限大的数字。",
          "遇到超长输入时，不要直接放进整型变量，否则可能溢出。",
          "用 string 读入大整数，可以完整保留每一位字符。",
          "后续高精度运算会把字符串中的字符逐位转成数字。",
        ],
        code: bigIntegerOverflowCode,
        problems: [
          {
            id: "big-integer-type-range",
            title: "判断最小可用整数类型",
            difficulty: "入门",
            focus: "用字符串长度和字典序判断数字是否超出整型范围",
            status: "ready",
            starterCode: bigIntegerOverflowCode,
          },
          {
            id: "big-integer-raw-echo",
            title: "原样读入并输出大整数",
            difficulty: "入门",
            focus: "确认超大整数应先作为 string 保存",
            status: "ready",
            starterCode: `#include <iostream>
#include <string>
using namespace std;

int main() {
    int n;
    cin >> n;
    // TODO: 用 string 逐个读入并原样输出
    return 0;
}`,
          },
          {
            id: "big-integer-overflow-count",
            title: "统计超出 long long 的数字",
            difficulty: "基础",
            focus: "批量比较大整数和 long long 上界",
            status: "ready",
            starterCode: `#include <iostream>
#include <string>
using namespace std;

int compareNumberString(const string& a, const string& b) {
    // TODO: 返回 a 与 b 的大小关系
    return 0;
}

int main() {
    int n;
    cin >> n;
    int count = 0;
    // TODO: 统计大于 9223372036854775807 的输入个数
    cout << count;
    return 0;
}`,
          },
        ],
      },
      {
        id: "big-integer-storage",
        title: "字符串与数组存储大整数",
        summary: "字符串里的每一位是字符，不能直接当数字计算；通过 s[i] - '0' 可以把字符数字转成整数数字，并放入数组。",
        videoUrl: "/videos/big_integer_intro_scenes/1080p60/BigIntegerStorageVisualization.mp4",
        previewImage: "/previews/big_integer_storage_preview.png",
        duration: "约 17 秒",
        concepts: ["string", "字符数字", "s[i] - '0'", "vector<int>", "逐位访问"],
        steps: [
          "用 string 保存大整数，此时每一位仍然是字符。",
          "扫描字符串，使用 s[i] - '0' 把字符数字转换成整数数字。",
          "把转换后的 digit 放入 vector<int>，就能按位置访问每一位。",
          "拆成数组后，可以做各位求和、计数、比较等基础操作。",
        ],
        code: bigIntegerStorageCode,
        problems: [
          {
            id: "big-integer-digit-split",
            title: "把大整数拆成数字",
            difficulty: "入门",
            focus: "把字符串中的字符逐位转换成数字",
            status: "ready",
            starterCode: bigIntegerStorageCode,
          },
          {
            id: "big-integer-digit-sum",
            title: "大整数各位数字和",
            difficulty: "入门",
            focus: "转换成数字后累加每一位",
            status: "ready",
            starterCode: `#include <iostream>
#include <string>
using namespace std;

int main() {
    string s;
    cin >> s;
    int sum = 0;
    // TODO: 累加 s 中每一位数字
    cout << sum;
    return 0;
}`,
          },
          {
            id: "big-integer-digit-frequency",
            title: "统计每个数字出现次数",
            difficulty: "基础",
            focus: "用计数数组记录 0 到 9 的出现次数",
            status: "ready",
            starterCode: `#include <iostream>
#include <string>
using namespace std;

int main() {
    string s;
    cin >> s;
    int cnt[10] = {};
    // TODO: 统计每个数字字符的出现次数
    for (int d = 0; d < 10; d++) {
        if (d) cout << ' ';
        cout << cnt[d];
    }
    return 0;
}`,
          },
        ],
      },
      {
        id: "big-integer-reverse-storage",
        title: "为什么常用反向存储",
        summary: "竖式计算从个位开始；把个位放在 a[0]，循环变量 i 就能自然表示从低到高的第 i 位。",
        videoUrl: "/videos/big_integer_intro_scenes/1080p60/BigIntegerReverseStorageVisualization.mp4",
        previewImage: "/previews/big_integer_reverse_storage_preview.png",
        duration: "约 16 秒",
        concepts: ["反向存储", "个位", "下标 0", "倒序读入", "倒序输出", "缺位补 0"],
        steps: [
          "观察竖式计算：加减乘都从个位开始。",
          "正向数组里个位在最右侧，从低位开始访问时下标会绕。",
          "倒着扫描字符串，把个位先 push_back 到数组中。",
          "内部计算用反向数组，最终输出时再从数组末尾倒着打印。",
        ],
        code: bigIntegerReverseStorageCode,
        problems: [
          {
            id: "big-integer-reverse-store",
            title: "反向存储大整数",
            difficulty: "入门",
            focus: "倒序扫描字符串，把个位放到数组下标 0",
            status: "ready",
            starterCode: bigIntegerReverseStorageCode,
          },
          {
            id: "big-integer-reverse-restore",
            title: "反向数组还原大整数",
            difficulty: "基础",
            focus: "从数组最高位倒序输出正常数字",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    // TODO: 从最高位到最低位输出
    return 0;
}`,
          },
          {
            id: "big-integer-low-position-query",
            title: "查询从低位数的第 k 位",
            difficulty: "基础",
            focus: "理解反向存储时第 k 个低位就是 a[k]",
            status: "ready",
            starterCode: `#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    string s;
    int q;
    cin >> s >> q;
    vector<int> a;
    // TODO: 把 s 反向存入 a，并回答每个 k
    return 0;
}`,
          },
        ],
      },
      {
        id: "big-integer-addition",
        title: "高精度加法",
        summary: "把两个超出普通整数范围的大数拆成反向数组，从个位开始逐位相加，并把进位传给下一位。",
        videoUrl: "/videos/big_integer_addition_scene/1080p60/BigIntegerAdditionVisualization.mp4",
        previewImage: "/previews/big_integer_addition_preview.png",
        duration: "约 1 分钟",
        concepts: ["反向存储", "逐位相加", "carry 进位", "t % 10", "t / 10", "倒序输出"],
        steps: [
          "先用 string 读入大整数，避免普通整型溢出。",
          "把数字反向存入数组，让个位位于下标 0。",
          "第 i 位计算 t = carry + a[i] + b[i]，缺失的一位按 0 处理。",
          "把 t % 10 作为当前结果位，把 t / 10 作为下一位进位。",
          "循环结束后如果 carry 仍然大于 0，就把它加入结果最高位。",
          "结果数组仍然是反向存储，输出时需要从后往前打印。",
        ],
        code: bigIntegerAdditionCode,
        problems: [
          {
            id: "big-integer-add-basic",
            title: "大整数加法",
            difficulty: "入门",
            focus: "用反向数组模拟竖式加法",
            status: "ready",
            starterCode: bigIntegerAdditionCode,
          },
          {
            id: "big-integer-add-trace",
            title: "输出逐位计算轨迹",
            difficulty: "基础",
            focus: "观察每一列的 t、当前位和进位如何产生",
            status: "ready",
            starterCode: `#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    string x, y;
    cin >> x >> y;

    vector<int> a, b, c, trace;
    for (int i = (int)x.size() - 1; i >= 0; i--) a.push_back(x[i] - '0');
    for (int i = (int)y.size() - 1; i >= 0; i--) b.push_back(y[i] - '0');

    int carry = 0;
    int n = max(a.size(), b.size());
    // TODO: 完成逐位相加，并把每一轮的 t 放入 trace

    for (int i = (int)c.size() - 1; i >= 0; i--) cout << c[i];
    cout << '\\n';
    for (int i = 0; i < (int)trace.size(); i++) {
        if (i) cout << ' ';
        cout << trace[i];
    }
    cout << '\\n';
    return 0;
}`,
          },
          {
            id: "big-integer-add-multiple",
            title: "多个大整数求和",
            difficulty: "进阶",
            focus: "把高精度加法封装成函数后反复使用",
            status: "ready",
            starterCode: `#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

vector<int> toDigits(const string& s) {
    vector<int> digits;
    for (int i = (int)s.size() - 1; i >= 0; i--) digits.push_back(s[i] - '0');
    return digits;
}

vector<int> addBigInteger(const vector<int>& a, const vector<int>& b) {
    vector<int> c;
    int carry = 0;
    int n = max(a.size(), b.size());
    // TODO: 返回 a + b 的反向数组结果
    return c;
}

int main() {
    int n;
    cin >> n;
    vector<int> answer(1, 0);

    for (int i = 0; i < n; i++) {
        string s;
        cin >> s;
        // TODO: 把 s 加到 answer 上
    }

    for (int i = (int)answer.size() - 1; i >= 0; i--) cout << answer[i];
    return 0;
}`,
          },
        ],
      },
      {
        id: "big-integer-subtraction",
        title: "高精度减法与借位",
        summary: "在被减数不小于减数的前提下，从个位开始逐位相减；当前位不够减时，用 borrow 标记把借位传给下一位。",
        videoUrl: "/videos/big_integer_subtraction_scene/1080p60/BigIntegerSubtractionVisualization.mp4",
        previewImage: "/previews/big_integer_subtraction_preview.png",
        duration: "约 1 分钟",
        concepts: ["反向存储", "逐位相减", "borrow 借位", "t < 0", "t + 10", "清理前导零"],
        steps: [
          "本课先约定第一个大整数不小于第二个大整数，暂不处理负号。",
          "把两个数字反向存储，让个位位于下标 0。",
          "第 i 位计算 t = a[i] - borrow - b[i]，缺失的一位按 0 处理。",
          "如果 t < 0，说明当前位不够减，把 t 加 10，并令 borrow = 1。",
          "如果 t >= 0，当前位可以直接写入结果，并令 borrow = 0。",
          "结果生成后，从最高位删除多余的 0，但至少保留一个数字 0。",
        ],
        code: bigIntegerSubtractionCode,
        problems: [
          {
            id: "big-integer-sub-basic",
            title: "大整数减法",
            difficulty: "入门",
            focus: "用 borrow 标记模拟竖式借位",
            status: "ready",
            starterCode: bigIntegerSubtractionCode,
          },
          {
            id: "big-integer-sub-borrow-count",
            title: "统计借位次数",
            difficulty: "基础",
            focus: "看清每一次 t < 0 对应一次借位",
            status: "ready",
            starterCode: `#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    string x, y;
    cin >> x >> y; // 保证 x >= y

    vector<int> a, b, c;
    for (int i = (int)x.size() - 1; i >= 0; i--) a.push_back(x[i] - '0');
    for (int i = (int)y.size() - 1; i >= 0; i--) b.push_back(y[i] - '0');

    int borrow = 0;
    int borrowCount = 0;
    // TODO: 完成高精度减法，并统计 t < 0 的次数

    while (c.size() > 1 && c.back() == 0) c.pop_back();
    for (int i = (int)c.size() - 1; i >= 0; i--) cout << c[i];
    cout << '\\n' << borrowCount << '\\n';
    return 0;
}`,
          },
          {
            id: "big-integer-sub-ledger",
            title: "连续扣款",
            difficulty: "进阶",
            focus: "把高精度减法封装成函数后反复使用",
            status: "ready",
            starterCode: `#include <iostream>
#include <string>
#include <vector>
using namespace std;

vector<int> toDigits(const string& s) {
    vector<int> digits;
    for (int i = (int)s.size() - 1; i >= 0; i--) digits.push_back(s[i] - '0');
    return digits;
}

vector<int> subtractBigInteger(const vector<int>& a, const vector<int>& b) {
    vector<int> c;
    int borrow = 0;
    // TODO: 返回 a - b 的反向数组结果，保证 a >= b
    return c;
}

int main() {
    string balance;
    int n;
    cin >> balance >> n;

    vector<int> answer = toDigits(balance);
    for (int i = 0; i < n; i++) {
        string cost;
        cin >> cost;
        // TODO: 从 answer 中扣除 cost
    }

    for (int i = (int)answer.size() - 1; i >= 0; i--) cout << answer[i];
    return 0;
}`,
          },
        ],
      },
      {
        id: "big-integer-compare-sign",
        title: "大数比较与符号处理",
        summary: "减法前先比较两个非负大整数的大小；如果被减数更小，就交换绝对值减法的顺序，并在答案前补上负号。",
        videoUrl: "/videos/big_integer_compare_scene/1080p60/BigIntegerCompareVisualization.mp4",
        previewImage: "/previews/big_integer_compare_preview.png",
        duration: "约 1 分钟",
        concepts: ["长度比较", "最高位比较", "cmp 函数", "负号标记", "交换操作数", "复用绝对值减法"],
        steps: [
          "先比较两个字符串长度，长度更长的非负整数更大。",
          "如果长度相同，就从最高位开始逐个字符比较，第一处不同决定大小。",
          "当 x == y 时，结果直接输出 0，不需要进入减法流程。",
          "当 x < y 时，先交换 x 和 y，再记录 negative = true。",
          "对较大的绝对值减去较小的绝对值，复用上一课的 subtractAbs 函数。",
          "输出时如果 negative 为 true，就先输出负号，再输出差值。",
        ],
        code: bigIntegerCompareCode,
        problems: [
          {
            id: "big-integer-compare",
            title: "比较两个大整数",
            difficulty: "入门",
            focus: "用长度和最高位顺序判断大整数大小",
            status: "ready",
            starterCode: `#include <iostream>
#include <string>
using namespace std;

int compareBigInteger(const string& a, const string& b) {
    // TODO: 如果 a > b 返回 1，a < b 返回 -1，相等返回 0
    return 0;
}

int main() {
    string a, b;
    cin >> a >> b;

    int result = compareBigInteger(a, b);
    if (result > 0) cout << ">" << '\\n';
    else if (result < 0) cout << "<" << '\\n';
    else cout << "=" << '\\n';
    return 0;
}`,
          },
          {
            id: "big-integer-sub-signed",
            title: "任意两个大整数相减",
            difficulty: "基础",
            focus: "先比较大小，再决定是否输出负号",
            status: "ready",
            starterCode: bigIntegerCompareCode,
          },
          {
            id: "big-integer-sub-sign-batch",
            title: "多组带符号差值",
            difficulty: "进阶",
            focus: "把比较和绝对值减法封装成可复用函数",
            status: "ready",
            starterCode: `#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int compareBigInteger(const string& a, const string& b) {
    // TODO: 返回 1、0、-1 表示 a 与 b 的大小关系
    return 0;
}

string subtractSigned(string a, string b) {
    // TODO: 返回 a - b 的带符号字符串
    return "0";
}

int main() {
    int q;
    cin >> q;
    while (q--) {
        string a, b;
        cin >> a >> b;
        cout << subtractSigned(a, b) << '\\n';
    }
    return 0;
}`,
          },
        ],
      },
      {
        id: "big-integer-multiply-small",
        title: "高精度乘低精度",
        summary: "把一个大整数按位拆开，与一个普通整数 b 相乘；每一位计算 a[i] * b + carry，当前位留下个位，其余继续作为进位。",
        videoUrl: "/videos/big_integer_multiply_small_scene/1080p60/BigIntegerMultiplySmallVisualization.mp4",
        previewImage: "/previews/big_integer_multiply_small_preview.png",
        duration: "约 1 分钟",
        concepts: ["反向存储", "逐位相乘", "小整数 b", "carry 连续进位", "t % 10", "拆分剩余进位"],
        steps: [
          "仍然用 string 读入大整数，并把它反向存入数组。",
          "小整数 b 不需要拆成数组，直接作为一个普通变量参与计算。",
          "第 i 位计算 t = a[i] * b + carry，注意 t 可能远大于 9。",
          "把 t % 10 写入结果数组当前位，把 t / 10 留给下一位作为新进位。",
          "主循环结束后，如果 carry 仍然大于 0，就用 while(carry) 把它继续拆成十进制数字。",
          "最后清理多余前导零，并倒序输出结果数组。",
        ],
        code: bigIntegerMultiplySmallCode,
        problems: [
          {
            id: "big-integer-mul-small-basic",
            title: "大整数乘小整数",
            difficulty: "入门",
            focus: "用 carry 模拟竖式乘法中的连续进位",
            status: "ready",
            starterCode: bigIntegerMultiplySmallCode,
          },
          {
            id: "big-integer-mul-small-trace",
            title: "输出乘法进位轨迹",
            difficulty: "基础",
            focus: "观察每一轮的 t 如何决定当前位和下一轮进位",
            status: "ready",
            starterCode: `#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    string x;
    int b;
    cin >> x >> b;

    vector<int> a, c;
    vector<long long> trace;
    for (int i = (int)x.size() - 1; i >= 0; i--) a.push_back(x[i] - '0');

    long long carry = 0;
    // TODO: 完成高精度乘低精度，并把主循环每一轮的 t 放入 trace

    while (c.size() > 1 && c.back() == 0) c.pop_back();
    for (int i = (int)c.size() - 1; i >= 0; i--) cout << c[i];
    cout << '\\n';
    for (int i = 0; i < (int)trace.size(); i++) {
        if (i) cout << ' ';
        cout << trace[i];
    }
    cout << '\\n';
    return 0;
}`,
          },
          {
            id: "big-integer-factorial-small",
            title: "高精度阶乘",
            difficulty: "进阶",
            focus: "把乘低精度封装成函数，在循环中反复更新答案",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

vector<int> multiplyBigInteger(const vector<int>& a, int b) {
    vector<int> c;
    long long carry = 0;
    // TODO: 返回 a * b 的反向数组结果
    return c;
}

int main() {
    int n;
    cin >> n;

    vector<int> answer(1, 1);
    for (int i = 2; i <= n; i++) {
        // TODO: answer = answer * i
    }

    for (int i = (int)answer.size() - 1; i >= 0; i--) cout << answer[i];
    return 0;
}`,
          },
        ],
      },
      {
        id: "big-integer-multiply-big",
        title: "高精度乘高精度",
        summary: "把两个大整数都拆成反向数组，用双重循环枚举每一对数字；a[i] 与 b[j] 的乘积会贡献到 c[i+j]，全部累加后再统一处理进位。",
        videoUrl: "/videos/big_integer_multiply_big_scene/1080p60/BigIntegerMultiplyBigVisualization.mp4",
        previewImage: "/previews/big_integer_multiply_big_preview.png",
        duration: "约 1 分钟",
        concepts: ["反向存储", "乘法网格", "双重循环", "c[i+j]", "贡献累加", "统一进位", "清理前导零"],
        steps: [
          "先把两个输入字符串都反向存入数组，让下标 0 对应个位。",
          "准备长度为 a.size() + b.size() 的结果数组 c，初始全部为 0。",
          "双重循环枚举 i 和 j，把 a[i] * b[j] 累加到 c[i+j]。",
          "第一阶段只负责累加贡献，暂时允许 c 的某些位置大于 9。",
          "第二阶段从低位到高位统一处理进位：c[i+1] += c[i] / 10，c[i] %= 10。",
          "最后删除多余前导零，并倒序输出结果数组。",
        ],
        code: bigIntegerMultiplyBigCode,
        problems: [
          {
            id: "big-integer-mul-big-basic",
            title: "大整数乘大整数",
            difficulty: "入门",
            focus: "用 c[i+j] 记录每一对数字乘积的贡献",
            status: "ready",
            starterCode: bigIntegerMultiplyBigCode,
          },
          {
            id: "big-integer-mul-big-grid-trace",
            title: "输出乘法网格累加",
            difficulty: "基础",
            focus: "观察统一进位之前，每个结果格子收到了哪些贡献",
            status: "ready",
            starterCode: `#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    string x, y;
    cin >> x >> y;

    vector<int> a, b;
    for (int i = (int)x.size() - 1; i >= 0; i--) a.push_back(x[i] - '0');
    for (int i = (int)y.size() - 1; i >= 0; i--) b.push_back(y[i] - '0');

    vector<int> raw(a.size() + b.size(), 0);
    // TODO: 双重循环，把 a[i] * b[j] 累加到 raw[i + j]

    vector<int> c = raw;
    // TODO: 对 c 统一处理进位，并清理前导零

    for (int i = (int)c.size() - 1; i >= 0; i--) cout << c[i];
    cout << '\\n';
    for (int i = 0; i < (int)raw.size(); i++) {
        if (i) cout << ' ';
        cout << raw[i];
    }
    cout << '\\n';
    return 0;
}`,
          },
          {
            id: "big-integer-power-small",
            title: "大整数的小指数幂",
            difficulty: "进阶",
            focus: "复用高精度乘高精度函数，反复更新答案",
            status: "ready",
            starterCode: `#include <iostream>
#include <string>
#include <vector>
using namespace std;

vector<int> multiplyBigInteger(const vector<int>& a, const vector<int>& b) {
    vector<int> c(a.size() + b.size(), 0);
    // TODO: 完成高精度乘高精度，并返回反向数组结果
    return c;
}

int main() {
    string x;
    int n;
    cin >> x >> n;

    vector<int> base, answer(1, 1);
    for (int i = (int)x.size() - 1; i >= 0; i--) base.push_back(x[i] - '0');

    // TODO: 循环 n 次，把 answer 乘上 base

    for (int i = (int)answer.size() - 1; i >= 0; i--) cout << answer[i];
    return 0;
}`,
          },
        ],
      },
      {
        id: "big-integer-divide-small",
        title: "高精度除低精度",
        summary: "像手算长除法一样，从大整数最高位开始向右扫描；每次让旧余数乘 10 加上当前位，写出一位商，再保留新的余数。",
        videoUrl: "/videos/big_integer_divide_small_scene/1080p60/BigIntegerDivideSmallVisualization.mp4",
        previewImage: "/previews/big_integer_divide_small_preview.png",
        duration: "约 1 分钟",
        concepts: ["正常顺序扫描", "长除法", "余数 r", "r*10+digit", "商的一位", "清理商前导零"],
        steps: [
          "除法从最高位开始处理，所以输入字符串可以保持正常顺序扫描。",
          "维护一个余数 r，初始为 0，它代表前面还没有除尽的部分。",
          "每读入一位 digit，就计算 r = r * 10 + digit，相当于手算时“落下一位”。",
          "当前商的一位是 r / b，把它追加到商字符串末尾。",
          "新的余数是 r % b，它会带到下一位继续参与计算。",
          "扫描结束后，删除商最前面多余的 0；如果整商为 0，则保留一个 0。",
        ],
        code: bigIntegerDivideSmallCode,
        problems: [
          {
            id: "big-integer-div-small-basic",
            title: "大整数除小整数",
            difficulty: "入门",
            focus: "从高位到低位维护余数并输出商",
            status: "ready",
            starterCode: bigIntegerDivideSmallCode,
          },
          {
            id: "big-integer-div-small-quot-rem",
            title: "输出商和余数",
            difficulty: "基础",
            focus: "同时掌握 r / b 写商、r % b 留余数",
            status: "ready",
            starterCode: `#include <iostream>
#include <string>
using namespace std;

int main() {
    string a;
    int b;
    cin >> a >> b;

    string q;
    long long r = 0;
    // TODO: 从左到右扫描 a，完成高精度除低精度

    int start = 0;
    // TODO: 删除 q 的多余前导零，但至少保留一位

    cout << q.substr(start) << '\\n' << r << '\\n';
    return 0;
}`,
          },
          {
            id: "big-integer-div-small-trace",
            title: "输出长除法轨迹",
            difficulty: "进阶",
            focus: "记录每次落下一位后，除法发生前的临时余数",
            status: "ready",
            starterCode: `#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    string a;
    int b;
    cin >> a >> b;

    string q;
    vector<long long> trace;
    long long r = 0;
    // TODO: 每次计算 r = r * 10 + digit 后，先把 r 放入 trace，再写商并更新余数

    int start = 0;
    while (start + 1 < (int)q.size() && q[start] == '0') start++;

    cout << q.substr(start) << '\\n' << r << '\\n';
    for (int i = 0; i < (int)trace.size(); i++) {
        if (i) cout << ' ';
        cout << trace[i];
    }
    cout << '\\n';
    return 0;
}`,
          },
        ],
      },
      {
        id: "big-integer-leading-zero-normalization",
        title: "前导零与边界整理",
        summary: "高精度计算结束后，要删除结果最高位多余的 0；但如果整个结果就是 0，必须保留一个 0，避免输出空答案。",
        videoUrl: "/videos/leading_zero_normalization_scene/1080p60/LeadingZeroNormalizationVisualization.mp4",
        previewImage: "/previews/leading_zero_normalization_preview.png",
        duration: "约 1 分钟",
        concepts: ["结果规范化", "前导零", "c.back()", "pop_back", "保留一个 0", "边界测试"],
        steps: [
          "倒序数组里，下标越大代表数位越高，所以多余的前导零通常出现在 c.back()。",
          "只要 c.size() > 1 并且 c.back() == 0，就可以删除最高位 0。",
          "条件里的 c.size() > 1 很重要，它保证数字 0 不会被删成空数组。",
          "除法得到的商字符串是正常顺序，要从左侧跳过多余的 0。",
          "如果整串都是 0，也只能跳到最后一个字符之前，最终输出一个 0。",
          "每个高精度函数返回前，都应该做一次 normalize，并用 0、相等相减、小数除大数等边界数据测试。",
        ],
        code: bigIntegerNormalizeCode,
        problems: [
          {
            id: "big-integer-normalize-array",
            title: "整理倒序结果数组",
            difficulty: "入门",
            focus: "用 c.back() 和 pop_back 删除最高位多余 0",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> c(n);
    for (int i = 0; i < n; i++) cin >> c[i];

    // TODO: 删除倒序数组最高位的多余 0，但至少保留一个数字

    cout << c.size() << '\\n';
    for (int i = 0; i < (int)c.size(); i++) {
        if (i) cout << ' ';
        cout << c[i];
    }
    cout << '\\n';
    return 0;
}`,
          },
          {
            id: "big-integer-trim-string",
            title: "整理商字符串",
            difficulty: "基础",
            focus: "从左到右跳过前导零，同时保留 0 本身",
            status: "ready",
            starterCode: `#include <iostream>
#include <string>
using namespace std;

int main() {
    string q;
    cin >> q;

    int start = 0;
    // TODO: 让 start 跳过多余前导零，但不要越过最后一个字符

    cout << q.substr(start) << '\\n';
    return 0;
}`,
          },
          {
            id: "big-integer-normalized-calculator",
            title: "边界结果计算器",
            difficulty: "进阶",
            focus: "在加、减、乘、除的结果返回前统一做规范化",
            status: "ready",
            starterCode: `#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

vector<int> toDigits(const string& s) {
    vector<int> digits;
    for (int i = (int)s.size() - 1; i >= 0; i--) digits.push_back(s[i] - '0');
    return digits;
}

void normalize(vector<int>& c) {
    // TODO: 删除倒序数组的多余最高位 0
}

string toString(const vector<int>& c) {
    string answer;
    for (int i = (int)c.size() - 1; i >= 0; i--) answer.push_back(char('0' + c[i]));
    return answer;
}

int main() {
    int q;
    cin >> q;
    while (q--) {
        string op, a, b;
        cin >> op >> a >> b;
        // TODO: 支持 add、sub、mul_small、div_small，并输出规范结果
    }
    return 0;
}`,
          },
        ],
      },
      {
        id: "big-integer-composite-factorial-fibonacci",
        title: "高精度综合：阶乘与 Fibonacci",
        summary: "把已经封装好的高精度加法、乘低精度函数放进循环和递推中：阶乘不断乘上下一个整数，Fibonacci 不断用 a + b 生成下一项。",
        videoUrl: "/videos/big_integer_composite_scene/1080p60/BigIntegerCompositeVisualization.mp4",
        previewImage: "/previews/big_integer_composite_preview.png",
        duration: "约 1 分钟",
        concepts: ["函数封装", "循环外壳", "阶乘", "Fibonacci 递推", "状态更新", "复用高精度函数"],
        steps: [
          "先把高精度加法、乘低精度封装成独立函数，让主流程只关心调用时机。",
          "计算 n! 时，维护 answer，循环 i = 2 到 n，每一轮执行 answer = multiplySmall(answer, i)。",
          "answer 的位数会逐渐增长，但外层循环不需要知道进位细节，这些都交给高精度函数完成。",
          "计算 Fibonacci 时，维护两个状态 a 和 b，分别代表相邻两项。",
          "每一轮先算 c = addBigInteger(a, b)，再整体前移：a = b，b = c。",
          "这类综合题的关键不是写更复杂的进位，而是让函数、循环、状态更新配合得清楚可靠。",
        ],
        code: bigIntegerCompositeCode,
        problems: [
          {
            id: "big-integer-factorial-small",
            title: "高精度阶乘",
            difficulty: "入门",
            focus: "复用高精度乘低精度函数，在循环中不断更新 answer",
            status: "ready",
            starterCode: bigIntegerCompositeCode,
          },
          {
            id: "big-integer-fibonacci",
            title: "高精度 Fibonacci",
            difficulty: "基础",
            focus: "用高精度加法完成 a、b、c 三个状态的递推更新",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

vector<int> addBigInteger(const vector<int>& a, const vector<int>& b) {
    vector<int> c;
    int carry = 0;
    // TODO: 返回 a + b 的倒序数组结果
    return c;
}

int main() {
    int n;
    cin >> n;

    vector<int> a(1, 0), b(1, 1);
    // TODO: 如果 n 为 0，输出 0；否则用 a、b 滚动求出第 n 项

    for (int i = (int)b.size() - 1; i >= 0; i--) cout << b[i];
    return 0;
}`,
          },
          {
            id: "big-integer-factorial-sum",
            title: "阶乘和",
            difficulty: "进阶",
            focus: "同时复用高精度乘低精度和高精度加法，累加 1! + 2! + ... + n!",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

vector<int> addBigInteger(const vector<int>& a, const vector<int>& b) {
    vector<int> c;
    // TODO: 返回 a + b
    return c;
}

vector<int> multiplySmall(const vector<int>& a, int b) {
    vector<int> c;
    // TODO: 返回 a * b
    return c;
}

int main() {
    int n;
    cin >> n;

    vector<int> fact(1, 1), sum(1, 0);
    // TODO: 从 1! 到 n!，一边更新 fact，一边累加到 sum

    for (int i = (int)sum.size() - 1; i >= 0; i--) cout << sum[i];
    return 0;
}`,
          },
        ],
      },
    ],
  },
  {
    id: "sorting",
    order: 2,
    title: "数据排序",
    subtitle: "观察比较、交换、插入与合并",
    status: "ready",
    icon: SortAsc,
    lessons: [
      {
        id: "bubble-sort",
        title: "冒泡排序",
        summary: "从左到右比较相邻元素，必要时交换；每一轮把当前最大值推到右侧。",
        videoUrl: "/videos/bubble_sort_scene/1080p60/BubbleSortVisualization.mp4",
        previewImage: "/previews/bubble_sort_preview.png",
        duration: "约 37 秒",
        concepts: ["相邻比较", "交换", "已排序区", "提前结束优化", "O(n²)"],
        steps: [
          "先观察每次只比较相邻两个元素。",
          "如果左边更大，就让它和右边交换位置。",
          "一轮结束后，当前最大值会停在最右侧的最终位置。",
          "如果某一轮没有交换，说明数组已经有序，可以提前停止。",
        ],
        code: bubbleSortCode,
        problems: [
          {
            id: "bubble-sort-basic",
            title: "手写冒泡排序",
            difficulty: "入门",
            focus: "双重循环与相邻交换",
            status: "ready",
            starterCode: bubbleSortCode,
          },
          {
            id: "bubble-sort-count",
            title: "统计交换次数",
            difficulty: "基础",
            focus: "理解每一次交换发生的原因",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    int swaps = 0;
    // TODO: 完成冒泡排序，并在每次交换时让 swaps++

    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << a[i];
    }
    cout << '\\n' << swaps << '\\n';
    return 0;
}`,
          },
          {
            id: "bubble-sort-flag",
            title: "提前结束优化",
            difficulty: "进阶",
            focus: "用 changed 标记识别已经有序",
            status: "ready",
            starterCode: bubbleSortCode,
          },
        ],
      },
      {
        id: "selection-sort",
        title: "选择排序",
        summary: "每一轮从未排序区找出最小值，把它放到当前最左侧的位置，逐步扩张已排序区。",
        videoUrl: "/videos/selection_sort_scene/1080p60/SelectionSortVisualization.mp4",
        previewImage: "/previews/selection_sort_preview.png",
        duration: "约 37 秒",
        concepts: ["最小值下标", "未排序区", "选择后交换", "不稳定性", "O(n²)"],
        steps: [
          "把数组分成左侧已排序区和右侧未排序区。",
          "每一轮先假设未排序区第一个元素最小。",
          "用 j 指针向右扫描，遇到更小的值就更新 minIndex。",
          "扫描结束后，把最小值交换到当前轮的起点 i。",
          "i 向右移动一格，已排序区扩大。",
        ],
        code: selectionSortCode,
        problems: [
          {
            id: "selection-sort-basic",
            title: "手写选择排序",
            difficulty: "入门",
            focus: "维护 minIndex 并在每轮结束后交换",
            status: "ready",
            starterCode: selectionSortCode,
          },
          {
            id: "selection-sort-trace",
            title: "记录每轮最小值下标",
            difficulty: "基础",
            focus: "看懂 minIndex 如何随着扫描变化",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    vector<int> chosen;
    // TODO: 完成选择排序，并把每一轮最终选中的 minIndex 放入 chosen

    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << a[i];
    }
    cout << '\\n';
    for (int i = 0; i < (int)chosen.size(); i++) {
        if (i) cout << ' ';
        cout << chosen[i];
    }
    cout << '\\n';
    return 0;
}`,
          },
          {
            id: "selection-sort-desc",
            title: "选择排序降序版",
            difficulty: "进阶",
            focus: "把选择最小值改造成选择最大值",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    // TODO: 每一轮选择未排序区的最大值，放到当前位置

    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << a[i];
    }
    return 0;
}`,
          },
        ],
      },
      {
        id: "insertion-sort",
        title: "插入排序",
        summary: "把当前元素当作 key，向左寻找插入位置；比 key 大的元素依次右移，最后把 key 放回空位。",
        videoUrl: "/videos/insertion_sort_scene/1080p60/InsertionSortVisualization.mp4",
        previewImage: "/previews/insertion_sort_preview.png",
        duration: "约 32 秒",
        concepts: ["key", "向右移动", "插入位置", "稳定排序", "O(n²)"],
        steps: [
          "左侧区间始终保持有序。",
          "每一轮取出当前位置 i 的元素作为 key。",
          "从 i - 1 向左比较，如果元素比 key 大，就向右移动一格。",
          "当遇到不大于 key 的元素，或已经到达数组开头，就找到了插入位置。",
          "把 key 放入空出来的位置，已排序区扩大一格。",
        ],
        code: insertionSortCode,
        problems: [
          {
            id: "insertion-sort-basic",
            title: "手写插入排序",
            difficulty: "入门",
            focus: "取出 key、右移元素、放回 key",
            status: "ready",
            starterCode: insertionSortCode,
          },
          {
            id: "insertion-sort-shifts",
            title: "统计右移次数",
            difficulty: "基础",
            focus: "理解每次腾位置对应的一次移动",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    int shifts = 0;
    // TODO: 完成插入排序，并在每次 a[j + 1] = a[j] 时让 shifts++

    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << a[i];
    }
    cout << '\\n' << shifts << '\\n';
    return 0;
}`,
          },
          {
            id: "insertion-sort-desc",
            title: "插入排序降序版",
            difficulty: "进阶",
            focus: "把升序插入条件改造成降序插入",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    // TODO: 使用插入排序输出从大到小的结果

    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << a[i];
    }
    return 0;
}`,
          },
        ],
      },
      {
        id: "counting-sort",
        title: "计数排序",
        summary: "当数值范围不大时，不再反复比较元素；用 count 桶记录每个值出现几次，再按值从小到大展开。",
        videoUrl: "/videos/counting_sort_scene/1080p60/CountingSortVisualization.mp4",
        previewImage: "/previews/counting_sort_preview.png",
        duration: "约 28 秒",
        concepts: ["计数桶", "值域 K", "下标映射", "按桶展开", "O(n + K)"],
        steps: [
          "先确认数据可以映射到数组下标，通常从非负整数小范围开始。",
          "建立 count 数组，count[x] 表示数值 x 出现了多少次。",
          "从左到右扫描原数组，遇到 x 就让 count[x]++。",
          "统计完成后，从小到大枚举 value，把 value 输出 count[value] 次。",
          "如果数据里有负数，可以用 offset 把真实值平移到非负下标。",
        ],
        code: countingSortCode,
        problems: [
          {
            id: "counting-sort-basic",
            title: "小值域计数排序",
            difficulty: "入门",
            focus: "用 count[x]++ 统计出现次数",
            status: "ready",
            starterCode: countingSortCode,
          },
          {
            id: "counting-sort-frequency",
            title: "输出频率表",
            difficulty: "基础",
            focus: "理解 count 数组每一格的含义",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<int> count(m + 1, 0);

    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        // TODO: 统计 x 出现的次数
    }

    for (int value = 0; value <= m; value++) {
        if (value) cout << ' ';
        cout << count[value];
    }
    return 0;
}`,
          },
          {
            id: "counting-sort-offset",
            title: "带负数的计数排序",
            difficulty: "进阶",
            focus: "用 value - minValue 把真实值映射到下标",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    int minValue = 1000000;
    int maxValue = -1000000;

    for (int i = 0; i < n; i++) {
        cin >> a[i];
        minValue = min(minValue, a[i]);
        maxValue = max(maxValue, a[i]);
    }

    // TODO: 创建大小为 maxValue - minValue + 1 的 count 数组
    // TODO: 用 a[i] - minValue 作为下标统计次数
    // TODO: 从 minValue 到 maxValue 还原有序结果

    return 0;
}`,
          },
        ],
      },
      {
        id: "merge-sort",
        title: "归并排序",
        summary: "把数组递归拆成更小的有序段，再用双指针稳定合并；它是理解分治思想最清晰的一扇门。",
        videoUrl: "/videos/merge_sort_scene/1080p60/MergeSortVisualization.mp4",
        previewImage: "/previews/merge_sort_preview.png",
        duration: "约 26 秒",
        concepts: ["分治", "递归拆分", "双指针合并", "稳定排序", "O(n log n)"],
        steps: [
          "先把区间 [left, right] 从中间切开，分别处理左半段和右半段。",
          "当区间只剩一个元素时，它天然有序，可以作为递归出口。",
          "合并两个已经有序的子数组时，使用 i 和 j 指向左右两段的当前元素。",
          "每次把更小的元素写入临时数组 temp；若相等，优先取左段元素以保持稳定性。",
          "合并完成后，把 temp 中的结果复制回原数组对应区间。",
        ],
        code: mergeSortCode,
        problems: [
          {
            id: "merge-sort-basic",
            title: "手写归并排序",
            difficulty: "基础",
            focus: "递归拆分与有序合并",
            status: "ready",
            starterCode: mergeSortCode,
          },
          {
            id: "merge-two-sorted-arrays",
            title: "合并两个有序数组",
            difficulty: "入门",
            focus: "掌握归并过程中的双指针",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<int> a(n), b(m);
    for (int i = 0; i < n; i++) cin >> a[i];
    for (int i = 0; i < m; i++) cin >> b[i];

    vector<int> result;
    int i = 0;
    int j = 0;
    // TODO: 用双指针把两个有序数组合并到 result

    for (int k = 0; k < (int)result.size(); k++) {
        if (k) cout << ' ';
        cout << result[k];
    }
    return 0;
}`,
          },
          {
            id: "merge-sort-inversions",
            title: "归并排序数逆序对",
            difficulty: "进阶",
            focus: "在合并时统计右侧元素跨过左侧元素的次数",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

long long mergeSort(vector<int>& a, int left, int right, vector<int>& temp) {
    if (left >= right) return 0;

    int mid = (left + right) / 2;
    long long answer = 0;
    answer += mergeSort(a, left, mid, temp);
    answer += mergeSort(a, mid + 1, right, temp);

    int i = left;
    int j = mid + 1;
    int k = left;
    // TODO: 合并两个有序段，并统计逆序对数量

    for (int p = left; p <= right; p++) {
        a[p] = temp[p];
    }
    return answer;
}

int main() {
    int n;
    cin >> n;
    vector<int> a(n), temp(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    cout << mergeSort(a, 0, n - 1, temp);
    return 0;
}`,
          },
        ],
      },
      {
        id: "quick-sort",
        title: "快速排序初步",
        summary: "选择一个基准值 pivot，通过一次分区把数组分成左右两部分，再递归处理；它把“分而治之”变成了非常有动作感的过程。",
        videoUrl: "/videos/quick_sort_scene/1080p60/QuickSortVisualization.mp4",
        previewImage: "/previews/quick_sort_preview.png",
        duration: "约 24 秒",
        concepts: ["pivot", "分区", "双指针边界", "递归", "平均 O(n log n)"],
        steps: [
          "选择一个基准值 pivot，入门版本可以先使用当前区间最后一个元素。",
          "用 j 从左到右扫描，用 i 维护小于等于 pivot 的区域边界。",
          "当 a[j] <= pivot 时，先让 i 右移，再交换 a[i] 和 a[j]。",
          "扫描结束后，把 pivot 交换到 i + 1 的位置，此时 pivot 左边都不大于它，右边都大于它。",
          "对 pivot 左右两侧继续递归排序，直到区间长度小于等于 1。",
        ],
        code: quickSortCode,
        problems: [
          {
            id: "quick-sort-basic",
            title: "手写快速排序",
            difficulty: "基础",
            focus: "partition 返回基准值的最终位置",
            status: "ready",
            starterCode: quickSortCode,
          },
          {
            id: "quick-sort-partition",
            title: "完成一次分区",
            difficulty: "入门",
            focus: "观察 i、j 和 pivot 如何改变数组结构",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int partition(vector<int>& a, int left, int right) {
    int pivot = a[right];
    int i = left - 1;

    for (int j = left; j < right; j++) {
        // TODO: 如果 a[j] <= pivot，就扩大小区间并交换
    }

    // TODO: 把 pivot 放到最终位置，并返回这个位置
    return -1;
}

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    int pos = partition(a, 0, n - 1);
    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << a[i];
    }
    cout << '\\n' << pos << '\\n';
    return 0;
}`,
          },
          {
            id: "quick-select-kth",
            title: "快速选择第 k 小",
            difficulty: "进阶",
            focus: "只递归进入包含答案的一侧",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int partition(vector<int>& a, int left, int right) {
    int pivot = a[right];
    int i = left - 1;
    for (int j = left; j < right; j++) {
        if (a[j] <= pivot) {
            i++;
            swap(a[i], a[j]);
        }
    }
    swap(a[i + 1], a[right]);
    return i + 1;
}

int quickSelect(vector<int>& a, int left, int right, int target) {
    // TODO: target 是 0-based 下标，只递归进入包含 target 的一侧
    return a[target];
}

int main() {
    int n, k;
    cin >> n >> k;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    cout << quickSelect(a, 0, n - 1, k - 1);
    return 0;
}`,
          },
        ],
      },
    ],
  },
  {
    id: "recurrence",
    order: 3,
    title: "递推算法",
    subtitle: "用已知状态推出下一个状态",
    status: "building",
    icon: Repeat2,
    lessons: [
      {
        id: "recurrence-state-definition",
        title: "什么是状态",
        summary: "用爬楼梯问题把“状态”看成一张记录进度的表：先说清 f[i] 记录什么，再决定初始格和答案格。",
        videoUrl: "/videos/state_definition_scene/1080p60/RecurrenceStateVisualization.mp4",
        previewImage: "/previews/recurrence_state_preview.png",
        duration: "约 30 秒",
        concepts: ["状态定义", "问题进度", "f[i] 含义", "状态表", "初始化", "答案位置"],
        steps: [
          "先观察原问题：走到第 n 阶有多少种方法？只看终点时缺少中间记录。",
          "把终点拆成每一个位置：第 0 阶、第 1 阶、第 2 阶……直到第 i 阶。",
          "给每个位置一个记录盒子，用 f[i] 表示“走到第 i 阶的方法数”。",
          "把“问全部”变成“问每个位置”，让状态表中的每个格子负责一个小问题。",
          "先写清状态含义，再补初始条件，例如 f[0] = 1、f[1] = 1。",
          "最后确认答案在哪个格子：走到第 n 阶的方法数就是 f[n]。",
        ],
        code: recurrenceStateCode,
        problems: [
          {
            id: "recurrence-climb-stairs-basic",
            title: "爬楼梯方法数",
            difficulty: "入门",
            focus: "用 f[i] 表示走到第 i 阶的方法数，并输出 f[n]",
            status: "ready",
            starterCode: recurrenceStateCode,
          },
          {
            id: "recurrence-state-table",
            title: "输出状态表",
            difficulty: "基础",
            focus: "按顺序填出 f[0] 到 f[n]，观察状态表怎样增长",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    // f[i] 表示走到第 i 阶的方法数
    vector<long long> f(n + 2, 0);
    f[0] = 1;
    f[1] = 1;

    // TODO: 从 i = 2 开始填表

    for (int i = 0; i <= n; i++) {
        if (i) cout << ' ';
        cout << f[i];
    }
    return 0;
}`,
          },
          {
            id: "recurrence-domino-tiling",
            title: "2 x n 骨牌覆盖",
            difficulty: "进阶",
            focus: "把不同题目翻译成同一种状态表：f[i] 表示覆盖 2 x i 矩形的方法数",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    // f[i] 表示覆盖 2 x i 矩形的方法数
    vector<long long> f(n + 2, 0);
    f[0] = 1;
    f[1] = 1;

    // TODO: 想清楚最后一列竖放、最后两列横放分别对应哪些旧状态

    cout << f[n];
    return 0;
}`,
          },
        ],
      },
      {
        id: "recurrence-known-to-unknown",
        title: "从已知推出未知",
        summary: "从 f[1]、f[2] 两个已知起点出发，用依赖箭头推出第一个未知格，再让已知区一格一格向右扩展。",
        videoUrl: "/videos/known_to_unknown_scene/1080p60/RecurrenceKnownToUnknownVisualization.mp4",
        previewImage: "/previews/recurrence_known_to_unknown_preview.png",
        duration: "约 25 秒",
        concepts: ["已知状态", "未知状态", "依赖关系", "循环起点", "递推方向", "状态扩展"],
        steps: [
          "先确认哪些状态已经知道，例如 f[1] = 1、f[2] = 2。",
          "找到第一个未知格：在这个例子里，第一个需要计算的是 f[3]。",
          "看当前格依赖谁：f[3] 依赖 f[2] 和 f[1]，所以这两个旧状态必须先算好。",
          "算出 f[3] 后，把它加入已知区，后面的 f[4] 就可以继续使用它。",
          "循环从第一个未知格开始：for (int i = 3; i <= n; i++)。",
          "每一轮都只做一件事：用已经知道的旧格子推出当前格。",
        ],
        code: recurrenceKnownToUnknownCode,
        problems: [
          {
            id: "recurrence-known-to-unknown-sequence",
            title: "从已知推出第 n 项",
            difficulty: "入门",
            focus: "从 f[1] 和 f[2] 开始，按顺序推出 f[n]",
            status: "ready",
            starterCode: recurrenceKnownToUnknownCode,
          },
          {
            id: "recurrence-new-state-log",
            title: "输出新状态",
            difficulty: "基础",
            focus: "只输出从第一个未知格开始新算出的状态值",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    vector<long long> f(n + 3, 0);
    f[1] = 1;
    f[2] = 2;

    // TODO: 从 f[3] 开始填表，并输出每个新算出的状态

    return 0;
}`,
          },
          {
            id: "recurrence-third-order-sequence",
            title: "前三项推出当前项",
            difficulty: "进阶",
            focus: "依赖前三个旧状态时，循环要从第一个未知格 f[4] 开始",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    vector<long long> f(n + 4, 0);
    f[1] = 1;
    f[2] = 1;
    f[3] = 2;

    // TODO: 当前格依赖前三个旧格，想一想循环从哪里开始

    cout << f[n];
    return 0;
}`,
          },
        ],
      },
      {
        id: "recurrence-climb-stairs",
        title: "一维递推：爬楼梯",
        summary: "用“最后一步分类”推导爬楼梯公式：到第 i 阶只能来自 i-1 或 i-2，所以 f[i] = f[i-1] + f[i-2]。",
        videoUrl: "/videos/climb_stairs_scene/1080p60/RecurrenceClimbStairsVisualization.mp4",
        previewImage: "/previews/recurrence_climb_stairs_preview.png",
        duration: "约 25 秒",
        concepts: ["最后一步分类", "一维递推", "爬楼梯", "状态转移", "初始化", "答案格"],
        steps: [
          "继续使用状态定义：f[i] 表示走到第 i 阶的方法数。",
          "观察到达第 i 阶的最后一步：要么从 i-1 走 1 阶，要么从 i-2 走 2 阶。",
          "这两类方案的最后一步不同，不会重复，所以总数可以相加。",
          "得到转移式：f[i] = f[i - 1] + f[i - 2]。",
          "放好初始条件：f[0] = 1、f[1] = 1。",
          "从 i = 2 开始向右填表，最后输出 f[n]。",
        ],
        code: recurrenceClimbStairsCode,
        problems: [
          {
            id: "recurrence-climb-stairs-transition",
            title: "最后一步分类求方法数",
            difficulty: "入门",
            focus: "用 f[i] = f[i-1] + f[i-2] 求走到第 n 阶的方法数",
            status: "ready",
            starterCode: recurrenceClimbStairsCode,
          },
          {
            id: "recurrence-climb-stairs-transition-table",
            title: "输出转移表",
            difficulty: "基础",
            focus: "输出从 f[2] 开始每个新格子的值，观察表格如何向右填充",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    vector<long long> f(n + 2, 0);
    f[0] = 1;
    f[1] = 1;

    // TODO: 从 i = 2 开始填表，并输出每个 f[i]

    return 0;
}`,
          },
          {
            id: "recurrence-climb-stairs-source-trace",
            title: "最后一步来源分解",
            difficulty: "进阶",
            focus: "把每个 f[i] 拆成 f[i-1] 与 f[i-2] 两个来源",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    vector<long long> f(n + 2, 0);
    f[0] = 1;
    f[1] = 1;

    // TODO: 输出每一行 i:a+b=c，表示 f[i]=f[i-1]+f[i-2]

    return 0;
}`,
          },
        ],
      },
      {
        id: "recurrence-fibonacci-sequence",
        title: "简单数列：Fibonacci",
        summary: "用同一串 Fibonacci 数列对比 0-based 与 1-based 两种写法，理解题目定义如何决定初始化、循环起点和答案格。",
        videoUrl: "/videos/fibonacci_sequence_scene/1080p60/RecurrenceFibonacciSequenceVisualization.mp4",
        previewImage: "/previews/recurrence_fibonacci_sequence_preview.png",
        duration: "约 22 秒",
        concepts: ["Fibonacci", "数列递推", "0-based", "1-based", "初始化", "循环起点"],
        steps: [
          "先看数值规律：从第三项开始，每一项都等于前两项之和。",
          "如果题目定义 F(0)=0, F(1)=1，就使用 f[0] 和 f[1] 初始化。",
          "在 0-based 写法中，第一个未知格是 f[2]，循环从 i = 2 开始。",
          "如果题目定义 F(1)=1, F(2)=1，就使用 F[1] 和 F[2] 初始化。",
          "在 1-based 写法中，第一个未知格是 F[3]，循环从 i = 3 开始。",
          "写代码前先翻译题目下标，再决定输出哪一个答案格。",
        ],
        code: recurrenceFibonacciZeroBasedCode,
        problems: [
          {
            id: "recurrence-fibonacci-zero-based",
            title: "0-based Fibonacci",
            difficulty: "入门",
            focus: "按 F(0)=0、F(1)=1 的定义输出第 n 项",
            status: "ready",
            starterCode: recurrenceFibonacciZeroBasedCode,
          },
          {
            id: "recurrence-fibonacci-one-based",
            title: "1-based Fibonacci",
            difficulty: "基础",
            focus: "按 F(1)=1、F(2)=1 的定义选择初始化和循环起点",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    // 题目定义：F(1) = 1, F(2) = 1
    vector<long long> f(n + 2, 0);
    f[1] = 1;
    f[2] = 1;

    // TODO: 第一个未知格应该从哪里开始？

    cout << f[n];
    return 0;
}`,
          },
          {
            id: "recurrence-fibonacci-index-table",
            title: "下标对照表",
            difficulty: "进阶",
            focus: "同时输出 0-based 的 f[k] 和 1-based 的 F[k+1]，看清下标偏移",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    vector<long long> zero(n + 3, 0);
    vector<long long> one(n + 3, 0);
    zero[0] = 0;
    zero[1] = 1;
    one[1] = 1;
    one[2] = 1;

    // TODO: 分别补全两张表，并输出每一行 k:zero[k] one[k+1]

    return 0;
}`,
          },
        ],
      },
      {
        id: "recurrence-rolling-variables",
        title: "滚动变量优化",
        summary: "当递推只依赖最近几个旧状态时，把完整数组压缩成少量变量，先计算新值 c，再让 a、b 向前滚动。",
        videoUrl: "/videos/rolling_variables_scene/1080p60/RecurrenceRollingVariablesVisualization.mp4",
        previewImage: "/previews/recurrence_rolling_variables_preview.png",
        duration: "约 28 秒",
        concepts: ["滚动变量", "空间优化", "Fibonacci", "状态覆盖", "O(1) 空间", "更新顺序"],
        steps: [
          "先观察转移式：当前状态只依赖 f[i - 1] 和 f[i - 2]。",
          "用 a 保存较旧的状态 f[i - 2]，用 b 保存较新的状态 f[i - 1]。",
          "每一步先计算 c = a + b，得到当前新状态。",
          "再执行 a = b、b = c，让两个变量向前滚动一格。",
          "注意更新顺序：如果先改旧变量，再计算 c，就会丢失原来的状态。",
          "数组写法需要保存整张表，滚动变量写法只需要常数个变量。",
        ],
        code: recurrenceRollingFibonacciCode,
        problems: [
          {
            id: "recurrence-rolling-fibonacci",
            title: "滚动变量求 Fibonacci",
            difficulty: "入门",
            focus: "不用数组，只用 a、b、c 输出 0-based Fibonacci 的第 n 项",
            status: "ready",
            starterCode: recurrenceRollingFibonacciCode,
          },
          {
            id: "recurrence-rolling-climb-stairs",
            title: "滚动变量求爬楼梯",
            difficulty: "基础",
            focus: "把爬楼梯数组表压缩成两个变量，保持答案不变",
            status: "ready",
            starterCode: `#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;

    // f[0] = 1, f[1] = 1
    long long a = 1; // f[i - 2]
    long long b = 1; // f[i - 1]

    // TODO: 先算 c，再执行 a = b、b = c

    cout << (n == 0 ? a : b);
    return 0;
}`,
          },
          {
            id: "recurrence-rolling-trace",
            title: "输出滚动过程",
            difficulty: "进阶",
            focus: "按 i:a+b=c 输出每一步，检查滚动变量的更新顺序",
            status: "ready",
            starterCode: `#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;

    long long a = 0;
    long long b = 1;

    // TODO: 从 i = 2 到 n，输出 i:a+b=c，再滚动变量

    return 0;
}`,
          },
        ],
      },
      {
        id: "recurrence-pascal-triangle",
        title: "二维递推：杨辉三角",
        summary: "把状态从一维数组扩展到二维表格：先放好每一行两端的边界 1，再用上一行的左上和右上两个状态推出内部格。",
        videoUrl: "/videos/pascal_triangle_scene/1080p60/RecurrencePascalTriangleVisualization.mp4",
        previewImage: "/previews/recurrence_pascal_triangle_preview.png",
        duration: "约 26 秒",
        concepts: ["二维递推", "杨辉三角", "边界条件", "左上依赖", "右上依赖", "双重循环"],
        steps: [
          "先定义状态：f[i][j] 表示杨辉三角第 i 行第 j 个数。",
          "每一行的最左和最右都是边界格，直接设为 1。",
          "内部格来自上一行的两个旧状态：左上 f[i - 1][j - 1] 和右上 f[i - 1][j]。",
          "转移式写成 f[i][j] = f[i - 1][j - 1] + f[i - 1][j]。",
          "外层循环按行从上到下，内层循环只枚举内部列。",
          "输出时按题目要求取某一行、整张表，或单个 f[n][k]。",
        ],
        code: recurrencePascalTriangleCode,
        problems: [
          {
            id: "recurrence-pascal-triangle-row",
            title: "输出杨辉三角第 n 行",
            difficulty: "入门",
            focus: "按行填二维表，并输出最后一行",
            status: "ready",
            starterCode: recurrencePascalTriangleCode,
          },
          {
            id: "recurrence-pascal-triangle-table",
            title: "输出前 n 行杨辉三角",
            difficulty: "基础",
            focus: "一行一行向下填表，练习二维状态的输出格式",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    vector<vector<long long>> f(n + 1, vector<long long>(n + 1, 0));

    // TODO: 先设置边界，再填内部格

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) {
            if (j > 1) cout << ' ';
            cout << f[i][j];
        }
        cout << '\\n';
    }
    return 0;
}`,
          },
          {
            id: "recurrence-pascal-triangle-query",
            title: "查询杨辉三角中的一个数",
            difficulty: "进阶",
            focus: "根据 n 和 k 输出 f[n][k]，检查边界和内部转移是否完整",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, k;
    cin >> n >> k;

    vector<vector<long long>> f(n + 1, vector<long long>(n + 1, 0));

    // TODO: 填好杨辉三角，再输出第 n 行第 k 个数

    cout << f[n][k];
    return 0;
}`,
          },
        ],
      },
      {
        id: "recurrence-grid-paths",
        title: "路径计数：走方格",
        summary: "把二维递推放进方格地图里：先确定第一行和第一列的边界，再让每个内部格从上方和左方两个旧状态累加而来。",
        videoUrl: "/videos/grid_paths_scene/1080p60/RecurrenceGridPathsVisualization.mp4",
        previewImage: "/previews/recurrence_grid_paths_preview.png",
        duration: "约 30 秒",
        concepts: ["二维递推", "路径计数", "网格 DP", "边界条件", "上方依赖", "左方依赖"],
        steps: [
          "先定义状态：dp[i][j] 表示从左上角走到第 i 行第 j 列的方法数。",
          "因为只能向右或向下，第一行每个格子都只有一种走法。",
          "第一列每个格子也只有一种走法，边界先初始化为 1。",
          "内部格的最后一步只能来自上方或左方。",
          "转移式写成 dp[i][j] = dp[i - 1][j] + dp[i][j - 1]。",
          "按行从左上填到右下，最终输出 dp[n][m]。",
        ],
        code: recurrenceGridPathsCode,
        problems: [
          {
            id: "recurrence-grid-paths-basic",
            title: "走方格路径数",
            difficulty: "入门",
            focus: "给定 n 行 m 列，输出从左上到右下的走法数量",
            status: "ready",
            starterCode: recurrenceGridPathsCode,
          },
          {
            id: "recurrence-grid-paths-table",
            title: "输出路径计数表",
            difficulty: "基础",
            focus: "把整张 dp 表输出出来，检查边界和填表顺序",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;

    vector<vector<long long>> dp(n + 1, vector<long long>(m + 1, 0));

    // TODO: 先初始化第一行和第一列，再填内部格

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (j > 1) cout << ' ';
            cout << dp[i][j];
        }
        cout << '\\n';
    }
    return 0;
}`,
          },
          {
            id: "recurrence-grid-paths-obstacle",
            title: "带障碍的走方格",
            difficulty: "进阶",
            focus: "遇到障碍格时方法数为 0，其余格继续看上方和左方",
            status: "ready",
            starterCode: `#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;

    vector<string> grid(n);
    for (int i = 0; i < n; i++) cin >> grid[i];

    vector<vector<long long>> dp(n, vector<long long>(m, 0));

    // TODO: 如果格子不是障碍，就从上方和左方累加路径数

    cout << dp[n - 1][m - 1];
    return 0;
}`,
          },
        ],
      },
      {
        id: "recurrence-number-tower",
        title: "数塔递推",
        summary: "把二维递推从“计数”推进到“最值”：从底层开始，每个位置只需要看下面两个已知状态中的较大者，最终把最大路径和汇总到顶端。",
        videoUrl: "/videos/number_tower_scene/1080p60/RecurrenceNumberTowerVisualization.mp4",
        previewImage: "/previews/recurrence_number_tower_preview.png",
        duration: "约 30 秒",
        concepts: ["数塔", "最值递推", "自底向上", "状态含义", "max 转移", "答案汇总"],
        steps: [
          "先读懂路径规则：从顶端出发，每一步只能走到下一层的左下或右下。",
          "定义状态：f[i][j] 表示从第 i 行第 j 个数字出发，走到底层能得到的最大和。",
          "底层没有下一步，所以直接初始化：f[n][j] = a[n][j]。",
          "对于上面的格子，后续只有两个选择：左下 f[i + 1][j] 和右下 f[i + 1][j + 1]。",
          "转移式写成 f[i][j] = a[i][j] + max(f[i + 1][j], f[i + 1][j + 1])。",
          "循环方向必须从 n - 1 倒着走到 1，最后输出 f[1][1]。",
        ],
        code: recurrenceNumberTowerCode,
        problems: [
          {
            id: "recurrence-number-tower-basic",
            title: "数塔最大路径和",
            difficulty: "入门",
            focus: "自底向上填表，输出顶端 f[1][1]",
            status: "ready",
            starterCode: recurrenceNumberTowerCode,
          },
          {
            id: "recurrence-number-tower-table",
            title: "输出数塔递推表",
            difficulty: "基础",
            focus: "输出每个 f[i][j]，观察最大路径和如何逐层向上汇总",
            status: "ready",
            starterCode: `#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    vector<vector<long long>> a(n + 1, vector<long long>(n + 2, 0));
    vector<vector<long long>> f(n + 2, vector<long long>(n + 2, 0));

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) {
            cin >> a[i][j];
        }
    }

    // TODO: 自底向上填出 f 表

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) {
            if (j > 1) cout << ' ';
            cout << f[i][j];
        }
        cout << '\\n';
    }
    return 0;
}`,
          },
          {
            id: "recurrence-number-tower-min",
            title: "数塔最小路径和",
            difficulty: "进阶",
            focus: "把 max 转移改成 min 转移，理解最值方向由题意决定",
            status: "ready",
            starterCode: `#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    vector<vector<long long>> a(n + 1, vector<long long>(n + 2, 0));
    vector<vector<long long>> f(n + 2, vector<long long>(n + 2, 0));

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) {
            cin >> a[i][j];
        }
    }

    // TODO: 用 min 完成自底向上的最小路径和递推

    cout << f[1][1];
    return 0;
}`,
          },
        ],
      },
      {
        id: "recurrence-initial-conditions-boundary",
        title: "初始条件与边界",
        summary: "递推式只是中间规则；程序还必须给出最小状态、合法数组范围和正确循环起点。用极小输入逐项检查，能在长状态链扩散前抓住大多数边界错误。",
        videoUrl: "/videos/initial_conditions_boundary_scene/480p15/RecurrenceInitialBoundaryVisualization.mp4",
        previewImage: "/previews/recurrence_initial_boundary_preview.png",
        duration: "约 24 秒",
        concepts: ["初始条件", "循环起点", "数组边界", "极小输入", "哨兵初始化", "递推调试"],
        steps: [
          "先用一句话定义 f[i]，确认这个定义在 n = 0、n = 1 等最小输入下仍有意义。",
          "把不需要递推就能直接回答的状态写成初值；爬楼梯可设 f[0] = 1、f[1] = 1。",
          "检查转移读取哪些旧状态：既然需要 i - 1 和 i - 2，第一个可计算位置就是 i = 2。",
          "数组容量必须覆盖所有将被读写的下标；用 n + 2 能让 n = 0 时的 f[1] 初始化仍然合法。",
          "写完后先跑 n = 0、n = 1、n = 2，再检查单行、单列等退化数据。",
          "二维递推可以使用哨兵初值统一边界，例如 dp[0][1] = 1，让左上角自然得到一种起点方案。",
        ],
        code: recurrenceInitialBoundaryCode,
        problems: [
          {
            id: "recurrence-boundary-climb-stairs",
            title: "边界版爬楼梯",
            difficulty: "入门",
            focus: "覆盖 n = 0 和 n = 1，并从第一个未知状态开始递推",
            status: "ready",
            starterCode: recurrenceInitialBoundaryCode,
          },
          {
            id: "recurrence-boundary-state-table",
            title: "补齐递推状态表",
            difficulty: "基础",
            focus: "先写两个给定初值，再完整输出 f[0] 到 f[n]",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    vector<long long> f(n + 2, 0);

    // TODO: 写出 f[0]、f[1]，再从第一个未知状态开始递推

    for (int i = 0; i <= n; i++) {
        if (i > 0) cout << ' ';
        cout << f[i];
    }
    return 0;
}`,
          },
          {
            id: "recurrence-boundary-grid-sentinel",
            title: "哨兵边界走方格",
            difficulty: "进阶",
            focus: "用 dp[0][1] = 1 统一首行、首列和 1 × 1 网格",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;

    vector<vector<long long>> dp(n + 1, vector<long long>(m + 1, 0));

    // TODO: 设置一个哨兵初值，让每个格子都能统一从上方和左方累加

    cout << dp[n][m];
    return 0;
}`,
          },
        ],
      },
    ],
  },
  {
    id: "recursion",
    order: 4,
    title: "递归算法",
    subtitle: "看见调用栈的展开与回收",
    status: "ready",
    icon: Braces,
    lessons: [
      {
        id: "recursion-self-call",
        title: "函数为什么能调用自己",
        summary: "递归不是让同一个函数停在原地，而是每次创建一份新的调用任务；只要问题规模持续变小，就能一步步走向最小任务。",
        videoUrl: "/videos/recursion_chapter_scenes/1080p60/RecursionSelfCallVisualization.mp4",
        previewImage: "/previews/recursion_self_call_preview.png",
        duration: "约 24 秒",
        concepts: ["递归", "自调用", "问题规模", "子问题", "调用任务", "递归结构"],
        steps: [
          "把 countdown(n) 理解成一张写着参数 n 的独立任务卡。",
          "函数输出当前 n 后，调用 countdown(n - 1)，把更小任务交给下一层。",
          "每次调用都会得到自己的参数和局部变量，不会覆盖上一层。",
          "参数从 n 逐步减到 0，说明任务规模在持续缩小。",
          "当最小任务能够直接处理时，递归链就可以结束。",
          "判断能否递归时，先找相似子问题，再确认规模确实变小。",
        ],
        code: recursionSelfCallCode,
        problems: [
          { id: "recursion-countdown", title: "递归倒计时", difficulty: "入门", focus: "输出当前值后递归处理 n-1", status: "ready", starterCode: recursionSelfCallCode },
          {
            id: "recursion-sum-to-n",
            title: "递归求 1 到 n 的和",
            difficulty: "基础",
            focus: "把 sum(n) 拆成 n 与 sum(n-1)",
            status: "ready",
            starterCode: `#include <iostream>
using namespace std;

long long sumTo(int n) {
    // TODO: 写出最小问题和规模更小的子问题
}

int main() {
    int n;
    cin >> n;
    cout << sumTo(n);
    return 0;
}`,
          },
          {
            id: "recursion-power-two",
            title: "递归计算 2 的幂",
            difficulty: "进阶",
            focus: "用 power(n)=2*power(n-1) 识别同构子问题",
            status: "ready",
            starterCode: `#include <iostream>
using namespace std;

long long powerTwo(int n) {
    // TODO: 约定 2^0 = 1
}

int main() {
    int n;
    cin >> n;
    cout << powerTwo(n);
    return 0;
}`,
          },
        ],
      },
      {
        id: "recursion-base-case",
        title: "递归出口",
        summary: "出口负责直接解决最小问题，并阻止继续调用；把出口放在递归调用之前，调用栈才能停止增长并开始返回。",
        videoUrl: "/videos/recursion_chapter_scenes/1080p60/RecursionBaseCaseVisualization.mp4",
        previewImage: "/previews/recursion_base_case_preview.png",
        duration: "约 22 秒",
        concepts: ["递归出口", "最小问题", "无限递归", "栈溢出", "返回", "边界"],
        steps: [
          "先问最小规模是什么，以及它的答案能否直接写出。",
          "在函数开头判断出口，满足条件时立即 return。",
          "如果出口缺失，函数会持续创建新栈帧，最终发生栈溢出。",
          "如果出口永远到不了，写了判断也无法结束递归。",
          "到达出口后，不再压入新调用，执行方向转为逐层返回。",
          "用 n=0、n=1 等最小输入单独检查出口是否正确。",
        ],
        code: recursionBaseCaseCode,
        problems: [
          { id: "recursion-print-up", title: "从 1 递归输出到 n", difficulty: "入门", focus: "先递归后输出，出口设在 n=0", status: "ready", starterCode: recursionBaseCaseCode },
          {
            id: "recursion-digit-sum",
            title: "递归求各位数字和",
            difficulty: "基础",
            focus: "n=0 时返回 0，其余情况拆出个位",
            status: "ready",
            starterCode: `#include <iostream>
using namespace std;

int digitSum(long long n) {
    // TODO: 当前个位是 n % 10，剩余数字是 n / 10
}

int main() {
    long long n;
    cin >> n;
    cout << digitSum(n);
    return 0;
}`,
          },
          {
            id: "recursion-gcd",
            title: "欧几里得递归求最大公约数",
            difficulty: "进阶",
            focus: "b=0 是出口，gcd(a,b) 转为 gcd(b,a%b)",
            status: "ready",
            starterCode: `#include <iostream>
using namespace std;

long long gcdRecursive(long long a, long long b) {
    // TODO: 当 b 为 0 时直接返回 a
}

int main() {
    long long a, b;
    cin >> a >> b;
    cout << gcdRecursive(a, b);
    return 0;
}`,
          },
        ],
      },
      {
        id: "recursion-parameter-change",
        title: "参数变化",
        summary: "递归参数是通往出口的路标：每次调用都应让某个度量严格靠近边界，否则调用会在原地打转。",
        videoUrl: "/videos/recursion_chapter_scenes/1080p60/RecursionParameterVisualization.mp4",
        previewImage: "/previews/recursion_parameter_preview.png",
        duration: "约 21 秒",
        concepts: ["参数变化", "递归进度", "单调靠近", "区间", "下标", "终止性"],
        steps: [
          "先为参数找到一个可度量的规模，例如 n 或区间长度 r-l+1。",
          "当前调用只处理一小步，再把剩余任务交给下一组参数。",
          "递减写法常见 n-1，递增写法常见 index+1 或 left+1。",
          "区间递归可以同时收缩左右边界，让长度减少 2。",
          "若下一层参数完全不变，出口条件就可能永远不成立。",
          "手动写出前三层参数，是检查递归是否前进的最快方法。",
        ],
        code: recursionParameterCode,
        problems: [
          { id: "recursion-print-range", title: "递归输出整数区间", difficulty: "入门", focus: "让 current 每层增加 1，直到越过 right", status: "ready", starterCode: recursionParameterCode },
          {
            id: "recursion-reverse-string",
            title: "递归反转字符串",
            difficulty: "基础",
            focus: "下标向右推进，回收阶段逆序输出",
            status: "ready",
            starterCode: `#include <iostream>
#include <string>
using namespace std;

void printReverse(const string& s, int index) {
    // TODO: index 到达 s.size() 后返回；先递归，再输出当前字符
}

int main() {
    string s;
    cin >> s;
    printReverse(s, 0);
    return 0;
}`,
          },
          {
            id: "recursion-palindrome",
            title: "递归判断回文串",
            difficulty: "进阶",
            focus: "左右边界同时向中间收缩",
            status: "ready",
            starterCode: `#include <iostream>
#include <string>
using namespace std;

bool isPalindrome(const string& s, int left, int right) {
    // TODO: 先判断出口和两端字符，再收缩区间
}

int main() {
    string s;
    cin >> s;
    cout << (isPalindrome(s, 0, (int)s.size() - 1) ? "YES" : "NO");
    return 0;
}`,
          },
        ],
      },
      {
        id: "recursion-call-stack",
        title: "调用栈压入与弹出",
        summary: "每次递归调用都会压入一个保存参数、局部变量和返回位置的栈帧；最深层先返回，结果再沿调用链逐层向上流动。",
        videoUrl: "/videos/recursion_chapter_scenes/1080p60/RecursionCallStackVisualization.mp4",
        previewImage: "/previews/recursion_call_stack_preview.png",
        duration: "约 25 秒",
        concepts: ["调用栈", "栈帧", "压栈", "弹栈", "局部变量", "返回值"],
        steps: [
          "调用 recursiveSum(4) 时，第一张栈帧保存参数 n=4。",
          "调用 recursiveSum(3) 会压入新栈帧，上一层暂停等待。",
          "直到 recursiveSum(1) 命中出口，压栈阶段才结束。",
          "最深层返回 1，上一层取到子结果后计算 2+1。",
          "栈帧按后进先出顺序弹出，最终回到 main。",
          "同名局部变量分别属于不同栈帧，互不覆盖。",
        ],
        code: recursionCallStackCode,
        problems: [
          { id: "recursion-sum-stack", title: "调用栈递归求和", difficulty: "入门", focus: "保存子调用返回值并逐层相加", status: "ready", starterCode: recursionCallStackCode },
          {
            id: "recursion-enter-leave",
            title: "输出进入与返回顺序",
            difficulty: "基础",
            focus: "观察 enter 正序、leave 逆序",
            status: "ready",
            starterCode: `#include <iostream>
using namespace std;

void visit(int n) {
    // TODO: 输出 enter n，递归，再输出 leave n
}

int main() {
    int n;
    cin >> n;
    visit(n);
    return 0;
}`,
          },
          {
            id: "recursion-array-max",
            title: "递归求数组最大值",
            difficulty: "进阶",
            focus: "每层把当前元素与子区间答案比较",
            status: "ready",
            starterCode: `#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int arrayMax(const vector<int>& a, int index) {
    // TODO: 最后一项直接返回；否则比较当前项和后缀答案
}

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int& x : a) cin >> x;
    cout << arrayMax(a, 0);
    return 0;
}`,
          },
        ],
      },
      {
        id: "recursion-factorial",
        title: "递归展开与回收：阶乘",
        summary: "n! 可以拆成 n×(n-1)!：展开阶段保留尚未完成的乘法，出口给出 1，回收阶段再逐层得到完整结果。",
        videoUrl: "/videos/recursion_chapter_scenes/1080p60/RecursionFactorialVisualization.mp4",
        previewImage: "/previews/recursion_factorial_preview.png",
        duration: "约 22 秒",
        concepts: ["阶乘", "递归展开", "递归回收", "返回表达式", "乘法链", "组合数"],
        steps: [
          "根据定义把 n! 改写为 n×(n-1)!。",
          "每一层先保留当前因子 n，再请求更小阶乘的答案。",
          "当 n<=1 时直接返回 1，这是乘法链的起点。",
          "展开顺序是 5、4、3、2、1，回收计算顺序正好相反。",
          "return n*factorial(n-1) 同时写出了子问题和合并方式。",
          "用 n=0、n=1 检查 0!=1 和 1!=1 两个边界。",
        ],
        code: recursionFactorialCode,
        problems: [
          { id: "recursion-factorial-basic", title: "递归求阶乘", difficulty: "入门", focus: "展开 n×factorial(n-1) 并逐层回收", status: "ready", starterCode: recursionFactorialCode },
          {
            id: "recursion-factorial-trace",
            title: "输出阶乘回收过程",
            difficulty: "基础",
            focus: "在子调用返回后输出 n! 的当前结果",
            status: "ready",
            starterCode: `#include <iostream>
using namespace std;

long long factorialTrace(int n) {
    // TODO: 回收时按 n!=answer 输出每层结果
}

int main() {
    int n;
    cin >> n;
    factorialTrace(n);
    return 0;
}`,
          },
          {
            id: "recursion-combination",
            title: "递归计算组合数",
            difficulty: "进阶",
            focus: "用 C(n,k)=C(n-1,k-1)+C(n-1,k) 建立双分支",
            status: "ready",
            starterCode: `#include <iostream>
using namespace std;

long long combination(int n, int k) {
    // TODO: k=0 或 k=n 时返回 1
}

int main() {
    int n, k;
    cin >> n >> k;
    cout << combination(n, k);
    return 0;
}`,
          },
        ],
      },
      {
        id: "recursion-fibonacci-tree",
        title: "Fibonacci 递归树",
        summary: "Fibonacci 的递归调用会分裂成一棵树；同一个子问题在不同分支重复出现，既解释了执行顺序，也暴露了朴素递归的低效。",
        videoUrl: "/videos/recursion_chapter_scenes/1080p60/RecursionFibonacciVisualization.mp4",
        previewImage: "/previews/recursion_fibonacci_preview.png",
        duration: "约 23 秒",
        concepts: ["树形递归", "Fibonacci", "重复计算", "递归树", "调用次数", "记忆化"],
        steps: [
          "fib(n) 会同时请求 fib(n-1) 与 fib(n-2) 两个子结果。",
          "每个非出口节点继续分裂，形成一棵二叉递归树。",
          "fib(2)、fib(3) 等相同子问题会在不同分支重复出现。",
          "返回时先得到左右子树结果，再在父节点把它们相加。",
          "朴素写法适合观察结构，但 n 增大后调用次数增长很快。",
          "把算过的 fib(k) 保存下来，就得到记忆化递归。",
        ],
        code: recursionFibonacciCode,
        problems: [
          { id: "recursion-fibonacci-basic", title: "朴素递归 Fibonacci", difficulty: "入门", focus: "写出双分支递归和两个出口", status: "ready", starterCode: recursionFibonacciCode },
          {
            id: "recursion-fibonacci-calls",
            title: "统计递归调用次数",
            difficulty: "基础",
            focus: "每进入一次 fib 就把计数增加 1",
            status: "ready",
            starterCode: `#include <iostream>
using namespace std;

long long calls = 0;
long long fibonacci(int n) {
    // TODO: 统计包括出口在内的每一次函数调用
}

int main() {
    int n;
    cin >> n;
    long long value = fibonacci(n);
    cout << value << '\\n' << calls;
    return 0;
}`,
          },
          {
            id: "recursion-fibonacci-memo",
            title: "记忆化递归 Fibonacci",
            difficulty: "进阶",
            focus: "命中已保存结果时直接返回，避免重复展开",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

vector<long long> memo;
long long fibonacci(int n) {
    // TODO: 先查 memo，再递归计算并保存
}

int main() {
    int n;
    cin >> n;
    memo.assign(n + 1, -1);
    cout << fibonacci(n);
    return 0;
}`,
          },
        ],
      },
      {
        id: "recursion-hanoi",
        title: "汉诺塔",
        summary: "移动 n 个盘子的任务可以固定拆成三步：移走上面 n-1 个、移动最大盘、再把 n-1 个盘子移到目标柱。",
        videoUrl: "/videos/recursion_chapter_scenes/1080p60/RecursionHanoiVisualization.mp4",
        previewImage: "/previews/recursion_hanoi_preview.png",
        duration: "约 22 秒",
        concepts: ["汉诺塔", "任务分解", "辅助柱", "递归三步", "移动序列", "2^n-1"],
        steps: [
          "目标是把 n 个盘子从起点柱移动到目标柱，且大盘不能压小盘。",
          "先递归地把上面 n-1 个盘子从起点移到辅助柱。",
          "空出最大盘后，把它从起点直接移动到目标柱。",
          "再递归地把 n-1 个盘子从辅助柱移动到目标柱。",
          "n=0 时没有盘子需要移动，直接返回。",
          "参数 from、auxiliary、to 会随子任务交换角色。",
        ],
        code: recursionHanoiCode,
        problems: [
          { id: "recursion-hanoi-moves", title: "输出汉诺塔移动步骤", difficulty: "入门", focus: "按三步分解输出标准移动序列", status: "ready", starterCode: recursionHanoiCode },
          {
            id: "recursion-hanoi-count",
            title: "汉诺塔最少移动次数",
            difficulty: "基础",
            focus: "用 T(n)=2T(n-1)+1 计算总次数",
            status: "ready",
            starterCode: `#include <iostream>
using namespace std;

long long moveCount(int n) {
    // TODO: 没有盘子时为 0，其余为两次子任务加一次最大盘移动
}

int main() {
    int n;
    cin >> n;
    cout << moveCount(n);
    return 0;
}`,
          },
          {
            id: "recursion-hanoi-disk-counts",
            title: "统计每个盘子的移动次数",
            difficulty: "进阶",
            focus: "在移动盘子时按编号累计次数",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

vector<long long> counts;
void hanoi(int n) {
    // TODO: 两次处理 n-1 个盘子，中间记录第 n 个盘子移动一次
}

int main() {
    int n;
    cin >> n;
    counts.assign(n + 1, 0);
    hanoi(n);
    for (int disk = 1; disk <= n; disk++) {
        if (disk > 1) cout << ' ';
        cout << counts[disk];
    }
    return 0;
}`,
          },
        ],
      },
      {
        id: "recursion-tree-traversal",
        title: "树形递归输出",
        summary: "树的左右孩子本身仍是树，递归天然适合遍历；把访问根节点的位置放在两次子调用之前、中间或之后，就得到三种遍历。",
        videoUrl: "/videos/recursion_chapter_scenes/1080p60/RecursionTreeTraversalVisualization.mp4",
        previewImage: "/previews/recursion_tree_traversal_preview.png",
        duration: "约 23 秒",
        concepts: ["二叉树", "前序遍历", "中序遍历", "后序遍历", "空节点", "访问时机"],
        steps: [
          "把当前节点看作根，把左右孩子看作两个更小的同类问题。",
          "遇到下标越界或值为 0 的空节点时直接返回。",
          "先访问根，再递归左右孩子，就是前序遍历。",
          "把访问放在两次递归之间，就是中序遍历。",
          "先处理左右孩子，最后访问根，就是后序遍历。",
          "三种写法的递归骨架相同，变化的只是 visit 的位置。",
        ],
        code: recursionTreeTraversalCode,
        problems: [
          { id: "recursion-tree-preorder", title: "递归前序遍历", difficulty: "入门", focus: "按根、左、右访问数组表示的二叉树", status: "ready", starterCode: recursionTreeTraversalCode },
          {
            id: "recursion-tree-inorder",
            title: "递归中序遍历",
            difficulty: "基础",
            focus: "把访问语句放在左右子调用之间",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

vector<int> tree;
void inorder(int index) {
    // TODO: 空节点返回；访问顺序为左、根、右
}

int main() {
    int n;
    cin >> n;
    tree.resize(n + 1);
    for (int i = 1; i <= n; i++) cin >> tree[i];
    inorder(1);
    return 0;
}`,
          },
          {
            id: "recursion-tree-postorder",
            title: "递归后序遍历",
            difficulty: "进阶",
            focus: "先完成左右子树，再访问当前根节点",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

vector<int> tree;
void postorder(int index) {
    // TODO: 空节点返回；访问顺序为左、右、根
}

int main() {
    int n;
    cin >> n;
    tree.resize(n + 1);
    for (int i = 1; i <= n; i++) cin >> tree[i];
    postorder(1);
    return 0;
}`,
          },
        ],
      },
      {
        id: "recursion-debugging",
        title: "递归调试方法",
        summary: "为每层调用增加 depth，并在进入和返回时打印参数与结果；缩进轨迹能把看不见的调用栈变成可逐行核对的执行记录。",
        videoUrl: "/videos/recursion_chapter_scenes/1080p60/RecursionDebugVisualization.mp4",
        previewImage: "/previews/recursion_debug_preview.png",
        duration: "约 21 秒",
        concepts: ["递归调试", "depth", "缩进日志", "进入", "返回", "参数轨迹"],
        steps: [
          "给递归函数临时增加 depth 参数，下一层传 depth+1。",
          "进入函数时打印参数，前面加 depth 个短横线作为缩进。",
          "在出口也打印返回信息，确认最深层是否正确停止。",
          "子调用结束后再次打印，观察控制权回到哪一层。",
          "二分递归可记录 left、right、mid，快速发现区间没有缩小的问题。",
          "调试完成后移除日志，不让辅助输出污染题目答案。",
        ],
        code: recursionDebugCode,
        problems: [
          { id: "recursion-depth-trace", title: "输出缩进递归轨迹", difficulty: "入门", focus: "用 depth 对齐进入与返回日志", status: "ready", starterCode: recursionDebugCode },
          {
            id: "recursion-binary-search-trace",
            title: "递归二分查找轨迹",
            difficulty: "基础",
            focus: "输出每层 mid，检查搜索区间是否严格缩小",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int binarySearch(const vector<int>& a, int left, int right, int target) {
    // TODO: 每层先输出 mid，再进入包含 target 的更小区间
}

int main() {
    int n, target;
    cin >> n >> target;
    vector<int> a(n);
    for (int& x : a) cin >> x;
    cout << "result=" << binarySearch(a, 0, n - 1, target);
    return 0;
}`,
          },
          {
            id: "recursion-euclid-trace",
            title: "欧几里得参数轨迹",
            difficulty: "进阶",
            focus: "逐层输出 a,b 并观察余数如何走向 0",
            status: "ready",
            starterCode: `#include <iostream>
using namespace std;

long long gcdTrace(long long a, long long b, int depth) {
    // TODO: 输出 depth:a,b；b=0 时返回，否则递归 gcd(b,a%b)
}

int main() {
    long long a, b;
    cin >> a >> b;
    cout << "gcd=" << gcdTrace(a, b, 0);
    return 0;
}`,
          },
        ],
      },
    ],
  },
  {
    id: "search-backtracking",
    order: 5,
    title: "搜索与回溯",
    subtitle: "在搜索树里选择、尝试、撤销",
    status: "building",
    icon: GitBranch,
    lessons: [
      {
        id: "search-enumeration-tree",
        title: "枚举与搜索树",
        summary: "把“所有可能”按决策次序展开成一棵树：层表示正在决定的位置，边表示一次选择，叶子就是一个完整方案。",
        duration: "讲义约 8 分钟",
        concepts: ["系统枚举", "决策层", "搜索树", "叶子方案", "path 数组"],
        steps: [
          "先明确每个位置有哪些候选项，不要边写代码边猜分支。",
          "用 pos 表示当前要决定第几个位置，path 保存从根到当前节点的选择。",
          "为当前候选项创建分支，进入 pos + 1 这一层。",
          "当 pos == n 时，所有位置都已决定，当前 path 就是一个叶子方案。",
          "二进制串的搜索树每层有 0、1 两个分支，深度 n 会产生 2^n 个叶子。",
        ],
        code: searchBinaryTreeCode,
        problems: [
          {
            id: "search-binary-strings",
            title: "枚举所有二进制串",
            difficulty: "入门",
            focus: "按 0 分支、1 分支的顺序展开一棵完整搜索树",
            status: "ready",
            starterCode: searchBinaryTreeCode,
          },
          {
            id: "search-tree-level-count",
            title: "计算搜索树各层节点数",
            difficulty: "基础",
            focus: "用 DFS 记录每个 depth 被访问的次数",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int n;
vector<long long> levelCount;

void dfs(int depth) {
    // TODO: 记录当前节点，再进入 0 和 1 两个分支
}

int main() {
    cin >> n;
    levelCount.assign(n + 1, 0);
    dfs(0);
    for (int depth = 0; depth <= n; depth++) {
        if (depth) cout << ' ';
        cout << levelCount[depth];
    }
    return 0;
}`,
          },
        ],
      },
      {
        id: "search-dfs-framework",
        title: "DFS 基本框架",
        summary: "深度优先搜索会先把一条路走到底，到达出口后返回最近的岔路口，再继续下一个候选分支。",
        duration: "讲义约 9 分钟",
        concepts: ["DFS", "递归出口", "候选循环", "深度优先", "调用栈"],
        steps: [
          "一个 DFS 通常有三部分：出口、候选循环、进入下一层。",
          "出口要放在函数前部；本题 pos == n 时已经得到完整序列。",
          "for 循环按约定顺序枚举当前层的候选项，它也决定最终输出顺序。",
          "每次递归都必须让 pos 接近出口，否则会无限递归。",
          "读代码时可以先画 n=2、m=2 的小树，再对齐每一次调用。",
        ],
        code: searchDfsFrameworkCode,
        problems: [
          {
            id: "search-dfs-sequences",
            title: "DFS 枚举定长序列",
            difficulty: "入门",
            focus: "每层从 1 到 m 选一个数，按 DFS 顺序输出所有序列",
            status: "ready",
            starterCode: searchDfsFrameworkCode,
          },
          {
            id: "search-dfs-leaf-count",
            title: "统计 DFS 叶子数",
            difficulty: "基础",
            focus: "不保存方案，只在递归出口统计完整方案",
            status: "ready",
            starterCode: `#include <iostream>
using namespace std;

int n, m;
long long leaves = 0;

void dfs(int pos) {
    // TODO: pos == n 时累加叶子，否则枚举 m 个分支
}

int main() {
    cin >> n >> m;
    dfs(0);
    cout << leaves;
    return 0;
}`,
          },
        ],
      },
      {
        id: "search-choose-recurse-undo",
        title: "选择、递归、撤销选择",
        summary: "回溯的核心是让同一份 path 在不同分支之间复用：先加入选择，再递归进入下一层，返回后立即恢复现场。",
        duration: "讲义约 10 分钟",
        concepts: ["回溯", "选择", "递归", "撤销", "恢复现场"],
        steps: [
          "path.push_back(choice) 把当前选择放入路径，此时才能进入下一层。",
          "dfs(...) 会完成这个选择之下的整棵子树，返回时说明子树已经搜完。",
          "path.pop_back() 必须与 push 成对，把 path 恢复到进入这个分支之前的状态。",
          "若还有 used、sum 或棋盘标记，也要在同一层完成对称的设置与撤销。",
          "调试回溯时，优先检查每个选择动作是否都有对应的撤销动作。",
        ],
        code: searchChooseUndoCode,
        problems: [
          {
            id: "search-fixed-weight-binary",
            title: "枚举恰有 k 个 1 的二进制串",
            difficulty: "基础",
            focus: "维护 path 和 ones，练习两个分支后的恢复现场",
            status: "ready",
            starterCode: searchChooseUndoCode,
          },
          {
            id: "search-balanced-parentheses",
            title: "生成合法括号序列",
            difficulty: "进阶",
            focus: "用 left、right 约束可选括号，每次递归后撤销字符",
            status: "ready",
            starterCode: `#include <iostream>
#include <string>
using namespace std;

int n;
string path;

void dfs(int left, int right) {
    // TODO: 只在 left < n 时放 '(' ，只在 right < left 时放 ')'
}

int main() {
    cin >> n;
    dfs(0, 0);
    return 0;
}`,
          },
        ],
      },
      {
        id: "search-full-permutation",
        title: "全排列",
        summary: "全排列要把每个数恰好使用一次：path 管理已填好的位置，used 数组管理哪些候选值暂时不可选。",
        duration: "讲义约 11 分钟",
        concepts: ["全排列", "used 数组", "候选过滤", "字典序", "恢复标记"],
        steps: [
          "当 path.size() == n 时，每个位置已经填好，输出一个排列。",
          "当前层枚举 1..n，如果 used[value] 为 true，说明它已经在路径中。",
          "选择 value 时同时设置 used 并放入 path，两份状态始终保持一致。",
          "子树搜完后，先移除 path 末尾，再把 used[value] 恢复为 false。",
          "候选值从小到大枚举，可自然得到字典序的排列。",
        ],
        code: searchPermutationCode,
        problems: [
          {
            id: "search-permutation-basic",
            title: "输出 1 到 n 的全排列",
            difficulty: "基础",
            focus: "用 used 数组避免同一个数在一条路径中重复使用",
            status: "ready",
            starterCode: searchPermutationCode,
          },
          {
            id: "search-permutation-kth",
            title: "第 k 个全排列",
            difficulty: "进阶",
            focus: "按字典序 DFS，在叶子处计数并停在第 k 个方案",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int n;
long long k, visitedLeaves = 0;
vector<int> path;
vector<bool> used;
bool found = false;

void dfs() {
    // TODO: 在第 k 个叶子输出 path，并让后续递归提前停止
}

int main() {
    cin >> n >> k;
    used.assign(n + 1, false);
    dfs();
    return 0;
}`,
          },
        ],
      },
      {
        id: "search-combination-enumeration",
        title: "组合枚举",
        summary: "组合不关心选择顺序。用 start 限制下一层只能向后选，就能避免 1,2 和 2,1 这类重复方案。",
        duration: "讲义约 10 分钟",
        concepts: ["组合", "start 起点", "去除顺序重复", "剩余名额", "循环剪枝"],
        steps: [
          "start 表示本层最小可选的数，选了 value 后，下一层从 value + 1 开始。",
          "路径中的数严格递增，因此同一个集合只会被生成一次。",
          "当 path.size() == k 时立即输出并 return，避免继续选出过长路径。",
          "need = k - path.size() 表示还缺多少个数。",
          "若从 value 到 n 连 need 个数都凑不齐，这个候选之后的循环可直接结束。",
        ],
        code: searchCombinationCode,
        problems: [
          {
            id: "search-combinations-basic",
            title: "输出 1 到 n 中的 k 数组合",
            difficulty: "基础",
            focus: "用 start 保证路径递增，按字典序输出组合",
            status: "ready",
            starterCode: searchCombinationCode,
          },
          {
            id: "search-combination-sum-k",
            title: "k 数组合求和",
            difficulty: "进阶",
            focus: "在组合搜索中维护 chosen 和 sum，统计和等于 target 的方案",
            status: "ready",
            starterCode: `#include <iostream>
using namespace std;

int n, k, target;
long long answer = 0;

void dfs(int start, int chosen, int sum) {
    // TODO: 选满 k 个数时检查 sum，否则从 start 继续选
}

int main() {
    cin >> n >> k >> target;
    dfs(1, 0, 0);
    cout << answer;
    return 0;
}`,
          },
        ],
      },
      {
        id: "search-subset-enumeration",
        title: "子集枚举",
        summary: "对每个元素都做“不选”或“选”两次递归，就会得到一棵深度为 n 的二叉搜索树，所有叶子恰好对应全部子集。",
        duration: "讲义约 9 分钟",
        concepts: ["子集", "选或不选", "二叉分支", "空集", "2^n"],
        steps: [
          "dfs(value) 表示正在决定元素 value 是否加入子集。",
          "不选 value 时不改 path，直接进入 dfs(value + 1)。",
          "选 value 时先 push，进入下一层，再 pop 恢复现场。",
          "当 value == n + 1 时，每个元素的去留都已确定，包括 path 为空的空集。",
          "n 个独立的二选一决策会生成 2^n 个子集，数据范围不能过大。",
        ],
        code: searchSubsetCode,
        problems: [
          {
            id: "search-subsets-basic",
            title: "枚举 1 到 n 的所有子集",
            difficulty: "基础",
            focus: "先不选后选，并正确输出空集",
            status: "ready",
            starterCode: searchSubsetCode,
          },
          {
            id: "search-subset-sum-count",
            title: "统计子集和等于 target 的方案",
            difficulty: "进阶",
            focus: "在选或不选的搜索树中传递当前和",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int n, target;
long long answer = 0;
vector<int> numbers;

void dfs(int index, int sum) {
    // TODO: 分别搜索不选 numbers[index] 和选它的分支
}

int main() {
    cin >> n >> target;
    numbers.resize(n);
    for (int& value : numbers) cin >> value;
    dfs(0, 0);
    cout << answer;
    return 0;
}`,
          },
        ],
      },
      {
        id: "search-maze-dfs",
        title: "迷宫 DFS",
        summary: "把 DFS 从抽象搜索树放进网格：方向数组产生候选移动，边界、墙和 visited 标记负责拦住非法分支。",
        duration: "讲义约 12 分钟",
        concepts: ["迷宫", "方向数组", "边界判断", "visited", "死路回退"],
        steps: [
          "dfs(x, y) 表示已经到达格子 (x, y)，目标是继续寻找终点。",
          "生成新坐标后，依次检查越界、墙和已访问，任一不满足就 continue。",
          "在进入相邻格之前标记 visited，避免在两个格子之间来回递归。",
          "只判断是否存在路径时，全局 visited 无需撤销；统计所有简单路径时则必须撤销。",
          "起点或终点是墙要先单独处理，否则 DFS 的起始状态就是非法的。",
        ],
        code: searchMazeCode,
        problems: [
          {
            id: "search-maze-reachable",
            title: "迷宫是否可达",
            difficulty: "基础",
            focus: "使用四方向 DFS 和 visited 判断左上到右下是否连通",
            status: "ready",
            starterCode: searchMazeCode,
          },
          {
            id: "search-maze-path-count",
            title: "统计迷宫简单路径",
            difficulty: "进阶",
            focus: "为当前路径标记 visited，回退时撤销，统计不重复走格子的路径",
            status: "ready",
            starterCode: `#include <iostream>
#include <string>
#include <vector>
using namespace std;

int n, m;
long long answer = 0;
vector<string> grid;
vector<vector<bool>> visited;
int dx[4] = {1, 0, -1, 0};
int dy[4] = {0, 1, 0, -1};

void dfs(int x, int y) {
    // TODO: 到达终点时计数；离开当前格子前撤销 visited
}

int main() {
    cin >> n >> m;
    grid.resize(n);
    for (string& row : grid) cin >> row;
    visited.assign(n, vector<bool>(m, false));
    if (grid[0][0] == '.' && grid[n - 1][m - 1] == '.') dfs(0, 0);
    cout << answer;
    return 0;
}`,
          },
        ],
      },
      {
        id: "search-pruning",
        title: "剪枝",
        summary: "剪枝是在可证明当前分支不可能产生答案时提前返回，一次判断可以跳过整棵子树，但条件必须保证不漏解。",
        duration: "讲义约 11 分钟",
        concepts: ["可行性剪枝", "上界", "下界", "后缀和", "不漏解"],
        steps: [
          "若所有数都为正数，当前 sum > target 后再选只会更大，可直接 return。",
          "suffixSum[index] 表示剩余数全选时最多还能增加多少。",
          "sum + suffixSum[index] < target 时，即使全选也不够，整个分支都可以剪掉。",
          "剪枝条件要写在叶子判断之前，让不可能的状态尽早停止。",
          "一旦输入允许负数，sum > target 就不再是安全剪枝，必须重新证明边界。",
        ],
        code: searchPruningCode,
        problems: [
          {
            id: "search-pruned-subset-sum",
            title: "剪枝统计目标子集和",
            difficulty: "进阶",
            focus: "用超过 target 和剩余上界两个安全条件剪掉子树",
            status: "ready",
            starterCode: searchPruningCode,
          },
          {
            id: "search-knapsack-backtrack",
            title: "回溯求背包最大价值",
            difficulty: "进阶",
            focus: "容量超限时剪枝，用剩余价值上界跳过不可能更优的分支",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int n, capacity, best = 0;
vector<int> weight, value, suffixValue;

void dfs(int index, int totalWeight, int totalValue) {
    // TODO: 剪掉超容量和价值上界不足的分支，再搜索选或不选
}

int main() {
    cin >> n >> capacity;
    weight.resize(n);
    value.resize(n);
    suffixValue.assign(n + 1, 0);
    for (int i = 0; i < n; i++) cin >> weight[i] >> value[i];
    for (int i = n - 1; i >= 0; i--) suffixValue[i] = suffixValue[i + 1] + value[i];
    dfs(0, 0, 0);
    cout << best;
    return 0;
}`,
          },
        ],
      },
      {
        id: "search-n-queens",
        title: "N 皇后简化版",
        summary: "按行放置皇后，每层只决定当前行的列；三组布尔数组保存列、主对角线和副对角线是否已被占用。",
        duration: "讲义约 13 分钟",
        concepts: ["N 皇后", "按行搜索", "列冲突", "对角线下标", "约束剪枝"],
        steps: [
          "dfs(row) 表示前 row 行已经合法放好，本层只尝试第 row 行的各列。",
          "同一列用 columnUsed[col] 判断，不需要再扫描棋盘上方。",
          "主对角线上 row-col 相同，加 n-1 后映射到非负下标。",
          "副对角线上 row+col 相同，两类对角线各有 2n-1 条。",
          "选择一列后同时锁定三组标记，子树结束后再同时解锁。",
        ],
        code: searchNQueensCode,
        problems: [
          {
            id: "search-n-queens-count",
            title: "统计 N 皇后方案数",
            difficulty: "进阶",
            focus: "用列与两类对角线标记快速判断当前位置是否安全",
            status: "ready",
            starterCode: searchNQueensCode,
          },
          {
            id: "search-n-queens-first",
            title: "输出第一个 N 皇后方案",
            difficulty: "进阶",
            focus: "让 DFS 返回 bool，找到按列字典序的第一个方案后提前停止",
            status: "ready",
            starterCode: `#include <iostream>
#include <vector>
using namespace std;

int n;
vector<int> queenColumn;
vector<bool> columnUsed, diagonalDown, diagonalUp;

bool dfs(int row) {
    // TODO: 从小到大尝试列，子问题返回 true 时立即向上返回
    return false;
}

int main() {
    cin >> n;
    queenColumn.assign(n, -1);
    columnUsed.assign(n, false);
    diagonalDown.assign(2 * n - 1, false);
    diagonalUp.assign(2 * n - 1, false);
    if (!dfs(0)) {
        cout << "NONE";
    } else {
        for (int i = 0; i < n; i++) {
            if (i) cout << ' ';
            cout << queenColumn[i] + 1;
        }
    }
    return 0;
}`,
          },
        ],
      },
      {
        id: "search-complexity-intuition",
        title: "回溯复杂度直觉",
        summary: "搜索题的关键不是只记 O(b^d)，而是会估算分支数 b、决策深度 d和剪枝后的有效节点，再对照题目数据范围。",
        duration: "讲义约 9 分钟",
        concepts: ["分支因子 b", "搜索深度 d", "b^d", "节点数", "预估与溢出"],
        steps: [
          "每层最多 b 个候选、共做 d 层决策时，叶子数的上界是 b^d。",
          "完整搜索树的总节点是 1 + b + b^2 + ... + b^d，通常与最后一层处在同一量级。",
          "全排列的分支会逐层减少，叶子数是 n!，不能机械地当成 n^n。",
          "剪枝能减少实际访问节点，但最坏上界仍要用于判断风险。",
          "计算 b^d 时要在乘法前检查 limit / b，避免先溢出再比较。",
        ],
        code: searchComplexityCode,
        problems: [
          {
            id: "search-budget-check",
            title: "搜索规模是否超预算",
            difficulty: "基础",
            focus: "逐次乘以 b，在溢出前判断 b^d 是否超过 limit",
            status: "ready",
            starterCode: searchComplexityCode,
          },
          {
            id: "search-full-tree-node-count",
            title: "计算完整搜索树节点数",
            difficulty: "基础",
            focus: "逐层累加 1+b+...+b^d，理解叶子数与总节点的区别",
            status: "ready",
            starterCode: `#include <iostream>
using namespace std;

int main() {
    long long b, d;
    cin >> b >> d;
    long long nodesOnLevel = 1;
    long long total = 0;
    // TODO: 累加第 0 层到第 d 层的节点数
    cout << total;
    return 0;
}`,
          },
        ],
      },
    ],
  },
  {
    id: "greedy",
    order: 6,
    title: "贪心算法",
    subtitle: "理解局部选择何时可靠",
    status: "ready",
    icon: Compass,
    lessons: greedyLessons,
  },
  {
    id: "divide-conquer",
    order: 7,
    title: "分治算法",
    subtitle: "把大问题拆成可合并的小问题",
    status: "ready",
    icon: Layers3,
    lessons: divideConquerLessons,
  },
  {
    id: "bfs",
    order: 8,
    title: "广度优先搜索",
    subtitle: "队列驱动的一层层扩散",
    status: "ready",
    icon: Grid3X3,
    lessons: bfsLessons,
  },
  {
    id: "dynamic-programming",
    order: 9,
    title: "动态规划",
    subtitle: "定义状态，沿依赖关系填表",
    status: "ready",
    icon: BrainCircuit,
    lessons: dynamicProgrammingLessons,
  },
];

export const firstLessonPath = "/chapters/big-integer/lessons/big-integer-addition";

export function findProblem(problemId: string) {
  for (const chapter of chapters) {
    for (const lesson of chapter.lessons) {
      const problem = lesson.problems.find((item) => item.id === problemId);
      if (problem) {
        return { chapter, lesson, problem };
      }
    }
  }
  return undefined;
}
