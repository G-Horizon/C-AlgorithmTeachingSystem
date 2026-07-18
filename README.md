# 青少年 C++ 算法可视化教学系统

这个项目用于建设面向青少年 C++ 编程能力培养的算法可视化教学系统。当前阶段先从 Manim 算法演示视频开始，逐步接入 React 学习前台和临时 OJ。

目前已完成第一章高精度计算 11 支规划视频的课程、视频和练习入口闭环，并把第二章排序扩展为 6 个课时、18 道练习、6 支高清动画的完整样板章节。
第一章已补充章节总结测验、回刷题包，以及所有高精度练习题的分层提示、题解要点和常见坑，学生可以在课程页和题目页完成复盘闭环。
第二章也已补充章节总结测验、三组回刷题包，以及全部排序练习的分层提示、题解要点和常见坑。
第五章搜索与回溯已完成 10 个课时的内容生产，接入 20 道可判题练习、6 题章节测验、全题分层题解与 10 份视频制作脚本；Manim 成片为下一阶段。
第六章贪心算法与第七章分治算法也已完成内容生产；其中第七章包含 8 个课时、16 道可判题练习、6 题章节测验、全题分层题解与 8 份视频制作脚本。

## 当前结构

```text
docs/
  需求与实现规划.md
  算法视频分镜规划.md
  新对话接续提示.md
  判题隔离与OJ接入规划.md
  完整Demo冲刺规划.md
  第五章内容生产说明.md
  第七章内容生产清单.md
frontend/
  src/
backend/
  app/
scripts/
  student_start.ps1
  demo_start.ps1
  demo_stop.ps1
  check_demo.ps1
  seed_demo_data.py
  render_hd_videos.ps1
manim/
  common/
    theme.py
    array_widgets.py
  scenes/
    high_precision/
      big_integer_intro_scenes.py
      big_integer_addition_scene.py
      big_integer_subtraction_scene.py
      big_integer_compare_scene.py
      big_integer_multiply_small_scene.py
      big_integer_multiply_big_scene.py
      big_integer_divide_small_scene.py
      leading_zero_normalization_scene.py
      big_integer_composite_scene.py
    recurrence/
      state_definition_scene.py
      known_to_unknown_scene.py
      climb_stairs_scene.py
      fibonacci_sequence_scene.py
      rolling_variables_scene.py
      pascal_triangle_scene.py
      grid_paths_scene.py
      number_tower_scene.py
    sorting/
      bubble_sort_scene.py
      selection_sort_scene.py
      insertion_sort_scene.py
      counting_sort_scene.py
      merge_sort_scene.py
      quick_sort_scene.py
media/
  videos/
  previews/
```

## 渲染命令

高质量渲染：

```powershell
python -m manim -pqh manim/scenes/sorting/bubble_sort_scene.py BubbleSortVisualization
python -m manim -pqh manim/scenes/sorting/selection_sort_scene.py SelectionSortVisualization
python -m manim -pqh manim/scenes/sorting/insertion_sort_scene.py InsertionSortVisualization
python -m manim -pqh manim/scenes/sorting/counting_sort_scene.py CountingSortVisualization
python -m manim -pqh manim/scenes/sorting/merge_sort_scene.py MergeSortVisualization
python -m manim -pqh manim/scenes/sorting/quick_sort_scene.py QuickSortVisualization
python -m manim -pqh manim/scenes/high_precision/big_integer_intro_scenes.py BigIntegerOverflowVisualization
python -m manim -pqh manim/scenes/high_precision/big_integer_intro_scenes.py BigIntegerStorageVisualization
python -m manim -pqh manim/scenes/high_precision/big_integer_intro_scenes.py BigIntegerReverseStorageVisualization
python -m manim -pqh manim/scenes/high_precision/big_integer_addition_scene.py BigIntegerAdditionVisualization
python -m manim -pqh manim/scenes/high_precision/big_integer_subtraction_scene.py BigIntegerSubtractionVisualization
python -m manim -pqh manim/scenes/high_precision/big_integer_compare_scene.py BigIntegerCompareVisualization
python -m manim -pqh manim/scenes/high_precision/big_integer_multiply_small_scene.py BigIntegerMultiplySmallVisualization
python -m manim -pqh manim/scenes/high_precision/big_integer_multiply_big_scene.py BigIntegerMultiplyBigVisualization
python -m manim -pqh manim/scenes/high_precision/big_integer_divide_small_scene.py BigIntegerDivideSmallVisualization
python -m manim -pqh manim/scenes/high_precision/leading_zero_normalization_scene.py LeadingZeroNormalizationVisualization
python -m manim -pqh manim/scenes/high_precision/big_integer_composite_scene.py BigIntegerCompositeVisualization
python -m manim -pqh manim/scenes/recurrence/state_definition_scene.py RecurrenceStateVisualization
python -m manim -pqh manim/scenes/recurrence/known_to_unknown_scene.py RecurrenceKnownToUnknownVisualization
python -m manim -pqh manim/scenes/recurrence/climb_stairs_scene.py RecurrenceClimbStairsVisualization
python -m manim -pqh manim/scenes/recurrence/fibonacci_sequence_scene.py RecurrenceFibonacciSequenceVisualization
python -m manim -pqh manim/scenes/recurrence/rolling_variables_scene.py RecurrenceRollingVariablesVisualization
python -m manim -pqh manim/scenes/recurrence/pascal_triangle_scene.py RecurrencePascalTriangleVisualization
python -m manim -pqh manim/scenes/recurrence/grid_paths_scene.py RecurrenceGridPathsVisualization
python -m manim -pqh manim/scenes/recurrence/number_tower_scene.py RecurrenceNumberTowerVisualization
python -m manim -pqh manim/scenes/recurrence/initial_conditions_boundary_scene.py RecurrenceInitialBoundaryVisualization
```

