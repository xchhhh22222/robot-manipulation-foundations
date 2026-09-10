#!/usr/bin/env python3

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def main():

    package_dir = Path(__file__).parent.parent
    results_dir = package_dir / "results"

    no_obstacle = pd.read_csv(
        results_dir / "no_obstacle.csv"
    )

    with_obstacle = pd.read_csv(
        results_dir / "with_obstacle.csv"
    )

    plt.figure(figsize=(8, 6))

    # 无障碍轨迹
    plt.plot(
        no_obstacle["joint1"],
        no_obstacle["joint2"],
        marker="o",
        label="No obstacle"
    )

    # 有障碍轨迹
    plt.plot(
        with_obstacle["joint1"],
        with_obstacle["joint2"],
        marker="o",
        label="With obstacle"
    )

    # home
    plt.scatter(
        [0.0],
        [0.0],
        s=100,
        label="Home"
    )

    # ready
    plt.scatter(
        [-0.6],
        [0.8],
        s=100,
        label="Ready"
    )

    plt.xlabel("joint1 (rad)")
    plt.ylabel("joint2 (rad)")
    plt.title(
        "MoveIt2 Joint-Space Trajectory Comparison"
    )

    plt.grid(True)
    plt.legend()

    output_file = (
        results_dir / "trajectory_comparison.png"
    )

    plt.savefig(
        output_file,
        dpi=200,
        bbox_inches="tight"
    )

    print(f"Saved plot to: {output_file}")

    plt.show()


if __name__ == "__main__":
    main()