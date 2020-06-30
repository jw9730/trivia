def main():
    # Try running the various size of benchmarks to test your implmentation and
    # see how efficient an approximation algorithm is!

    # SMALL_BENCHMARK
    small_v = [1, 3, 2, 1, 4]
    small_w = [3, 4, 3, 3, 6]
    small_M = 11

    # MEDIUM_BENCHMARK
    medium_v = [135, 139, 149, 150, 156, 163, 173, 184, 192, 201, 210, 214, 221, 229, 240]
    medium_w = [70, 73, 77, 80, 82, 87, 90, 94, 98, 106, 110, 113, 115, 118, 120]
    medium_M = 750

    # LARGE_BENCHMARK
    large_w = [382745, 799601, 909247, 729069, 467902, 44328, 34610, 698150, 823460, 903959, 853665, 551830,
               610856, 670702, 488960, 951111, 323046, 446298, 931161, 31385, 496951, 264724, 224916, 169684]
    large_v = [825594, 1677009, 1676628, 1523970, 943972, 97426, 69666, 1296457, 1679693,
               1902996, 1844992, 1049289, 1252836, 1319836, 953277, 2067538, 675367, 853655, 1826027, 65731, 901489,
               577243, 466257, 369261]
    large_M = 6404180

    e = 0.001

    A = zero_one_knapsack(small_v, small_w, small_M)
    B = approximate_zero_one_knapsack(small_v, small_w, small_M, e)

    s = "pick "
    for i in range(len(A)):
        if A[i]:
            s += str(i) + " "
    print(s + "as an exact solution")
    s = "pick "
    for i in range(len(A)):
        if B[i]:
            s += str(i) + " "
    print(s + "as an " + str(e) + "-approximating solution")

    A = zero_one_knapsack(large_v, large_w, large_M)
    B = approximate_zero_one_knapsack(large_v, large_w, large_M, e)

    s = "pick "
    for i in range(len(A)):
        if A[i]:
            s += str(i) + " "
    print(s + "as an exact solution")
    s = "pick "
    for i in range(len(A)):
        if B[i]:
            s += str(i) + " "
    print(s + "as an " + str(e) + "-approximating solution")


def zero_one_knapsack(v, w, M):
    """
    Compute an item packing that yields the optimal profit of a 0/1-knapsack packing.
    v[i] and w[i] represents value and weight of i'th item type (starting from index 0) respectively.
    You are required to find out a boolean vector A such that argmax_A{sum_i v[i]*A[i] : w[i]*A[i] <= M} where
    A[i] in {0,1} represents whether the item of type i is picked..

    :param v: list of nonzero positive integer which represents values of item types
    :param w: list of nonzero positive integer which represents weights of item types
    :param M: limitation of packing; summation of weights of all packed items should be less than or equal to M
    :type v: list of nonzero positive integer
    :type w: list of nonzero positive integer
    :type M: nonzero positive integer
    :return an array of boolean whose length is same as the input v, w;
        A[i] = True if i'th item is selected and A[i] = False if not.
    """

    # implement here
    """
    v = sum_i v[i]*A[i], w = sum_i w[i]*A[i]
    T(v,m) := min { w(S) : S subset of {1,…m}, v(S) ≥ v }
    i)      T(0,n) ≤ T(1,n) ≤ … ≤ T(V,n) ≤ W < T(V+1,n)
    ii)     V = max { v : T(v,n) ≤ W }
    iii)    T(v,m) = 0 for v≤0
    iv)     T(v,0) = ∞ for v>0
    v)      T(v,m) = min { T(v,m-1), wm + T(v-vm , m-1) }
    """
    #print("w {}, v {}, M {}".format(w, v, M))
    # Dynamic programming
    # Stop when T(v+1,n) > M and return A for T(v,n)
    def dec(binary):
        lst = [int(x) for x in list('{0:0b}'.format(binary))][::-1]
        return lst + (len(v)-len(lst))*[0]

    T = [(len(v)+1) * [0]]
    A = [(len(v)+1) * [0]]
    while T[-1][-1] <= M:
        v_now = len(T)
        T.append((len(v)+1) * [1e20])
        A.append((len(v)+1) * [0])
        T_now = T[-1]
        A_now = A[-1]
        # T[v, 1] ... T[v, n]
        for m in range(len(v)): # 0 ... n-1
            v_m = v[m]
            w_m = w[m]
            t1 = T_now[m] # T[v, m-1]
            t2 = w_m       # w_m + T[v-v_m, m-1]
            if v_now-1 >= v_m:
                t2 += T[-1-v_m][m]
            if t1 < t2:
                T_now[m+1] = t1
                A_now[m+1] = A_now[m]
                continue
            T_now[m+1] = t2
            if v_now-1 >= v_m:
                A_now[m+1] = A[-1-v_m][m] + 2 ** m
            else:
                A_now[m+1] = 2 ** m
        #print("T[{},:]: {}".format(len(T)-1, T[-1][1:]))
        #print("A[{},:]: {}".format(len(A)-1, A[-1][1:]))
    #print("pick {}".format(dec(A[-2][-1])))
    return dec(A[-2][-1])


def approximate_zero_one_knapsack(v, w, M, e):
    """
    Compute e-approximation of the optimal profit of a 0/1-knapsack packing (e>0);
    If P is the optimal profit of a maximum packing,
    you are required to compute a boolean vector B such that
    P*(1-e) <= (sum_i v[i]*B[i]) with sum_i w[i] * B[i] <= M.
    B[i] in {0, 1} represents whether the item of type i is picked.

    :param v: list of nonzero positive integer which represents values of item types
    :param w: list of nonzero positive integer which represents weights of item types
    :param M: limitation of packing; summation of weights of all packed items should be less than or equal to M
    :param e: parameter of approximation
    :type v: list of nonzero positive integer
    :type w: list of nonzero positive integer
    :type M: nonzero positive integer
    :type e: python float in (0,1)
    :return an array of boolean whose length is same as the input v, w;
        B[i] = True if i'th item is selected and B[i] = False if not.
    """

    # implement here
    """
    k = floor(e·sum(v)/n²) <= e·V/n
    Let v_p' = floor(v_p/k)
    V' = k*V(v_1', v_2', ..., v_n')
    """
    def floor(f): return int(f//1)
    k = max(1, floor(e * sum(v)/len(v)/len(v)))
    v_ = list()
    for v_p in v: v_.append(floor(v_p/k))
    B = zero_one_knapsack(v_, w, M)
    return B


if __name__ == "__main__":
    main()
