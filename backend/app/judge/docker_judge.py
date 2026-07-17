from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import time
import uuid
from pathlib import Path

from app.content.problems import Problem
from app.schemas import CaseResult, JudgeInfo, SubmissionResult


RUN_ROOT = Path(__file__).resolve().parents[2] / ".judge_runs"
MAX_OUTPUT_CHARS = 20_000


class DockerJudge:
    """Docker-backed judge adapter.

    This adapter is not the default because local Windows machines may not have
    Docker Desktop running. Enable it with JUDGE_ADAPTER=docker after verifying
    the configured image is available.
    """

    def __init__(self, image: str | None = None) -> None:
        self.image = image or os.getenv("JUDGE_DOCKER_IMAGE", "gcc:13")

    @property
    def info(self) -> JudgeInfo:
        return JudgeInfo(
            name="docker",
            display_name="Docker 沙箱判题器",
            isolation="docker-network-none",
            languages=["cpp17"],
            supports_hidden_tests=True,
            notes=[
                f"镜像：{self.image}",
                "使用一次性容器运行编译和测试，默认关闭网络。",
                "仍需在生产环境继续配置非 root 用户、只读挂载和资源监控。",
            ],
        )

    def judge(self, problem: Problem, source_code: str) -> SubmissionResult:
        docker_error = self._docker_error()
        if docker_error:
            return SubmissionResult(
                status="System Error",
                problem_id=problem.id,
                language="cpp",
                message=docker_error,
            )

        RUN_ROOT.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=RUN_ROOT) as workdir:
            workdir_path = Path(workdir)
            (workdir_path / "main.cpp").write_text(source_code, encoding="utf-8")

            compile_result = self._compile(workdir_path, problem.memory_limit_mb)
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
                case_result = self._run_case(
                    index=index,
                    workdir_path=workdir_path,
                    input_text=case.input,
                    expected_output=case.output,
                    time_limit_ms=problem.time_limit_ms,
                    memory_limit_mb=problem.memory_limit_mb,
                )
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

    def _docker_error(self) -> str | None:
        if shutil.which("docker") is None:
            return "Docker CLI was not found in PATH."

        try:
            completed = subprocess.run(
                ["docker", "version", "--format", "{{.Server.Version}}"],
                capture_output=True,
                text=True,
                timeout=5,
            )
        except subprocess.TimeoutExpired:
            return "Docker daemon check timed out."

        if completed.returncode != 0:
            return self._clip(completed.stderr + completed.stdout)
        return None

    def _compile(self, workdir_path: Path, memory_limit_mb: int) -> subprocess.CompletedProcess[str]:
        command = self._command(
            workdir_path=workdir_path,
            memory_limit_mb=memory_limit_mb,
            container_command=["sh", "-lc", "g++ -std=c++17 -O2 main.cpp -o main"],
        )
        try:
            return self._run_docker(command, timeout=20)
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
        workdir_path: Path,
        input_text: str,
        expected_output: str,
        time_limit_ms: int,
        memory_limit_mb: int,
    ) -> CaseResult:
        start = time.perf_counter()
        command = self._command(
            workdir_path=workdir_path,
            memory_limit_mb=memory_limit_mb,
            container_command=["./main"],
        )

        try:
            completed = self._run_docker(
                command,
                timeout=max(1, time_limit_ms / 1000),
                input_text=input_text,
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

    def _command(
        self,
        workdir_path: Path,
        memory_limit_mb: int,
        container_command: list[str],
    ) -> list[str]:
        return [
            "docker",
            "run",
            "--rm",
            "--name",
            f"algo-judge-{uuid.uuid4().hex}",
            "--network",
            "none",
            "--cpus",
            "1",
            "--memory",
            f"{memory_limit_mb}m",
            "--pids-limit",
            "64",
            "--workdir",
            "/workspace",
            "--volume",
            f"{workdir_path}:/workspace",
            self.image,
            *container_command,
        ]

    def _run_docker(
        self,
        command: list[str],
        timeout: float,
        input_text: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        container_name = command[command.index("--name") + 1]
        try:
            return subprocess.run(
                command,
                input=input_text,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            try:
                subprocess.run(
                    ["docker", "rm", "-f", container_name],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
            except subprocess.SubprocessError:
                pass
            raise

    def _normalize(self, output: str) -> str:
        return "\n".join(line.rstrip() for line in output.strip().splitlines())

    def _clip(self, output: str) -> str:
        if len(output) <= MAX_OUTPUT_CHARS:
            return output
        return output[:MAX_OUTPUT_CHARS] + "\n[output truncated]"
