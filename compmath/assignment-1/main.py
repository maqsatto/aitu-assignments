import math

# Bisection (needs a bracket [a,b] with f(a)*f(b) < 0)
def bisection(f, a, b, tol=1e-10, max_iter=1000):
    fa, fb = f(a), f(b)
    if fa == 0: return a
    if fb == 0: return b
    if fa * fb > 0:
        raise ValueError("Bisection needs f(a) and f(b) of opposite signs.")

    for _ in range(max_iter):
        c = (a + b) / 2.0
        fc = f(c)
        if abs(fc) < tol or abs(b - a) / 2.0 < tol:
            return c
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    return c


# Fixed-point iteration: x_{n+1} = g(x_n)
def fixed_point(g, x0, tol=1e-10, max_iter=1000):
    x = x0
    for _ in range(max_iter):
        x1 = g(x)
        if abs(x1 - x) < tol:
            return x1
        x = x1
    return x


# Newton-Raphson
def newton(f, x0, df=None, tol=1e-10, max_iter=1000, h=1e-6):
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x
        dfx = df(x) if df else (f(x + h) - f(x - h)) / (2 * h)
        if dfx == 0:
            raise ZeroDivisionError("Zero derivative encountered.")
        x1 = x - fx / dfx
        if abs(x1 - x) < tol:
            return x1
        x = x1
    return x


# Secant
def secant(f, x0, x1, tol=1e-10, max_iter=1000):
    f0, f1 = f(x0), f(x1)
    for _ in range(max_iter):
        if f1 == f0:
            raise ZeroDivisionError("Zero slope in secant step.")
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        if abs(x2 - x1) < tol or abs(f(x2)) < tol:
            return x2
        x0, x1 = x1, x2
        f0, f1 = f1, f(x1)
    return x1


# False position
def false_position(f, a, b, tol=1e-10, max_iter=1000):
    fa, fb = f(a), f(b)
    if fa == 0: return a
    if fb == 0: return b
    if fa * fb > 0:
        raise ValueError("False position needs f(a) and f(b) of opposite signs.")

    for _ in range(max_iter):
        # secant intersection within [a,b]
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)
        if abs(fc) < tol:
            return c
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
        if abs(b - a) < tol:
            return c
    return c


# Requires 3 initial guesses near a real root.
def muller(f, x0, x1, x2, tol=1e-10, max_iter=1000):
    for _ in range(max_iter):
        f0, f1, f2 = f(x0), f(x1), f(x2)

        h1 = x1 - x0
        h2 = x2 - x1
        if h1 == 0 or h2 == 0:
            raise ZeroDivisionError("Repeated x values.")

        d1 = (f1 - f0) / h1
        d2 = (f2 - f1) / h2
        d = (d2 - d1) / (h1 + h2)

        a = d
        b = d2 + h2 * d
        c = f2

        disc = b * b - 4 * a * c
        if disc < 0:
            raise ValueError("Negative discriminant.")
        sqrt_disc = math.sqrt(disc)

        # choose denominator to avoid cancellation
        denom = b + sqrt_disc if abs(b + sqrt_disc) > abs(b - sqrt_disc) else b - sqrt_disc
        if denom == 0:
            raise ZeroDivisionError("Zero denominator.")

        dx = -2 * c / denom
        x3 = x2 + dx

        if abs(dx) < tol or abs(f(x3)) < tol:
            return x3

        x0, x1, x2 = x1, x2, x3
    return x2

if __name__ == "__main__":
    f = lambda x: math.cos(x) - x
    df = lambda x: -math.sin(x) - 1

    print("Bisection:", bisection(f, 0.0, 1.0))
    print("False position:", false_position(f, 0.0, 1.0))
    print("Newton:", newton(f, 0.7, df=df))
    print("Secant:", secant(f, 0.0, 1.0))
    print("Fixed-point:", fixed_point(lambda x: math.cos(x), 0.7))

    # Muller on a real-root-friendly function:
    f2 = lambda x: x**3 - x - 2  # real root near 1.521...
    print("Muller:", muller(f2, 1.0, 1.5, 2.0))