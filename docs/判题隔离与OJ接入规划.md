# 判题隔离与 OJ 接入规划

## 当前状态

当前临时 OJ 使用 `local-process` 判题器：

```text
FastAPI /api/submissions
  -> JudgeService
    -> LocalJudge
      -> g++ 编译
      -> 本机进程运行测试点
      -> SQLite 保存提交记录
```

当前能力：

- 支持 C++17。
- 支持公开测试点和隐藏测试点。
- 支持编译错误、答案错误、运行错误、超时等基础状态。
- 支持提交记录 SQLite 持久化。
- 暴露 `GET /api/judge` 查询当前判题器能力。

当前隔离级别：

```text
process-timeout-only
```

含义是：只依赖临时目录、进程超时和输出截断。它适合 MVP 本地开发验证，不适合正式开放给不可信用户提交任意代码。

## 已建立的 Adapter 边界

后端入口不再直接调用具体判题器，而是通过：

```text
backend/app/judge/base.py
backend/app/judge/service.py
backend/app/judge/local_judge.py
```

后续替换方向：

```text
JudgeService
  -> LocalJudge
  -> DockerJudge
  -> ExternalOjJudge
```

目前可通过环境变量预留选择入口：

```text
JUDGE_ADAPTER=local-process
JUDGE_ADAPTER=docker
```

当前已新增 `DockerJudge` 适配器骨架。它默认不启用；本机已检测到 Docker CLI，但 Docker daemon 当前未启动，因此本地开发默认仍保持 `local-process`。

## 风险清单

本地进程判题器仍存在以下风险：

- 学生代码在宿主机进程中运行。
- 没有文件系统隔离。
- 没有系统调用隔离。
- 没有内存限制。
- 没有网络隔离。
- Windows 下资源限制能力较弱。

因此正式部署前必须替换为 Docker 沙箱或外部 OJ。

## Docker 沙箱方案

推荐下一阶段实现 `DockerJudge`：
当前已有第一版 `DockerJudge`，后续需要在 Docker daemon 可用的机器上完成实测和加固。

```text
FastAPI
  -> DockerJudge
    -> 创建一次性工作目录
    -> docker run --rm
    -> 挂载只读源码和测试数据
    -> 限制 CPU、内存、网络、运行时间
    -> 收集 stdout/stderr
```

建议限制：

- `--network none`
- `--memory 128m` 或按题目配置。
- `--cpus 1`
- `--pids-limit 64`
- 只挂载单次提交目录。
- 容器内使用非 root 用户。
- 编译和运行分阶段执行。
- 输出长度继续截断。

Windows 本地开发可先确认 Docker Desktop 是否可用；生产环境建议使用 Linux 容器宿主机。

## 外部 OJ 方案

如果后续接入公司在线 OJ，建议实现 `ExternalOjJudge`：

```text
FastAPI
  -> ExternalOjJudge
    -> 将 problem_id 映射到外部 OJ 题目 ID
    -> 提交源码
    -> 轮询判题状态
    -> 转换为本系统 SubmissionResult
    -> 保存到本地 SQLite / 数据库
```

需要确认：

- 外部 OJ 的题目 ID 映射方式。
- 是否允许上传隐藏测试点，或只能使用外部题库。
- 判题状态枚举。
- 提交频率限制。
- 用户身份和班级数据如何同步。
- 错误输出和测试点详情是否可获取。

## 推荐实施顺序

1. 保持 `LocalJudge` 作为本地开发默认适配器。
2. 增加 `DockerJudge` 骨架和可用性检测。
3. 在 Linux / Docker Desktop 环境下完成一次容器判题。
4. 将 `JUDGE_ADAPTER=docker` 接入启动配置。
5. 再根据合作方接口实现 `ExternalOjJudge`。
6. 最后把 SQLite 迁移到正式数据库，并加入用户、班级和统计维度。
