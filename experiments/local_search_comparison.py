"""Compare greedy, local-search, and exact covers on small random graphs.

Run from the repository root:
    python -m experiments.local_search_comparison
"""
import csv
from pathlib import Path

from sensorplace import (
    erdos_renyi, exact_branch_and_bound, greedy_degree, local_search
)


def run(output_dir="figures", seed=31):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    rows = []
    for n in (12, 16, 20):
        for repeat in range(5):
            edges = erdos_renyi(n, 4 / (n - 1), seed=seed + n * 10 + repeat)
            greedy = greedy_degree(edges)
            improved = local_search(edges)
            exact, finished = exact_branch_and_bound(
                edges, time_limit=10.0
            )
            rows.append({
                "n": n, "repeat": repeat, "edges": len(edges),
                "greedy_size": len(greedy),
                "local_search_size": len(improved),
                "exact_size": len(exact),
                "exact_finished": finished,
            })
            print(
                f"n={n:2d} sample={repeat} greedy={len(greedy):2d} "
                f"local={len(improved):2d} exact={len(exact):2d} "
                f"finished={finished}"
            )

    csv_path = output / "local_search_comparison.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {csv_path}")
    return rows


if __name__ == "__main__":
    run()
