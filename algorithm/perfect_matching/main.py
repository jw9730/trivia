import random
from lib import determinant
import time

DEBUG = False

def main():
    A = [[1, 2, 3], [4, 5, 6], [7, 8, 10]]
    print(determinant(A))

    def f(vars):
        x = vars[0]
        y = vars[1]
        z = vars[2]
        return x * y * z + x * x + 123 + 4 * y

    assert pit_repeater(f, 3, 10, 100) == True

    assert pit_repeater(lambda v: v[0], 1, 1, 10)
    assert not pit_repeater(lambda v: 0, 1, 1, 10)

    graph = [[0, 1], [1, 0]]
    assert has_perfect_matching(graph)

    graph = [
        [0, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0]]
    assert not has_perfect_matching(graph)

    result = estimate_perfect_matching()
    print(result)


#PROBLEM a) - pit(f, n, d) & pit_repeater(f, n, d, N)  
def pit(f, n, d):
    """
    Conducts polynomial identity test on a given funtion f once then
    decides whether a function f is nonzero polynomial or not.
    @param f:
        A function to check if it is non zero polynomial or not.
        f recieves a list of values as argument.
    @param n:
        The number of variables the function f takes.
    @param d:
        The upper bound of the degree of the function f.
    @return: 
        True if the function f is nonzero polynomial, False otherwise.
    """

    # implement here
    # Let S = {1, ..., 2*d}
    x = list()
    for i in range(n):
        x.append(random.randrange(1, 2*d))
    nonzero = f(x) != 0
    #print(x, f(x), nonzero)
    return nonzero


def pit_repeater(f, n, d, N):
    """
    Repeats polynomial identity test on a given funtion up to error bound 2^-N
    @param f:
        A function to check if it is non zero polynomial or not.
        f recieves a list of values as argument.
    @param n:
        The number of variables the function f takes.
    @param d:
        The upper bound of the degree of the function f.
    @param N:
        Repeat count of polynomial identity testing.
    @return:
        True if the function f is nonzero polynomial, False otherwise.
    """
    
    # implement here
    """
    Schwartz-Zippel Lemma
    Fix finite S \in C
    Sample x1...xn from S uniformly random
    Then, p(f(x1...xn)=0) <= d/|S|
    Let |S| = 2d, then do multiple times
    p(f(x1...xn)=0 for trial 1...k) < (d/|S|)^k
    Let S = {-d, ..., d-1}. Then, (1/2)^k <= (1/2)^N
    Therefore, let k >= N
    """
    nonzero = True
    for i in range(N):
        nonzero_i = pit(f, n, d)
        nonzero = nonzero and nonzero_i
    return nonzero
    

def det(val_list, graph):
    V = len(graph)
    ij_list = list()
    for j in range(V):
        for i in range(j):
            if graph[i][j]:
                ij_list.append((i, j))

    #print(val_list, ij_list)
    mat = graph[:][:]
    for k, v in enumerate(val_list):
        i, j = ij_list[k]
        mat[i][j], mat[j][i] = v, -v
    return determinant(mat)


#PROBLEM b) - generate_polynomial_function(graph) & has_perfect_matching(graph)
def generate_polynomial_function(graph):
    """    
    @param graph:
        A 2 dimensional list (matrix) representing n by n graph.
        Element 0 indicates no edge exists between two vertices, and
        Element 1 indicates an edge exists between two vertices.
    @return (f, n, d):   
        f is a polynomial function calculating the determinant of a Tutte matrix of the graph.
        f takes one list of n variables.
        Since Tutte matrix is symbolic ,
        the polynomial function f 
        takes integer values (in one list) and 
        assigns them to variables then 
        calculates and returns the integer determinant.
        n is the number of variables in the polynomial function f.
        d is the degree of the polynomial function f.
    @note: 
        You are recommended to use the provided function `lib.determinant()`.
        Otherwise, you can write a function calculating the determinant of a matrix on your own. 
    """
    
    # implement here
    # 1. compute n by naively counting variables
    num_vars = 0
    V = len(graph)
    for j in range(V):
        for i in range(j):
            num_vars += graph[i][j]
    # 2. give an upper bound of d
    total_deg = num_vars
    # 3. compute a lambda expression that computes Tutte matrix determinant
    f = lambda val_list:(det(val_list=val_list, graph=graph))
    return f, int(num_vars), int(total_deg)


