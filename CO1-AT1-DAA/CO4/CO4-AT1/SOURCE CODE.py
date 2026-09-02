import heapq


def huffman_cost(freq):
    # No merge is required for 0 or 1 frequency
    if len(freq) <= 1:
        return 0

    # Convert list into a min-heap
    heapq.heapify(freq)

    total_cost = 0

    # Merge until only one node remains
    while len(freq) > 1:
        first = heapq.heappop(freq)
        second = heapq.heappop(freq)

        merged = first + second
        total_cost += merged

        heapq.heappush(freq, merged)

    return total_cost


# Input
n = int(input("Enter number of frequencies: "))
freq = list(map(int, input("Enter frequencies: ").split()))

# Validate input
if len(freq) != n:
    print("Invalid input: number of frequencies must equal n.")
elif n < 1:
    print("Invalid input: n must be at least 1.")
elif any(f < 0 for f in freq):
    print("Invalid input: frequencies cannot be negative.")
else:
    result = huffman_cost(freq)
    print("Minimum Cost =", result)