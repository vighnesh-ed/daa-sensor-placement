"""Measure how degree-1 and lower-bound pruning affect exact-search nodes.

Run from the repository root:
    python -m experiments.pruning_ablation
"""
import csv
import time
from pathlib import Path

import matplotlib.pyplot as plt

from sensorplace import erdos_renyi, exact_branch_and_bound

SIZES = (20,  30, 40, 50)
MODES = {
    "no_pruning": (False, False),
    "degree1_only": (True, False),
    "bound_only": (False, True),
    "both": (True, True),
}


def run(output_dir="figures", time_limit=5.0, seed=7):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    rows = []
    for n in SIZES:
        # Expected average degree is approximately four.
        edges = erdos_renyi(n, 4 / (n - 1), seed=seed + n)
        for label, (degree1, bound) in MODES.items():
            stats = {}
            started = time.perf_counter()
            cover, finished = exact_branch_and_bound(
                edges, time_limit=time_limit, stats=stats,
                use_degree1=degree1, use_bound=bound
            )
            elapsed = time.perf_counter() - started
            rows.append({
                "n": n, "mode": label, "nodes": stats["nodes"],
                "seconds": round(elapsed, 6),
                "finished": finished, "cover_size": len(cover),
            })
            print(f"n={n:3d} {label:14s} nodes={stats['nodes']:9d} "
                  f"finished={finished} cover={len(cover)}")

    csv_path = output / "pruning_ablation.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    fig, ax = plt.subplots(figsize=(9, 5))
    for label in MODES:
        selected = [r for r in rows if r["mode"] == label]
        ax.plot([r["n"] for r in selected], [r["nodes"] for r in selected],
                marker="o", label=label)
    ax.set_yscale("log")
    ax.set_xlabel("Number of vertices (n)")
    ax.set_ylabel("Recursive search nodes (log scale)")
    ax.set_title("Effect of pruning rules on exact vertex-cover search")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output / "pruning_ablation.png", dpi=200)
    plt.close(fig)
    print(f"Saved {csv_path} and {output / 'pruning_ablation.png'}")
    return rows


if __name__ == "__main__":
    run()
