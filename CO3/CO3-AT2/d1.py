import random
import time


# -----------------------------------
# Quick Sort with Comparison Counter
# -----------------------------------
comparisons = 0

def quick_sort(arr):
    global comparisons

    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]      # Middle element as pivot

    left = []
    middle = []
    right = []

    for x in arr:
        comparisons += 1
        if x < pivot:
            left.append(x)
        elif x > pivot:
            right.append(x)
        else:
            middle.append(x)

    return quick_sort(left) + middle + quick_sort(right)


# -----------------------------------
# Generate Stock Prices
# -----------------------------------
SIZE = 10000

stock_prices = [round(random.uniform(100, 5000), 2) for _ in range(SIZE)]

print("=" * 60)
print(" Stock Market Analysis using Quick Sort")
print("=" * 60)

print("\nTotal Stock Prices :", SIZE)

start = time.perf_counter()

sorted_prices = quick_sort(stock_prices)

end = time.perf_counter()

execution_time = (end - start) * 1000

print("\nSorting Completed Successfully")

print("Execution Time (ms) :", round(execution_time, 4))
print("Comparisons         :", comparisons)

print("\nFirst 10 Sorted Prices")
print(sorted_prices[:10])

print("\nLast 10 Sorted Prices")
print(sorted_prices[-10:])

print("\nAnalysis")
print("---------------------------------------")
print("Average Case Complexity : O(n log n)")
print("Worst Case Complexity   : O(n²)")
print("Optimized Pivot Used    : Middle Element")
print("Divide and Conquer      : Yes")