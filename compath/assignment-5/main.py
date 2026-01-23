import numpy as np

# -----------------------------
# Newton–Cotes (closed) general
# -----------------------------

def newton_cotes_closed_weights(n: int) -> np.ndarray:
    """
    Closed Newton–Cotes weights for n subintervals (n+1 equally spaced points).
    Nodes i=0..n on [0,n]. Rule:
        ∫_a^b f(x) dx ≈ h * Σ w_i f(a + i h),  h=(b-a)/n
    """
    if n < 1:
        raise ValueError("n must be >= 1.")
    i = np.arange(n + 1, dtype=float)
    k = np.arange(n + 1, dtype=float)

    # Vandermonde with entries i^k (rows k, cols i)
    A = i[None, :] ** k[:, None]
    b = (n ** (k + 1)) / (k + 1)
    w = np.linalg.solve(A, b)
    return w


def newton_cotes_closed(f, a: float, b: float, n: int) -> float:
    """Single-panel closed Newton–Cotes of degree n (n subintervals, n+1 points)."""
    if a == b:
        return 0.0
    w = newton_cotes_closed_weights(n)
    h = (b - a) / n
    x = a + h * np.arange(n + 1, dtype=float)
    return h * np.dot(w, f(x))


# -----------------------------
# Classic specific rules
# -----------------------------

def trapezoidal_rule(f, a: float, b: float) -> float:
    x = np.array([a, b], dtype=float)
    fx = f(x)
    return 0.5 * (b - a) * (fx[0] + fx[1])


def simpson_one_third_rule(f, a: float, b: float) -> float:
    h = (b - a) / 2.0
    x = np.array([a, a + h, b], dtype=float)
    fx = f(x)
    return (h / 3.0) * (fx[0] + 4.0 * fx[1] + fx[2])


def simpson_three_eighth_rule(f, a: float, b: float) -> float:
    h = (b - a) / 3.0
    x = np.array([a, a + h, a + 2*h, b], dtype=float)
    fx = f(x)
    return (3.0 * h / 8.0) * (fx[0] + 3.0 * fx[1] + 3.0 * fx[2] + fx[3])


def boole_rule(f, a: float, b: float) -> float:
    h = (b - a) / 4.0
    x = np.array([a, a + h, a + 2*h, a + 3*h, b], dtype=float)
    fx = f(x)
    return (2.0 * h / 45.0) * (7*fx[0] + 32*fx[1] + 12*fx[2] + 32*fx[3] + 7*fx[4])


def weddle_rule(f, a: float, b: float) -> float:
    h = (b - a) / 6.0
    x = np.array([a, a + h, a + 2*h, a + 3*h, a + 4*h, a + 5*h, b], dtype=float)
    fx = f(x)
    return (3.0 * h / 10.0) * (fx[0] + 5*fx[1] + fx[2] + 6*fx[3] + fx[4] + 5*fx[5] + fx[6])


# -----------------------------
# Example
# -----------------------------
if __name__ == "__main__":
    f = np.sin
    a, b = 0.0, np.pi
    print("Exact:", 2.0)
    print("Trap:", trapezoidal_rule(f, a, b))
    print("Simpson 1/3:", simpson_one_third_rule(f, a, b))
    print("Simpson 3/8:", simpson_three_eighth_rule(f, a, b))
    print("Boole:", boole_rule(f, a, b))
    print("Weddle:", weddle_rule(f, a, b))
    print("Newton–Cotes n=2:", newton_cotes_closed(f, a, b, 2))  # same as Simpson 1/3
