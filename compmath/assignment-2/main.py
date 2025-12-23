import numpy as np

EPS = 1e-12

# -------------------------
# Helpers
# -------------------------
def as_float_array(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float).reshape(-1)
    if A.ndim != 2 or b.ndim != 1 or A.shape[0] != A.shape[1] or A.shape[0] != b.size:
        raise ValueError("Shapes must be: A is (n,n), b is (n,).")
    return A, b

def residual_norm(A, x, b):
    return np.linalg.norm(A @ x - b, ord=np.inf)

# -------------------------
# Direct methods
# -------------------------
def cramer(A, b):
    """
    Cramer's rule. O(n^4) with determinants, OK only for small n.
    Requires det(A) != 0.
    """
    A, b = as_float_array(A, b)
    n = A.shape[0]
    detA = np.linalg.det(A)
    if abs(detA) < EPS:
        raise ValueError("det(A) is zero (or near zero). No unique solution for Cramer's method.")
    x = np.zeros(n)
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b
        x[i] = np.linalg.det(Ai) / detA
    return x

def gaussian_elimination(A, b, pivot=True):
    """
    Gaussian elimination with (optional) partial pivoting.
    Returns x for unique solution.
    """
    A, b = as_float_array(A, b)
    n = A.shape[0]
    M = np.hstack([A.copy(), b.reshape(-1, 1)])

    # Forward elimination
    for k in range(n):
        if pivot:
            # partial pivoting
            r = k + np.argmax(np.abs(M[k:, k]))
            if abs(M[r, k]) < EPS:
                raise ValueError("Matrix is singular or nearly singular.")
            if r != k:
                M[[k, r]] = M[[r, k]]
        else:
            if abs(M[k, k]) < EPS:
                raise ValueError("Zero pivot encountered. Try pivot=True.")

        for i in range(k + 1, n):
            factor = M[i, k] / M[k, k]
            M[i, k:] -= factor * M[k, k:]

    # Back substitution
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        if abs(M[i, i]) < EPS:
            raise ValueError("Matrix is singular or nearly singular.")
        x[i] = (M[i, -1] - np.dot(M[i, i + 1:n], x[i + 1:n])) / M[i, i]
    return x

def gauss_jordan(A, b, pivot=True):
    """
    Gauss-Jordan elimination to reduced row echelon form (RREF).
    """
    A, b = as_float_array(A, b)
    n = A.shape[0]
    M = np.hstack([A.copy(), b.reshape(-1, 1)])

    row = 0
    for col in range(n):
        if row >= n:
            break

        if pivot:
            r = row + np.argmax(np.abs(M[row:, col]))
            if abs(M[r, col]) < EPS:
                continue
            if r != row:
                M[[row, r]] = M[[r, row]]
        else:
            if abs(M[row, col]) < EPS:
                continue

        # Normalize pivot row
        piv = M[row, col]
        M[row, :] /= piv

        # Eliminate other rows
        for r in range(n):
            if r != row:
                factor = M[r, col]
                M[r, :] -= factor * M[row, :]

        row += 1

    # Check for consistency / uniqueness
    # If left side is identity (approximately), unique solution:
    # Otherwise might be infinite/no solutions (not deeply handled here).
    x = M[:, -1]
    if np.linalg.matrix_rank(A) < n:
        raise ValueError("A is rank-deficient: system may have infinite or no solutions.")
    return x

# -------------------------
# Iterative methods
# -------------------------
def jacobi(A, b, x0=None, tol=1e-10, max_iter=10000):
    """
    Jacobi iteration: x^{k+1} = D^{-1} (b - (L+U)x^k)
    """
    A, b = as_float_array(A, b)
    n = A.shape[0]
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float).reshape(-1)
    D = np.diag(A)
    if np.any(np.abs(D) < EPS):
        raise ValueError("Zero on diagonal -> Jacobi not applicable.")

    R = A - np.diagflat(D)

    for it in range(1, max_iter + 1):
        x_new = (b - R @ x) / D
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new, it
        x = x_new

    return x, max_iter

