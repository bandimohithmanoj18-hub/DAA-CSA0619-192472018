ALGORITHM GeneratePermutations(A, left, right)

INPUT:
    A     = array containing n distinct elements
    left  = starting index
    right = final index

OUTPUT:
    all possible permutations of A

BEGIN
    IF left = right THEN
        PRINT A
        RETURN
    END IF

    FOR i <- left TO right DO
        SWAP A[left] AND A[i]

        GeneratePermutations(A, left + 1, right)

        SWAP A[left] AND A[i]    // backtracking
    END FOR
END

MAIN
    READ n
    READ elements into A
    GeneratePermutations(A, 0, n - 1)
END