from __future__ import annotations

import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from app.content.problems import Problem
from app.schemas import CaseResult, JudgeInfo, SubmissionResult


RUN_ROOT = Path(__file__).resolve().parents[2] / ".judge_runs"
MAX_OUTPUT_CHARS = 20_000


class LocalJudge:
    """Synchronous local C++ judge for the MVP.

    This is intentionally small and replaceable. For production, replace it with
    a Docker sandbox or an external OJ adapter.
    """

    @property
    def info(self) -> JudgeInfo:
        return JudgeInfo(
            name="local-process",
            display_name="本地进程判题器",
            isolation="process-timeout-only",
            languages=["cpp17"],
            supports_hidden_tests=True,
            notes=[
                "MVP 开发用途：使用本机 g++ 编译并运行学生代码。",
                "只提供时间限制、临时目录和输出截断，不提供生产级文件系统或系统调用隔离。",
                "正式部署前需要替换为 Docker 沙箱或外部 OJ Adapter。",
            ],
        )

    def judge(self, problem: Problem, source_code: str) -> SubmissionResult:
        RUN_ROOT.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory(dir=RUN_ROOT) as workdir:
            workdir_path = Path(workdir)
            source_path = workdir_path / "main.cpp"
            exe_path = workdir_path / "main.exe"
            source_path.write_text(source_code, encoding="utf-8")

            compile_result = self._compile(source_path, exe_path)
            if compile_result.returncode != 0:
                return SubmissionResult(
                    status="Compile Error",
                    problem_id=problem.id,
                    language="cpp",
                    compile_output=self._clip(compile_result.stderr + compile_result.stdout),
                )

            case_results: list[CaseResult] = []
            final_status = "Accepted"

            for index, case in enumerate(problem.tests, start=1):
                case_result = self._run_case(index, exe_path, case.input, case.output, problem.time_limit_ms)
                case_result.hidden = case.hidden

                if case.hidden:
                    case_result.input = None
                    case_result.expected_output = None

                case_results.append(case_result)
                if case_result.status != "Accepted":
                    final_status = case_result.status
                    break

            return SubmissionResult(
                status=final_status,
                problem_id=problem.id,
                language="cpp",
                cases=case_results,
            )

    def _compile(self, source_path: Path, exe_path: Path) -> subprocess.CompletedProcess[str]:
        if shutil.which("g++") is None:
            return subprocess.CompletedProcess(
                args=[],
                returncode=1,
                stdout="",
                stderr="g++ was not found in PATH.",
            )

        command = [
            "g++",
            "-std=c++17",
            "-O2",
            str(source_path),
            "-o",
            str(exe_path),
        ]
        try:
            return subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=10,
            )
        except subprocess.TimeoutExpired as exc:
            return subprocess.CompletedProcess(
                args=command,
                returncode=1,
                stdout=exc.stdout or "",
                stderr="Compilation timed out.",
            )

    def _run_case(
        self,
        index: int,
        exe_path: Path,
        input_text: str,
        expected_output: str,
        time_limit_ms: int,
    ) -> CaseResult:
        start = time.perf_counter()
        try:
            completed = subprocess.run(
                [str(exe_path)],
                input=input_text,
                capture_output=True,
                text=True,
                timeout=time_limit_ms / 1000,
            )
        except subprocess.TimeoutExpired:
            return CaseResult(
                index=index,
                status="Time Limit Exceeded",
                hidden=False,
                input=input_text,
                expected_output=expected_output,
                run_time_ms=time_limit_ms,
                message="Program exceeded the time limit.",
            )

        run_time_ms = int((time.perf_counter() - start) * 1000)

        if completed.returncode != 0:
            return CaseResult(
                index=index,
                status="Runtime Error",
                hidden=False,
                input=input_text,
                expected_output=expected_output,
                actual_output=self._clip(completed.stderr + completed.stdout),
                run_time_ms=run_time_ms,
                message=f"Program exited with code {completed.returncode}.",
            )

        actual_output = self._clip(completed.stdout)
        if self._normalize(actual_output) != self._normalize(expected_output):
            return CaseResult(
                index=index,
                status="Wrong Answer",
                hidden=False,
                input=input_text,
                expected_output=expected_output,
                actual_output=actual_output,
                run_time_ms=run_time_ms,
            )

        return CaseResult(
            index=index,
            status="Accepted",
            hidden=False,
            input=input_text,
            expected_output=expected_output,
            actual_output=actual_output,
            run_time_ms=run_time_ms,
        )

    def _normalize(self, output: str) -> str:
        return "\n".join(line.rstrip() for line in output.strip().splitlines())

    def _clip(self, output: str) -> str:
        if len(output) <= MAX_OUTPUT_CHARS:
            return output
        return output[:MAX_OUTPUT_CHARS] + "\n[output truncated]"
