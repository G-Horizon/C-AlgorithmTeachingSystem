from __future__ import annotations

import os

from app.content.problems import Problem
from app.judge.base import JudgeAdapter
from app.judge.docker_judge import DockerJudge
from app.judge.local_judge import LocalJudge
from app.schemas import JudgeInfo, SubmissionResult


class JudgeService:
    def __init__(self, adapter: JudgeAdapter) -> None:
        self.adapter = adapter

    @property
    def info(self) -> JudgeInfo:
        return self.adapter.info

    def judge(self, problem: Problem, source_code: str) -> SubmissionResult:
        return self.adapter.judge(problem, source_code)


def create_judge_service() -> JudgeService:
    adapter_name = os.getenv("JUDGE_ADAPTER", "local-process").strip().lower()
    if adapter_name in {"local", "local-process"}:
        return JudgeService(LocalJudge())
    if adapter_name == "docker":
        return JudgeService(DockerJudge())

    raise RuntimeError(f"Unsupported JUDGE_ADAPTER: {adapter_name}")
