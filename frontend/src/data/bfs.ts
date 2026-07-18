import type { Lesson, Problem } from "./curriculum";

const cpp = (body: string, headers = "#include <iostream>\n#include <queue>\n#include <vector>") => `${headers}
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

const lesson = (
  id: string,
  title: string,
  summary: string,
  concepts: string[],
  steps: string[],
  code: string,
  problems: Problem[],
): Lesson => ({ id, title, summary, duration: "约 8 分钟", concepts, steps, code, problems });

const queueCode = cpp(`    int q;
    cin >> q;
    queue<int> line;
    while (q--) {
        string op;
        cin >> op;
        if (op == "push") {
            int x; cin >> x;
            line.push(x);
        } else if (op == "pop") {
            if (line.empty()) cout << "EMPTY\\n";
            else { cout << line.front() << '\\n'; line.pop(); }
        } else {
            cout << line.size() << '\\n';
        }
    }`, "#include <iostream>\n#include <queue>\n#include <string>");

const graphDistanceCode = cpp(`    int n, m, start;
    cin >> n >> m >> start;
    vector<vector<int>> graph(n + 1);
    while (m--) {
        int a, b; cin >> a >> b;
        graph[a].push_back(b);
        graph[b].push_back(a);
    }
    vector<int> dist(n + 1, -1);
    queue<int> q;
    dist[start] = 0;
    q.push(start);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : graph[u]) if (dist[v] == -1) {
            dist[v] = dist[u] + 1;
            q.push(v);
        }
    }
    for (int i = 1; i <= n; i++) {
        if (i > 1) cout << ' ';
        cout << dist[i];
    }`);

const gridDistanceCode = cpp(`    int n, m;
    cin >> n >> m;
    vector<string> grid(n);
    for (string& row : grid) cin >> row;
    vector<vector<int>> dist(n, vector<int>(m, -1));
    queue<pair<int, int>> q;
    if (grid[0][0] == '.') { dist[0][0] = 0; q.push({0, 0}); }
    int dx[4] = {-1, 1, 0, 0};
    int dy[4] = {0, 0, -1, 1};
    while (!q.empty()) {
        auto [x, y] = q.front(); q.pop();
        for (int k = 0; k < 4; k++) {
            int nx = x + dx[k], ny = y + dy[k];
            if (nx < 0 || nx >= n || ny < 0 || ny >= m) continue;
            if (grid[nx][ny] == '#' || dist[nx][ny] != -1) continue;
            dist[nx][ny] = dist[x][y] + 1;
            q.push({nx, ny});
        }
    }
    cout << dist[n - 1][m - 1];`, "#include <iostream>\n#include <queue>\n#include <string>\n#include <vector>");

const shortestCode = cpp(`    int start, target;
    cin >> start >> target;
    const int LIMIT = 100000;
    vector<int> dist(LIMIT + 1, -1);
    queue<int> q;
    dist[start] = 0; q.push(start);
    while (!q.empty()) {
        int x = q.front(); q.pop();
        if (x == target) break;
        int next[3] = {x - 1, x + 1, x * 2};
        for (int y : next) if (y >= 0 && y <= LIMIT && dist[y] == -1) {
            dist[y] = dist[x] + 1;
            q.push(y);
        }
    }
    cout << dist[target];`);

const restorePathCode = cpp(`    int n, m;
    cin >> n >> m;
    vector<string> grid(n);
    for (string& row : grid) cin >> row;
    vector<vector<pair<int,int>>> pre(n, vector<pair<int,int>>(m, {-2, -2}));
    queue<pair<int,int>> q;
    if (grid[0][0] == '.') { pre[0][0] = {-1, -1}; q.push({0, 0}); }
    int dx[4] = {-1, 1, 0, 0}, dy[4] = {0, 0, -1, 1};
    while (!q.empty()) {
        auto [x, y] = q.front(); q.pop();
        for (int k = 0; k < 4; k++) {
            int nx = x + dx[k], ny = y + dy[k];
            if (nx < 0 || nx >= n || ny < 0 || ny >= m) continue;
            if (grid[nx][ny] == '#' || pre[nx][ny].first != -2) continue;
            pre[nx][ny] = {x, y}; q.push({nx, ny});
        }
    }
    if (pre[n-1][m-1].first == -2) { cout << -1; return 0; }
    vector<pair<int,int>> path;
    for (pair<int,int> cur = {n-1, m-1}; cur.first != -1; cur = pre[cur.first][cur.second]) path.push_back(cur);
    reverse(path.begin(), path.end());
    cout << path.size() - 1 << '\\n';
    for (auto [x, y] : path) cout << x + 1 << ' ' << y + 1 << '\\n';`, "#include <algorithm>\n#include <iostream>\n#include <queue>\n#include <string>\n#include <vector>");

const multiSourceCode = cpp(`    int n, m;
    cin >> n >> m;
    vector<string> grid(n);
    for (string& row : grid) cin >> row;
    vector<vector<int>> dist(n, vector<int>(m, -1));
    queue<pair<int,int>> q;
    for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) if (grid[i][j] == '1') {
        dist[i][j] = 0; q.push({i, j});
    }
    int dx[4] = {-1, 1, 0, 0}, dy[4] = {0, 0, -1, 1};
    while (!q.empty()) {
        auto [x, y] = q.front(); q.pop();
        for (int k = 0; k < 4; k++) {
            int nx = x + dx[k], ny = y + dy[k];
            if (nx < 0 || nx >= n || ny < 0 || ny >= m || dist[nx][ny] != -1) continue;
            dist[nx][ny] = dist[x][y] + 1; q.push({nx, ny});
        }
    }
    int answer = 0;
    for (const auto& row : dist) for (int d : row) answer = max(answer, d);
    cout << answer;`, "#include <algorithm>\n#include <iostream>\n#include <queue>\n#include <string>\n#include <vector>");

const knightCode = cpp(`    int n, sx, sy, tx, ty;
    cin >> n >> sx >> sy >> tx >> ty;
    --sx; --sy; --tx; --ty;
    vector<vector<int>> dist(n, vector<int>(n, -1));
    queue<pair<int,int>> q;
    dist[sx][sy] = 0; q.push({sx, sy});
    int dx[8] = {-2,-2,-1,-1,1,1,2,2};
    int dy[8] = {-1,1,-2,2,-2,2,-1,1};
    while (!q.empty()) {
        auto [x, y] = q.front(); q.pop();
        for (int k = 0; k < 8; k++) {
            int nx = x + dx[k], ny = y + dy[k];
            if (nx < 0 || nx >= n || ny < 0 || ny >= n || dist[nx][ny] != -1) continue;
            dist[nx][ny] = dist[x][y] + 1; q.push({nx, ny});
        }
    }
    cout << dist[tx][ty];`);

const stateCode = cpp(`    int start, target;
    cin >> start >> target;
    const int LIMIT = 100000;
    vector<int> dist(LIMIT + 1, -1);
    queue<int> q;
    dist[start] = 0; q.push(start);
    while (!q.empty()) {
        int x = q.front(); q.pop();
        int next[3] = {x + 1, x - 1, x * 2};
        for (int y : next) if (0 <= y && y <= LIMIT && dist[y] == -1) {
            dist[y] = dist[x] + 1; q.push(y);
        }
    }
    cout << dist[target];`);

const compareCode = cpp(`    int n, m;
    cin >> n >> m;
    vector<vector<int>> graph(n + 1);
    while (m--) { int a, b; cin >> a >> b; graph[a].push_back(b); graph[b].push_back(a); }
    vector<int> dist(n + 1, -1);
    queue<int> q; dist[1] = 0; q.push(1);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : graph[u]) if (dist[v] == -1) { dist[v] = dist[u] + 1; q.push(v); }
    }
    cout << dist[n];`);

export const bfsLessons: Lesson[] = [
  lesson("bfs-queue-fifo", "队列与 FIFO", "先进入队列的状态先处理。掌握 front、push、pop 的职责，是读懂 BFS 主循环的第一步。", ["队列", "FIFO", "队首", "入队", "出队"], ["起点先入队。", "每轮读取并弹出队首。", "扩展出的新状态从队尾入队。", "空队列表示所有可达状态都已处理。", "不要把 front() 与 pop() 的职责混淆。"], queueCode, [problem("bfs-queue-commands", "队列指令模拟", "入门", "准确模拟 push、pop 与 size", queueCode), problem("bfs-round-robin", "轮转队列", "基础", "未完成的任务回到队尾", queueCode)]),
  lesson("bfs-level-expansion", "BFS 层序扩散", "距离相同的状态形成同一层；队列会先处理完近层，再进入远层。", ["层序", "距离数组", "首次访问", "无权图", "O(n+m)"], ["给起点距离赋 0。", "相邻未访问点的距离等于当前距离加 1。", "赋值与入队必须同时发生，防止重复入队。", "队列中的距离不会下降。", "最终 -1 表示不可达。"], graphDistanceCode, [problem("bfs-graph-distances", "无权图单源距离", "基础", "输出起点到每个点的最少边数", graphDistanceCode), problem("bfs-level-counts", "统计 BFS 各层节点数", "基础", "按 dist 汇总每一层节点数", graphDistanceCode)]),
  lesson("bfs-grid", "网格 BFS", "把每个可通行格看成节点，用方向数组统一尝试上下左右，并依次拦截越界、墙和已访问状态。", ["网格", "方向数组", "边界", "障碍", "访问标记"], ["用 pair<int,int> 表示坐标。", "方向数组生成四个相邻格。", "先判边界，再访问数组。", "dist=-1 同时承担未访问标记。", "起点或终点为墙时答案不可达。"], gridDistanceCode, [problem("bfs-maze-shortest", "迷宫最短步数", "基础", "四方向 BFS 求左上到右下距离", gridDistanceCode), problem("bfs-grid-reachable-count", "统计可达格子", "入门", "每个格第一次入队时累加计数", gridDistanceCode)]),
  lesson("bfs-shortest-proof", "最短步数为什么成立", "BFS 按非递减距离出队，因此一个状态第一次被发现时，已经得到无权图中的最短距离。", ["最短路", "第一次到达", "队列不变量", "无权边", "提前结束"], ["起点距离为 0，是最短的。", "假设当前出队状态距离已最短。", "它扩展出的未访问邻居距离只多 1。", "更短路径若存在，邻居应在更早层被发现，产生矛盾。", "只在所有边代价相同的场景直接使用此结论。"], shortestCode, [problem("bfs-number-line-shortest", "数轴最少操作", "基础", "用 -1、+1、*2 建立隐式图", shortestCode), problem("bfs-modulo-shortest", "模环上的最少操作", "进阶", "有限状态去重并证明首次到达最短", stateCode)]),
  lesson("bfs-path-restore", "路径还原", "距离告诉我们走了几步，前驱数组则保存每个状态由谁首次扩展而来；从终点逆推并反转即可恢复路径。", ["前驱", "路径还原", "反转", "哨兵", "不可达"], ["起点前驱设置为特殊哨兵。", "邻居第一次入队时记录 pre[邻居]=当前。", "到达终点后沿 pre 反向移动。", "逆序收集到的是终点到起点。", "反转后输出完整最短路径。"], restorePathCode, [problem("bfs-maze-path", "还原迷宫最短路径", "进阶", "记录坐标前驱并输出一条确定路径", restorePathCode), problem("bfs-graph-path", "还原图中最短路径", "基础", "记录节点前驱并逆序恢复", graphDistanceCode)]),
  lesson("bfs-multi-source", "多源 BFS", "把所有源点以距离 0 同时入队，就像多圈波纹同时扩散；每个位置第一次到达的时间就是最近源距离。", ["多源", "统一起点", "最近距离", "同时扩散", "感染时间"], ["扫描并收集全部源点。", "所有源点距离设为 0 后入同一个队列。", "之后的循环与单源 BFS 完全相同。", "第一次访问来自最近的某个源。", "总复杂度仍是每个状态至多入队一次。"], multiSourceCode, [problem("bfs-infection-time", "全部感染的最短时间", "基础", "所有感染源同时入队", multiSourceCode), problem("bfs-nearest-source", "每格到最近源的距离", "基础", "输出完整多源距离矩阵", multiSourceCode)]),
  lesson("bfs-knight", "骑士移动", "BFS 不局限于四方向网格。只要列出一个状态能到达的所有下一状态，就能处理骑士的八种 L 形移动。", ["骑士", "八方向", "状态扩展", "棋盘边界", "最少步数"], ["状态仍是棋盘坐标。", "把八种位移写入 dx、dy。", "每次循环用同一套边界与访问判断。", "起点等于终点时距离为 0。", "小棋盘上某些目标可能不可达。"], knightCode, [problem("bfs-knight-shortest", "骑士最少步数", "基础", "八种 L 形移动的 BFS", knightCode), problem("bfs-knight-reachable", "骑士恰好 k 步可达格数", "进阶", "按距离层统计目标层状态", knightCode)]),
  lesson("bfs-state", "状态 BFS", "节点可以是数字、字符串或局面。先定义完整状态，再列操作生成邻居，并用集合或数组避免重复状态。", ["隐式图", "状态", "操作", "去重", "状态空间"], ["先回答一个节点需要哪些信息才能决定后续。", "每种合法操作对应一条边。", "估计状态总数并设置安全边界。", "整数范围连续时优先用数组去重。", "字符串或复合状态可用 set/unordered_set。"], stateCode, [problem("bfs-integer-transform", "整数最少变换", "基础", "把整数作为节点、操作作为边", stateCode), problem("bfs-lock-four-digits", "四位密码锁", "进阶", "编码四位状态并避开禁用状态", stateCode)]),
  lesson("bfs-vs-dfs", "BFS 与 DFS 对比", "DFS 擅长沿一条决策链深入、枚举与回溯；BFS 付出队列内存换取按层次确认无权最短路。", ["BFS", "DFS", "最短步数", "枚举", "空间复杂度"], ["只判断可达时两者都可能适用。", "求无权最少步数优先 BFS。", "枚举全部方案或需要撤销选择时优先 DFS。", "BFS 内存取决于最宽的一层。", "有权边不能仅凭普通 BFS 求最短路。"], compareCode, [problem("bfs-unweighted-shortest", "无权图最少边数", "入门", "识别最短步数目标并使用 BFS", compareCode), problem("bfs-method-signals", "搜索方法判断信号", "基础", "根据任务特征统计应优先选择 BFS 的场景", compareCode)]),
];
