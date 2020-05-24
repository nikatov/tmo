# -*- coding: utf-8 -*-

# +-------------------------------+
# |    Многоканальная СМО без     |
# | ограничений на длину очереди, |
# |   но с ограниченным временем  |
# |      ожидания в очереди.      |
# +-------------------------------+

from math import factorial
import matplotlib.pyplot as plt


def multiply(lst):
    result = 1
    for i in lst:
        result *= i
    return result


# Приведенная интенсивность потока
def p_f(Tc, Ts):
    l = 1 / Tc
    m = 1 / Ts
    return l / m


# Приведенная интенсивность потока ухода
def b_f(Ts, Tw):
    v = 1 / Tw
    m = 1 / Ts
    return v / m


# Вероятность того, что все каналы обслуживания свободны
def p0_f(p, b, n: int, m: int):
    sum = 1
    for k in range(1, n + 1):
        sum += (p ** k) / factorial(k)
    for i in range(1, m + 1):
        sum += (p ** n / factorial(n)) * (p ** i) / multiply([n + l * b for l in range(1, i + 1)])
    return 1 / sum


# Вероятность того, что k каналов обслуживания заняты
def pk_f(p0, p, b, k: int, n: int):
    if k <= n:
        return (p ** k) * p0 / factorial(k)
    i = k - n
    return pk_f(p0, p, b, n, n) * p ** i / multiply([n + l * b for l in range(1, i + 1)])


def m_f(p, b, n, eps):
    m = 0
    p0 = p0_f(p, b, n, m)
    delta = p0 ** m - p0 ** (m + 1)
    while delta >= eps:
        m += 1
        p0 = p0_f(p, b, n, m)
        delta = p0 ** m - p0 ** (m + 1)
    return m


# Математическое ожидание среднего числа занятых каналов
def ksr_f(p, b, n, m):
    p0 = p0_f(p, b, n, m)
    sum = 0
    for k in range(0, n + 1):
        # sum += k * pk_f(p0, p, b, k, n)
        sum += (k * (p ** k) * p0) / factorial(k)
    sum2 = 0
    for i in range(1, m + 1):
        sum2 += (p ** i) / multiply([n + l * b for l in range(1, i + 1)])

    sum2 *= (n * (p ** n) * p0) / factorial(n)
    sum += sum2
    return sum


# Коэффициент загрузки операторов
def q_f(p, b, n, m):
    return ksr_f(p, b, n, m) / n


# Вероятность существования очереди
def poch_f(p, b, n, m):
    if p / n >= 1:
        return 1

    p0 = p0_f(p, b, n, m)
    sum = 1
    for i in range(1, m):
        sum += p ** i / multiply([n + l * b for l in range(1, i + 1)])
    return (p ** n * p0 / factorial(n)) * sum


# Математическое ожидание длины очереди
def loch_f(p, b, n, m):
    p0 = p0_f(p, b, n, m)
    sum = 0
    for i in range(1, m + 1):
        sum += i * (p ** i) / multiply([n + l * b for l in range(1, i + 1)])
    return (p ** n * p0 / factorial(n)) * sum


# Функция отрисовки графиков
def plot(x_list: list,
         y_list: list,
         x_tytle: str = "",
         y_tytle: str = ""):
    fig, ax1 = plt.subplots()
    plt.grid(True)
    ax1.plot(x_list, y_list, 'r-')
    ax1.set_xlabel(x_tytle)
    ax1.set_ylabel(y_tytle)


if __name__ == '__main__':
    # Константы
    Tc = 39  # время возникновения заявки
    Ts = 229  # время обслуживания заявки
    Tw = 517  # приемлемое время ожидания
    n_lim = 12  # предельное количество операторов

    oper_tytle = "Количество операторов"
    ksr_tytle = "Мат. ожидание числа занятых операторов"
    q_tytle = "Коэффициент загрузки операторов"
    poch_tytle = "Вероятность существования очереди"
    loch_tytle = "Мат. ожидание длины очереди"

    p = p_f(Tc, Ts)
    b = b_f(Ts, Tw)

    n_list = [n + 1 for n in range(n_lim)]
    m_list = [m_f(p, b, n, 0.000001) for n in n_list]

    ksr_list = [ksr_f(p, b, n, m) for n, m in zip(n_list, m_list)]
    q_list = [q_f(p, b, n, m) for n, m in zip(n_list, m_list)]
    poch_list = [poch_f(p, b, n, m) for n, m in zip(n_list, m_list)]
    loch_list = [loch_f(p, b, n, m) for n, m in zip(n_list, m_list)]

    plot(n_list, ksr_list, oper_tytle, ksr_tytle)
    plot(n_list, q_list, oper_tytle, q_tytle)
    plot(n_list, poch_list, oper_tytle, poch_tytle)
    plot(n_list, loch_list, oper_tytle, loch_tytle)

    plt.show()
