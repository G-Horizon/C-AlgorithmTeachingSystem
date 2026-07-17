from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.content.problems import Problem, get_problem, list_problems
from app.judge.service import create_judge_service
from app.schemas import (
    JudgeInfo,
    ProblemDetail,
    ProblemSubmissionStats,
    ProblemSummary,
    SampleCase,
    SubmissionRecord,
    SubmissionRequest,
    SubmissionResult,
    SubmissionStatsSummary,
    StatusCount,
)
from app.storage import SubmissionStore


app = FastAPI(title="算法可视化教学系统临时 OJ", version="0.1.0")
judge = create_judge_service()
submission_store = SubmissionStore()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/judge", response_model=JudgeInfo)
def judge_info() -> JudgeInfo:
    return judge.info


@app.get("/api/problems", response_model=list[ProblemSummary])
def problems() -> list[ProblemSummary]:
    return [_problem_summary(problem) for problem in list_problems()]


@app.get("/api/problems/{problem_id}", response_model=ProblemDetail)
def problem_detail(problem_id: str) -> ProblemDetail:
    problem = get_problem(problem_id)
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found.")
    return _problem_detail(problem)


@app.get("/api/submissions", response_model=list[SubmissionRecord])
def submissions(
    problem_id: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
) -> list[SubmissionRecord]:
    if problem_id and get_problem(problem_id) is None:
        raise HTTPException(status_code=404, detail="Problem not found.")

    return submission_store.list(problem_id=problem_id, limit=limit)


@app.get("/api/submissions/{submission_id}", response_model=SubmissionRecord)
def submission_detail(submission_id: str) -> SubmissionRecord:
    record = submission_store.get(submission_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Submission not found.")
    return record


@app.get("/api/stats/submissions", response_model=SubmissionStatsSummary)
def submission_stats() -> SubmissionStatsSummary:
    stats_by_problem = submission_store.stats_by_problem()
    problem_stats: list[ProblemSubmissionStats] = []

    total_submissions = 0
    accepted_submissions = 0
    latest_submitted_at: str | None = None

    for problem in list_problems():
        raw = stats_by_problem.get(problem.id, {})
        total = int(raw.get("total_submissions", 0))
        accepted = int(raw.get("accepted_submissions", 0))
        last_submitted_at = raw.get("last_submitted_at")
        last_accepted_at = raw.get("last_accepted_at")
        status_counts = raw.get("status_counts", [])

        total_submissions += total
        accepted_submissions += accepted
        if isinstance(last_submitted_at, str) and (
            latest_submitted_at is None or last_submitted_at > latest_submitted_at
        ):
            latest_submitted_at = last_submitted_at

        problem_stats.append(
            ProblemSubmissionStats(
                problem_id=problem.id,
                title=problem.title,
                difficulty=problem.difficulty,
                total_submissions=total,
                accepted_submissions=accepted,
                acceptance_rate=_acceptance_rate(accepted, total),
                last_submitted_at=last_submitted_at if isinstance(last_submitted_at, str) else None,
                last_accepted_at=last_accepted_at if isinstance(last_accepted_at, str) else None,
                status_counts=[
                    StatusCount(status=str(item["status"]), count=int(item["count"]))
                    for item in status_counts
                    if isinstance(item, dict) and "status" in item and "count" in item
                ],
            )
        )

    return SubmissionStatsSummary(
        total_submissions=total_submissions,
        accepted_submissions=accepted_submissions,
        acceptance_rate=_acceptance_rate(accepted_submissions, total_submissions),
        active_problems=sum(1 for item in problem_stats if item.total_submissions > 0),
        latest_submitted_at=latest_submitted_at,
        problems=problem_stats,
    )


@app.post("/api/submissions", response_model=SubmissionResult)
def submit(payload: SubmissionRequest) -> SubmissionResult:
    if payload.language != "cpp":
        raise HTTPException(status_code=400, detail="Only cpp is supported in the MVP judge.")

    problem = get_problem(payload.problem_id)
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found.")

    result = judge.judge(problem, payload.source_code)
    return submission_store.save(payload.source_code, result)


def _problem_summary(problem: Problem) -> ProblemSummary:
    return ProblemSummary(
        id=problem.id,
        title=problem.title,
        difficulty=problem.difficulty,
        tags=problem.tags,
        time_limit_ms=problem.time_limit_ms,
        memory_limit_mb=problem.memory_limit_mb,
    )


def _problem_detail(problem: Problem) -> ProblemDetail:
    return ProblemDetail(
        **_problem_summary(problem).model_dump(),
        statement=problem.statement,
        input_format=problem.input_format,
        output_format=problem.output_format,
        constraints=problem.constraints,
        samples=[SampleCase(input=case.input, output=case.output) for case in problem.samples],
    )


def _acceptance_rate(accepted: int, total: int) -> float:
    if total == 0:
        return 0.0
    return round(accepted / total, 4)
