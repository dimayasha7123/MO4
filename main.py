from scipy.optimize import minimize
from math import exp

# функция, которую минимизируем
#fx = lambda x: pow(x[0], 2) - 4 * x[0]

fx = lambda x: 2 * pow(x[0], 2) + pow(x[1], 2)

#fx = lambda x: pow((1 - x[0]), 2) + 100 * pow((x[1] - pow(x[0], 2)), 2)

# условия
#g1 = lambda x: -(x[0] - 1)


g1 = lambda x: -(-x[0] - x[1] + 2)
g2 = lambda x: -(x[0] - 2 * x[1] + 1)
g3 = lambda x: -(-2 * x[0] + x[1])


# g1 = lambda x: -(x[0] - 2 * x[1] + 2)
# g2 = lambda x: -(-x[0] - 2 * x[1] + 6)
# g3 = lambda x: -(-x[0] + 2 * x[1] + 2)

g = [g1, g2, g3]
#g=[g1]

# начальная точка
x0 = [0.8, 1.3]

# используя scipy.optimize
cons = ({'type': 'ineq', 'fun': g1},
        {'type': 'ineq', 'fun': g2},
        {'type': 'ineq', 'fun': g3})
# cons = ({'type': 'ineq', 'fun': g1})
answer = minimize(fx, x0, constraints=cons)
print('scipy:', answer.x)

# g1 = lambda x: (x[0] - 1)
# g=[g1]

# g1 = lambda x: (x[0] - 2 * x[1] + 2)
# g2 = lambda x: (-x[0] - 2 * x[1] + 6)
# g3 = lambda x: (-x[0] + 2 * x[1] + 2)

g1 = lambda x: (-x[0] - x[1] + 2)
g2 = lambda x: (x[0] - 2 * x[1] + 1)
g3 = lambda x: (-2 * x[0] + x[1])

# Знаки в условиях между scipy и кодом ниже должны отличаться

g = [g1, g2, g3]

# мой вариант метода штрафной функции
x0 = [0.8, 1.3]
eps = 0.0001
C = 1
beta = 2
#pen4 0 < beta < 1
#pen1-2 beta > 1
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
    if (k >= 1000):
        print('Многовато, блин')
        break

print('Моя реализация:', x0)


# todo Организовать функцию, в которую будем передавать саму функцию минимизации, условия, eps, и выбор метода
# todo организовать вывод таблицы
# todo пожанглировать кодом
# todo попитониться