def has_perfect_matching(graph):
    """
    Checks if a given graph has a perfect matching or not.
    The answers are correct with sufficient certainty.
    @return: 
        True if the graph can have a perfect matching, False, otherwise.
    """
    
    # implement here
    """
    graph has a perfect matching iff Tutte matrix determinant is a nonzero polynomial
    error bound 2^-N
    """
    N = 10
    f, n, d = generate_polynomial_function(graph)
    #print(f, n, d)
    return pit_repeater(f, n, d, N)


#PROBLEM c)
def generate_random_graph(n, m):
    """
    Generates a random graph with 
    n exact vertices and 
    m expected edges such that
    - the graph is undirected, simple, and without self loops;
    - let $X_{uv}$ be the 2-valued random variable that reports 
      whether there is an edge between vertices $u$ and $v$. 
      All $X_{uv}$'s are independently and indentically distributed.
    @param n:
        The exact number of vertices.
    @param m:
        The expected number of edges.
    @return:
        A 2 dimensional list (matrix) representing a graph with 
        n vertices and 
        m undirected edges.
        Element 0 indicates no edge exists between two vertices, and
        Element 1 indicates an edge exists between two vertices.
        The 2-dimensional list must be symmetric; that is,
        A[i][j] == A[j][i] for every i, j.
    """

    # implement here
    """
    generate binary vector sized n*(n-1)/2 with m ones
    permute and distribute as edges
    """
    len_tri = int(n*(n-1)/2)
    bitmask = list()
    for i in range(len_tri):
        bitmask.append(random.uniform(0, 1) < float(m) / float(len_tri))

    if DEBUG:
        s = 0
        for i in range(len_tri):
            s += bitmask[i]
        print("generated {} / expected {}".format(s, m))

    graph = list()
    for i in range(n):
        row = list()
        for j in range(n):
            row.append(0)
        graph.append(row)

    k = 0
    for j in range(n):
        for i in range(j):
            graph[i][j], graph[j][i] = bitmask[k], bitmask[k]
            k += 1
    return graph


# PROBLEM d)
def estimate_perfect_matching():
    """
    Reports how many of them admit a perfect matching out of 50 randomly
    generated graphs having 100 vertices and 350/200 edges.
    @return (n_pm_350, n_pm_200):
        A pair of two numbers.
        0 <= n_pm_350 <=50.
        0 <= n_pm_200 <=50.
        n_pm_350 is the number of graphs that admits a perfect matching
        out of 50 randomly generated graphs with 100 vertices and 350 edges.
        n_pm_200 is the number of graphs that admits a perfect matching
        out of 50 randomly generated graphs with 100 vertices and 200 edges.
    @Note:
        This problem is not about testing the efficiency of your code.
        If grading does not finish in time,
        you are allowed to do the experiment on your local machine
        and record the values and just write them in this function.
        In that case, please still leave your code (in comment, for example).
    """

    # implement here
    n_pm_350, n_pm_200 = 0, 0
    for trial in range(50):
        tic = time.time()
        n_pm_350 += has_perfect_matching(generate_random_graph(100, 350))
        n_pm_200 += has_perfect_matching(generate_random_graph(100, 200))
        toc = time.time()
        if DEBUG:
            print("trial {} took {}s: {}, {}".format(trial+1, toc-tic, n_pm_350, n_pm_200))
    return n_pm_350, n_pm_200


if __name__ == "__main__":
    main()
