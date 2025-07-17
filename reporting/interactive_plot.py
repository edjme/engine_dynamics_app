# reporting/interactive_plot.py
import matplotlib
# переключаемся на Qt-бэкенд для интерактивного показа
matplotlib.use("Qt5Agg")  

import matplotlib.pyplot as plt
import numpy as np

def plot_interactive(data):
    """
    Рисует интерактивное окно (Matplotlib) по данным расчёта.
    data — словарь с массивами numpy: alpha_deg, Pg, Pj, P_sum, N, K, Z, T
    """
    alpha = data.get("alpha_deg")
    Pg    = data.get("Pg")
    Pj    = data.get("Pj")
    P_sum = data.get("P_sum")
    N     = data.get("N")
    K     = data.get("K")
    Z     = data.get("Z")
    T     = data.get("T")

    fig, axes = plt.subplots(3, 2, figsize=(10, 8))
    ax = axes.flatten()

    # Pg vs α
    if alpha is not None and Pg is not None:
        ax[0].plot(alpha, Pg, label="Pg")
        ax[0].set_title("Давление газов Pg(α)")
        ax[0].legend()

    # Pj vs α
    if alpha is not None and Pj is not None:
        ax[1].plot(alpha, Pj, label="Pj", color="orange")
        ax[1].set_title("Инерционное давление Pj(α)")
        ax[1].legend()

    # P_sum vs α
    if alpha is not None and P_sum is not None:
        ax[2].plot(alpha, P_sum, label="P_sum", color="green")
        ax[2].set_title("Суммарное давление")
        ax[2].legend()

    # Силы N и K
    if alpha is not None and N is not None and K is not None:
        ax[3].plot(alpha, N, label="N")
        ax[3].plot(alpha, K, label="K")
        ax[3].set_title("Силы N и K")
        ax[3].legend()

    # Силы Z и T
    if alpha is not None and Z is not None and T is not None:
        ax[4].plot(alpha, Z, label="Z")
        ax[4].plot(alpha, T, label="T")
        ax[4].set_title("Силы Z и T")
        ax[4].legend()

    # Последний график оставляем пустым
    ax[5].axis("off")

    plt.tight_layout()
    plt.show()
