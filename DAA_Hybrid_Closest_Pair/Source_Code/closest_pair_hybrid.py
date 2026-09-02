from __future__ import annotations

"""Adaptive Hybrid Closest-Pair benchmark for the DAA assignment.

The implementation follows the assignment requirements:
- Brute Force closest pair
- Divide-and-Conquer closest pair
- Hybrid version that switches to Brute Force below a threshold
- Experimental threshold selection
- Correctness validation
- Runtime, distance-computation, and peak-memory measurements
- Reproducible benchmarking and CSV outputs

The assignment explicitly requires Euclidean distance, so latitude/longitude are
used as 2-D Cartesian coordinates rather than geodesic distance.
"""

import argparse
import csv
import math
import os
import platform
import statistics
import sys
import time
import tracemalloc
from dataclasses import dataclass
from pathlib import Path
from random import Random
from typing import Iterable, Optional


@dataclass(frozen=True)
class Point:
    x: float
    y: float
    name: str = ""


@dataclass
class Result:
    p1: Optional[Point]
    p2: Optional[Point]
    distance: float
    distance_computations: int = 0


class DistanceCounter:
    def __init__(self) -> None:
        self.count = 0

    def distance_sq(self, a: Point, b: Point) -> float:
        self.count += 1
        dx = a.x - b.x
        dy = a.y - b.y
        return dx * dx + dy * dy


def brute_force(points: list[Point], counter: DistanceCounter | None = None) -> Result:
    counter = counter or DistanceCounter()
    if len(points) < 2:
        return Result(None, None, math.inf, counter.count)

    best_d2 = math.inf
    best_pair: tuple[Point | None, Point | None] = (None, None)
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            d2 = counter.distance_sq(points[i], points[j])
            if d2 < best_d2:
                best_d2 = d2
                best_pair = (points[i], points[j])

    return Result(best_pair[0], best_pair[1], math.sqrt(best_d2), counter.count)


def _better(a: Result, b: Result) -> Result:
    return a if a.distance <= b.distance else b


def _split_y(points_y: list[Point], left_points: list[Point]) -> tuple[list[Point], list[Point]]:
    left_ids = {id(p) for p in left_points}
    left_y: list[Point] = []
    right_y: list[Point] = []
    for p in points_y:
        if id(p) in left_ids:
            left_y.append(p)
        else:
            right_y.append(p)
    return left_y, right_y


def _closest_recursive(
    px: list[Point],
    py: list[Point],
    counter: DistanceCounter,
    threshold: int | None = None,
) -> Result:
    n = len(px)
    if n <= 3 or (threshold is not None and n <= threshold):
        return brute_force(px, counter)

    mid = n // 2
    left_x = px[:mid]
    right_x = px[mid:]
    mid_x = px[mid].x
    left_y, right_y = _split_y(py, left_x)

    left_result = _closest_recursive(left_x, left_y, counter, threshold)
    right_result = _closest_recursive(right_x, right_y, counter, threshold)
    best = _better(left_result, right_result)
    delta2 = best.distance * best.distance

    strip = [p for p in py if (p.x - mid_x) ** 2 < delta2]
    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and (strip[j].y - strip[i].y) ** 2 < delta2:
            d2 = counter.distance_sq(strip[i], strip[j])
            if d2 < delta2:
                delta2 = d2
                best = Result(strip[i], strip[j], math.sqrt(d2), counter.count)
            j += 1

    best.distance_computations = counter.count
    return best


def _prepared(points: list[Point]) -> tuple[list[Point], list[Point]]:
    px = sorted(points, key=lambda p: (p.x, p.y, p.name))
    py = sorted(points, key=lambda p: (p.y, p.x, p.name))
    return px, py


def divide_and_conquer(points: list[Point], counter: DistanceCounter | None = None) -> Result:
    counter = counter or DistanceCounter()
    if len(points) < 2:
        return Result(None, None, math.inf, counter.count)
    px, py = _prepared(points)
    result = _closest_recursive(px, py, counter)
    result.distance_computations = counter.count
    return result


def hybrid_closest_pair(
    points: list[Point], threshold: int = 16, counter: DistanceCounter | None = None
) -> Result:
    if threshold < 2:
        raise ValueError("threshold must be >= 2")
    counter = counter or DistanceCounter()
    if len(points) < 2:
        return Result(None, None, math.inf, counter.count)
    px, py = _prepared(points)
    result = _closest_recursive(px, py, counter, threshold)
    result.distance_computations = counter.count
    return result


