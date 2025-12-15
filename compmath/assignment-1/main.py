def f(x):
    return x**2+x-1

a, b = map(int, input().split())

c = (a+b)/2

if (abs(f(c))<=0):
    print("C can not be zero or less")
    