import numpy as np
from dataclasses import dataclass
from typing import Optional


def _as_float_array(a):
    return np.asarray(a, dtype=float)

def _check_distinct_x(x):
    if len(np.unique(x)) != len(x):
        raise ValueError("x values must be distinct")

def _is_uniform_grid(x, tol=1e-12):
    if len(x) < 2:
        return True, 0.0
    h = x[1] - x[0]
    return np.all(np.abs(np.diff(x) - h) <= tol), h


def lagrange_interpolation(x_nodes, y_nodes, x):
    x_nodes = _as_float_array(x_nodes)
    y_nodes = _as_float_array(y_nodes)
    _check_distinct_x(x_nodes)

    x = np.asarray(x, dtype=float)
    result = np.zeros_like(x, dtype=float)

    n = len(x_nodes)
    for i in range(n):
        Li = np.ones_like(x, dtype=float)
        for j in range(n):
            if i != j:
                Li *= (x - x_nodes[j]) / (x_nodes[i] - x_nodes[j])
        result += y_nodes[i] * Li

    return result



def _forward_differences(y):
    diffs = [y.copy()]
    while len(diffs[-1]) > 1:
        diffs.append(np.diff(diffs[-1]))
    return diffs

def newton_forward_interpolation(x_nodes, y_nodes, x):
    x_nodes = _as_float_array(x_nodes)
    y_nodes = _as_float_array(y_nodes)
    _check_distinct_x(x_nodes)

    ok, h = _is_uniform_grid(x_nodes)
    if not ok:
        raise ValueError("Forward Newton requires uniform grid")

    diffs = _forward_differences(y_nodes)
    x = np.asarray(x, dtype=float)
    u = (x - x_nodes[0]) / h

    result = diffs[0][0]
    term = np.ones_like(x, dtype=float)

    for k in range(1, len(diffs)):
        term *= (u - (k - 1)) / k
        result += term * diffs[k][0]

    return result



def _backward_differences(y):
    n = len(y)
    diffs = [y.copy()]
    for k in range(1, n):
        diff = np.zeros(n)
        diff[k:] = diffs[k - 1][k:] - diffs[k - 1][k - 1:-1]
        diffs.append(diff)
    return diffs

def newton_backward_interpolation(x_nodes, y_nodes, x):
    x_nodes = _as_float_array(x_nodes)
    y_nodes = _as_float_array(y_nodes)
    _check_distinct_x(x_nodes)

    ok, h = _is_uniform_grid(x_nodes)
    if not ok:
        raise ValueError("Backward Newton requires uniform grid")

    diffs = _backward_differences(y_nodes)
    x = np.asarray(x, dtype=float)
    v = (x - x_nodes[-1]) / h

    result = y_nodes[-1]
    term = np.ones_like(x, dtype=float)

    for k in range(1, len(y_nodes)):
        term *= (v + (k - 1)) / k
        result += term * diffs[k][-1]

    return result


def divided_difference_table(x_nodes, y_nodes):
    x_nodes = _as_float_array(x_nodes)
    y_nodes = _as_float_array(y_nodes)
    _check_distinct_x(x_nodes)

    n = len(x_nodes)
    table = np.zeros((n, n))
    table[:, 0] = y_nodes

    for j in range(1, n):
        for i in range(n - j):
            table[i, j] = (
                table[i + 1, j - 1] - table[i, j - 1]
            ) / (x_nodes[i + j] - x_nodes[i])

    return table

def newton_divided_interpolation(x_nodes, y_nodes, x):
    table = divided_difference_table(x_nodes, y_nodes)
    x_nodes = _as_float_array(x_nodes)
    x = np.asarray(x, dtype=float)

    result = table[0, 0]
    product = np.ones_like(x, dtype=float)

    for j in range(1, len(x_nodes)):
        product *= (x - x_nodes[j - 1])
        result += table[0, j] * product

    return result


@dataclass
class CubicSpline:
    x: np.ndarray
    a: np.ndarray
    b: np.ndarray
    c: np.ndarray
    d: np.ndarray

    def __call__(self, xq):
        xq = np.asarray(xq, dtype=float)
        yq = np.zeros_like(xq)

        for idx, val in np.ndenumerate(xq):
            i = np.searchsorted(self.x, val) - 1
            i = max(0, min(i, len(self.a) - 1))
            dx = val - self.x[i]
            yq[idx] = (
                self.a[i]
                + self.b[i] * dx
                + self.c[i] * dx**2
                + self.d[i] * dx**3
            )
        return yq

def cubic_spline(x_nodes, y_nodes, fp0: Optional[float] = None, fpn: Optional[float] = None):
    x = _as_float_array(x_nodes)
    y = _as_float_array(y_nodes)
    n = len(x) - 1
    h = np.diff(x)

    A = np.zeros((n + 1, n + 1))
    b = np.zeros(n + 1)

    if fp0 is None and fpn is None:
        A[0, 0] = A[n, n] = 1
    else:
        A[0, 0], A[0, 1] = 2 * h[0], h[0]
        b[0] = 6 * ((y[1] - y[0]) / h[0] - fp0)

        A[n, n - 1], A[n, n] = h[-1], 2 * h[-1]
        b[n] = 6 * (fpn - (y[-1] - y[-2]) / h[-1])

    for i in range(1, n):
        A[i, i - 1] = h[i - 1]
        A[i, i] = 2 * (h[i - 1] + h[i])
        A[i, i + 1] = h[i]
        b[i] = 6 * (
            (y[i + 1] - y[i]) / h[i]
            - (y[i] - y[i - 1]) / h[i - 1]
        )

    M = np.linalg.solve(A, b)

    a = y[:-1]
    b = np.zeros(n)
    c = M[:-1] / 2
    d = np.zeros(n)

    for i in range(n):
        b[i] = (y[i + 1] - y[i]) / h[i] - h[i] * (2 * M[i] + M[i + 1]) / 6
        d[i] = (M[i + 1] - M[i]) / (6 * h[i])

    return CubicSpline(x, a, b, c, d)

if __name__ == "__main__":
    pass
