'''
This skeleton code shows you how to deal with input/output.
You may or may not utilize this skeleton code.
You can also start from scratch.
'''
threahold = 16

def main():
    N = int(input())
    A = list(map(float, input().split()))
    B = list(map(float, input().split()))

    C = multiply(A, B, N)
    for c in C:
        print('%.10f' % c, end=' ')


def multiply(A, B, N):
    assert len(A) == len(B) == N
    if N > threahold:
        return karatsuba_multiplication(A, B, N)
    else:
        return long_multiplication(A, B, N)


def karatsuba_multiplication(A, B, N):
    # TODO: Implement Karatsuba multiplication
    if N % 2 == 0:
        # (A0(x) + A1(x)*x^N/2)*(B0(x) + B1(x)*x^N/2)
        #   = C0(x) + C1(x)*x^N/2 + C2(x)*x^N
        # C0(x) = A0(x) * B0(x)
        # C2(x) = A1(x) * B1(x)
        # C1(x) = (A0(x) + A1(x)) * (B0(x) + B1(x)) - C0(x) - C2(x)

        A0 = A[:N // 2]  # ind 0        ...     N/2 - 1
        A1 = A[N // 2:]  # ind N/2      ...     N - 1
        B0 = B[:N // 2]  # ind 0        ...     N/2 - 1
        B1 = B[N // 2:]  # ind N/2      ...     N - 1
        assert len(A0) == len(A1) == len(B0) == len(B1)

        def list_add(a, b): return [a_i + b_i for a_i, b_i in zip(a, b)]
        def list_sub(a, b): return [a_i - b_i for a_i, b_i in zip(a, b)]

        C0 = multiply(A0, B0, N // 2)
        C2 = multiply(A1, B1, N // 2)
        C1 = list_sub(multiply(list_add(A0, A1), list_add(B0, B1), N // 2), list_add(C0, C2))

        # Degrees of coefficients
        # C:        0   - 2N-2
        # C0:       0   - N-2
        # C1*x^N/2: N/2 - N+N/2-2
        # C2*x^N:   N   - 2*N-2
        C = [0] * (2 * N - 1)
        for k in range(0, N - 1, 1): C[k] = C[k] + C0[k]
        for k in range(N // 2, N + N // 2 - 1, 1): C[k] = C[k] + C1[k - N // 2]
        for k in range(N, 2 * N - 1, 1): C[k] = C[k] + C2[k - N]

    else:
        # Let M = N + 1
        # Then M % 2 == 0
        # Compute [A, 0] * [B, 0] -> discard last 2 coefficients
        M = N + 1
        A_ = A + [0]
        B_ = B + [0]
        C_ = multiply(A_, B_, M)
        assert C_[-2] == C_[-1] == 0
        C = C_[:-2]
        
    return C


def long_multiplication(A, B, N):
    # TODO: Implement long multiplication
    C = [0]*(2*N-1)
    for k in range(2*N-1):
        for i in range(N):
            j = k - i
            if 0 <= j < N:
                # print(f"C[{k}] = A[{i}] * B[{j}] = {A[i]} * {B[j]}")
                C[k] = C[k] + A[i] * B[j]
    return C


if __name__ == '__main__':
    main()
