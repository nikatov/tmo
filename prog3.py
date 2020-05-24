# -*- coding: utf-8 -*-

# +-------------------------------+
# |    Многоканальная СМО без     |
# | ограничений на длину очереди  |
# +-------------------------------+

from math import factorial
import matplotlib.pyplot as plt


# Приведенная интенсивность потока
def p_f(Tc, Ts):
    l = 1 / Tc
    m = 1 / Ts
    return l / m


# Вероятность того, что все каналы обслуживания свободны
def p0_f(p, n: int):
    sum = 1
    for k in range(1, n):
        sum += p ** k / factorial(k)
    sum += p ** n / (factorial(n) * (1 - p/n))
    return 1 / sum


# Вероятность того, что k каналов обслуживания заняты
def pk_f(p0, p, k: int):
    return (p ** k) * p0 / factorial(k)


# Вероятность отказа
def pn_f(Tc, Ts, n):
    p = p_f(Tc, Ts)
    P0 = p0_f(p, n)
    return pk_f(P0, p, n)


# Математическое ожидание среднего числа занятых каналов
def ksr_f(Tc, Ts, n):
    p = p_f(Tc, Ts)
    if p/n >= 1:
        return n
    return p_f(Tc, Ts)


# Коэффициент загрузки операторов
def q_f(Tc, Ts, n):
    return ksr_f(Tc, Ts, n) / n


# Вероятность существования очереди
def poch_f(Tc, Ts, n):
    p = p_f(Tc, Ts)
    if p / n >= 1:
        return 1
    p0 = p0_f(p, n)
    return (p ** n) * n * p0 / (factorial(n) * (n - p))


# Математическое ожидание длины очереди
def loch_f(Tc, Ts, n):
    p = p_f(Tc, Ts)
    if p / n >= 1:
        return -10
    p0 = p0_f(p, n)
    return (p ** (n + 1)) * n * p0 / (factorial(n) * ((n - p) ** 2))


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
    n_lim = 12  # предельное количество операторов

    oper_tytle = "Количество операторов"
    ksr_tytle = "Мат. ожидание числа занятых операторов"
    q_tytle = "Коэффициент загрузки операторов"
    poch_tytle = "Вероятность существования очереди"
    loch_tytle = "Мат. ожидание длины очереди"

    n_list = [n + 1 for n in range(n_lim)]
    ksr_list = [ksr_f(Tc, Ts, n) for n in n_list]
    q_list = [q_f(Tc, Ts, n) for n in n_list]
    poch_list = [poch_f(Tc, Ts, n) for n in n_list]
    loch_list = [loch_f(Tc, Ts, n) for n in n_list]

    plot(n_list, ksr_list, oper_tytle, ksr_tytle)
    plot(n_list, q_list, oper_tytle, q_tytle)
    plot(n_list, poch_list, oper_tytle, poch_tytle)
    plot(n_list, loch_list, oper_tytle, loch_tytle)

    plt.show()
