#!/usr/bin/env python3

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt


# ============================================================
# 2DOF simple_arm 的正运动学 FK
# ============================================================
def forward_kinematics(q1, q2):

    link1_length = 0.5
    link2_length = 0.4
    base_height = 0.1

    x = (
        link1_length * math.sin(q1)
        + link2_length * math.cos(q1 + q2)
    )

    z = (
        base_height
        + link1_length * math.cos(q1)
        - link2_length * math.sin(q1 + q2)
    )

    return x, z


def main():

    results_dir = (
        Path(__file__).parent.parent
        / "results"
    )

    csv_file = (
        results_dir
        / "cartesian_waypoints.csv"
    )

    # ========================================================
    # 1. 读取 Day 14 的 Cartesian waypoint
    # ========================================================
    cartesian_x = []
    cartesian_z = []
    t_values = []
    q1_values = []
    q2_values = []

    with open(csv_file, "r") as f:

        reader = csv.DictReader(f)

        for row in reader:

            t_values.append(
                float(row["t"])
            )

            cartesian_x.append(
                float(row["x"])
            )

            cartesian_z.append(
                float(row["z"])
            )

            q1_values.append(
                float(row["joint1"])
            )

            q2_values.append(
                float(row["joint2"])
            )

    # ========================================================
    # 2. 取相同的起点和终点关节角
    # ========================================================
    q1_start = q1_values[0]
    q2_start = q2_values[0]

    q1_goal = q1_values[-1]
    q2_goal = q2_values[-1]

    print("Joint-space interpolation:")
    print(
        f"START q = "
        f"({q1_start:.4f}, {q2_start:.4f})"
    )

    print(
        f"GOAL  q = "
        f"({q1_goal:.4f}, {q2_goal:.4f})"
    )

    # ========================================================
    # 3. 在关节空间做线性插值
    #
    # q(t) = q_start + t * (q_goal - q_start)
    # ========================================================
    joint_space_x = []
    joint_space_z = []

    for t in t_values:

        q1 = (
            q1_start
            + t * (q1_goal - q1_start)
        )

        q2 = (
            q2_start
            + t * (q2_goal - q2_start)
        )

        # 用 FK 求这组关节角对应的末端位置
        x, z = forward_kinematics(
            q1,
            q2
        )

        joint_space_x.append(x)
        joint_space_z.append(z)

        print(
            f"t={t:.1f} "
            f"q=({q1:.4f}, {q2:.4f}) "
            f"-> xyz=({x:.3f}, 0.000, {z:.3f})"
        )

    # ========================================================
    # 4. 绘图
    # ========================================================
    plt.figure(
        figsize=(8, 6)
    )

    plt.plot(
        cartesian_x,
        cartesian_z,
        marker="o",
        label="Cartesian interpolation"
    )

    plt.plot(
        joint_space_x,
        joint_space_z,
        marker="x",
        label="Joint-space interpolation"
    )

    # 起点
    plt.scatter(
        [cartesian_x[0]],
        [cartesian_z[0]],
        s=100,
        label="Start"
    )

    # 终点
    plt.scatter(
        [cartesian_x[-1]],
        [cartesian_z[-1]],
        s=100,
        label="Goal"
    )

    plt.xlabel(
        "X position (m)"
    )

    plt.ylabel(
        "Z position (m)"
    )

    plt.title(
        "End-Effector Path Comparison"
    )

    plt.grid(True)

    plt.axis("equal")

    plt.legend()

    plt.tight_layout()

    # ========================================================
    # 5. 保存图片
    # ========================================================
    output_file = (
        results_dir
        / "cartesian_vs_joint_path.png"
    )

    plt.savefig(
        output_file,
        dpi=200
    )

    print()
    print(
        f"Saved plot to: "
        f"{output_file}"
    )

    plt.show()


if __name__ == "__main__":
    main()