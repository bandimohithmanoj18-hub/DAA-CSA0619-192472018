# Adaptive Hybrid Closest-Pair Algorithm

## DAA Assignment

Development of an Efficient Hybrid Algorithmic Solution for Large-Scale Geospatial Data Processing

### Algorithms
1. Brute Force
2. Divide and Conquer
3. Adaptive Hybrid (Divide and Conquer + Brute Force threshold)

### Experimental improvements
The benchmark uses:
- identical reproducible point subsets for all algorithms at each input size;
- multiple timing repetitions;
- median runtime as the primary timing statistic;
- a robust threshold experiment across multiple input sizes;
- separate memory measurement so `tracemalloc` overhead does not distort the runtime metric;
- correctness validation before benchmarking;
- distance-computation counting;
- full result and environment files for report preparation.

### Dataset
Place the real OpenFlights `airports.dat` file in:

```text
Dataset/airports.dat
```

The benchmark interprets latitude and longitude as 2-D coordinates because the assignment explicitly requires Euclidean distance.

### Run

```powershell
pip install -r requirements.txt
python Source_Code/closest_pair_hybrid.py
python Source_Code/plot_results.py
```

### Optional custom benchmark

```powershell
python Source_Code/closest_pair_hybrid.py --sizes 100 250 500 1000 2000 5000 7500 --repeats 5
```

### Outputs

```text
Results/
├── performance_results.csv
├── threshold_results.csv
├── selected_threshold.txt
├── environment.txt
├── final_summary.txt
└── graphs/
    ├── execution_time.png
    ├── execution_time_log.png
    ├── distance_computations.png
    ├── memory_usage.png
    └── threshold_effect.png
```

Do not use synthetic-mode results in the final report. Synthetic mode is only for implementation testing.
