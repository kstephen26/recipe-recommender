from math import sqrt
from pprint import pprint
import numpy as np

# Source: We did not write this code. This code is a simple Python implementation of the well-known QR matrix decomposition method for matrix factorization
# and can be found here: https://www.quantstart.com/articles/QR-Decomposition-with-Python-and-NumPy. This algorithm is called in basicscrape.py.

def mult_matrix(M, N):
    """Multiply square matrices of same dimension M and N"""
    # Converts N into a list of tuples of columns                                                                     
    tuple_N = zip(*N)

    # Nested list comprehension to calculate matrix multiplication                                                    
    # return [[sum(el_m * el_n for el_m, el_n in zip(row_m, col_n)) for col_n in tuple_N] for row_m in M]
    return np.dot(M, N) 

def trans_matrix(M):
    """Take the transpose of a matrix."""
    n = len(M)
    print("M is ", M)
    return [[ M[i][j] for i in range(n)] for j in range(n)]

def norm(x):
    """Return the Euclidean norm of the vector x."""
    return sqrt(sum([x_i**2 for x_i in x]))

def Q_i(Q_min, i, j, k):
    """Construct the Q_t matrix by left-top padding the matrix Q                                                      
    with elements from the identity matrix."""
    if i < k or j < k:
        return float(i == j)
    else:
        return Q_min[i-k][j-k]

def cmp(a, b):
    return (a > b) - (a < b)

def householder(A):
    """Performs a Householder Reflections based QR Decomposition of the                                               
    matrix A. The function returns Q, an orthogonal matrix and R, an                                                  
    upper triangular matrix such that A = QR."""
    n = len(A)

    # Set R equal to A, and create Q as a zero matrix of the same size
    R = A
    print(R)
    Q = [[0.0] * n for i in range(n)]

    # The Householder procedure
    for k in range(n-1):  # We don't perform the procedure on a 1x1 matrix, so we reduce the index by 1
        # Create identity matrix of same size as A                                                                    
        I = [[float(i == j) for i in range(n)] for j in range(n)]
        R = A
        print(R)
        Q = [[0.0] * n for i in range(n)]
        # Create the vectors x, e and the scalar alpha
        # Python does not have a sgn function, so we use cmp instead
        print(R)

        x = [row[k] for row in R[k:]]
        e = [row[k] for row in I[k:]]
        alpha = -cmp(x[0],0) * norm(x)

        # Using anonymous functions, we create u and v
        u = list(map(lambda p,q: p + alpha * q, x, e))
        norm_u = norm(u)
        v = list(map(lambda p: p/norm_u, u))

        # Create the Q minor matrix
        Q_min = [ [float(i==j) - 2.0 * v[i] * v[j] for i in range(n-k)] for j in range(n-k) ]

        # "Pad out" the Q minor matrix with elements from the identity
        Q_t = [[ Q_i(Q_min,i,j,k) for i in range(n)] for j in range(n)]

        # If this is the first run through, right multiply by A,
        # else right multiply by Q
        if k == 0:
            Q = Q_t
            R = mult_matrix(Q_t,A)
            print("Q is: ", Q)
        else:
            print("Q is first: ", Q)
            print("Qt is first: ", Q_t)
            Q = mult_matrix(Q_t,Q)
            R = mult_matrix(Q_t,R)
            print("Q is else: ", Q)

    # Since Q is defined as the product of transposes of Q_t,
    # we need to take the transpose upon returning it
    return trans_matrix(Q), R

A = [[12, -51, 4], [6, 167, -68], [-4, 24, -41]]
Q, R = householder(A)

print(A)
print(Q)
print(R)
print(np.linalg.qr(A))
