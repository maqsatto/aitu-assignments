EPS = 1e-10
MAX_ITER = 1000

#Cramer’s Method
def det(A):
    n = len(A)
    if n == 1:
        return A[0][0]

    d = 0
    for j in range(n):
        minor = [row[:j] + row[j+1:] for row in A[1:]]
        d += (-1)**j * A[0][j] * det(minor)
    return d


def cramer(A, b):
    D = det(A)
    if abs(D) < EPS:
        raise ValueError("det(A) = 0")

    n = len(b)
    x = []

    for i in range(n):
        Ai = [row[:] for row in A]
        for j in range(n):
            Ai[j][i] = b[j]
        x.append(det(Ai) / D)

    return x

#Gaussian Method
def gauss(A, b):
    n = len(b)
    A = [A[i] + [b[i]] for i in range(n)]

    for i in range(n):
        for j in range(i+1, n):
            k = A[j][i] / A[i][i]
            for m in range(i, n+1):
                A[j][m] -= k * A[i][m]

    x = [0]*n
    for i in range(n-1, -1, -1):
        s = sum(A[i][j]*x[j] for j in range(i+1, n))
        x[i] = (A[i][n] - s) / A[i][i]

    return x

#Gauss–Jordan Method
def gauss_jordan(A, b):
    n = len(b)
    A = [A[i] + [b[i]] for i in range(n)]

    for i in range(n):
        k = A[i][i]
        for j in range(n+1):
            A[i][j] /= k

        for r in range(n):
            if r != i:
                k = A[r][i]
                for j in range(n+1):
                    A[r][j] -= k * A[i][j]

    return [A[i][-1] for i in range(n)]

#Jacobi Method
def jacobi(A, b, x):
    n = len(b)

    for _ in range(MAX_ITER):
        x_new = x[:]
        for i in range(n):
            s = sum(A[i][j]*x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]

        if max(abs(x_new[i]-x[i]) for i in range(n)) < EPS:
            return x_new
        x = x_new

    return x

#Gauss–Seidel Method
def gauss_seidel(A, b, x):
    n = len(b)

    for _ in range(MAX_ITER):
        x_ne= x[:]
        for i in range(n):
            s1 = sum(A[i][j]*x[j] for j in range(i))
            s2 = sum(A[i][j]*x_old[j] for j in range(i+1, n))
            x[i] = (b[i] - s1 - s2) / A[i][i]

        if max(abs(x[i]-x_old[i]) for i in range(n)) < EPS:
            return x

    return x

#Relaxation Method
def relaxation(A, b, x, w):
    n = len(b)

    for _ in range(MAX_ITER):
        x_old = x[:]
        for i in range(n):
            s1 = sum(A[i][j]*x[j] for j in range(i))
            s2 = sum(A[i][j]*x_old[j] for j in range(i+1, n))
            gs = (b[i] - s1 - s2) / A[i][i]
            x[i] = (1-w)*x_old[i] + w*gs

        if max(abs(x[i]-x_old[i]) for i in range(n)) < EPS:
            return x

    return x

A = [
    [4, 1, 1],
    [1, 5, 2],
    [1, 2, 6]
]
b = [7, 10, 14]

print("Cramer:", cramer(A, b))
print("Gauss:", gauss(A, b))
print("Gauss-Jordan:", gauss_jordan(A, b))

x0 = [0, 0, 0]
print("Jacobi:", jacobi(A, b, x0))
print("Gauss-Seidel:", gauss_seidel(A, b, x0))
print("Relaxation:", relaxation(A, b, x0, 1.2))