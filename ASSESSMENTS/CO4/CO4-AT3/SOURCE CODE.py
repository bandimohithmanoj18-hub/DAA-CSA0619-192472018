def lcs_dp(x, y):
    """Return one LCS and its length using Dynamic Programming."""
    m = len(x)
    n = len(y)

    # dp[i][j] = LCS length of x[:i] and y[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Reconstruct one optimal LCS
    i, j = m, n
    result = []

    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            result.append(x[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    result.reverse()
    return "".join(result), dp[m][n]


def greedy_lcs_attempt(x, y):
    """
    Greedy attempt:
    Scan x from left to right and always choose the first
    matching character available in y after the current position.
    """
    j = 0
    result = []

    for ch in x:
        while j < len(y) and y[j] != ch:
            j += 1

        if j == len(y):
            break

        result.append(ch)
        j += 1

    return "".join(result)


# Input
x = input("Enter first string: ").strip()
y = input("Enter second string: ").strip()

lcs_result, lcs_length = lcs_dp(x, y)
greedy_result = greedy_lcs_attempt(x, y)

print("\nDynamic Programming")
print("LCS =", lcs_result)
print("LCS Length =", lcs_length)

print("\nGreedy Matching Attempt")
print("Greedy Result =", greedy_result)
print("Greedy Length =", len(greedy_result))

if len(greedy_result) == lcs_length:
    print("\nConclusion: Greedy found an optimal LCS for this input.")
else:
    print("\nConclusion: Greedy failed to find the optimal LCS.")
