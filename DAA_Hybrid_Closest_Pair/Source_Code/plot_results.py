from __future__ import annotations

import csv
from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "Results"
GRAPHS = RESULTS / "graphs"
GRAPHS.mkdir(parents=True, exist_ok=True)


def read_csv(name: str) -> list[dict[str, str]]:
    with (RESULTS / name).open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def plot_metric(perf: list[dict[str, str]], metric: str, ylabel: str, filename: str, log_y: bool = False) -> None:
    algorithms = ["Brute Force", "Divide and Conquer", "Hybrid"]
    plt.figure(figsize=(9, 5.5))
    for alg in algorithms:
        rows = [r for r in perf if r["algorithm"] == alg]
        rows.sort(key=lambda r: int(r["input_size"]))
        x = [int(r["input_size"]) for r in rows]
        y = [float(r[metric]) for r in rows]
        plt.plot(x, y, marker="o", linewidth=1.8, label=alg)
    plt.xlabel("Input size (n)")
    plt.ylabel(ylabel)
    plt.title(ylabel + " vs input size")
    if log_y:
        plt.yscale("log")
    plt.grid(True, alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(GRAPHS / filename, dpi=200)
    plt.close()


def main() -> None:
    perf = read_csv("performance_results.csv")
    threshold = read_csv("threshold_results.csv")

    plot_metric(perf, "time_seconds_median", "Median execution time (s)", "execution_time.png")
    plot_metric(perf, "time_seconds_median", "Median execution time (s, log scale)", "execution_time_log.png", log_y=True)
    plot_metric(perf, "distance_computations", "Distance computations", "distance_computations.png", log_y=True)
    plot_metric(perf, "memory_kb_peak_median", "Peak memory (KB)", "memory_usage.png")

    plt.figure(figsize=(9, 5.5))
    x = [int(r["threshold"]) for r in threshold]
    y = [float(r["median_time_seconds_across_sizes"]) for r in threshold]
    plt.plot(x, y, marker="o")
    best_index = min(range(len(y)), key=lambda i: y[i])
    plt.scatter([x[best_index]], [y[best_index]], s=70, zorder=3, label=f"Selected k={x[best_index]}")
    plt.xlabel("Hybrid switching threshold (k)")
    plt.ylabel("Median runtime across threshold-test sizes (s)")
    plt.title("Robust hybrid threshold experiment")
    plt.grid(True, alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(GRAPHS / "threshold_effect.png", dpi=200)
    plt.close()

    print(f"Graphs written to {GRAPHS}")


if __name__ == "__main__":
    main()
