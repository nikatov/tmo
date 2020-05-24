# -*- coding: utf-8 -*-

# +-------------------------------+
# |    Многоканальная СМО без     |
# | ограничений на длину очереди, |
# |   но с ограниченным временем  |
# |      ожидания в очереди.      |
# +-------------------------------+

from math import factorial
import matplotlib.pyplot as plt


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


def pn_f(p, N, n):
    p0 = p0_f(p, N, n)
    return factorial(N) * (p ** n) * p0 / factorial(N - n)


def p0_f(p, N, n):
    if p != 1 / (N - n):
        s = 0
        for i in range(0, n + 1):
            s += (factorial(N) / factorial(N - i)) * p ** i
        s += (factorial(N) / factorial(N - n - 1) * p ** (n + 1) * ((1 - (((N - n) * p) ** (N - n))) / (1 - (N - n) * p)))
    else:
        s = N - n + 2
        for k in range(1, n + 1):
            s += factorial(N) / ((N - n) ** k * factorial(N - k))
    return 1 / s


def poch_f(p, N, n):
    if (N - n) * p != 1:
        return pn_f(p, N, n) * (1 - ((N - n) * p) ** (N - n)) * (N - n) * p / (1 - (N - n) * p)
    else:
        return (N - n) * pn_f(p, N, n)


def loch_f(p, N, n):
    s = 0
    for i in range(1, N - n + 1):
        s += i * ((N - n) ** i) * (p ** i)
    return pn_f(p, N, n) * s


def lobs_f(p, N, n):
    s = 0
    for k in range(1, n + 1):
        s += factorial(N) * (p ** k) * k / factorial(N - k)
    return p0_f(p, N, n) * s


def lsmo_f(p, N, n):
    return loch_f(p, N, n) + lobs_f(p, N, n)


def q_f(p, N, n):
    return lobs_f(p, N, n) / n


if __name__ == '__main__':
    # Константы
    Tc = 444  # среднее время между наладками
    Ts = 12  # среднее время наладки
    N = 38  # количество станков
    n_lim = N - 1  # предельное количество операторов

    oper_tytle = "Количество наладчиков"
    lsmo_tytle = "Мат. ожидание числа простаивающих станков"
    loch_tytle = "Мат. ожидание числа ожидающих обслуживание станков"
    poch_tytle = "Вероятность ожидания обслуживания"
    lobs_tytle = "Мат. ожидание числа занятых наладчиков"
    q_tytle = "Коэффициент занятости наладчиков"

    l = 1 / Tc
    m = 1 / Ts
    p = l / m
    n_list = [n + 1 for n in range(n_lim)]

    lsmo_list = [lsmo_f(p, N, n) for n in n_list]
    loch_list = [loch_f(p, N, n) for n in n_list]
    poch_list = [poch_f(p, N, n) for n in n_list]
    lobs_list = [lobs_f(p, N, n) for n in n_list]
    q_list = [q_f(p, N, n) for n in n_list]

    plot(n_list, lsmo_list, oper_tytle, lsmo_tytle)
    plot(n_list, loch_list, oper_tytle, loch_tytle)
    plot(n_list, poch_list, oper_tytle, poch_tytle)
    plot(n_list, lobs_list, oper_tytle, lobs_tytle)
    plot(n_list, q_list, oper_tytle, q_tytle)

    plt.show()