如果需要更快预览，可以使用低清版本：

```powershell
python -m manim -pql manim/scenes/sorting/bubble_sort_scene.py BubbleSortVisualization
python -m manim -pql manim/scenes/sorting/selection_sort_scene.py SelectionSortVisualization
python -m manim -pql manim/scenes/sorting/insertion_sort_scene.py InsertionSortVisualization
python -m manim -pql manim/scenes/sorting/counting_sort_scene.py CountingSortVisualization
python -m manim -pql manim/scenes/sorting/merge_sort_scene.py MergeSortVisualization
python -m manim -pql manim/scenes/sorting/quick_sort_scene.py QuickSortVisualization
python -m manim -pql manim/scenes/high_precision/big_integer_intro_scenes.py BigIntegerOverflowVisualization
python -m manim -pql manim/scenes/high_precision/big_integer_intro_scenes.py BigIntegerStorageVisualization
python -m manim -pql manim/scenes/high_precision/big_integer_intro_scenes.py BigIntegerReverseStorageVisualization
python -m manim -pql manim/scenes/high_precision/big_integer_addition_scene.py BigIntegerAdditionVisualization
python -m manim -pql manim/scenes/high_precision/big_integer_subtraction_scene.py BigIntegerSubtractionVisualization
python -m manim -pql manim/scenes/high_precision/big_integer_compare_scene.py BigIntegerCompareVisualization
python -m manim -pql manim/scenes/high_precision/big_integer_multiply_small_scene.py BigIntegerMultiplySmallVisualization
python -m manim -pql manim/scenes/high_precision/big_integer_multiply_big_scene.py BigIntegerMultiplyBigVisualization
python -m manim -pql manim/scenes/high_precision/big_integer_divide_small_scene.py BigIntegerDivideSmallVisualization
python -m manim -pql manim/scenes/high_precision/leading_zero_normalization_scene.py LeadingZeroNormalizationVisualization
python -m manim -pql manim/scenes/high_precision/big_integer_composite_scene.py BigIntegerCompositeVisualization
python -m manim -pql manim/scenes/recurrence/state_definition_scene.py RecurrenceStateVisualization
python -m manim -pql manim/scenes/recurrence/known_to_unknown_scene.py RecurrenceKnownToUnknownVisualization
python -m manim -pql manim/scenes/recurrence/climb_stairs_scene.py RecurrenceClimbStairsVisualization
python -m manim -pql manim/scenes/recurrence/fibonacci_sequence_scene.py RecurrenceFibonacciSequenceVisualization
python -m manim -pql manim/scenes/recurrence/rolling_variables_scene.py RecurrenceRollingVariablesVisualization
python -m manim -pql manim/scenes/recurrence/pascal_triangle_scene.py RecurrencePascalTriangleVisualization
python -m manim -pql manim/scenes/recurrence/grid_paths_scene.py RecurrenceGridPathsVisualization
python -m manim -pql manim/scenes/recurrence/number_tower_scene.py RecurrenceNumberTowerVisualization
python -m manim -pql manim/scenes/recurrence/initial_conditions_boundary_scene.py RecurrenceInitialBoundaryVisualization
```

批量后台渲染高清版本：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/render_hd_videos.ps1 -Background -DelaySeconds 120
```

脚本会按课程队列逐个生成 `1080p60` 视频，跳过已经存在的高清文件，并把运行日志写入 `logs/`。常用续跑方式：

```powershell
# 只预演命令，不实际渲染
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/render_hd_videos.ps1 -DryRun -DelaySeconds 0

# 从某个课时继续
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/render_hd_videos.ps1 -Background -StartAt C01-04 -DelaySeconds 120

