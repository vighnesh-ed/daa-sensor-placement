"""Check the derived running times of approx_matching and greedy_degree.
Run from the project root:  python -m experiments.complexity_timing

If a function is linear in its input, doubling the input should roughly double
the time (ratio about 2); if it is quadratic, the time should roughly quadruple
(ratio about 4). We use graphs made of n/2 separate links (a perfect matching),
the worst case derived for greedy_degree: every round removes one link but
rescans all n machines."""
import time

from sensorplace import approx_matching, greedy_degree

SIZES = [2000, 4000, 8000, 16000]
REPEATS = 3


def best_time(fn, edges):
    """Fastest of REPEATS runs, which hides one-off slowdowns of the machine."""
    best = float("inf")
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        fn(edges)
        best = min(best, time.perf_counter() - t0)
    return best


def main():
    for fn in (approx_matching, greedy_degree):
        print(fn.__name__)
        prev = None
        for n in SIZES:
            edges = {(2 * i, 2 * i + 1) for i in range(n // 2)}
            t = best_time(fn, edges)
            ratio = f"x{t / prev:.1f} vs previous" if prev else ""
            print(f"  n={n:<6} links={len(edges):<6} time={t * 1000:9.2f} ms  {ratio}")
            prev = t


if __name__ == "__main__":
    main()
