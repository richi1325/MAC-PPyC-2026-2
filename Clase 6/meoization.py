import sys
sys.setrecursionlimit(50000)


def f(n, memoria = {}):
    if n in (1,0):
        return 1
    if n not in memoria:
        memoria[n] = f(n-1) + f(n-2)
    return memoria[n]

print(f(10000))