# 强制重渲染已有高清文件
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/render_hd_videos.ps1 -Background -Force -DelaySeconds 120
```

渲染完成后，视频通常会输出到：

```text
media/videos/bubble_sort_scene/1080p60/BubbleSortVisualization.mp4
media/videos/selection_sort_scene/480p15/SelectionSortVisualization.mp4
media/videos/insertion_sort_scene/480p15/InsertionSortVisualization.mp4
media/videos/counting_sort_scene/480p15/CountingSortVisualization.mp4
media/videos/merge_sort_scene/480p15/MergeSortVisualization.mp4
media/videos/quick_sort_scene/480p15/QuickSortVisualization.mp4
media/videos/big_integer_intro_scenes/480p15/BigIntegerOverflowVisualization.mp4
media/videos/big_integer_intro_scenes/480p15/BigIntegerStorageVisualization.mp4
media/videos/big_integer_intro_scenes/480p15/BigIntegerReverseStorageVisualization.mp4
media/videos/big_integer_addition_scene/480p15/BigIntegerAdditionVisualization.mp4
media/videos/big_integer_subtraction_scene/480p15/BigIntegerSubtractionVisualization.mp4
media/videos/big_integer_compare_scene/480p15/BigIntegerCompareVisualization.mp4
media/videos/big_integer_multiply_small_scene/480p15/BigIntegerMultiplySmallVisualization.mp4
media/videos/big_integer_multiply_big_scene/480p15/BigIntegerMultiplyBigVisualization.mp4
media/videos/big_integer_divide_small_scene/480p15/BigIntegerDivideSmallVisualization.mp4
media/videos/leading_zero_normalization_scene/480p15/LeadingZeroNormalizationVisualization.mp4
media/videos/big_integer_composite_scene/480p15/BigIntegerCompositeVisualization.mp4
media/videos/state_definition_scene/480p15/RecurrenceStateVisualization.mp4
media/videos/known_to_unknown_scene/480p15/RecurrenceKnownToUnknownVisualization.mp4
media/videos/climb_stairs_scene/480p15/RecurrenceClimbStairsVisualization.mp4
media/videos/fibonacci_sequence_scene/480p15/RecurrenceFibonacciSequenceVisualization.mp4
media/videos/rolling_variables_scene/480p15/RecurrenceRollingVariablesVisualization.mp4
media/videos/pascal_triangle_scene/480p15/RecurrencePascalTriangleVisualization.mp4
media/videos/grid_paths_scene/480p15/RecurrenceGridPathsVisualization.mp4
```

## 依赖

需要安装 Manim：

```powershell
python -m pip install manim
```

## 后续实施

完整项目需求和实现路线见：

- `docs/需求与实现规划.md`
- `docs/算法视频分镜规划.md`
- `docs/新对话接续提示.md`
- `docs/判题隔离与OJ接入规划.md`
- `docs/完整Demo冲刺规划.md`

## 完整 Demo 演示

作为学生体验，可以直接双击仓库根目录的 `start_student_demo.cmd`。

也可以在 PowerShell 中运行：

```powershell
powershell.exe -ExecutionPolicy Bypass -File scripts/student_start.ps1
```

脚本会启动前端和后端，并打开第一章第一课：

```text
http://127.0.0.1:5173/chapters/big-integer/lessons/big-integer-overflow
```

演示前可以先写入一组可重复生成的提交记录，让 `/stats` 看板有通过、错答和编译错误等数据：

```powershell
python scripts/seed_demo_data.py
```

一键启动前端和后端，并顺手准备演示数据：

```powershell
powershell.exe -ExecutionPolicy Bypass -File scripts/demo_start.ps1 -SeedData
```

启动后访问：

```text
http://127.0.0.1:5173
http://127.0.0.1:5173/stats
```

演示结束后停止前端和后端：

```powershell
powershell.exe -ExecutionPolicy Bypass -File scripts/demo_stop.ps1
```

如果想先确认会停止哪些进程，可以使用：

```powershell
powershell.exe -ExecutionPolicy Bypass -File scripts/demo_stop.ps1 -DryRun
```

演示前完整检查：

```powershell
powershell.exe -ExecutionPolicy Bypass -File scripts/check_demo.ps1
```

该检查会验证 Python 语法、数塔课时归属、前后端题目 ID、媒体引用和 demo 数据。前端构建建议在 `frontend/` 目录直接运行：

```powershell
cd frontend
npm.cmd run build
```

在普通本地 PowerShell 环境中，也可以用 `scripts/check_demo.ps1 -Build` 把构建纳入检查；在受限沙箱里建议保持默认检查，避免 Vite 向上探测目录造成误报。

## 前端预览

前端骨架位于 `frontend/`，使用 React + TypeScript + Vite。首次运行需要安装依赖：

```powershell
cd frontend
npm install
npm run dev
```

启动后打开 Vite 输出的本地地址即可查看课程目录和排序课时页。前端通过 Vite `publicDir` 直接读取仓库根目录下的 `media/` 课程视频资源。

当前已实现：

- 九章课程导航。
- 浏览器本地学习进度：总进度、章节进度条、课时完成状态、题目 Accepted 点亮和继续学习入口。
- 高精度计算 11 课时、数据排序 6 课时、递推算法 9 课时、递归算法 9 课时、搜索与回溯 10 课时、贪心算法 9 课时，以及分治算法 8 课时。
- 已有 Manim 视频播放。
- 高精度计算、递推算法与递归算法均已形成“每课 3 题”的练习链路；第五章新增 20 道搜索与回溯练习，第七章新增 16 道分治练习。
- 第一章、第三章、第四章、第五章、第六章与第七章已接入章节总结测验、掌握清单、回刷题包，以及全章练习的分层提示、题解要点和常见坑。
- Monaco C++ 代码编辑器。
- 代码草稿本地自动保存。
- C++ 代码提交页。
- 判题结果、公开测试点输入输出对比。
- 后端 SQLite 提交记录同步。
- 最近提交记录与历史回看，后端不可用时保留浏览器本地兜底。
- 提交统计与教师视角看板，包含总提交、通过率、活跃题目、薄弱题排行、错误类型分布、演示学生观察和下一次课建议。
- 判题器能力提示，当前可通过 `/api/judge` 查询。

高精度计算开篇三课补充：

- 已新增制作文档 `docs/视频脚本/C01-01-普通整数为什么不够用.md`、`docs/视频脚本/C01-02-字符串与数组存储大整数.md`、`docs/视频脚本/C01-03-为什么常用反向存储.md`。
- 已新增 `manim/scenes/high_precision/big_integer_intro_scenes.py`，并生成三支低清视频：`media/videos/big_integer_intro_scenes/480p15/BigIntegerOverflowVisualization.mp4`、`media/videos/big_integer_intro_scenes/480p15/BigIntegerStorageVisualization.mp4`、`media/videos/big_integer_intro_scenes/480p15/BigIntegerReverseStorageVisualization.mp4`。
- 已生成预览图 `media/previews/big_integer_overflow_preview.png`、`media/previews/big_integer_storage_preview.png`、`media/previews/big_integer_reverse_storage_preview.png`。
- 前端已新增三节课时，路由为 `/chapters/big-integer/lessons/big-integer-overflow`、`/chapters/big-integer/lessons/big-integer-storage`、`/chapters/big-integer/lessons/big-integer-reverse-storage`。
- 后端已新增 9 道练习：`big-integer-type-range`、`big-integer-raw-echo`、`big-integer-overflow-count`、`big-integer-digit-split`、`big-integer-digit-sum`、`big-integer-digit-frequency`、`big-integer-reverse-store`、`big-integer-reverse-restore`、`big-integer-low-position-query`。
- 已用 TestClient 验证标准解：6/6、3/3、4/4、3/3、4/4、4/4、4/4、4/4、4/4 Accepted。

高精度加法补充：

- 已新增 `manim/scenes/high_precision/big_integer_addition_scene.py`，并生成低清视频 `media/videos/big_integer_addition_scene/480p15/BigIntegerAdditionVisualization.mp4`。
- 已生成预览图 `media/previews/big_integer_addition_preview.png`。
- 前端已新增高精度加法课时，路由为 `/chapters/big-integer/lessons/big-integer-addition`。
- 后端已新增 3 道高精度加法练习：`big-integer-add-basic`、`big-integer-add-trace`、`big-integer-add-multiple`。
- 已用 TestClient 验证三题标准解分别为 5/5、5/5、4/4 Accepted。

高精度减法补充：

- 已新增 `manim/scenes/high_precision/big_integer_subtraction_scene.py`，并生成低清视频 `media/videos/big_integer_subtraction_scene/480p15/BigIntegerSubtractionVisualization.mp4`。
- 已生成预览图 `media/previews/big_integer_subtraction_preview.png`。
- 前端已新增高精度减法课时，路由为 `/chapters/big-integer/lessons/big-integer-subtraction`。
- 后端已新增 3 道高精度减法练习：`big-integer-sub-basic`、`big-integer-sub-borrow-count`、`big-integer-sub-ledger`。
- 已用 TestClient 验证三题标准解分别为 5/5、5/5、4/4 Accepted，并通过真实 HTTP 提交验证 `big-integer-sub-basic` Accepted。

大数比较与符号处理补充：

- 已新增 `manim/scenes/high_precision/big_integer_compare_scene.py`，并生成低清视频 `media/videos/big_integer_compare_scene/480p15/BigIntegerCompareVisualization.mp4`。
- 已生成预览图 `media/previews/big_integer_compare_preview.png`。
- 前端已新增大数比较与符号处理课时，路由为 `/chapters/big-integer/lessons/big-integer-compare-sign`。
- 后端已新增 3 道练习：`big-integer-compare`、`big-integer-sub-signed`、`big-integer-sub-sign-batch`。
- 已用 TestClient 验证三题标准解分别为 5/5、5/5、4/4 Accepted，并通过真实 HTTP 提交验证 `big-integer-compare` Accepted。

高精度乘低精度补充：

- 已新增 `manim/scenes/high_precision/big_integer_multiply_small_scene.py`，并生成低清视频 `media/videos/big_integer_multiply_small_scene/480p15/BigIntegerMultiplySmallVisualization.mp4`。
- 已生成预览图 `media/previews/big_integer_multiply_small_preview.png`。
- 前端已新增高精度乘低精度课时，路由为 `/chapters/big-integer/lessons/big-integer-multiply-small`。
- 后端已新增 3 道练习：`big-integer-mul-small-basic`、`big-integer-mul-small-trace`、`big-integer-factorial-small`。
- 已用 TestClient 验证三题标准解均为 5/5 Accepted，并通过真实 HTTP 提交验证 `big-integer-mul-small-basic` Accepted。
高精度乘高精度补充：

- 已新增 `manim/scenes/high_precision/big_integer_multiply_big_scene.py`，并生成低清视频 `media/videos/big_integer_multiply_big_scene/480p15/BigIntegerMultiplyBigVisualization.mp4`。
- 已生成预览图 `media/previews/big_integer_multiply_big_preview.png`。
- 前端已新增高精度乘高精度课时，路由为 `/chapters/big-integer/lessons/big-integer-multiply-big`。
- 后端已新增 3 道练习：`big-integer-mul-big-basic`、`big-integer-mul-big-grid-trace`、`big-integer-power-small`。
- 已用 TestClient 验证三题标准解均为 5/5 Accepted。

高精度除低精度补充：

- 已新增 `manim/scenes/high_precision/big_integer_divide_small_scene.py`，并生成低清视频 `media/videos/big_integer_divide_small_scene/480p15/BigIntegerDivideSmallVisualization.mp4`。
- 已生成预览图 `media/previews/big_integer_divide_small_preview.png`。
- 前端已新增高精度除低精度课时，路由为 `/chapters/big-integer/lessons/big-integer-divide-small`。
- 后端已新增 3 道练习：`big-integer-div-small-basic`、`big-integer-div-small-quot-rem`、`big-integer-div-small-trace`。
- 已用 TestClient 验证三题标准解均为 5/5 Accepted。

前导零与边界整理补充：

- 已新增 `manim/scenes/high_precision/leading_zero_normalization_scene.py`，并生成低清视频 `media/videos/leading_zero_normalization_scene/480p15/LeadingZeroNormalizationVisualization.mp4`。
- 已生成预览图 `media/previews/leading_zero_normalization_preview.png`。
- 前端已新增前导零与边界整理课时，路由为 `/chapters/big-integer/lessons/big-integer-leading-zero-normalization`。
- 后端已新增 3 道练习：`big-integer-normalize-array`、`big-integer-trim-string`、`big-integer-normalized-calculator`。
- 已用 TestClient 验证三题标准解均为 5/5 Accepted。

高精度综合：阶乘与 Fibonacci 补充：

- 已新增 `manim/scenes/high_precision/big_integer_composite_scene.py`，并生成低清视频 `media/videos/big_integer_composite_scene/480p15/BigIntegerCompositeVisualization.mp4`。
- 已生成预览图 `media/previews/big_integer_composite_preview.png`。
- 前端已新增高精度综合课时，路由为 `/chapters/big-integer/lessons/big-integer-composite-factorial-fibonacci`。
- 后端已新增/复用 3 道练习：`big-integer-factorial-small`、`big-integer-fibonacci`、`big-integer-factorial-sum`。
- 已用 TestClient 验证标准解：阶乘 5/5 Accepted，Fibonacci 6/6 Accepted，阶乘和 5/5 Accepted。

递推算法：什么是状态补充：

- 已新增制作文档 `docs/视频脚本/C03-01-什么是状态.md`，包含详细分镜安排和逐镜头视频脚本。
- 已新增 `manim/scenes/recurrence/state_definition_scene.py`，并生成低清视频 `media/videos/state_definition_scene/480p15/RecurrenceStateVisualization.mp4`。
- 已生成预览图 `media/previews/recurrence_state_preview.png`。
- 前端已新增递推入口课时，路由为 `/chapters/recurrence/lessons/recurrence-state-definition`。
- 后端已新增 3 道练习：`recurrence-climb-stairs-basic`、`recurrence-state-table`、`recurrence-domino-tiling`。
- 已用 TestClient 验证标准解：爬楼梯 6/6 Accepted，状态表 5/5 Accepted，骨牌覆盖 6/6 Accepted。

递推算法：从已知推出未知补充：

- 已新增制作文档 `docs/视频脚本/C03-02-从已知推出未知.md`，包含详细分镜安排和逐镜头视频脚本。
- 已新增 `manim/scenes/recurrence/known_to_unknown_scene.py`，并生成低清视频 `media/videos/known_to_unknown_scene/480p15/RecurrenceKnownToUnknownVisualization.mp4`。
- 已生成预览图 `media/previews/recurrence_known_to_unknown_preview.png`。
- 前端已新增递推第二课时，路由为 `/chapters/recurrence/lessons/recurrence-known-to-unknown`。
- 后端已新增 3 道练习：`recurrence-known-to-unknown-sequence`、`recurrence-new-state-log`、`recurrence-third-order-sequence`。
- 已用 TestClient 验证标准解：第 n 项 6/6 Accepted，新状态输出 5/5 Accepted，三项递推 6/6 Accepted。

递推算法：一维递推：爬楼梯补充：

- 已新增制作文档 `docs/视频脚本/C03-03-一维递推爬楼梯.md`，包含详细分镜安排和逐镜头视频脚本。
- 已新增 `manim/scenes/recurrence/climb_stairs_scene.py`，并生成低清视频 `media/videos/climb_stairs_scene/480p15/RecurrenceClimbStairsVisualization.mp4`。
- 已生成预览图 `media/previews/recurrence_climb_stairs_preview.png`。
- 前端已新增递推第三课时，路由为 `/chapters/recurrence/lessons/recurrence-climb-stairs`。
- 后端已新增 3 道练习：`recurrence-climb-stairs-transition`、`recurrence-climb-stairs-transition-table`、`recurrence-climb-stairs-source-trace`。
- 已用 TestClient 验证标准解：方法数 6/6 Accepted，转移表 5/5 Accepted，来源分解 5/5 Accepted。

递推算法：简单数列：Fibonacci 补充：

- 已新增制作文档 `docs/视频脚本/C03-04-简单数列Fibonacci.md`，包含详细分镜安排和逐镜头视频脚本。
- 已新增 `manim/scenes/recurrence/fibonacci_sequence_scene.py`，并生成低清视频 `media/videos/fibonacci_sequence_scene/480p15/RecurrenceFibonacciSequenceVisualization.mp4`。
- 已生成预览图 `media/previews/recurrence_fibonacci_sequence_preview.png`。
- 前端已新增递推第四课时，路由为 `/chapters/recurrence/lessons/recurrence-fibonacci-sequence`。
- 后端已新增 3 道练习：`recurrence-fibonacci-zero-based`、`recurrence-fibonacci-one-based`、`recurrence-fibonacci-index-table`。
- 已用 TestClient 验证标准解：0-based 6/6 Accepted，1-based 6/6 Accepted，下标对照表 5/5 Accepted。

递推算法：滚动变量优化补充：

- 已新增制作文档 `docs/视频脚本/C03-05-滚动变量优化.md`，包含详细分镜安排和逐镜头视频脚本。
- 已新增 `manim/scenes/recurrence/rolling_variables_scene.py`，并生成低清视频 `media/videos/rolling_variables_scene/480p15/RecurrenceRollingVariablesVisualization.mp4`。
- 已生成预览图 `media/previews/recurrence_rolling_variables_preview.png`。
- 前端已新增递推第五课时，路由为 `/chapters/recurrence/lessons/recurrence-rolling-variables`。
- 后端已新增 3 道练习：`recurrence-rolling-fibonacci`、`recurrence-rolling-climb-stairs`、`recurrence-rolling-trace`。
- 已用 TestClient 验证标准解：滚动 Fibonacci 6/6 Accepted，滚动爬楼梯 6/6 Accepted，滚动过程 5/5 Accepted。

递推算法：二维递推：杨辉三角补充：

- 已新增制作文档 `docs/视频脚本/C03-06-二维递推杨辉三角.md`，包含详细分镜安排和逐镜头视频脚本。
- 已新增 `manim/scenes/recurrence/pascal_triangle_scene.py`，并生成低清视频 `media/videos/pascal_triangle_scene/480p15/RecurrencePascalTriangleVisualization.mp4`。
- 已生成预览图 `media/previews/recurrence_pascal_triangle_preview.png`。
- 前端已新增递推第六课时，路由为 `/chapters/recurrence/lessons/recurrence-pascal-triangle`。
- 后端已新增 3 道练习：`recurrence-pascal-triangle-row`、`recurrence-pascal-triangle-table`、`recurrence-pascal-triangle-query`。
- 已用 TestClient 验证标准解：第 n 行 6/6 Accepted，前 n 行 5/5 Accepted，单点查询 7/7 Accepted。

递推算法：路径计数：走方格补充：

- 已新增制作文档 `docs/视频脚本/C03-07-路径计数走方格.md`，包含详细分镜安排和逐镜头视频脚本。
- 已新增 `manim/scenes/recurrence/grid_paths_scene.py`，并生成低清视频 `media/videos/grid_paths_scene/480p15/RecurrenceGridPathsVisualization.mp4`。
- 已生成预览图 `media/previews/recurrence_grid_paths_preview.png`。
- 前端已新增递推第七课时，路由为 `/chapters/recurrence/lessons/recurrence-grid-paths`。
- 后端已新增 3 道练习：`recurrence-grid-paths-basic`、`recurrence-grid-paths-table`、`recurrence-grid-paths-obstacle`。
- 已用 TestClient 验证标准解：基础路径数 7/7 Accepted，路径计数表 5/5 Accepted，带障碍路径数 7/7 Accepted，并通过真实 HTTP 提交验证 `recurrence-grid-paths-obstacle` Accepted。

递推算法：数塔递推补充：

- 已新增制作文档 `docs/视频脚本/C03-08-数塔递推.md`，包含详细分镜安排和逐镜头视频脚本。
- 已新增 `manim/scenes/recurrence/number_tower_scene.py`，并生成高清视频 `media/videos/number_tower_scene/1080p60/RecurrenceNumberTowerVisualization.mp4`。
- 已生成预览图 `media/previews/recurrence_number_tower_preview.png`。
- 前端已新增递推第八课时，路由为 `/chapters/recurrence/lessons/recurrence-number-tower`。
- 后端已新增 3 道练习：`recurrence-number-tower-basic`、`recurrence-number-tower-table`、`recurrence-number-tower-min`。
- 已用本地判题器验证标准解：最大路径和 6/6 Accepted，递推表 4/4 Accepted，最小路径和 5/5 Accepted。

递推算法：初始条件与边界补充：

- 已新增制作文档 `docs/视频脚本/C03-09-初始条件与边界.md`，包含边界错误诊断分镜、逐镜头字幕、代码映射和练习衔接。
- 已新增 `manim/scenes/recurrence/initial_conditions_boundary_scene.py`，并生成低清视频 `media/videos/initial_conditions_boundary_scene/480p15/RecurrenceInitialBoundaryVisualization.mp4`。
- 已生成预览图 `media/previews/recurrence_initial_boundary_preview.png`。
- 前端已新增递推第九课时，路由为 `/chapters/recurrence/lessons/recurrence-initial-conditions-boundary`。
- 后端已新增 3 道练习：`recurrence-boundary-climb-stairs`、`recurrence-boundary-state-table`、`recurrence-boundary-grid-sentinel`。
- 已用本地判题器验证标准解：边界版爬楼梯 7/7、递推状态表 5/5、哨兵边界走方格 8/8 Accepted。
- 第三章已新增 7 题总结测验、6 项掌握清单、3 组回刷题包，并覆盖全章 27 道练习的分层题解。

递归算法第四章补充：

- 已新增 9 份制作文档：`docs/视频脚本/C04-01-函数为什么能调用自己.md` 至 `C04-09-递归调试方法.md`。
- 已新增 `manim/scenes/recursion/recursion_chapter_scenes.py`，包含 9 个统一视觉语言、各自独立的递归动画场景。
- 已生成 9 支 1080p60 视频，统一位于 `media/videos/recursion_chapter_scenes/1080p60/`，并生成 9 张课程预览图。
- 前端第四章状态已切换为 `ready`，新增 9 个课时页、章节总结测验、掌握清单和 3 组回刷题包。
- 后端已新增 27 道递归练习，覆盖出口、参数、调用栈、阶乘、Fibonacci、汉诺塔、树遍历与递归调试。
- 已用本地判题器验证 9 个代表性标准解，修正一处回收阶段空格格式后全部 Accepted；完整 demo 一致性检查与前端生产构建均通过。

搜索与回溯第五章补充：

- 前端已新增枚举与搜索树、DFS 基本框架、选择/递归/撤销、全排列、组合、子集、迷宫 DFS、剪枝、N 皇后与回溯复杂度 10 个课时。
- 后端已新增 20 道可判题练习，代码定义集中在 `backend/app/content/search_problems.py`。
- 章节页已接入 6 题总结测验、6 项掌握清单和 3 组回刷题包；20 道题均有分层提示、题解要点与常见坑。
- `docs/视频脚本/C05-01-枚举与搜索树.md` 至 `C05-10-回溯复杂度直觉.md` 已完成逐镜头制作脚本；当前课时页会显示清晰的视频制作中状态，避免空播放器。
- 20 道标准解已经本地 C++17 判题全部 Accepted，第五章前后端题目 ID 20/20 对齐，Vite 生产构建通过。

分治算法第七章补充：

- 前端已新增分治框架、二分查找、边界二分、归并排序、快速排序、快速幂、逆序对与递归树复杂度 8 个课时。
- 后端已新增 16 道可判题练习，代码定义集中在 `backend/app/content/divide_conquer_problems.py`。
- 章节页已接入 6 题总结测验、6 项掌握清单和 3 组回刷题包；16 道题均有分层提示、题解要点与常见坑。
- `docs/视频脚本/C07-01-分解解决合并.md` 至 `C07-08-递归树复杂度.md` 已完成逐镜头制作脚本，完整映射见 `docs/第七章内容生产清单.md`。
- 16 道参考代码已经用 C++17 编译并跑过全部 65 个公开与隐藏测试点，前端生产构建通过。

计数排序补充：

- 已新增 `manim/scenes/sorting/counting_sort_scene.py`，并生成低清视频 `media/videos/counting_sort_scene/480p15/CountingSortVisualization.mp4`。
- 前端已新增计数排序课时，路由为 `/chapters/sorting/lessons/counting-sort`。
- 后端已新增 3 道计数排序练习：`counting-sort-basic`、`counting-sort-frequency`、`counting-sort-offset`。
- 已用 TestClient 验证三题标准解均为 4/4 Accepted。

归并排序补充：

- 已新增 `manim/scenes/sorting/merge_sort_scene.py`，并生成低清视频 `media/videos/merge_sort_scene/480p15/MergeSortVisualization.mp4`。
- 前端已新增归并排序课时，路由为 `/chapters/sorting/lessons/merge-sort`。
- 后端已新增 3 道归并排序练习：`merge-sort-basic`、`merge-two-sorted-arrays`、`merge-sort-inversions`。
- 已用 TestClient 验证三题标准解均为 4/4 Accepted。

快速排序补充：

- 已新增 `manim/scenes/sorting/quick_sort_scene.py`，并生成低清视频 `media/videos/quick_sort_scene/480p15/QuickSortVisualization.mp4`。
- 前端已新增快速排序初步课时，路由为 `/chapters/sorting/lessons/quick-sort`。
- 后端已新增 3 道快速排序练习：`quick-sort-basic`、`quick-sort-partition`、`quick-select-kth`。
- 已用 TestClient 验证三题标准解均为 4/4 Accepted。

依赖审计提示：当前 `@monaco-editor/react` 依赖链中的 `monaco-editor -> dompurify` 会触发 `npm audit --omit=dev` 的低/中危提示，且 npm 暂无自动修复版本。MVP 本地开发可继续使用，正式部署前需要重新评估编辑器依赖、版本升级或前端隔离策略。

## 临时 OJ 后端

后端骨架位于 `backend/`，使用 FastAPI，并内置高精度入门、加法、高精度减法、大数比较与符号处理、高精度乘低精度、高精度乘高精度、高精度除低精度、前导零与边界整理、高精度综合、递推入门、Fibonacci 数列、滚动变量优化、杨辉三角、路径计数、数塔递推、冒泡排序、选择排序、插入排序、计数排序、归并排序和快速排序练习的本地 C++ 判题：

```powershell
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

健康检查：

```text
http://127.0.0.1:8000/api/health
```

当前本地判题器仅用于 MVP 开发验证，正式部署前需要替换为 Docker 沙箱或外部 OJ Adapter。

后端已经抽出 Judge Adapter 边界：

```text
JudgeService -> LocalJudge
             -> DockerJudge
```

当前默认：

```text
JUDGE_ADAPTER=local-process
```

可选 Docker 判题器：

```powershell
$env:JUDGE_ADAPTER="docker"
$env:JUDGE_DOCKER_IMAGE="gcc:13"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

当前机器能检测到 Docker CLI，但 Docker daemon 未启动，因此默认仍使用本地进程判题器。

提交记录会写入本地 SQLite：

```text
backend/app/.data/submissions.sqlite3
```

这个目录已加入 `.gitignore`。当前可用接口：

```text
GET  /api/submissions?problem_id=bubble-sort-basic&limit=8
GET  /api/submissions/{submission_id}
POST /api/submissions
GET  /api/stats/submissions
GET  /api/judge
```

前端默认调用后端地址：

```text
http://127.0.0.1:8000
```
