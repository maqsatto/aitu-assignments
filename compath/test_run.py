from main import (
    lagrange_interpolation,
    newton_forward_interpolation,
    newton_backward_interpolation,
    newton_divided_interpolation,
    cubic_spline,
)

x = [1, 2, 3]
y = [1, 4, 9]
x_star = 2.5

print("Lagrange:", lagrange_interpolation(x, y, x_star))

# Newton forward/backward работают только на равномерной сетке
print("Newton forward:", newton_forward_interpolation(x, y, x_star))
print("Newton backward:", newton_backward_interpolation(x, y, x_star))

# Divided differences работает на любой сетке
print("Divided diff:", newton_divided_interpolation(x, y, x_star))

# Spline
s = cubic_spline(x, y)      # natural spline
print("Spline:", s(x_star))
