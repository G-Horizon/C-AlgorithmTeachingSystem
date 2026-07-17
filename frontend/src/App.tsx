import {
  Activity,
  BarChart3,
  BookOpen,
  CheckCircle2,
  ChevronRight,
  CircleDot,
  ClipboardCheck,
  Code2,
  FileTerminal,
  FlaskConical,
  HelpCircle,
  Lightbulb,
  ListChecks,
  PlayCircle,
  RefreshCw,
  RotateCcw,
  Send,
  Target,
  Timer,
  Trophy,
} from "lucide-react";
import Editor from "@monaco-editor/react";
import { useCallback, useEffect, useMemo, useState } from "react";
import { Navigate, NavLink, Route, Routes, useParams } from "react-router-dom";
import { chapters, findProblem, firstLessonPath, type Chapter, type Lesson } from "./data/curriculum";
import {
  getChapterSummaryQuiz,
  getProblemGuide,
  type ChapterSummaryQuiz,
  type ProblemGuide,
} from "./data/support";

const API_BASE_URL = "http://127.0.0.1:8000";
const DRAFT_PREFIX = "algorithm-learning:draft:";
const HISTORY_PREFIX = "algorithm-learning:history:";
const PROGRESS_KEY = "algorithm-learning:progress:v1";
const SIDEBAR_COLLAPSED_KEY = "algorithm-learning:sidebar-collapsed:v1";
const HISTORY_LIMIT = 8;
const DASHBOARD_SUBMISSION_LIMIT = 100;

const DEMO_STUDENT_PROFILES: DemoStudentProfile[] = [
  { id: "lin", name: "林一航", group: "A 组" },
  { id: "momo", name: "莫小满", group: "A 组" },
  { id: "chen", name: "陈序", group: "B 组" },
  { id: "yue", name: "岳晴", group: "B 组" },
  { id: "anon-1", name: "演示学生 1", group: "体验组" },
  { id: "anon-2", name: "演示学生 2", group: "体验组" },
];

function App() {
  const learning = useLearningProgress();
  const [sidebarCollapsed, setSidebarCollapsed] = useState(() => loadSidebarCollapsed());
  const courseSummary = useMemo(
    () => summarizeCourseProgress(chapters, learning.progress),
    [learning.progress],
  );
  const continuePath = useMemo(
    () => findContinuePath(chapters, learning.progress),
    [learning.progress],
  );

  useEffect(() => {
    saveSidebarCollapsed(sidebarCollapsed);
  }, [sidebarCollapsed]);

  return (
    <div className={`app-shell ${sidebarCollapsed ? "sidebar-collapsed" : ""}`}>
      <aside className="sidebar" aria-label="课程导航">
        <div className="sidebar-top">
          <div className="brand">
          <div className="brand-mark">C++</div>
          <div>
            <p className="eyebrow">算法可视化</p>
            <h1>学习工作台</h1>
          </div>
          </div>
          <button
            type="button"
            className={`sidebar-toggle ${sidebarCollapsed ? "" : "expanded"}`}
            aria-label={sidebarCollapsed ? "展开章节导航" : "收起章节导航"}
            aria-expanded={!sidebarCollapsed}
            title={sidebarCollapsed ? "展开章节导航" : "收起章节导航"}
            onClick={() => setSidebarCollapsed((current) => !current)}
          >
            <ChevronRight size={18} />
          </button>
        </div>

        <section className="learning-overview" aria-label="学习进度">
          <div className="learning-overview-head">
            <span>学习进度</span>
            <strong>{courseSummary.percent}%</strong>
          </div>
          <div className="progress-meter" aria-hidden="true">
            <span style={{ width: `${courseSummary.percent}%` }} />
          </div>
          <p>
            {courseSummary.completedLessons}/{courseSummary.totalLessons} 课时 ·{" "}
            {courseSummary.acceptedProblems}/{courseSummary.totalProblems} 题已通过
          </p>
          <NavLink className="continue-learning-link" to={continuePath}>
            <PlayCircle size={16} />
            继续学习
          </NavLink>
        </section>

        <nav className="utility-nav" aria-label="工作台导航">
          <NavLink
            to="/stats"
            title="提交统计"
            aria-label="提交统计"
            className={({ isActive }) => `chapter-link utility-link ${isActive ? "active" : ""}`}
          >
            <BarChart3 size={18} />
            <span>
              <strong>提交统计</strong>
              <small>通过率、错误分布与最近提交</small>
            </span>
          </NavLink>
        </nav>

        <nav className="chapter-nav" aria-label="章节导航">
          {chapters.map((chapter) => {
            const Icon = chapter.icon;
            const lesson = chapter.lessons[0];
            const chapterSummary = summarizeChapterProgress(chapter, learning.progress);
            const to = lesson
              ? `/chapters/${chapter.id}/lessons/${lesson.id}`
              : `/chapters/${chapter.id}`;

            return (
              <NavLink
                key={chapter.id}
                to={to}
                title={`${chapter.order}. ${chapter.title}`}
                aria-label={`${chapter.order}. ${chapter.title}`}
                className={({ isActive }) =>
                  `chapter-link ${isActive ? "active" : ""} ${chapter.status}`
                }
              >
                <Icon size={18} />
                <span>
                  <strong>
                    {chapter.order}. {chapter.title}
                  </strong>
                  <small>{chapter.subtitle}</small>
                  <span className="chapter-progress-mini" aria-hidden="true">
                    <span style={{ width: `${chapterSummary.percent}%` }} />
                  </span>
                  <small className="chapter-progress-text">
                    {chapterSummary.completedLessons}/{chapterSummary.totalLessons} 课时 ·{" "}
                    {chapterSummary.acceptedProblems}/{chapterSummary.totalProblems} 题
                  </small>
                </span>
              </NavLink>
            );
          })}
        </nav>
      </aside>

      <main className="workspace">
        <Routes>
          <Route path="/" element={<Navigate to={firstLessonPath} replace />} />
          <Route path="/stats" element={<StatsDashboard />} />
          <Route path="/chapters/:chapterId" element={<ChapterPlaceholder />} />
          <Route
            path="/chapters/:chapterId/lessons/:lessonId"
            element={
              <LessonPage
                progress={learning.progress}
                onSetLessonComplete={learning.setLessonComplete}
              />
            }
          />
          <Route
            path="/problems/:problemId"
            element={
              <ProblemPage
                progress={learning.progress}
                onProblemAccepted={learning.markProblemAccepted}
              />
            }
          />
          <Route path="*" element={<Navigate to={firstLessonPath} replace />} />
        </Routes>
      </main>
    </div>
  );
}

function ChapterPlaceholder() {
  const { chapterId } = useParams();
  const chapter = chapters.find((item) => item.id === chapterId) ?? chapters[0];
  const Icon = chapter.icon;

  return (
    <section className="placeholder-view">
      <Icon size={34} />
      <p className="eyebrow">第 {chapter.order} 章</p>
      <h2>{chapter.title}</h2>
      <p>{chapter.subtitle}</p>
      <div className="next-strip">
        <CircleDot size={18} />
        <span>该章节的视频、讲义与练习将在排序章节样板完成后继续补齐。</span>
      </div>
    </section>
  );
}

type LessonPageProps = {
  progress: LearningProgress;
  onSetLessonComplete: (lessonId: string, complete: boolean) => void;
};

