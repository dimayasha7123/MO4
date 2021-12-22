from scipy.optimize import minimize
from math import exp

fx = lambda x: 2 * pow(x[0], 2) + pow(x[1], 2)

g1 = lambda x: -(-x[0] - x[1] + 2)
g2 = lambda x: -(x[0] - 2 * x[1] + 1)
g3 = lambda x: -(-2 * x[0] + x[1])
g = [g1, g2, g3]

x0 = [0.8, 1.3]
cons = ({'type': 'ineq', 'fun': g1},
        {'type': 'ineq', 'fun': g2},
        {'type': 'ineq', 'fun': g3})
answer = minimize(fx, x0, constraints=cons)
print('scipy:', answer.x)

g1 = lambda x: (-x[0] - x[1] + 2)
g2 = lambda x: (x[0] - 2 * x[1] + 1)
g3 = lambda x: (-2 * x[0] + x[1])
g = [g1, g2, g3]

x0 = [0.8, 1.3]
eps = 0.0001
C = 1
beta = 2
k = 1
pen = 10
INF = 10 ** 10


def getPen4(x):
    lessZero = True
    for i in g:
        lessZero = lessZero and i(x) < 0
    if lessZero:
        return (-1) * C * sum([1 / i(x) for i in g])
    else:
        return INF


def getPen1(x):
    q = 2
    return C * sum([pow(max(0, i(x)), q) for i in g])


def getPen2(x):
    lessOrEqZero = True
    for i in g:
        lessOrEqZero = lessOrEqZero and i(x) <= 0
    if lessOrEqZero:
        return 0
    else:
        return C * exp((-1) / max([i(x) for i in g]))


while pen > eps:
    Fx = lambda x: fx(x) + getPen2(x)
    x0 = minimize(Fx, x0).x
    pen = getPen2(x0)
    print('k = ', k, 'x = ', x0, 'pen = ', pen, 'C = ', C)
    C *= beta
    k += 1

print('Моя реализация:', x0)