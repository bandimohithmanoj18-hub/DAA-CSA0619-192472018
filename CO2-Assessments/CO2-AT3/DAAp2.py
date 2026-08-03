def string_match(text, pattern):
    """
    Finds all occurrences of a pattern in a text using
    the Brute Force String Matching algorithm.

    Parameters:
        text (str): Input text
        pattern (str): Pattern to search

    Returns:
        list: Starting indices where pattern occurs
    """

    # Handle empty pattern explicitly
    if pattern == "":
        return []

    n = len(text)
    m = len(pattern)

    matches = []

    for i in range(n - m + 1):

        for j in range(m):

            if text[i + j] != pattern[j]:
                break

        else:
            matches.append(i)

    return matches


# Example

text = "ABABCABCAB"

pattern = "ABC"

print("Text :", text)
print("Pattern :", pattern)
print("Match Positions :", string_match(text, pattern))