function LessonPage({ progress, onSetLessonComplete }: LessonPageProps) {
  const { chapterId, lessonId } = useParams();
  const chapter = chapters.find((item) => item.id === chapterId) ?? chapters[1];
  const lesson = chapter.lessons.find((item) => item.id === lessonId) ?? chapter.lessons[0];

  if (!lesson) {
    return <Navigate to={firstLessonPath} replace />;
  }

  const lessonProgress = summarizeLessonProgress(lesson, progress);
  const recommendedProblem = lesson.problems.find((problem) => !progress.acceptedProblems[problem.id]);
  const nextLessonPath = findNextLessonPath(chapter.id, lesson.id);
  const recommendedPath = recommendedProblem
    ? `/problems/${recommendedProblem.id}`
    : nextLessonPath ?? "/stats";
  const chapterQuiz = getChapterSummaryQuiz(chapter.id);
  const recommendedLabel = recommendedProblem
    ? "继续练习"
    : nextLessonPath
      ? "进入下一课"
      : "查看统计看板";

  return (
    <div className="lesson-layout">
      <section className="lesson-main">
        <div className="lesson-heading">
          <div>
            <p className="eyebrow">
              第 {chapter.order} 章 / {chapter.title}
            </p>
            <h2>{lesson.title}</h2>
            <p>{lesson.summary}</p>
          </div>
          <div className="lesson-heading-actions">
            <div className="duration-pill">
              <Timer size={16} />
              {lesson.duration}
            </div>
            <button
              type="button"
              className={`complete-button ${lessonProgress.completed ? "done" : ""}`}
              onClick={() => onSetLessonComplete(lesson.id, !lessonProgress.completed)}
            >
              <CheckCircle2 size={16} />
              {lessonProgress.completed ? "已完成" : "标记完成"}
            </button>
          </div>
        </div>

        <div className="video-panel">
          <video
            controls
            preload="metadata"
            poster={lesson.previewImage}
            src={lesson.videoUrl}
          />
        </div>

        <section className="concept-band" aria-label="核心概念">
          {lesson.concepts.map((concept) => (
            <span key={concept}>{concept}</span>
          ))}
        </section>

        <section className="notes-grid">
          <article>
            <div className="section-title">
              <BookOpen size={18} />
              <h3>理解路径</h3>
            </div>
            <ol className="steps">
              {lesson.steps.map((step) => (
                <li key={step}>{step}</li>
              ))}
            </ol>
          </article>

          <article>
            <div className="section-title">
              <Code2 size={18} />
              <h3>C++ 代码</h3>
            </div>
            <pre className="code-block">
              <code>{lesson.code}</code>
            </pre>
          </article>
        </section>

        {chapterQuiz && (
          <ChapterSummaryQuizPanel quiz={chapterQuiz} chapter={chapter} progress={progress} />
        )}
      </section>

      <aside className="practice-panel">
        <div className="section-title">
          <BookOpen size={18} />
          <h3>课时</h3>
        </div>

        <div className="lesson-switch-list">
          {chapter.lessons.map((item) => {
            const itemProgress = summarizeLessonProgress(item, progress);
            return (
              <NavLink
                className={({ isActive }) =>
                  `lesson-switch ${isActive ? "active" : ""} ${itemProgress.completed ? "completed" : ""}`
                }
                key={item.id}
                to={`/chapters/${chapter.id}/lessons/${item.id}`}
              >
                <span>{item.title}</span>
                <span className="switch-meta">
                  {itemProgress.completed && <CheckCircle2 size={15} />}
                  <ChevronRight size={16} />
                </span>
              </NavLink>
            );
          })}
        </div>

        <div className="section-title">
          <ListChecks size={18} />
          <h3>练习</h3>
        </div>

        <div className="problem-list">
          {lesson.problems.map((problem) => {
            const accepted = Boolean(progress.acceptedProblems[problem.id]);
            return (
              <article className={`problem-card ${accepted ? "accepted" : ""}`} key={problem.id}>
                <div>
                  <div className="problem-card-topline">
                    <span className={`difficulty ${problem.difficulty}`}>{problem.difficulty}</span>
                    <span className={`problem-state ${accepted ? "accepted" : ""}`}>
                      {accepted ? "已通过" : "待练习"}
                    </span>
                  </div>
                  <h4>{problem.title}</h4>
                  <p>{problem.focus}</p>
                </div>
                <NavLink className={`problem-action ${accepted ? "accepted" : ""}`} to={`/problems/${problem.id}`}>
                  {accepted ? <CheckCircle2 size={16} /> : <FlaskConical size={16} />}
                  {accepted ? "查看题目" : "开始练习"}
                </NavLink>
              </article>
            );
          })}
        </div>

        <div className="progress-box">
          <div>
            <CheckCircle2 size={18} />
            <strong>本课进度</strong>
          </div>
          <div className="lesson-progress-grid">
            <span>
              课时状态
              <strong>{lessonProgress.completed ? "已完成" : "进行中"}</strong>
            </span>
            <span>
              练习通过
              <strong>
                {lessonProgress.acceptedProblems}/{lessonProgress.totalProblems}
              </strong>
            </span>
          </div>
          <p>看完视频和讲义后可以手动标记课时；题目获得 Accepted 后会自动计入进度。</p>
          <NavLink className="inline-action" to={recommendedPath}>
            <PlayCircle size={16} />
            {recommendedLabel}
            <ChevronRight size={16} />
          </NavLink>
        </div>

      </aside>
    </div>
  );
}

