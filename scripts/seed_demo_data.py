from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.content.problems import get_problem  # noqa: E402
from app.schemas import CaseResult, SubmissionResult  # noqa: E402
from app.storage import SubmissionStore  # noqa: E402


DEMO_MARKER = "// demo-seed:"


@dataclass(frozen=True)
class DemoSubmission:
    student: str
    problem_id: str
    status: str
    minutes_ago: int
    passed_before_fail: int = 0


DEMO_SUBMISSIONS = [
    DemoSubmission("lin", "bubble-sort-basic", "Wrong Answer", 270, 1),
    DemoSubmission("lin", "bubble-sort-basic", "Accepted", 252),
    DemoSubmission("lin", "bubble-sort-count", "Wrong Answer", 235, 2),
    DemoSubmission("lin", "selection-sort-basic", "Accepted", 210),
    DemoSubmission("lin", "recurrence-state-table", "Wrong Answer", 120, 1),
    DemoSubmission("lin", "recurrence-climb-stairs-transition", "Accepted", 96),
    DemoSubmission("momo", "big-integer-raw-echo", "Accepted", 360),
    DemoSubmission("momo", "big-integer-add-basic", "Wrong Answer", 330, 2),
    DemoSubmission("momo", "big-integer-add-basic", "Accepted", 318),
    DemoSubmission("momo", "big-integer-sub-basic", "Accepted", 288),
    DemoSubmission("momo", "big-integer-div-small-basic", "Wrong Answer", 180, 1),
    DemoSubmission("momo", "big-integer-div-small-basic", "Accepted", 150),
    DemoSubmission("chen", "insertion-sort-basic", "Compile Error", 410),
    DemoSubmission("chen", "insertion-sort-basic", "Accepted", 390),
    DemoSubmission("chen", "merge-two-sorted-arrays", "Accepted", 315),
    DemoSubmission("chen", "quick-sort-partition", "Wrong Answer", 255, 1),
    DemoSubmission("chen", "quick-sort-partition", "Accepted", 230),
    DemoSubmission("yue", "recurrence-fibonacci-zero-based", "Accepted", 210),
    DemoSubmission("yue", "recurrence-rolling-trace", "Wrong Answer", 170, 1),
    DemoSubmission("yue", "recurrence-grid-paths-obstacle", "Accepted", 130),
    DemoSubmission("yue", "recurrence-number-tower-basic", "Accepted", 75),
    DemoSubmission("yue", "recurrence-number-tower-table", "Wrong Answer", 50, 2),
    DemoSubmission("yue", "recurrence-number-tower-min", "Accepted", 18),
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed repeatable demo submissions for the MVP dashboard.")
    parser.add_argument(
        "--reset-all",
        action="store_true",
        help="Delete every submission before inserting demo data. By default only old demo-seed rows are removed.",
    )
    parser.add_argument(
        "--count-only",
        action="store_true",
        help="Print the current number of demo-seed rows and exit.",
    )
    args = parser.parse_args()

    store = SubmissionStore()
    store._ensure_schema()

    if args.count_only:
        print(count_demo_rows(store))
        return

    with store._connect() as connection:
        if args.reset_all:
            deleted = connection.execute("DELETE FROM submissions").rowcount
        else:
            deleted = connection.execute(
                "DELETE FROM submissions WHERE source_code LIKE ?",
                (f"{DEMO_MARKER}%",),
            ).rowcount

        inserted = 0
        for index, demo in enumerate(DEMO_SUBMISSIONS, start=1):
            problem = get_problem(demo.problem_id)
            if problem is None:
                raise ValueError(f"Unknown problem id: {demo.problem_id}")

            result = build_result(demo)
            submission_id = uuid.uuid4().hex
            submitted_at = (datetime.now(timezone.utc) - timedelta(minutes=demo.minutes_ago)).isoformat()
            result = result.model_copy(update={"submission_id": submission_id, "submitted_at": submitted_at})
            passed_cases = sum(1 for case in result.cases if case.status == "Accepted")
            total_cases = len(result.cases)
            source_code = build_source_code(demo, index)

            connection.execute(
                """
                INSERT INTO submissions (
                    id,
                    problem_id,
                    language,
                    source_code,
                    status,
                    passed_cases,
                    total_cases,
                    submitted_at,
                    result_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    submission_id,
                    demo.problem_id,
                    "cpp",
                    source_code,
                    result.status,
                    passed_cases,
                    total_cases,
                    submitted_at,
                    json.dumps(result.model_dump(mode="json"), ensure_ascii=False),
                ),
            )
            inserted += 1

    print(f"Deleted {deleted} old rows.")
    print(f"Inserted {inserted} demo submissions.")
    print(f"Database: {store.db_path}")


def count_demo_rows(store: SubmissionStore) -> int:
    with store._connect() as connection:
        row = connection.execute(
            "SELECT COUNT(*) FROM submissions WHERE source_code LIKE ?",
            (f"{DEMO_MARKER}%",),
        ).fetchone()
    return int(row[0])


def build_result(demo: DemoSubmission) -> SubmissionResult:
    problem = get_problem(demo.problem_id)
    if problem is None:
        raise ValueError(f"Unknown problem id: {demo.problem_id}")

    if demo.status == "Compile Error":
        return SubmissionResult(
            status="Compile Error",
            problem_id=demo.problem_id,
            language="cpp",
            compile_output="demo.cpp:12:5: error: expected ';' before 'return'",
            cases=[],
            message="Demo record: compile error used to populate the dashboard.",
        )

    if demo.status == "Accepted":
        cases = [
            case_from_test(index, test.input, test.output, "Accepted", hidden=test.hidden)
            for index, test in enumerate(problem.tests, start=1)
        ]
        return SubmissionResult(
            status="Accepted",
            problem_id=demo.problem_id,
            language="cpp",
            cases=cases,
        )

    cases: list[CaseResult] = []
    pass_count = min(demo.passed_before_fail, max(len(problem.tests) - 1, 0))
    for index, test in enumerate(problem.tests[:pass_count], start=1):
        cases.append(case_from_test(index, test.input, test.output, "Accepted", hidden=test.hidden))

    failing_test = problem.tests[pass_count]
    cases.append(
        case_from_test(
            pass_count + 1,
            failing_test.input,
            failing_test.output,
            demo.status,
            hidden=failing_test.hidden,
            actual_output=wrong_output_for(failing_test.output),
        )
    )
    return SubmissionResult(
        status=demo.status,
        problem_id=demo.problem_id,
        language="cpp",
        cases=cases,
        message="Demo record: intentional non-accepted submission.",
    )


def case_from_test(
    index: int,
    input_text: str,
    expected_output: str,
    status: str,
    *,
    hidden: bool,
    actual_output: str | None = None,
) -> CaseResult:
    return CaseResult(
        index=index,
        status=status,
        hidden=hidden,
        input=None if hidden else input_text,
        expected_output=None if hidden else expected_output,
        actual_output=actual_output if status != "Accepted" else expected_output,
        run_time_ms=2 + (index % 5),
    )


def wrong_output_for(expected_output: str) -> str:
    normalized = expected_output.strip()
    if not normalized:
        return "0\n"
    first_line = normalized.splitlines()[0]
    return f"{first_line} 0\n"


def build_source_code(demo: DemoSubmission, index: int) -> str:
    return "\n".join(
        [
            f"{DEMO_MARKER} student={demo.student} attempt={index}",
            f"// problem={demo.problem_id} status={demo.status}",
            "#include <iostream>",
            "using namespace std;",
            "int main() {",
            "    // This synthetic source keeps the demo dashboard populated.",
            '    cout << "demo";',
            "    return 0;",
            "}",
            "",
        ]
    )


if __name__ == "__main__":
    try:
        main()
    except sqlite3.Error as exc:
        raise SystemExit(f"SQLite error: {exc}") from exc
