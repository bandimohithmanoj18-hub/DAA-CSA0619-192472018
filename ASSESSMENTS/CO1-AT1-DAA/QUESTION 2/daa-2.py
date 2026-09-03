import time
import math

def smart_grid(n):
    if n == 1:
        return 1
    return 4 * smart_grid(n // 2) + int(n * math.log2(n))

n = int(input("Enter the value of n (power of 2): "))

if n < 1:
    print("Invalid Input")
    exit()

start = time.perf_counter()

result = smart_grid(n)

end = time.perf_counter()

depth = int(math.log2(n)) if n > 1 else 0

print("\n========== OUTPUT ==========")
print("Recurrence Relation : T(n) = 4T(n/2) + nlog₂n")
print("Input Size (n)      :", n)
print("Computed Value      :", result)
print("Recursion Depth     :", depth)
print("Execution Time      : {:.10f} seconds".format(end - start))
print("Time Complexity     : Θ(n²)")
print("Space Complexity    : Θ(log₂ n)")