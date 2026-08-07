import random
import time
def binary_search(arr, target):
    left = 0
    right = len(arr) - 1
    comparisons = 0
    while left <= right:
        mid = (left + right) // 2
        comparisons += 1
        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1, comparisons
SIZE = 100000
integer_data = sorted(random.sample(range(1, 1000000), SIZE))
integer_target = integer_data[SIZE // 2]
start = time.perf_counter()
index_int, comparisons_int = binary_search(integer_data, integer_target)
end = time.perf_counter()
time_int = (end - start) * 1000
float_data = sorted([round(random.uniform(1, 1000000), 4) for _ in range(SIZE)])
float_target = float_data[SIZE // 2]
start = time.perf_counter()
index_float, comparisons_float = binary_search(float_data, float_target)
end = time.perf_counter()
time_float = (end - start) * 1000
print("=" * 55)
print("      Binary Search Performance Comparison")
print("=" * 55)
print("\nInteger Dataset")
print("----------------------------")
print("Dataset Size        :", SIZE)
print("Target Value        :", integer_target)
print("Index Found         :", index_int)
print("Comparisons         :", comparisons_int)
print("Execution Time(ms)  : {:.6f}".format(time_int))
print("\nFloating Point Dataset")
print("----------------------------")
print("Dataset Size        :", SIZE)
print("Target Value        :", float_target)
print("Index Found         :", index_float)
print("Comparisons         :", comparisons_float)
print("Execution Time(ms)  : {:.6f}".format(time_float))
print("\nAnalysis")
print("----------------------------")
if comparisons_int == comparisons_float:
    print("Both datasets required the same number of comparisons.")
if time_float > time_int:
    print("Floating-point search is slightly slower due to decimal precision handling.")
else:
    print("Execution times are almost identical.")
