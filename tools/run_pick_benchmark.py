#!/usr/bin/env python3
import csv
import argparse
from datetime import datetime
from pathlib import Path
import subprocess


# ============================================================
# 路径
# ============================================================

REPO_ROOT = Path(__file__).resolve().parents[1]

ROS2_WS = REPO_ROOT / "ros2_ws"

LOG_DIR = (
    REPO_ROOT
    / "artifacts"
    / "baseline_logs"
)
BENCHMARK_DIR = (
    REPO_ROOT
    / "artifacts"
    / "benchmarks"
)

RESULTS_CSV = (
    BENCHMARK_DIR
    / "pick_benchmark_results.csv"
)

# ============================================================
# 运行结果分类
# ============================================================

def classify_result(
    log_text,
    return_code,
):
    """
    根据运行日志和进程返回码，
    对一次 Pick & Place 运行进行分类。

    返回：
        result
        failure_stage
        failure_type
        detail
    """

    # --------------------------------------------------------
    # 1. 完整成功
    # --------------------------------------------------------

    if (
        "完整 Pick & Place 执行成功 ✅"
        in log_text
        and return_code == 0
    ):
        return (
            "PASS",
            "NONE",
            "NONE",
            "full pick-and-place success",
        )

    # --------------------------------------------------------
    # 2. 启动 / Python packaging 失败
    #
    # 对应我们真实遇到的 run02：
    #
    # PackageNotFoundError:
    # No package metadata was found for moveit-6dof-demos
    # --------------------------------------------------------

    if "PackageNotFoundError" in log_text:
        return (
            "FAIL",
            "STARTUP",
            "PACKAGE_ERROR",
            "PackageNotFoundError",
        )

    # --------------------------------------------------------
    # 3. Planning Failure
    #
    # 每个规划阶段分别识别，
    # 这样以后不仅知道 PLAN_FAILED，
    # 还能知道具体死在哪一步。
    # --------------------------------------------------------

    planning_failures = [
        (
            "Pre-grasp Joint Goal 规划失败",
            "PREGRASP",
        ),
        (
            "Grasp Joint Goal 规划失败",
            "GRASP",
        ),
        (
            "Lift Joint Goal 规划失败",
            "LIFT",
        ),
        (
            "Pre-place Joint Goal 规划失败",
            "PREPLACE",
        ),
        (
            "Place Joint Goal 规划失败",
            "PLACE",
        ),
        (
            "Retreat Joint Goal 规划失败",
            "RETREAT",
        ),
    ]

    for message, stage in planning_failures:

        if message in log_text:
            return (
                "FAIL",
                stage,
                "PLAN_FAILED",
                message,
            )

    # --------------------------------------------------------
    # 4. Gripper Failure
    # --------------------------------------------------------

    gripper_failures = [
        "gripper_controller 不可用",
        "夹爪 Action 未返回 GoalHandle",
        "夹爪目标被拒绝",
        "夹爪 Action 未返回结果",
        "夹爪动作失败",
        "夹爪 CLOSED 失败",
        "Place OPEN 失败",
    ]

    for message in gripper_failures:

        if message in log_text:
            return (
                "FAIL",
                "GRIPPER",
                "GRIPPER_FAILED",
                message,
            )

    # --------------------------------------------------------
    # 5. Arm Execution Failure
    # --------------------------------------------------------

    execution_failures = [
        (
            "Pre-grasp 执行失败",
            "PREGRASP",
        ),
        (
            "Grasp 执行失败",
            "GRASP",
        ),
        (
            "Lift 执行失败",
            "LIFT",
        ),
        (
            "Pre-place 执行失败",
            "PREPLACE",
        ),
        (
            "Place 执行失败",
            "PLACE",
        ),
        (
            "Retreat 执行失败",
            "RETREAT",
        ),
    ]

    for message, stage in execution_failures:

        if message in log_text:
            return (
                "FAIL",
                stage,
                "EXECUTION_FAILED",
                message,
            )

    # --------------------------------------------------------
    # 6. 未知失败
    #
    # 程序确实没有完整成功，
    # 但目前规则还不认识这种错误。
    #
    # 不能硬猜原因，所以统一留给 UNKNOWN。
    # --------------------------------------------------------

    return (
        "FAIL",
        "UNKNOWN",
        "UNKNOWN_FAILED",
        f"return_code={return_code}",
    )

