def determinant(A):
    """
    Compute the determinant of a square matrix.
    """

    # Assert that `A` is a square matrix.
    N = len(A)
    for row in A:
        assert len(row) == N

    A = [row.copy() for row in A]

    # Make `A` into an upper triangular matrix.
    sign = 1
    for k in range(N):
        if A[k][k] == 0:
            below = [i for i in range(k + 1, N) if A[i][k] != 0]
            if len(below) == 0:
                return 0
            else:
                i = below[0]
                A[k], A[i] = A[i], A[k]
                sign *= -1
                del i

        for i in range(k + 1, N):
            # Find c such that A[i][k] - c*A[k][k] = 0
            c = A[i][k] / A[k][k]
            A[i][k] = 0
            for j in range(k + 1, N):
                A[i][j] -= c * A[k][j]

    prod = 1
    for k in range(N):
        prod *= A[k][k]
    return sign * prod