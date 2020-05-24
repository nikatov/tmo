# -*- coding: utf-8 -*-

# +--------------------------------------------+
# | Многоканальная СМО с ограниченной очередью |
# +--------------------------------------------+

from math import factorial
import matplotlib.pyplot as plt


# Приведенная интенсивность потока
def p_f(Tc, Ts):
    l = 1 / Tc
    m = 1 / Ts
    return l / m


# Вероятность того, что все каналы обслуживания свободны
def p0_f(p, n, m):
    s = 1
    for k in range(1, n + 1):
        s += p ** k / factorial(k)
    for i in range(1, m + 1):
        s += (p ** (n + i)) / (factorial(n) * (n ** i))
    return 1 / s


# Вероятность состояния k [1; n + m]
def pk_f(p0, p, k, n):
    if k <= n:
        return p ** k * p0 / factorial(k)
    return p ** k * p0 / (factorial(n) * (n ** (k - n)))


# Вероятность отказа
def pn_f(Tc, Ts, n, m):
    p = p_f(Tc, Ts)
    P0 = p0_f(p, n, m)
    return pk_f(P0, p, n + m, n)


# Математическое ожидание среднего числа занятых операторов
def ksr_f(Tc, Ts, n, m):
    p = p_f(Tc, Ts)
    Pn = pn_f(Tc, Ts, n, m)
    Q = 1 - Pn
    return p * Q


# Коэффициент загрузки операторов
def q_f(Tc, Ts, n, m):
    return ksr_f(Tc, Ts, n, m) / n


# Вероятность существования очереди
def poch_f(Tc, Ts, n, m):
    s = 0
    p = p_f(Tc, Ts)
    p0 = p0_f(p, n, m)
    for i in range(m):
        s += pk_f(p0, p, n + i, n)
    return s


# Математическое ожидание длины очереди
def loch_f(Tc, Ts, n, m):
    s = 0
    p = p_f(Tc, Ts)
    p0 = p0_f(p, n, m)
    for i in range(1, m + 1):
        s += i * pk_f(p0, p, n + i, n)
    return s


# Коэффициент занятости мест в очереди
def qoch_f(Tc, Ts, n, m):
    try:
        return loch_f(Tc, Ts, n, m) / m
    except ZeroDivisionError:
        return 0


def plot(x_list: list,
         y_list: list,
         x_label: str,
         y_label: str,
         z_label: str):

    fig, ax1 = plt.subplots()
    plt.grid(True)
    for i, y in enumerate(y_list):
        ax1.plot(x_list, y, label=z_label + ' ' + str(i + 1))
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y_label)
    ax1.legend(loc='upper right')


if __name__ == '__main__':
    # Константы
    Tc = 39  # время возникновения заявки
    Ts = 229  # время обслуживания заявки
    n_lim = 12  # предельное количество операторов
    m_lim = 12  # предельная длина очереди

    oper_tytle = "Количество операторов"
    m_tytle = "Длина очереди"
    pn_tytle = "Вероятность отказа"
    ksr_tytle = "Мат. ожидание ср. числа занятых операторов"
    q_tytle = "Коэффициент загрузки операторов"
    poch_tytle = "Вероятность существования очереди"
    loch_tytle = "Мат. ожидание средней длины очереди"
    qoch_tytle = "Коэффициент занятости мест в очереди"

    n_list = [n + 1 for n in range(n_lim)]
    m_list = [m + 1 for m in range(m_lim)]

    # Варьируя число операторов, построение семейств графиков от числа мест в очереди
    Pn_list = []
    ksr_list = []
    q_list = []
    poch_list = []
    loch_list = []
    qoch_list = []

    for n in range(1, n_lim + 1):
        Pn_list.append([pn_f(Tc, Ts, n, m) for m in m_list])
        ksr_list.append([ksr_f(Tc, Ts, n, m) for m in m_list])
        q_list.append([q_f(Tc, Ts, n, m) for m in m_list])
        poch_list.append([poch_f(Tc, Ts, n, m) for m in m_list])
        loch_list.append([loch_f(Tc, Ts, n, m) for m in m_list])
        qoch_list.append([qoch_f(Tc, Ts, n, m) for m in m_list])

    plot(n_list, Pn_list, m_tytle, pn_tytle, oper_tytle)
    plot(n_list, ksr_list, m_tytle, ksr_tytle, oper_tytle)
    plot(n_list, q_list, m_tytle, q_tytle, oper_tytle)
    plot(n_list, poch_list, m_tytle, poch_tytle, oper_tytle)
    plot(n_list, loch_list, m_tytle, loch_tytle, oper_tytle)
    plot(n_list, qoch_list, m_tytle, qoch_tytle, oper_tytle)

    # Варьируя число мест в очереди, построение семейств графиков от числа операторов
    Pn_list = []
    ksr_list = []
    q_list = []
    poch_list = []
    loch_list = []
    qoch_list = []

    for m in range(m_lim + 1):
        Pn_list.append([pn_f(Tc, Ts, n, m) for n in n_list])
        ksr_list.append([ksr_f(Tc, Ts, n, m) for n in n_list])
        q_list.append([q_f(Tc, Ts, n, m) for n in n_list])
        poch_list.append([poch_f(Tc, Ts, n, m) for n in n_list])
        loch_list.append([loch_f(Tc, Ts, n, m) for n in n_list])
        qoch_list.append([qoch_f(Tc, Ts, n, m) for n in n_list])

    plot(n_list, Pn_list, oper_tytle, pn_tytle, m_tytle)
    plot(n_list, ksr_list, oper_tytle, ksr_tytle, m_tytle)
    plot(n_list, q_list, oper_tytle, q_tytle, m_tytle)
    plot(n_list, poch_list, oper_tytle, poch_tytle, m_tytle)
    plot(n_list, loch_list, oper_tytle, loch_tytle, m_tytle)
    plot(n_list, qoch_list, oper_tytle, qoch_tytle, m_tytle)

    plt.show()
