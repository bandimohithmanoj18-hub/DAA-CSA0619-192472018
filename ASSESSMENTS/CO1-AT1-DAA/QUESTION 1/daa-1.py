import time
import math

def sensor_network(n):
    if n == 1:
        return 1
    return 3 * sensor_network(n // 3) + 1

n = int(input("Enter the value of n (power of 3): "))

if n < 1:
    print("Invalid Input")
    exit()

start = time.perf_counter()

result = sensor_network(n)

end = time.perf_counter()

depth = int(math.log(n, 3)) if n > 1 else 0

print("\n========== OUTPUT ==========")
print("Recurrence Relation : T(n) = 3T(n/3) + 1")
print("Input Size (n)      :", n)
print("Computed Value      :", result)
print("Recursion Depth     :", depth)
print("Execution Time      : {:.10f} seconds".format(end - start))
print("Time Complexity     : Θ(n)")
print("Space Complexity    : Θ(log₃ n)")