def gauss_seidel(A, b, x0=None, tol=1e-10, max_iter=10000):
    """
    Gauss-Seidel iteration uses newest values immediately.
    """
    A, b = as_float_array(A, b)
    n = A.shape[0]
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float).reshape(-1)

    if np.any(np.abs(np.diag(A)) < EPS):
        raise ValueError("Zero on diagonal -> Gauss-Seidel not applicable.")

    for it in range(1, max_iter + 1):
        x_old = x.copy()
        for i in range(n):
            s1 = np.dot(A[i, :i], x[:i])      # new values
            s2 = np.dot(A[i, i+1:], x_old[i+1:])  # old values
            x[i] = (b[i] - s1 - s2) / A[i, i]

        if np.linalg.norm(x - x_old, ord=np.inf) < tol:
            return x, it

    return x, max_iter

def relaxation_sor(A, b, omega=1.1, x0=None, tol=1e-10, max_iter=10000):
    """
    Successive Over-Relaxation (SOR):
    x_i^{k+1} = (1-ω)x_i^k + ω * (b_i - sum_{j<i} a_ij x_j^{k+1} - sum_{j>i} a_ij x_j^k) / a_ii
    ω in (0,2). ω=1 -> Gauss-Seidel.
    """
    A, b = as_float_array(A, b)
    n = A.shape[0]
    if not (0 < omega < 2):
        raise ValueError("omega must be in (0, 2).")
    x = np.zeros(n) if x0 is None else np.array(x0, dtype=float).reshape(-1)

    if np.any(np.abs(np.diag(A)) < EPS):
        raise ValueError("Zero on diagonal -> SOR not applicable.")

    for it in range(1, max_iter + 1):
        x_old = x.copy()
        for i in range(n):
            s1 = np.dot(A[i, :i], x[:i])
            s2 = np.dot(A[i, i+1:], x_old[i+1:])
            x_gs = (b[i] - s1 - s2) / A[i, i]     # Gauss-Seidel update
            x[i] = (1 - omega) * x_old[i] + omega * x_gs

        if np.linalg.norm(x - x_old, ord=np.inf) < tol:
            return x, it

    return x, max_iter

if __name__ == "__main__":
    # Example system:
    # 10x + 2y + 1z =  7
    #  1x + 5y + 1z = -8
    #  2x + 3y + 10z = 6
    A = [
        [10, 2, 1],
        [1, 5, 1],
        [2, 3, 10],
    ]
    b = [7, -8, 6]

    print("A =\n", np.array(A, float))
    print("b =", np.array(b, float))

    print("\n--- Direct methods ---")
    x_cr = cramer(A, b)
    print("Cramer:", x_cr, "residual inf-norm =", residual_norm(np.array(A,float), x_cr, np.array(b,float)))

    x_ge = gaussian_elimination(A, b, pivot=True)
    print("Gaussian:", x_ge, "residual inf-norm =", residual_norm(np.array(A,float), x_ge, np.array(b,float)))

    x_gj = gauss_jordan(A, b, pivot=True)
    print("Gauss-Jordan:", x_gj, "residual inf-norm =", residual_norm(np.array(A,float), x_gj, np.array(b,float)))

    print("\n--- Iterative methods ---")
    x0 = [0, 0, 0]
    x_j, it_j = jacobi(A, b, x0=x0, tol=1e-10, max_iter=10000)
    print(f"Jacobi:       {x_j}  iterations={it_j}  residual inf-norm={residual_norm(np.array(A,float), x_j, np.array(b,float))}")

    x_gs, it_gs = gauss_seidel(A, b, x0=x0, tol=1e-10, max_iter=10000)
    print(f"Gauss-Seidel: {x_gs}  iterations={it_gs}  residual inf-norm={residual_norm(np.array(A,float), x_gs, np.array(b,float))}")

    x_sor, it_sor = relaxation_sor(A, b, omega=1.15, x0=x0, tol=1e-10, max_iter=10000)
    print(f"SOR(ω=1.15):  {x_sor}  iterations={it_sor}  residual inf-norm={residual_norm(np.array(A,float), x_sor, np.array(b,float))}")