def load_openflights_airports(path: str | Path) -> list[Point]:
    points: list[Point] = []
    with open(path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        for row in reader:
            if len(row) < 8:
                continue
            try:
                lat = float(row[6])
                lon = float(row[7])
            except (ValueError, TypeError):
                continue
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                continue
            name = row[1] if len(row) > 1 else "Unknown"
            points.append(Point(lat, lon, name))
    return points


def synthetic_points(n: int, seed: int = 2026) -> list[Point]:
    rng = Random(seed)
    return [
        Point(rng.uniform(-90, 90), rng.uniform(-180, 180), f"P{i:06d}")
        for i in range(n)
    ]


def pair_signature(result: Result) -> tuple[str, str]:
    if result.p1 is None or result.p2 is None:
        return ("", "")
    return tuple(sorted((result.p1.name, result.p2.name)))


def validate_all(points: list[Point], threshold: int) -> bool:
    brute = brute_force(points)
    divide = divide_and_conquer(points)
    hybrid = hybrid_closest_pair(points, threshold)
    tolerance = 1e-10
    return (
        math.isclose(brute.distance, divide.distance, rel_tol=0.0, abs_tol=tolerance)
        and math.isclose(brute.distance, hybrid.distance, rel_tol=0.0, abs_tol=tolerance)
        and pair_signature(brute) == pair_signature(divide) == pair_signature(hybrid)
    )


def _run(points: list[Point], algorithm: str, threshold: int) -> Result:
    counter = DistanceCounter()
    if algorithm == "Brute Force":
        result = brute_force(points, counter)
    elif algorithm == "Divide and Conquer":
        result = divide_and_conquer(points, counter)
    elif algorithm == "Hybrid":
        result = hybrid_closest_pair(points, threshold, counter)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")
    result.distance_computations = counter.count
    return result


def _timed_call(points: list[Point], algorithm: str, threshold: int) -> tuple[Result, float, int]:
    start = time.perf_counter()
    result = _run(points, algorithm, threshold)
    elapsed = time.perf_counter() - start
    return result, elapsed, result.distance_computations


def _memory_call(points: list[Point], algorithm: str, threshold: int) -> tuple[Result, float]:
    tracemalloc.start()
    result = _run(points, algorithm, threshold)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, peak / 1024.0


def benchmark(
    points: list[Point], algorithm: str, repeats: int, threshold: int
) -> dict[str, object]:
    # Runtime and memory are measured separately so tracemalloc overhead does not
    # contaminate the primary runtime comparison.
    samples: list[tuple[Result, float, int]] = [
        _timed_call(points, algorithm, threshold) for _ in range(repeats)
    ]
    results = [x[0] for x in samples]
    times = [x[1] for x in samples]
    counts = [x[2] for x in samples]
    memory_samples = [_memory_call(points, algorithm, threshold)[1] for _ in range(max(1, min(3, repeats)))]

    result = results[0]
    return {
        "algorithm": algorithm,
        "input_size": len(points),
        "threshold": threshold if algorithm == "Hybrid" else 0,
        "repeats": repeats,
        "time_seconds_median": statistics.median(times),
        "time_seconds_mean": statistics.mean(times),
        "time_seconds_min": min(times),
        "time_seconds_max": max(times),
        "memory_kb_peak_median": statistics.median(memory_samples),
        "distance_computations": counts[0],
        "distance": result.distance,
        "pair_1": result.p1.name if result.p1 else "",
        "pair_2": result.p2.name if result.p2 else "",
    }


def threshold_search(
    points_by_size: dict[int, list[Point]],
    thresholds: Iterable[int],
    repeats: int,
) -> tuple[list[dict[str, object]], int]:
    """Select a robust threshold using median runtime over multiple input sizes."""
    rows: list[dict[str, object]] = []
    for threshold in thresholds:
        per_size_medians: list[float] = []
        total_comparisons = 0
        for size in sorted(points_by_size):
            points = points_by_size[size]
            times: list[float] = []
            counts: list[int] = []
            for _ in range(repeats):
                _, elapsed, count = _timed_call(points, "Hybrid", threshold)
                times.append(elapsed)
                counts.append(count)
            per_size_medians.append(statistics.median(times))
            total_comparisons += statistics.median(counts)
        rows.append(
            {
                "threshold": threshold,
                "sizes_tested": ";".join(str(s) for s in sorted(points_by_size)),
                "median_time_seconds_across_sizes": statistics.median(per_size_medians),
                "mean_time_seconds_across_sizes": statistics.mean(per_size_medians),
                "median_distance_computations": total_comparisons / len(points_by_size),
            }
        )

    best = min(
        rows,
        key=lambda row: (
            float(row["median_time_seconds_across_sizes"]),
            int(row["threshold"]),
        ),
    )
    return rows, int(best["threshold"])


def save_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def make_subsets(all_points: list[Point], sizes: list[int], seed: int) -> dict[int, list[Point]]:
    rng = Random(seed)
    shuffled = list(all_points)
    rng.shuffle(shuffled)
    return {size: shuffled[:size] for size in sorted(set(sizes)) if size <= len(shuffled)}


def write_environment(results_dir: Path, dataset_label: str, point_count: int) -> None:
    info = {
        "dataset": dataset_label,
        "valid_points": point_count,
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
        "processor": platform.processor() or "unknown",
        "machine": platform.machine(),
        "cpu_count": os.cpu_count(),
    }
    results_dir.mkdir(parents=True, exist_ok=True)
    with (results_dir / "environment.txt").open("w", encoding="utf-8") as handle:
        for key, value in info.items():
            handle.write(f"{key}: {value}\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark Brute Force, Divide-and-Conquer and Hybrid Closest Pair."
    )
    parser.add_argument("--dataset", type=Path, default=None, help="Path to OpenFlights airports.dat")
    parser.add_argument(
        "--sizes",
        nargs="+",
        type=int,
        default=[100, 250, 500, 1000, 2000, 5000, 7500],
    )
    parser.add_argument(
        "--thresholds",
        nargs="+",
        type=int,
        default=[2, 4, 8, 12, 16, 20, 24, 28, 32, 40, 48, 64],
    )
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument(
        "--threshold-sizes",
        nargs="+",
        type=int,
        default=[1000, 2000, 5000],
        help="Input sizes used to select a robust hybrid threshold.",
    )
    parser.add_argument("--threshold-repeats", type=int, default=5)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument(
        "--synthetic-n",
        type=int,
        default=0,
        help="Explicit synthetic mode for implementation testing only.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    results_dir = root / "Results"

    dataset_path = args.dataset or (root / "Dataset" / "airports.dat")
    if args.synthetic_n > 0:
        all_points = synthetic_points(args.synthetic_n, args.seed)
        dataset_label = f"Synthetic test data (n={args.synthetic_n})"
    elif dataset_path.exists():
        all_points = load_openflights_airports(dataset_path)
        dataset_label = f"OpenFlights airports.dat ({dataset_path})"
    else:
        print("ERROR: Dataset/airports.dat was not found.")
        print("Place the real OpenFlights airports.dat file in Dataset/.")
        raise SystemExit(2)

    if len(all_points) < 2:
        raise SystemExit("Dataset contains fewer than two valid coordinate records.")

    write_environment(results_dir, dataset_label, len(all_points))
    print(f"Dataset: {dataset_label}")
    print(f"Valid coordinate records: {len(all_points)}")

    # Build one reproducible shuffled ordering. Every algorithm at a given n gets
    # exactly the same point subset, satisfying the fair-comparison requirement.
    sizes = sorted(set([*args.sizes, *args.threshold_sizes]))
    subsets = make_subsets(all_points, sizes, args.seed)
    threshold_points = {n: subsets[n] for n in args.threshold_sizes if n in subsets}
    if not threshold_points:
        raise SystemExit("None of the threshold-test sizes are available in the dataset.")

    threshold_rows, best_threshold = threshold_search(
        threshold_points, args.thresholds, args.threshold_repeats
    )
    save_csv(results_dir / "threshold_results.csv", threshold_rows)

    print("\nRobust threshold experiment")
    for row in threshold_rows:
        print(
            f"  k={int(row['threshold']):>2}: "
            f"median={float(row['median_time_seconds_across_sizes']):.6f}s, "
            f"mean={float(row['mean_time_seconds_across_sizes']):.6f}s, "
            f"distance calculations={float(row['median_distance_computations']):.1f}"
        )
    print(f"Selected hybrid threshold: {best_threshold}")

    with (results_dir / "selected_threshold.txt").open("w", encoding="utf-8") as handle:
        handle.write(str(best_threshold))

    performance_rows: list[dict[str, object]] = []
    for n in [s for s in sorted(set(args.sizes)) if s in subsets]:
        points = subsets[n]
        if not validate_all(points, best_threshold):
            raise RuntimeError(f"Correctness validation failed for input size {n}")
        print(f"\nInput size {n}: correctness PASS")
        for algorithm in ("Brute Force", "Divide and Conquer", "Hybrid"):
            row = benchmark(points, algorithm, args.repeats, best_threshold)
            performance_rows.append(row)
            print(
                f"  {algorithm:<18} "
                f"median={float(row['time_seconds_median']):.6f}s | "
                f"mean={float(row['time_seconds_mean']):.6f}s | "
                f"{int(row['distance_computations']):,} distance calculations | "
                f"peak memory={float(row['memory_kb_peak_median']):.1f} KB"
            )

    save_csv(results_dir / "performance_results.csv", performance_rows)

    # Compact report-ready summary with the full-dataset result when available.
    largest = max((int(r["input_size"]) for r in performance_rows), default=0)
    summary_rows = [r for r in performance_rows if int(r["input_size"]) == largest]
    with (results_dir / "final_summary.txt").open("w", encoding="utf-8") as handle:
        handle.write(f"Dataset: {dataset_label}\n")
        handle.write(f"Valid coordinate records: {len(all_points)}\n")
        handle.write(f"Selected hybrid threshold: {best_threshold}\n")
        handle.write(f"Largest benchmark size: {largest}\n\n")
        for row in summary_rows:
            handle.write(
                f"{row['algorithm']}: median={float(row['time_seconds_median']):.6f}s, "
                f"distance_calculations={int(row['distance_computations'])}, "
                f"peak_memory={float(row['memory_kb_peak_median']):.1f} KB, "
                f"closest_pair=({row['pair_1']}, {row['pair_2']}), "
                f"distance={float(row['distance']):.12f}\n"
            )

    print(f"\nSaved: {results_dir / 'threshold_results.csv'}")
    print(f"Saved: {results_dir / 'performance_results.csv'}")
    print(f"Saved: {results_dir / 'environment.txt'}")
    print(f"Saved: {results_dir / 'final_summary.txt'}")


if __name__ == "__main__":
    main()
