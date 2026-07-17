from pydantic import BaseModel, Field


class SampleCase(BaseModel):
    input: str
    output: str


class ProblemSummary(BaseModel):
    id: str
    title: str
    difficulty: str
    tags: list[str]
    time_limit_ms: int
    memory_limit_mb: int


class ProblemDetail(ProblemSummary):
    statement: str
    input_format: str
    output_format: str
    constraints: str
    samples: list[SampleCase]


class SubmissionRequest(BaseModel):
    problem_id: str = Field(..., min_length=1)
    language: str = "cpp"
    source_code: str = Field(..., min_length=1, max_length=100_000)


class CaseResult(BaseModel):
    index: int
    status: str
    hidden: bool
    input: str | None = None
    expected_output: str | None = None
    actual_output: str | None = None
    run_time_ms: int | None = None
    message: str | None = None


class SubmissionResult(BaseModel):
    submission_id: str | None = None
    submitted_at: str | None = None
    status: str
    problem_id: str
    language: str
    compile_output: str = ""
    cases: list[CaseResult] = Field(default_factory=list)
    message: str | None = None


class SubmissionRecord(BaseModel):
    id: str
    problem_id: str
    language: str
    source_code: str
    status: str
    passed_cases: int
    total_cases: int
    submitted_at: str
    result: SubmissionResult


class StatusCount(BaseModel):
    status: str
    count: int


class ProblemSubmissionStats(BaseModel):
    problem_id: str
    title: str
    difficulty: str
    total_submissions: int
    accepted_submissions: int
    acceptance_rate: float
    last_submitted_at: str | None = None
    last_accepted_at: str | None = None
    status_counts: list[StatusCount] = Field(default_factory=list)


class SubmissionStatsSummary(BaseModel):
    total_submissions: int
    accepted_submissions: int
    acceptance_rate: float
    active_problems: int
    latest_submitted_at: str | None = None
    problems: list[ProblemSubmissionStats]


class JudgeInfo(BaseModel):
    name: str
    display_name: str
    isolation: str
    languages: list[str]
    supports_hidden_tests: bool
    notes: list[str] = Field(default_factory=list)
