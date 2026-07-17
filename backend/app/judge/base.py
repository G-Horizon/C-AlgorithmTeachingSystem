from __future__ import annotations

from typing import Protocol

from app.content.problems import Problem
from app.schemas import JudgeInfo, SubmissionResult


class JudgeAdapter(Protocol):
    @property
    def info(self) -> JudgeInfo:
        ...

    def judge(self, problem: Problem, source_code: str) -> SubmissionResult:
        ...
