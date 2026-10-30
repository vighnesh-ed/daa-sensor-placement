"""Find the practical size limit ("wall") of exact vertex-cover search.

Run from the repository root:
    python -m experiments.wall
"""
import csv
import time
from pathlib import Path

import matplotlib.pyplot as plt

from sensorplace import erdos_renyi, exact_branch_and_bound, preferential_attachment

SIZES = (20, 40, 60, 80, 100, 120, 160)


def run(output_dir="figures", time_limit=10.0, seed=11):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    rows = []
    for family in ("random_avg_degree_8", "hub_heavy"):
        for n in SIZES:
            if family == "random_avg_degree_8":
                edges = erdos_renyi(n, 8 / (n - 1), seed=seed + n)
            else:
                edges = preferential_attachment(n, m=4, seed=seed + n)
            stats = {}
            started = time.perf_counter()
            cover, finished = exact_branch_and_bound(
                edges, time_limit=time_limit, stats=stats
            )
            elapsed = time.perf_counter() - started
            row = {
                "family": family, "n": n, "edges": len(edges),
                "seconds": round(elapsed, 6), "finished": finished,
                "cover_size": len(cover), "search_nodes": stats["nodes"],
            }
            rows.append(row)
            print(f"{family:22s} n={n:3d} E={len(edges):4d} "
                  f"time={elapsed:7.3f}s finished={finished} "
                  f"nodes={stats['nodes']}")

    csv_path = output / "exact_search_wall.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    fig, ax = plt.subplots(figsize=(9, 5))
    for family in ("random_avg_degree_8", "hub_heavy"):
        selected = [r for r in rows if r["family"] == family]
        ax.plot([r["n"] for r in selected], [r["seconds"] for r in selected],
                marker="o", label=family)
    ax.axhline(5.0, linestyle="--", label="5-second reference")
    ax.set_yscale("log")
    ax.set_xlabel("Number of vertices (n)")
    ax.set_ylabel("Runtime in seconds (log scale)")
    ax.set_title("Practical scalability of exact vertex-cover search")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output / "exact_search_wall.png", dpi=200)
    plt.close(fig)
    print(f"Saved {csv_path} and {output / 'exact_search_wall.png'}")
    return rows


if __name__ == "__main__":
    run()