function ChapterSummaryQuizPanel({
  quiz,
  chapter,
  progress,
}: {
  quiz: ChapterSummaryQuiz;
  chapter: Chapter;
  progress: LearningProgress;
}) {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const chapterSummary = summarizeChapterProgress(chapter, progress);
  const problemById = useMemo(() => {
    const next = new Map<string, { id: string; title: string }>();
    chapter.lessons.forEach((lesson) => {
      lesson.problems.forEach((problem) => {
        if (!next.has(problem.id)) {
          next.set(problem.id, { id: problem.id, title: problem.title });
        }
      });
    });
    return next;
  }, [chapter]);
  const answeredCount = quiz.questions.filter((question) => answers[question.id]).length;
  const correctCount = quiz.questions.filter((question) => answers[question.id] === question.answer).length;

  return (
    <section className="chapter-summary-panel" aria-label={quiz.title}>
      <div className="section-title">
        <ClipboardCheck size={18} />
        <h3>章节总结</h3>
      </div>
      <p className="chapter-summary-copy">{quiz.summary}</p>

      <div className="chapter-summary-score">
        <span>
          章节进度
          <strong>{chapterSummary.percent}%</strong>
        </span>
        <span>
          小测结果
          <strong>
            {correctCount}/{quiz.questions.length}
          </strong>
        </span>
      </div>

      <div className="chapter-checklist">
        {quiz.checklist.map((item) => (
          <div key={item}>
            <CheckCircle2 size={15} />
            <span>{item}</span>
          </div>
        ))}
      </div>

      <div className="summary-quiz">
        <div className="summary-quiz-head">
          <strong>收束测验</strong>
          <span>
            {answeredCount}/{quiz.questions.length}
          </span>
        </div>
        {quiz.questions.map((question, index) => {
          const selected = answers[question.id];
          return (
            <div className="quiz-question" key={question.id}>
              <p>
                {index + 1}. {question.prompt}
              </p>
              <div className="quiz-options">
                {question.options.map((option) => {
                  const isSelected = selected === option.id;
                  const isCorrectChoice = Boolean(selected) && option.id === question.answer;
                  const isWrongSelected = isSelected && selected !== question.answer;
                  return (
                    <button
                      type="button"
                      className={`quiz-option ${isSelected ? "selected" : ""} ${
                        isCorrectChoice ? "correct" : ""
                      } ${isWrongSelected ? "wrong" : ""}`}
                      key={option.id}
                      onClick={() =>
                        setAnswers((current) => ({ ...current, [question.id]: option.id }))
                      }
                    >
                      <strong>{option.id}</strong>
                      <span>{option.text}</span>
                    </button>
                  );
                })}
              </div>
              {selected && (
                <div className="quiz-explanation">
                  <HelpCircle size={15} />
                  <span>{question.explanation}</span>
                </div>
              )}
            </div>
          );
        })}
      </div>

      <div className="review-pack-list">
        <strong>回刷题包</strong>
        {quiz.reviewPlan.map((pack) => (
          <div className="review-pack" key={pack.title}>
            <span>{pack.title}</span>
            <p>{pack.description}</p>
            <div className="review-links">
              {pack.problemIds.map((problemId) => {
                const problem = problemById.get(problemId);
                return (
                  <NavLink className="review-link" to={`/problems/${problemId}`} key={problemId}>
                    {problem?.title ?? problemId}
                  </NavLink>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

type ProblemPageProps = {
  progress: LearningProgress;
  onProblemAccepted: (problemId: string) => void;
};

function ProblemPage({ progress, onProblemAccepted }: ProblemPageProps) {
  const { problemId = "" } = useParams();
  const context = useMemo(() => findProblem(problemId), [problemId]);
  const [sourceCode, setSourceCode] = useState(() =>
    context ? loadDraft(context.problem.id, context.problem.starterCode) : "",
  );
  const [draftProblemId, setDraftProblemId] = useState(context?.problem.id ?? "");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<SubmissionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [judgeInfo, setJudgeInfo] = useState<JudgeInfo | null>(null);
  const [history, setHistory] = useState<SubmissionHistoryItem[]>(() =>
    context ? loadSubmissionHistory(context.problem.id) : [],
  );

  useEffect(() => {
    if (!context) {
      return;
    }

    setSourceCode(loadDraft(context.problem.id, context.problem.starterCode));
    setDraftProblemId(context.problem.id);
    setHistory(loadSubmissionHistory(context.problem.id));
    setResult(null);
    setError(null);

    let cancelled = false;
    const activeProblemId = context.problem.id;

    async function loadServerHistory() {
      try {
        const response = await fetch(
          `${API_BASE_URL}/api/submissions?problem_id=${encodeURIComponent(activeProblemId)}&limit=${HISTORY_LIMIT}`,
        );

        if (!response.ok) {
          return;
        }

        const records = (await response.json()) as SubmissionRecord[];
        const next = records.map(recordToHistoryItem);
        if (!cancelled) {
          setHistory(next);
          saveSubmissionHistory(activeProblemId, next);
          if (next.some((item) => item.status === "Accepted")) {
            onProblemAccepted(activeProblemId);
          }
        }
      } catch {
        // Keep the local history fallback when the MVP backend is not running.
      }
    }

    void loadServerHistory();

    return () => {
      cancelled = true;
    };
  }, [context, onProblemAccepted]);

  useEffect(() => {
    if (!context) {
      return;
    }

    if (history.some((item) => item.status === "Accepted")) {
      onProblemAccepted(context.problem.id);
    }
  }, [context, history, onProblemAccepted]);

  useEffect(() => {
    let cancelled = false;

    async function loadJudgeInfo() {
      try {
        const response = await fetch(`${API_BASE_URL}/api/judge`);
        if (!response.ok) {
          return;
        }

        const payload = (await response.json()) as JudgeInfo;
        if (!cancelled) {
          setJudgeInfo(payload);
        }
      } catch {
        if (!cancelled) {
          setJudgeInfo(null);
        }
      }
    }

    void loadJudgeInfo();

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (!context) {
      return;
    }

    if (draftProblemId !== context.problem.id) {
      return;
    }

    saveDraft(context.problem.id, sourceCode);
  }, [context, draftProblemId, sourceCode]);

  if (!context) {
    return <Navigate to={firstLessonPath} replace />;
  }

  const { chapter, lesson, problem } = context;
  const problemGuide = getProblemGuide(problem.id);
  const passedCases = result?.cases.filter((caseResult) => caseResult.status === "Accepted").length ?? 0;

  function resetCode() {
    setSourceCode(problem.starterCode);
    setResult(null);
    setError(null);
  }

  async function submitCode() {
    setSubmitting(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/submissions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          problem_id: problem.id,
          language: "cpp",
          source_code: sourceCode,
        }),
      });

      const payload = (await response.json()) as SubmissionResult | { detail?: string };
      if (!response.ok) {
        throw new Error("detail" in payload && payload.detail ? payload.detail : "提交失败");
      }

      const judged = payload as SubmissionResult;
      setResult(judged);
      setHistory((current) => {
        const record = createHistoryItem(judged, sourceCode);
        const next = [record, ...current].slice(0, HISTORY_LIMIT);
        saveSubmissionHistory(problem.id, next);
        return next;
      });
      if (judged.status === "Accepted") {
        onProblemAccepted(problem.id);
      }
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "提交失败，请确认后端服务已启动。");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="problem-layout">
      <section className="problem-workbench">
        <div className="lesson-heading">
          <div>
            <p className="eyebrow">
              {chapter.title} / {lesson.title}
            </p>
            <h2>{problem.title}</h2>
            <p>{problem.focus}</p>
          </div>
          <div className="lesson-heading-actions">
            {progress.acceptedProblems[problem.id] && (
              <span className="accepted-badge">
                <CheckCircle2 size={16} />
                已通过
              </span>
            )}
            <NavLink className="inline-link" to={`/chapters/${chapter.id}/lessons/${lesson.id}`}>
              <PlayCircle size={16} />
              回到课程
            </NavLink>
          </div>
        </div>

        <div className="editor-shell">
          <div className="editor-toolbar">
            <div>
              <FileTerminal size={18} />
              <strong>C++17 · 自动保存</strong>
            </div>
            <div className="toolbar-actions">
              <button type="button" onClick={resetCode}>
                <RotateCcw size={16} />
                重置
              </button>
              <button type="button" className="primary-button" onClick={submitCode} disabled={submitting}>
                <Send size={16} />
                {submitting ? "提交中" : "提交"}
              </button>
            </div>
          </div>
          <div className="monaco-host">
            <Editor
              height="560px"
              language="cpp"
              theme="vs-dark"
              value={sourceCode}
              loading={<div className="editor-loading">编辑器加载中...</div>}
              options={{
                automaticLayout: true,
                fontFamily: 'Consolas, "Cascadia Code", monospace',
                fontSize: 14,
                insertSpaces: true,
                lineNumbers: "on",
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                tabSize: 4,
                wordWrap: "on",
              }}
              onChange={(value) => setSourceCode(value ?? "")}
            />
          </div>
        </div>

        {problemGuide && <ProblemGuidePanel guide={problemGuide} problemId={problem.id} />}
      </section>

      <aside className="result-panel">
        <div className="section-title">
          <ListChecks size={18} />
          <h3>判题结果</h3>
        </div>

        {judgeInfo && (
          <div className="judge-info-box">
            <strong>{judgeInfo.display_name}</strong>
            <span>{judgeInfo.isolation}</span>
          </div>
        )}

        <div className={`problem-progress-note ${progress.acceptedProblems[problem.id] ? "accepted" : ""}`}>
          <CheckCircle2 size={18} />
          <span>
            {progress.acceptedProblems[problem.id]
              ? "本题已计入学习进度。"
              : "获得一次 Accepted 后，本题会自动点亮。"}
          </span>
        </div>

        {error && <div className="error-box">{error}</div>}

        {!error && !result && (
          <div className="empty-result">
            <CircleDot size={18} />
            <p>后端默认地址：{API_BASE_URL}。提交后会保存记录并显示测试点反馈。</p>
          </div>
        )}

        {result && (
          <div className="submission-result">
            <div className={`status-banner ${statusClass(result.status)}`}>
              <strong>{result.status}</strong>
              <span>
                {passedCases}/{result.cases.length} 个测试点通过
              </span>
            </div>

            {result.compile_output && <pre className="judge-output">{result.compile_output}</pre>}
            {result.message && <p className="judge-message">{result.message}</p>}

            <div className="case-list">
              {result.cases.map((caseResult) => (
                <article className="case-card" key={caseResult.index}>
                  <div className="case-card-header">
                    <strong>测试点 {caseResult.index}</strong>
                    <span className={statusClass(caseResult.status)}>{caseResult.status}</span>
                  </div>
                  <p className="case-meta">
                    {caseResult.hidden ? "隐藏测试点" : "样例/公开测试点"}
                    {caseResult.run_time_ms != null ? ` · ${caseResult.run_time_ms} ms` : ""}
                  </p>
                  {!caseResult.hidden && (
                    <div className="case-io-grid">
                      <CaseOutput label="输入" value={caseResult.input} />
                      <CaseOutput label="期望输出" value={caseResult.expected_output} />
                      <CaseOutput label="你的输出" value={caseResult.actual_output} />
                    </div>
                  )}
                  {caseResult.message && <p className="judge-message">{caseResult.message}</p>}
                </article>
              ))}
            </div>
          </div>
        )}

        <section className="history-section" aria-label="提交记录">
          <div className="section-title">
            <Timer size={18} />
            <h3>最近提交</h3>
          </div>

          {history.length === 0 ? (
            <p className="muted-text">本题还没有提交记录。</p>
          ) : (
            <div className="history-list">
              {history.map((item) => (
                <button
                  type="button"
                  className={`history-card ${statusClass(item.status)}`}
                  key={item.id}
                  onClick={() => {
                    setSourceCode(item.sourceCode);
                    setResult(item.result);
                    setError(null);
                  }}
                >
                  <span>
                    <strong>{item.status}</strong>
                    <small>{formatTime(item.submittedAt)}</small>
                  </span>
                  <span>
                    {item.passedCases}/{item.totalCases}
                  </span>
                </button>
              ))}
            </div>
          )}
        </section>
      </aside>
    </div>
  );
}

function ProblemGuidePanel({ guide, problemId }: { guide: ProblemGuide; problemId: string }) {
  const [visibleHints, setVisibleHints] = useState(() => Math.min(1, guide.hints.length));

  useEffect(() => {
    setVisibleHints(Math.min(1, guide.hints.length));
  }, [guide, problemId]);

  const shownHints = guide.hints.slice(0, visibleHints);

  return (
    <section className="problem-guide-panel" aria-label="题目提示与题解">
      <div className="section-title">
        <Lightbulb size={18} />
        <h3>提示阶梯</h3>
      </div>

      <div className="guide-hint-list">
        {shownHints.map((hint, index) => (
          <div className="guide-hint" key={hint}>
            <span>{index + 1}</span>
            <p>{hint}</p>
          </div>
        ))}
      </div>

      {visibleHints < guide.hints.length && (
        <button
          type="button"
          className="guide-reveal-button"
          onClick={() => setVisibleHints((current) => Math.min(current + 1, guide.hints.length))}
        >
          <Lightbulb size={16} />
          显示下一条提示
        </button>
      )}

      <details className="guide-details">
        <summary>题解要点</summary>
        <ol>
          {guide.solution.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ol>
      </details>

      <details className="guide-details">
        <summary>常见坑</summary>
        <ul>
          {guide.pitfalls.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </details>
    </section>
  );
}

function StatsDashboard() {
  const [stats, setStats] = useState<SubmissionStatsSummary | null>(null);
  const [recentSubmissions, setRecentSubmissions] = useState<SubmissionRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [refreshIndex, setRefreshIndex] = useState(0);

  useEffect(() => {
    let cancelled = false;

    async function loadStats() {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`${API_BASE_URL}/api/stats/submissions`);
        if (!response.ok) {
          throw new Error("统计接口返回异常");
        }

        const payload = (await response.json()) as SubmissionStatsSummary;
        let submissionPayload: SubmissionRecord[] = [];

        try {
          const submissionsResponse = await fetch(
            `${API_BASE_URL}/api/submissions?limit=${DASHBOARD_SUBMISSION_LIMIT}`,
          );
          if (submissionsResponse.ok) {
            submissionPayload = (await submissionsResponse.json()) as SubmissionRecord[];
          }
        } catch {
          submissionPayload = [];
        }

        if (!cancelled) {
          setStats(payload);
          setRecentSubmissions(submissionPayload);
        }
      } catch (caught) {
        if (!cancelled) {
          setError(caught instanceof Error ? caught.message : "无法读取提交统计，请确认后端服务已启动。");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void loadStats();

    return () => {
      cancelled = true;
    };
  }, [refreshIndex]);

  const teacherInsight = useMemo(() => {
    if (!stats) {
      return null;
    }

    return buildTeacherDashboardInsight(stats, recentSubmissions);
  }, [stats, recentSubmissions]);

  const mostSubmitted = useMemo(() => {
    if (!stats) {
      return null;
    }

    return stats.problems.reduce<ProblemSubmissionStats | null>((best, item) => {
      if (!best || item.total_submissions > best.total_submissions) {
        return item;
      }
      return best;
    }, null);
  }, [stats]);

  const latestAccepted = useMemo(() => {
    if (!stats) {
      return null;
    }

    return stats.problems.reduce<ProblemSubmissionStats | null>((best, item) => {
      if (!item.last_accepted_at) {
        return best;
      }
      if (!best?.last_accepted_at || item.last_accepted_at > best.last_accepted_at) {
        return item;
      }
      return best;
    }, null);
  }, [stats]);

  return (
    <div className="stats-page">
      <section className="stats-header">
        <div>
          <p className="eyebrow">临时 OJ 数据</p>
          <h2>提交统计看板</h2>
          <p>观察练习热度、通过情况和错误分布，帮助后续按学生反馈调整讲解与练习梯度。</p>
        </div>
        <button
          type="button"
          className="inline-link dashboard-refresh"
          onClick={() => setRefreshIndex((value) => value + 1)}
          disabled={loading}
        >
          <RefreshCw size={16} />
          刷新
        </button>
      </section>

      {loading && !stats && (
        <div className="stats-state">
          <CircleDot size={18} />
          <span>正在读取提交统计...</span>
        </div>
      )}

      {error && <div className="error-box stats-error">{error}</div>}

      {stats && (
        <>
          <section className="stats-grid" aria-label="提交总览">
            <article className="stat-card">
              <Activity size={20} />
              <span>总提交</span>
              <strong>{stats.total_submissions}</strong>
              <small>所有题目累计</small>
            </article>
            <article className="stat-card">
              <CheckCircle2 size={20} />
              <span>通过提交</span>
              <strong>{stats.accepted_submissions}</strong>
              <small>Accepted 数量</small>
            </article>
            <article className="stat-card">
              <Target size={20} />
              <span>总通过率</span>
              <strong>{formatRate(stats.acceptance_rate)}</strong>
              <small>通过 / 提交</small>
            </article>
            <article className="stat-card">
              <BookOpen size={20} />
              <span>活跃题目</span>
              <strong>
                {stats.active_problems}/{stats.problems.length}
              </strong>
              <small>已有提交记录</small>
            </article>
            <article className="stat-card">
              <Timer size={20} />
              <span>最近提交</span>
              <strong>{formatDateTime(stats.latest_submitted_at)}</strong>
              <small>按提交时间统计</small>
            </article>
          </section>

          <section className="insight-strip" aria-label="提交洞察">
            <div>
              <Trophy size={20} />
              <span>
                <strong>
                  {mostSubmitted && mostSubmitted.total_submissions > 0 ? mostSubmitted.title : "暂无提交"}
                </strong>
                <small>
                  {mostSubmitted && mostSubmitted.total_submissions > 0
                    ? `最活跃题目，${mostSubmitted.total_submissions} 次提交`
                    : "完成一次练习后会自动更新"}
                </small>
              </span>
            </div>
            <div>
              <CheckCircle2 size={20} />
              <span>
                <strong>{latestAccepted ? latestAccepted.title : "暂无通过记录"}</strong>
                <small>
                  {latestAccepted
                    ? `最近通过：${formatDateTime(latestAccepted.last_accepted_at)}`
                    : "学生通过题目后会显示最近通过时间"}
                </small>
              </span>
            </div>
          </section>

          {teacherInsight && (
            <section className="teacher-dashboard" aria-label="教师视角看板">
              <div className="teacher-dashboard-head">
                <div className="section-title">
                  <ListChecks size={18} />
                  <h3>教师视角诊断</h3>
                </div>
                <p>基于当前 OJ 提交聚合生成班级反馈；演示学生来自 seed 数据标记，后续可替换为真实账号。</p>
              </div>

              <div className="teacher-metrics" aria-label="班级概览">
                <article className="teacher-metric-card">
                  <span>练习覆盖</span>
                  <strong>{formatRate(teacherInsight.coverageRate)}</strong>
                  <small>已有提交题目 / 全部题目</small>
                </article>
                <article className="teacher-metric-card">
                  <span>需讲解题</span>
                  <strong>{teacherInsight.attentionProblemCount}</strong>
                  <small>低通过率或错误密集</small>
                </article>
                <article className="teacher-metric-card">
                  <span>平均尝试</span>
                  <strong>{formatAttempts(teacherInsight.averageAttemptsPerSolved)}</strong>
                  <small>提交数 / 通过数</small>
                </article>
                <article className="teacher-metric-card">
                  <span>高频错误</span>
                  <strong>{teacherInsight.topIssueLabel}</strong>
                  <small>{teacherInsight.topIssueCount > 0 ? `${teacherInsight.topIssueCount} 次` : "暂无错误"}</small>
                </article>
              </div>

              <div className="teacher-dashboard-grid">
                <article className="teacher-panel weak-panel">
                  <div className="teacher-panel-title">
                    <Target size={18} />
                    <h4>薄弱题目排行</h4>
                  </div>
                  {teacherInsight.weakProblems.length === 0 ? (
                    <p className="empty-hint">暂无明显薄弱题；可以继续收集提交样本。</p>
                  ) : (
                    <div className="weak-problem-list">
                      {teacherInsight.weakProblems.map((problem, index) => (
                        <div className="weak-problem-row" key={problem.problem_id}>
                          <span className="rank-number">{index + 1}</span>
                          <div>
                            <NavLink className="stats-problem-link" to={`/problems/${problem.problem_id}`}>
                              {problem.title}
                            </NavLink>
                            <small>
                              {problem.mainIssue} · {problem.total_submissions} 次提交 ·{" "}
                              {formatRate(problem.acceptance_rate)} 通过率
                            </small>
                            <p>{problem.recommendation}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </article>

                <article className="teacher-panel">
                  <div className="teacher-panel-title">
                    <BarChart3 size={18} />
                    <h4>错误类型分布</h4>
                  </div>
                  {teacherInsight.statusDistribution.length === 0 ? (
                    <p className="empty-hint">暂无提交状态数据。</p>
                  ) : (
                    <div className="status-bar-list">
                      {teacherInsight.statusDistribution.map((item) => (
                        <div className="status-bar-row" key={item.status}>
                          <div>
                            <span>{formatStatus(item.status)}</span>
                            <strong>{item.count}</strong>
                          </div>
                          <span className="status-bar-track" aria-hidden="true">
                            <span
                              className={`status-bar-fill ${statusClass(item.status)}`}
                              style={{ width: `${Math.max(item.rate * 100, 4)}%` }}
                            />
                          </span>
                        </div>
                      ))}
                    </div>
                  )}
                </article>

                <article className="teacher-panel student-panel">
                  <div className="teacher-panel-title">
                    <BookOpen size={18} />
                    <h4>学生练习观察</h4>
                  </div>
                  {teacherInsight.students.length === 0 ? (
                    <p className="empty-hint">暂无最近提交，运行演示种子数据后会显示学生观察。</p>
                  ) : (
                    <div className="student-table-scroll">
                      <table className="student-table">
                        <thead>
                          <tr>
                            <th>学生</th>
                            <th>提交</th>
                            <th>通过题</th>
                            <th>通过率</th>
                            <th>关注点</th>
                            <th>最近</th>
                          </tr>
                        </thead>
                        <tbody>
                          {teacherInsight.students.map((student) => (
                            <tr key={student.id}>
                              <td>
                                <strong>{student.name}</strong>
                                <small>{student.group}</small>
                              </td>
                              <td>{student.submissions}</td>
                              <td>{student.solvedProblems}</td>
                              <td>{formatRate(student.acceptanceRate)}</td>
                              <td>{student.focus}</td>
                              <td>{formatDateTime(student.latestAt)}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </article>

                <article className="teacher-panel">
                  <div className="teacher-panel-title">
                    <FlaskConical size={18} />
                    <h4>下一次课建议</h4>
                  </div>
                  <ol className="teacher-action-list">
                    {teacherInsight.recommendedActions.map((action) => (
                      <li key={action}>{action}</li>
                    ))}
                  </ol>
                </article>
              </div>
            </section>
          )}

          <section className="stats-table-panel">
            <div className="section-title">
              <BarChart3 size={18} />
              <h3>题目提交明细</h3>
            </div>

            <div className="stats-table-scroll">
              <table className="stats-table">
                <thead>
                  <tr>
                    <th>题目</th>
                    <th>难度</th>
                    <th>提交</th>
                    <th>通过</th>
                    <th>通过率</th>
                    <th>最近提交</th>
                    <th>最近通过</th>
                    <th>状态分布</th>
                  </tr>
                </thead>
                <tbody>
                  {stats.problems.map((problem) => (
                    <tr key={problem.problem_id} className={problem.total_submissions === 0 ? "empty-row" : ""}>
                      <td>
                        <NavLink className="stats-problem-link" to={`/problems/${problem.problem_id}`}>
                          {problem.title}
                        </NavLink>
                        <small>{problem.problem_id}</small>
                      </td>
                      <td>
                        <span className={`difficulty ${problem.difficulty}`}>{problem.difficulty}</span>
                      </td>
                      <td>{problem.total_submissions}</td>
                      <td>{problem.accepted_submissions}</td>
                      <td>
                        <span className="rate-cell">{formatRate(problem.acceptance_rate)}</span>
                      </td>
                      <td>{formatDateTime(problem.last_submitted_at)}</td>
                      <td>{formatDateTime(problem.last_accepted_at)}</td>
                      <td>
                        <div className="status-chip-list">
                          {problem.status_counts.length === 0 ? (
                            <span className="muted-text compact">暂无</span>
                          ) : (
                            problem.status_counts.map((item) => (
                              <span className={`status-chip ${statusClass(item.status)}`} key={item.status}>
                                {formatStatus(item.status)} {item.count}
                              </span>
                            ))
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </>
      )}
    </div>
  );
}

function CaseOutput({ label, value }: { label: string; value?: string | null }) {
  return (
    <div className="case-output">
      <strong>{label}</strong>
      <pre>{value && value.length > 0 ? value : "（空）"}</pre>
    </div>
  );
}

type LearningProgress = {
  completedLessons: Record<string, string>;
  acceptedProblems: Record<string, string>;
  updatedAt?: string;
};

type ProgressSummary = {
  totalLessons: number;
  completedLessons: number;
  totalProblems: number;
  acceptedProblems: number;
  percent: number;
};

type LessonProgressSummary = {
  completed: boolean;
  totalProblems: number;
  acceptedProblems: number;
};

type SubmissionResult = {
  submission_id?: string | null;
  submitted_at?: string | null;
  status: string;
  problem_id: string;
  language: string;
  compile_output: string;
  cases: Array<{
    index: number;
    status: string;
    hidden: boolean;
    input?: string | null;
    expected_output?: string | null;
    actual_output?: string | null;
    run_time_ms?: number | null;
    message?: string | null;
  }>;
  message?: string | null;
};

type SubmissionHistoryItem = {
  id: string;
  status: string;
  submittedAt: string;
  passedCases: number;
  totalCases: number;
  sourceCode: string;
  result: SubmissionResult;
};

type JudgeInfo = {
  name: string;
  display_name: string;
  isolation: string;
  languages: string[];
  supports_hidden_tests: boolean;
  notes: string[];
};

type DemoStudentProfile = {
  id: string;
  name: string;
  group: string;
};

type SubmissionRecord = {
  id: string;
  problem_id: string;
  language: string;
  source_code: string;
  status: string;
  passed_cases: number;
  total_cases: number;
  submitted_at: string;
  result: SubmissionResult;
};

type TeacherProblemInsight = ProblemSubmissionStats & {
  wrongSubmissions: number;
  mainIssue: string;
  recommendation: string;
  attentionScore: number;
};

type TeacherStatusInsight = {
  status: string;
  count: number;
  rate: number;
};

type TeacherStudentInsight = {
  id: string;
  name: string;
  group: string;
  submissions: number;
  accepted: number;
  acceptanceRate: number;
  solvedProblems: number;
  latestAt?: string | null;
  focus: string;
};

type TeacherDashboardInsight = {
  coverageRate: number;
  attentionProblemCount: number;
  averageAttemptsPerSolved: number;
  topIssueLabel: string;
  topIssueCount: number;
  weakProblems: TeacherProblemInsight[];
  statusDistribution: TeacherStatusInsight[];
  students: TeacherStudentInsight[];
  recommendedActions: string[];
};

type StatusCount = {
  status: string;
  count: number;
};

type ProblemSubmissionStats = {
  problem_id: string;
  title: string;
  difficulty: string;
  total_submissions: number;
  accepted_submissions: number;
  acceptance_rate: number;
  last_submitted_at?: string | null;
  last_accepted_at?: string | null;
  status_counts: StatusCount[];
};

type SubmissionStatsSummary = {
  total_submissions: number;
  accepted_submissions: number;
  acceptance_rate: number;
  active_problems: number;
  latest_submitted_at?: string | null;
  problems: ProblemSubmissionStats[];
};

function buildTeacherDashboardInsight(
  stats: SubmissionStatsSummary,
  submissions: SubmissionRecord[],
): TeacherDashboardInsight {
  const weakCandidates = stats.problems
    .map(toTeacherProblemInsight)
    .filter((problem) => problem.total_submissions > 0 && problem.attentionScore > 0)
    .sort((left, right) => right.attentionScore - left.attentionScore);
  const statusDistribution = buildStatusDistribution(stats.problems);
  const topIssue = statusDistribution.find((item) => item.status !== "Accepted");
  const students = buildTeacherStudentInsights(submissions);
  const acceptedProblems = stats.problems.filter((problem) => problem.accepted_submissions > 0).length;
  const averageAttemptsPerSolved =
    stats.accepted_submissions > 0 ? stats.total_submissions / stats.accepted_submissions : 0;

  return {
    coverageRate: stats.problems.length > 0 ? stats.active_problems / stats.problems.length : 0,
    attentionProblemCount: weakCandidates.length,
    averageAttemptsPerSolved,
    topIssueLabel: topIssue ? formatStatus(topIssue.status) : "暂无",
    topIssueCount: topIssue?.count ?? 0,
    weakProblems: weakCandidates.slice(0, 5),
    statusDistribution,
    students,
    recommendedActions: buildTeacherActions({
      weakProblems: weakCandidates,
      topIssue,
      students,
      acceptedProblems,
      totalProblems: stats.problems.length,
    }),
  };
}

function toTeacherProblemInsight(problem: ProblemSubmissionStats): TeacherProblemInsight {
  const wrongSubmissions = Math.max(problem.total_submissions - problem.accepted_submissions, 0);
  const topIssue = topNonAcceptedStatus(problem.status_counts);
  const lowPassRate = problem.total_submissions >= 2 && problem.acceptance_rate < 0.65;
  const noAccepted = problem.total_submissions > 0 && problem.accepted_submissions === 0;
  const repeatedWrong = wrongSubmissions >= 2;
  const attentionScore =
    (lowPassRate ? (0.65 - problem.acceptance_rate) * 12 : 0) +
    (noAccepted ? 6 : 0) +
    (repeatedWrong ? wrongSubmissions * 1.6 : 0) +
    (problem.total_submissions >= 4 ? 1.5 : 0);

  return {
    ...problem,
    wrongSubmissions,
    mainIssue: topIssue ? formatStatus(topIssue.status) : "暂无明显错误",
    recommendation: recommendationForProblem(problem, topIssue?.status),
    attentionScore,
  };
}

function buildStatusDistribution(problems: ProblemSubmissionStats[]): TeacherStatusInsight[] {
  const counts = new Map<string, number>();
  let total = 0;

  problems.forEach((problem) => {
    problem.status_counts.forEach((item) => {
      counts.set(item.status, (counts.get(item.status) ?? 0) + item.count);
      total += item.count;
    });
  });

  return Array.from(counts.entries())
    .map(([status, count]) => ({
      status,
      count,
      rate: total > 0 ? count / total : 0,
    }))
    .sort((left, right) => right.count - left.count);
}

function buildTeacherStudentInsights(submissions: SubmissionRecord[]): TeacherStudentInsight[] {
  const demoSubmissions = submissions.filter((submission) => demoStudentIdForSubmission(submission));
  const sourceSubmissions = demoSubmissions.length > 0 ? demoSubmissions : submissions;
  const students = new Map<
    string,
    {
      profile: DemoStudentProfile;
      submissions: number;
      accepted: number;
      solvedProblems: Set<string>;
      statusCounts: Map<string, number>;
      latestAt?: string | null;
    }
  >();

  sourceSubmissions.forEach((submission, index) => {
    const profile = profileForSubmission(submission, index);
    const current =
      students.get(profile.id) ??
      {
        profile,
        submissions: 0,
        accepted: 0,
        solvedProblems: new Set<string>(),
        statusCounts: new Map<string, number>(),
        latestAt: null,
      };

    current.submissions += 1;
    current.statusCounts.set(submission.status, (current.statusCounts.get(submission.status) ?? 0) + 1);

    if (submission.status === "Accepted") {
      current.accepted += 1;
      current.solvedProblems.add(submission.problem_id);
    }

    if (!current.latestAt || submission.submitted_at > current.latestAt) {
      current.latestAt = submission.submitted_at;
    }

    students.set(profile.id, current);
  });

  return Array.from(students.values())
    .map((student) => ({
      id: student.profile.id,
      name: student.profile.name,
      group: student.profile.group,
      submissions: student.submissions,
      accepted: student.accepted,
      acceptanceRate: student.submissions > 0 ? student.accepted / student.submissions : 0,
      solvedProblems: student.solvedProblems.size,
      latestAt: student.latestAt,
      focus: focusForStudent(student.statusCounts, student.submissions, student.accepted),
    }))
    .sort((left, right) => {
      if (left.acceptanceRate !== right.acceptanceRate) {
        return left.acceptanceRate - right.acceptanceRate;
      }
      return right.submissions - left.submissions;
    })
    .slice(0, 8);
}

function buildTeacherActions({
  weakProblems,
  topIssue,
  students,
  acceptedProblems,
  totalProblems,
}: {
  weakProblems: TeacherProblemInsight[];
  topIssue?: TeacherStatusInsight;
  students: TeacherStudentInsight[];
  acceptedProblems: number;
  totalProblems: number;
}) {
  const actions: string[] = [];
  const firstWeak = weakProblems[0];
  const supportStudents = students.filter((student) => student.submissions >= 2 && student.acceptanceRate < 0.5);

  if (firstWeak) {
    actions.push(`先复盘《${firstWeak.title}》，用样例追踪定位 ${firstWeak.mainIssue} 的产生位置。`);
  }

  if (topIssue?.status === "Compile Error") {
    actions.push("课前安排 5 分钟 C++ 模板与常见编译错误检查，降低语法型挫败感。");
  } else if (topIssue?.status === "Wrong Answer") {
    actions.push("下一次讲解优先让学生口述边界条件、下标含义和样例推演过程。");
  } else if (topIssue?.status === "Runtime Error") {
    actions.push("补一段数组越界、除零和空输入的防错演示，再进入练习。");
  } else {
    actions.push("保留一次短讲短练节奏：讲 8 分钟核心模型，再做 12 分钟同类变式。");
  }

  if (supportStudents.length > 0) {
    actions.push(`给 ${supportStudents.map((student) => student.name).join("、")} 安排一次小组助教检查。`);
  } else {
    actions.push("当前学生通过情况较均衡，可以增加一道挑战题观察迁移能力。");
  }

  if (totalProblems > 0 && acceptedProblems / totalProblems < 0.25) {
    actions.push("章节练习覆盖还偏早期，演示时可先补充 2 到 3 条 Accepted 数据让趋势更明显。");
  }

  return actions.slice(0, 4);
}

function topNonAcceptedStatus(statusCounts: StatusCount[]) {
  return statusCounts
    .filter((item) => item.status !== "Accepted")
    .sort((left, right) => right.count - left.count)[0];
}

function recommendationForProblem(problem: ProblemSubmissionStats, issue?: string) {
  if (issue === "Compile Error") {
    return "建议先检查模板、头文件和分号，再让学生重跑最小样例。";
  }
  if (issue === "Runtime Error") {
    return "建议用数组边界和极小输入做一次现场排查。";
  }
  if (issue === "Time Limit Exceeded") {
    return "建议对比朴素写法与优化写法，明确复杂度瓶颈。";
  }
  if (issue === "Wrong Answer") {
    return "建议用一组样例逐位追踪变量变化，重点查边界与进位/状态转移。";
  }
  if (problem.accepted_submissions === 0) {
    return "建议先补一道引导题，确认学生理解题意和输入输出格式。";
  }
  return "建议保持当前练习节奏，再加入一道相邻变式巩固。";
}

function profileForSubmission(submission: SubmissionRecord, index: number): DemoStudentProfile {
  const demoStudent = demoStudentIdForSubmission(submission);
  const profile =
    DEMO_STUDENT_PROFILES.find((student) => student.id === demoStudent) ??
    DEMO_STUDENT_PROFILES[stableIndex(submission.id || `${submission.problem_id}-${index}`, DEMO_STUDENT_PROFILES.length)];

  return profile;
}

function demoStudentIdForSubmission(submission: SubmissionRecord) {
  return submission.source_code.match(/demo-seed:\s*student=([a-z0-9_-]+)/i)?.[1];
}

function stableIndex(value: string, modulo: number) {
  if (modulo <= 0) {
    return 0;
  }

  let hash = 0;
  for (let index = 0; index < value.length; index += 1) {
    hash = (hash * 31 + value.charCodeAt(index)) >>> 0;
  }
  return hash % modulo;
}

function focusForStudent(statusCounts: Map<string, number>, submissions: number, accepted: number) {
  if (submissions === 0) {
    return "等待首次提交";
  }
  if (accepted === submissions) {
    return "可尝试挑战题";
  }

  const topIssue = Array.from(statusCounts.entries())
    .filter(([status]) => status !== "Accepted")
    .sort((left, right) => right[1] - left[1])[0]?.[0];

  if (topIssue === "Compile Error") {
    return "先查语法模板";
  }
  if (topIssue === "Runtime Error") {
    return "关注越界与空输入";
  }
  if (topIssue === "Time Limit Exceeded") {
    return "复盘复杂度";
  }
  if (topIssue === "Wrong Answer") {
    return "重走样例和边界";
  }
  if (accepted / submissions < 0.5) {
    return "需要同伴讲解";
  }
  return "巩固同类变式";
}

function statusClass(status: string) {
  return status.toLowerCase().replace(/\s+/g, "-");
}

function useLearningProgress() {
  const [progress, setProgress] = useState<LearningProgress>(() => loadLearningProgress());

  useEffect(() => {
    saveLearningProgress(progress);
  }, [progress]);

  const setLessonComplete = useCallback((lessonId: string, complete: boolean) => {
    setProgress((current) => {
      const timestamp = new Date().toISOString();
      const completedLessons = { ...current.completedLessons };

      if (complete) {
        completedLessons[lessonId] = timestamp;
      } else {
        delete completedLessons[lessonId];
      }

      return {
        ...current,
        completedLessons,
        updatedAt: timestamp,
      };
    });
  }, []);

  const markProblemAccepted = useCallback((problemId: string) => {
    setProgress((current) => {
      if (current.acceptedProblems[problemId]) {
        return current;
      }

      const timestamp = new Date().toISOString();
      return {
        ...current,
        acceptedProblems: {
          ...current.acceptedProblems,
          [problemId]: timestamp,
        },
        updatedAt: timestamp,
      };
    });
  }, []);

  return { progress, setLessonComplete, markProblemAccepted };
}

function createEmptyProgress(): LearningProgress {
  return {
    completedLessons: {},
    acceptedProblems: {},
  };
}

function loadLearningProgress(): LearningProgress {
  if (typeof window === "undefined") {
    return createEmptyProgress();
  }

  try {
    const raw = window.localStorage.getItem(PROGRESS_KEY);
    return raw ? normalizeLearningProgress(JSON.parse(raw) as unknown) : createEmptyProgress();
  } catch {
    return createEmptyProgress();
  }
}

function saveLearningProgress(progress: LearningProgress) {
  if (typeof window === "undefined") {
    return;
  }

  window.localStorage.setItem(PROGRESS_KEY, JSON.stringify(progress));
}

function loadSidebarCollapsed() {
  if (typeof window === "undefined") {
    return false;
  }

  try {
    return window.localStorage.getItem(SIDEBAR_COLLAPSED_KEY) === "true";
  } catch {
    return false;
  }
}

function saveSidebarCollapsed(collapsed: boolean) {
  if (typeof window === "undefined") {
    return;
  }

  try {
    window.localStorage.setItem(SIDEBAR_COLLAPSED_KEY, String(collapsed));
  } catch {
    // The layout still works if persistence is unavailable.
  }
}

function normalizeLearningProgress(value: unknown): LearningProgress {
  if (!value || typeof value !== "object") {
    return createEmptyProgress();
  }

  const record = value as Record<string, unknown>;
  return {
    completedLessons: normalizeTimestampRecord(record.completedLessons),
    acceptedProblems: normalizeTimestampRecord(record.acceptedProblems),
    updatedAt: typeof record.updatedAt === "string" ? record.updatedAt : undefined,
  };
}

function normalizeTimestampRecord(value: unknown): Record<string, string> {
  if (!value || typeof value !== "object") {
    return {};
  }

  return Object.fromEntries(
    Object.entries(value as Record<string, unknown>).filter(
      ([key, timestamp]) => key.length > 0 && typeof timestamp === "string",
    ),
  ) as Record<string, string>;
}

function summarizeLessonProgress(lesson: Lesson, progress: LearningProgress): LessonProgressSummary {
  return {
    completed: Boolean(progress.completedLessons[lesson.id]),
    totalProblems: lesson.problems.length,
    acceptedProblems: lesson.problems.filter((problem) => progress.acceptedProblems[problem.id]).length,
  };
}

function summarizeChapterProgress(chapter: Chapter, progress: LearningProgress): ProgressSummary {
  const completedLessons = chapter.lessons.filter((lesson) => progress.completedLessons[lesson.id]).length;
  const totalProblems = chapter.lessons.reduce((sum, lesson) => sum + lesson.problems.length, 0);
  const acceptedProblems = chapter.lessons.reduce(
    (sum, lesson) => sum + lesson.problems.filter((problem) => progress.acceptedProblems[problem.id]).length,
    0,
  );

  return {
    totalLessons: chapter.lessons.length,
    completedLessons,
    totalProblems,
    acceptedProblems,
    percent: progressPercent(completedLessons + acceptedProblems, chapter.lessons.length + totalProblems),
  };
}

function summarizeCourseProgress(courseChapters: Chapter[], progress: LearningProgress): ProgressSummary {
  return courseChapters.reduce<ProgressSummary>(
    (summary, chapter) => {
      const chapterSummary = summarizeChapterProgress(chapter, progress);
      const completedUnits = summary.completedLessons + chapterSummary.completedLessons;
      const acceptedUnits = summary.acceptedProblems + chapterSummary.acceptedProblems;
      const totalLessons = summary.totalLessons + chapterSummary.totalLessons;
      const totalProblems = summary.totalProblems + chapterSummary.totalProblems;

      return {
        totalLessons,
        completedLessons: completedUnits,
        totalProblems,
        acceptedProblems: acceptedUnits,
        percent: progressPercent(completedUnits + acceptedUnits, totalLessons + totalProblems),
      };
    },
    {
      totalLessons: 0,
      completedLessons: 0,
      totalProblems: 0,
      acceptedProblems: 0,
      percent: 0,
    },
  );
}

function progressPercent(done: number, total: number) {
  if (total <= 0) {
    return 0;
  }

  return Math.min(100, Math.round((done / total) * 100));
}

function lessonPath(chapterId: string, lessonId: string) {
  return `/chapters/${chapterId}/lessons/${lessonId}`;
}

function findContinuePath(courseChapters: Chapter[], progress: LearningProgress) {
  for (const chapter of courseChapters) {
    for (const lesson of chapter.lessons) {
      if (!progress.completedLessons[lesson.id]) {
        return lessonPath(chapter.id, lesson.id);
      }

      const nextProblem = lesson.problems.find((problem) => !progress.acceptedProblems[problem.id]);
      if (nextProblem) {
        return `/problems/${nextProblem.id}`;
      }
    }
  }

  return firstLessonPath;
}

function findNextLessonPath(chapterId: string, lessonId: string) {
  let foundCurrent = false;

  for (const chapter of chapters) {
    for (const lesson of chapter.lessons) {
      if (foundCurrent) {
        return lessonPath(chapter.id, lesson.id);
      }

      if (chapter.id === chapterId && lesson.id === lessonId) {
        foundCurrent = true;
      }
    }
  }

  return null;
}

function draftKey(problemId: string) {
  return `${DRAFT_PREFIX}${problemId}`;
}

function historyKey(problemId: string) {
  return `${HISTORY_PREFIX}${problemId}`;
}

function loadDraft(problemId: string, fallback: string) {
  if (typeof window === "undefined") {
    return fallback;
  }

  return window.localStorage.getItem(draftKey(problemId)) ?? fallback;
}

function saveDraft(problemId: string, sourceCode: string) {
  if (typeof window === "undefined") {
    return;
  }

  window.localStorage.setItem(draftKey(problemId), sourceCode);
}

function loadSubmissionHistory(problemId: string): SubmissionHistoryItem[] {
  if (typeof window === "undefined") {
    return [];
  }

  try {
    const raw = window.localStorage.getItem(historyKey(problemId));
    return raw ? (JSON.parse(raw) as SubmissionHistoryItem[]) : [];
  } catch {
    return [];
  }
}

function saveSubmissionHistory(problemId: string, history: SubmissionHistoryItem[]) {
  if (typeof window === "undefined") {
    return;
  }

  window.localStorage.setItem(historyKey(problemId), JSON.stringify(history));
}

function createHistoryItem(result: SubmissionResult, sourceCode: string): SubmissionHistoryItem {
  return {
    id: result.submission_id ?? `${result.problem_id}-${Date.now()}`,
    status: result.status,
    submittedAt: result.submitted_at ?? new Date().toISOString(),
    passedCases: result.cases.filter((caseResult) => caseResult.status === "Accepted").length,
    totalCases: result.cases.length,
    sourceCode,
    result,
  };
}

function recordToHistoryItem(record: SubmissionRecord): SubmissionHistoryItem {
  return {
    id: record.id,
    status: record.status,
    submittedAt: record.submitted_at,
    passedCases: record.passed_cases,
    totalCases: record.total_cases,
    sourceCode: record.source_code,
    result: record.result,
  };
}

function formatTime(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "未知时间";
  }

  return new Intl.DateTimeFormat("zh-CN", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  }).format(date);
}

function formatDateTime(value?: string | null) {
  if (!value) {
    return "暂无";
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "暂无";
  }

  return new Intl.DateTimeFormat("zh-CN", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

function formatRate(rate: number) {
  if (rate <= 0) {
    return "0%";
  }
  if (rate >= 1) {
    return "100%";
  }
  return `${(rate * 100).toFixed(1)}%`;
}

function formatAttempts(value: number) {
  if (!Number.isFinite(value) || value <= 0) {
    return "0";
  }
  return value.toFixed(value >= 10 ? 0 : 1);
}

function formatStatus(status: string) {
  const labels: Record<string, string> = {
    Accepted: "通过",
    "Wrong Answer": "答案错误",
    "Compile Error": "编译错误",
    "Runtime Error": "运行错误",
    "Time Limit Exceeded": "超时",
    "System Error": "系统错误",
  };

  return labels[status] ?? status;
}

export default App;
