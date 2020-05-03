PRIME = 30011


def main():
    import time
    start = time.clock()
    
    # Evaluate implemented functions measuring its CPU time on various inputs.
    # Measurement is intended to be understood as per trial on a single input not as 'for n = 1...10^10 do f(n)'
    
    #print(FibRec(36))
    #print(FibIter(40000000))
    print(FibRepSq(2147483647))
    
    print("CPU time used (s): " + str(time.clock() - start))
    
    
def FibRec(n):
    """
    20pts. Implement Fibonacci number with Recursive algorithm
    @param n: 
    int
    @return:
    int. return fib(n) modulo PRIME. 
    See the side section its definition
    """    
    #implement here
    if n == 0 or n == 1: return n
    # Recursive call
    return (FibRec(n-1) + FibRec(n-2)) % PRIME


def FibIter(n):
    """
    20pts. Implement Fibonacci number with Iterative algorithm
    @param n: 
    int
    @return:
    int. return fib(n) modulo PRIME. 
    See the side section its definition
    """    
    #implement here
    if n == 0: return 0
    if n == 1: return 1
    if n == 2: return 1
    
    # Maintain 3 most recent fibonacci sequence values
    FibList = [0, 1, 1]
    
    for i in range(n-2):
        FibList[0] = FibList[1]
        FibList[1] = FibList[2]
        FibList[2] = (FibList[0] + FibList[1]) % PRIME
    
    return FibList[2] #% PRIME
    

def FibRepSq(n):
    """
    30pts. Implement Fibonacci number with Repeated Squaring algorithm
    @param n: 
    int
    @return:
    int. return fib(n) modulo PRIME. 
    See the side section its definition
    """    
    #implement here
    
    if n == 0: return 0
    if n == 1: return 1
    
    # Auxiliary function
    def SquaredArray(n):
        # Compute
        #   A^n = [[a c]
        #          [b d]]
        # where
        #   A = [[1 1]
        #        [1 0]]
        
        # divide-and-conquer
        if n == 1: return (1, 1, 1, 0)
        
        if n % 2 == 0:
            a, b, c, d = SquaredArray(n/2)
            tmp = b*c
            return ((a*a+tmp) % PRIME, (a*b+b*d) % PRIME, (a*c+c*d) % PRIME, (tmp+d*d) % PRIME)
        
        if n % 2 == 1:
            a, b, c, d = SquaredArray((n-1)/2)
            tmp1 = a*a+b*c
            tmp2 = a*c+c*d
            return ((tmp1+a*b+b*d) % PRIME, tmp1 % PRIME, (tmp2+b*c+d*d) % PRIME, tmp2 % PRIME)
    
    # Compute A^(n-1)
    a, b, c, d = SquaredArray(n-1)
    
    return a #% PRIME
    

'''
30pts (10pts each) Experiment
Try evaluating your implemented functions on different sizes of n
Determine the largest n which makes each function terminates within 30 seconds
The number ranges among (1: [0, 100], 2: [101, 10000], 
3: [10001, 1000000], 4: [1000001, 1000000000], 5: [1000000001, 2147483647])
Store the index of the range that you could reach for each function.
'''
MAX_OF_INPUT_REC = 1 # 7.16 sec taken for n=36
MAX_OF_INPUT_ITER = 4 # 8.30 sec taken for n=40000000
MAX_OF_INPUT_REPSQ = 5 # 7.4e-5 sec taken for n=2147483647


if __name__ == "__main__":
    main()
