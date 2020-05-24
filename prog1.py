# -*- coding: utf-8 -*-

# +-------------------------------+
# | Многоканальная СМО с отказами |
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
    for k in range(1, n + 1):
        sum += p ** k / factorial(k)
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
    Pn = pn_f(Tc, Ts, n)
    Q = 1 - Pn
    return p * Q


# Коэффициент загрузки операторов
def q_f(Tc, Ts, n):
    print(ksr_f(Tc, Ts, n), ' / ', n)
    return ksr_f(Tc, Ts, n) / n


def n_lim_f(Tc, Ts, Pn_delta):
    n = 1
    pn = pn_f(Tc, Ts, n)
    while Pn_delta < pn:
        n += 1
        pn = pn_f(Tc, Ts, n)
    return n


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

    oper_tytle = "Количество операторов"
    pn_tytle = "Вероятность отказа"
    ksr_tytle = "Мат. ожидание ср. числа занятых операторов"
    q_tytle = "Коэффициент загрузки операторов"

    pn_delta = 1 / 100  # вероятность отказа, до достижения которой увеличивать предельное количество операторов
    n_lim = n_lim_f(Tc, Ts, 1 / 100)  # предельное количество операторов

    n_list = [n + 1 for n in range(n_lim)]
    Pn_list = [pn_f(Tc, Ts, n) for n in n_list]
    ksr_list = [ksr_f(Tc, Ts, n) for n in n_list]
    q_list = [q_f(Tc, Ts, n) for n in n_list]

    plot(n_list, Pn_list, oper_tytle, pn_tytle)
    plot(n_list, ksr_list, oper_tytle, ksr_tytle)
    plot(n_list, q_list, oper_tytle, q_tytle)
    plt.show()