# ============================================================
# Benchmark CSV 写入
# ============================================================

def append_result_to_csv(
    timestamp,
    result,
    failure_stage,
    failure_type,
    detail,
    return_code,
    log_path,
):
    """
    把一次运行结果追加到 benchmark CSV。

    如果 CSV 第一次创建，
    自动写入表头。
    """

    BENCHMARK_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_exists = RESULTS_CSV.exists()

    with RESULTS_CSV.open(
        "a",
        encoding="utf-8",
        newline="",
    ) as csv_file:

        writer = csv.writer(csv_file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "result",
                "failure_stage",
                "failure_type",
                "detail",
                "return_code",
                "log_file",
            ])

        writer.writerow([
            timestamp,
            result,
            failure_stage,
            failure_type,
            detail,
            return_code,
            log_path.name,
        ])

# ============================================================
# 单次 Pick & Place 运行
# ============================================================

def run_once():

    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    log_path = (
        LOG_DIR
        / f"pick_benchmark_{timestamp}.log"
    )

    command = [
        "ros2",
        "launch",
        "moveit_6dof_demos",
        "pick_demo.launch.py",
    ]

    print(
        f"开始运行 Pick & Place",
        flush=True,
    )

    print(
        f"日志文件：{log_path}",
        flush=True,
    )

    process = subprocess.Popen(
        command,
        cwd=ROS2_WS,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    log_lines = []

    with log_path.open(
        "w",
        encoding="utf-8",
    ) as log_file:

        for line in process.stdout:

            print(
                line,
                end="",
                flush=True,
            )

            log_file.write(line)
            log_file.flush()

            log_lines.append(line)

    return_code = process.wait()

    log_text = "".join(log_lines)

    # ========================================================
    # 结果分类
    # ========================================================

    (
        result,
        failure_stage,
        failure_type,
        detail,
    ) = classify_result(
        log_text,
        return_code,
    )
    append_result_to_csv(
        timestamp,
        result,
        failure_stage,
        failure_type,
        detail,
        return_code,
        log_path,
    )

    print()
    return {
        "timestamp": timestamp,
        "result": result,
        "failure_stage": failure_stage,
        "failure_type": failure_type,
        "detail": detail,
        "return_code": return_code,
        "log_file": log_path.name,
    }
    print(
        f"运行结果：{result}",
        flush=True,
    )

    print(
        f"失败阶段：{failure_stage}",
        flush=True,
    )

    print(
        f"失败类型：{failure_type}",
        flush=True,
    )

    print(
        f"详细信息：{detail}",
        flush=True,
    )

# ============================================================
# 程序入口
# ============================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=(
            "Run repeated Pick & Place benchmark trials."
        )
    )

    parser.add_argument(
        "--runs",
        type=int,
        default=1,
        help="Number of benchmark runs.",
    )

    args = parser.parse_args()

    run_results = []

    for run_index in range(
        1,
        args.runs + 1,
    ):

        print()
        print(
            "=" * 60,
            flush=True,
        )

        print(
            f"Benchmark Run "
            f"{run_index}/{args.runs}",
            flush=True,
        )

        print(
            "=" * 60,
            flush=True,
        )

        run_result = run_once()

        run_results.append(
            run_result
        )
    # ========================================================
    # Benchmark Summary
    # ========================================================

    total_runs = len(
        run_results
    )

    pass_runs = sum(
        1
        for item in run_results
        if item["result"] == "PASS"
    )

    fail_runs = (
        total_runs
        - pass_runs
    )

    if total_runs > 0:
        success_rate = (
            pass_runs
            / total_runs
            * 100.0
        )
    else:
        success_rate = 0.0

    print()
    print(
        "=" * 60,
        flush=True,
    )

    print(
        "Benchmark Summary",
        flush=True,
    )

    print(
        "=" * 60,
        flush=True,
    )

    print(
        f"Runs: {total_runs}",
        flush=True,
    )

    print(
        f"PASS: {pass_runs}",
        flush=True,
    )

    print(
        f"FAIL: {fail_runs}",
        flush=True,
    )

    print(
        f"Success Rate: "
        f"{success_rate:.1f}%",
        flush=True,
    )