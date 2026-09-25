#! /usr/bin/env python3
def f(x):
    return 3*x**2 + 2*x -1

def bisection(f, a, b, tolerance=1e-8):
    fa = f(a)
    fb = f(b)

    if fa == 0:
        return a
    if fb == 0:
        return b
    if fa * fb > 0:
        raise ValueError("f(a) and f(b) must have opposite signs.")
    while (b - a) / 2 > tolerance:
        c = (a + b) / 2
        fc = f(c)

        if fc == 0:
            return c
        #The root should be between a and c
        if fa * fc < 0:
            b = c
            fb = fc
        else: 
            a = c
            fa = fc

    return (a + b) / 2
negative_root = bisection(f, -2, -0.5)
positive_root = bisection(f, 0, 1)
print("The negative root is:", negative_root)
print("The positive root is:", positive_root)
