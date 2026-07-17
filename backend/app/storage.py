from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

from app.schemas import SubmissionRecord, SubmissionResult


DB_PATH = Path(__file__).resolve().parent / ".data" / "submissions.sqlite3"


class SubmissionStore:
    def __init__(self, db_path: Path = DB_PATH) -> None:
        self.db_path = db_path

    def save(self, source_code: str, result: SubmissionResult) -> SubmissionResult:
        self._ensure_schema()

        submission_id = uuid.uuid4().hex
        submitted_at = datetime.now(timezone.utc).isoformat()
        enriched = result.model_copy(
            update={
                "submission_id": submission_id,
                "submitted_at": submitted_at,
            }
        )
        passed_cases = sum(1 for case in enriched.cases if case.status == "Accepted")
        total_cases = len(enriched.cases)

        with self._connect() as connection:
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
                    enriched.problem_id,
                    enriched.language,
                    source_code,
                    enriched.status,
                    passed_cases,
                    total_cases,
                    submitted_at,
                    json.dumps(enriched.model_dump(mode="json"), ensure_ascii=False),
                ),
            )

        return enriched

    def list(self, problem_id: str | None = None, limit: int = 20) -> list[SubmissionRecord]:
        self._ensure_schema()

        if problem_id:
            sql = """
                SELECT *
                FROM submissions
                WHERE problem_id = ?
                ORDER BY submitted_at DESC
                LIMIT ?
            """
            parameters: tuple[object, ...] = (problem_id, limit)
        else:
            sql = """
                SELECT *
                FROM submissions
                ORDER BY submitted_at DESC
                LIMIT ?
            """
            parameters = (limit,)

        with self._connect() as connection:
            rows = connection.execute(sql, parameters).fetchall()

        return [self._row_to_record(row) for row in rows]

    def get(self, submission_id: str) -> SubmissionRecord | None:
        self._ensure_schema()

        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM submissions WHERE id = ?",
                (submission_id,),
            ).fetchone()

        return self._row_to_record(row) if row else None

    def stats_by_problem(self) -> dict[str, dict[str, object]]:
        self._ensure_schema()

        with self._connect() as connection:
            summary_rows = connection.execute(
                """
                SELECT
                    problem_id,
                    COUNT(*) AS total_submissions,
                    SUM(CASE WHEN status = 'Accepted' THEN 1 ELSE 0 END) AS accepted_submissions,
                    MAX(submitted_at) AS last_submitted_at,
                    MAX(CASE WHEN status = 'Accepted' THEN submitted_at ELSE NULL END) AS last_accepted_at
                FROM submissions
                GROUP BY problem_id
                """
            ).fetchall()
            status_rows = connection.execute(
                """
                SELECT problem_id, status, COUNT(*) AS count
                FROM submissions
                GROUP BY problem_id, status
                ORDER BY problem_id ASC, status ASC
                """
            ).fetchall()

        stats: dict[str, dict[str, object]] = {}
        for row in summary_rows:
            stats[row["problem_id"]] = {
                "total_submissions": row["total_submissions"],
                "accepted_submissions": row["accepted_submissions"],
                "last_submitted_at": row["last_submitted_at"],
                "last_accepted_at": row["last_accepted_at"],
                "status_counts": [],
            }

        for row in status_rows:
            problem_stats = stats.setdefault(
                row["problem_id"],
                {
                    "total_submissions": 0,
                    "accepted_submissions": 0,
                    "last_submitted_at": None,
                    "last_accepted_at": None,
                    "status_counts": [],
                },
            )
            status_counts = problem_stats["status_counts"]
            if isinstance(status_counts, list):
                status_counts.append({"status": row["status"], "count": row["count"]})

        return stats

    def _ensure_schema(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS submissions (
                    id TEXT PRIMARY KEY,
                    problem_id TEXT NOT NULL,
                    language TEXT NOT NULL,
                    source_code TEXT NOT NULL,
                    status TEXT NOT NULL,
                    passed_cases INTEGER NOT NULL,
                    total_cases INTEGER NOT NULL,
                    submitted_at TEXT NOT NULL,
                    result_json TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_submissions_problem_time
                ON submissions(problem_id, submitted_at DESC)
                """
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _row_to_record(self, row: sqlite3.Row) -> SubmissionRecord:
        result = SubmissionResult.model_validate(json.loads(row["result_json"]))
        return SubmissionRecord(
            id=row["id"],
            problem_id=row["problem_id"],
            language=row["language"],
            source_code=row["source_code"],
            status=row["status"],
            passed_cases=row["passed_cases"],
            total_cases=row["total_cases"],
            submitted_at=row["submitted_at"],
            result=result,
        )
