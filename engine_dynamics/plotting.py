import os
import matplotlib.pyplot as plt
import numpy as np

def plot_graph(data: dict, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)

    alpha_deg = data["alpha_deg"]
    Pg = data["Pg"]
    Pj = data["Pj"]
    P_sum = data["P_sum"]
    N = data["N"]
    K = data["K"]
    Z = data["Z"]
    T = data["T"]
    V_alpha = data["V_alpha"]
    Pa = data["Pa"]
    Pr = data["Pr"]
    n1 = data["n1"]
    n2 = data["n2"]
    Va = data["Va"]
    Vc = data["Vc"]
    Vz = data["Vz"]
    Vz_ = data["Vz_"]
    Pc = data["Pc"]
    Pz = data["Pz"]
    Pz_ = data["Pz_"]
    Pb = data["Pb"]

    fig, axs = plt.subplots(3, 2, figsize=(13, 12))
    axs = axs.ravel()

    # 0. P-V диаграмма
    V_comp = np.linspace(Vc, Va, 1001)
    P_comp = Pa * (Va / V_comp) ** n1

    V_exp = np.linspace(Va, Vz_, 1001)
    P_exp = Pz_ * (Vz_ / V_exp) ** n2

    axs[0].plot(V_comp * 1e6, P_comp / 1e6, label="Сжатие")
    axs[0].plot([Vc * 1e6, Vc * 1e6], [Pc / 1e6, Pz / 1e6], 'k-', label="Изохора +Q")
    axs[0].plot([Vz * 1e6, Vz_ * 1e6], [Pz / 1e6, Pz_ / 1e6], 'r--', label="Изобара +Q")
    axs[0].plot(V_exp * 1e6, P_exp / 1e6, label="Расширение")
    axs[0].plot([Va * 1e6, Va * 1e6], [Pb / 1e6, Pr / 1e6], 'k-', label="Изохора –Q")
    axs[0].plot([Va * 1e6, Vc * 1e6], [Pr / 1e6, (Pr + 0.11e6) / 1e6], 'g-', label="Выпуск")
    axs[0].plot([Va * 1e6, Vc * 1e6], [Pr / 1e6, Pr / 1e6], 'g--', label="Полка Pr")
    axs[0].set_xlabel("V, см³")
    axs[0].set_ylabel("P, МПа")
    axs[0].set_title("P–V диаграмма")
    axs[0].legend()
    axs[0].grid()

    # 1. Pg(α)
    axs[1].plot(alpha_deg, Pg / 1e6)
    axs[1].set_xlabel("α, °")
    axs[1].set_ylabel("Pг, МПа")
    axs[1].set_title("Давление газов Pg(α)")
    axs[1].grid()

    # 2. Pg, Pj, PΣ
    axs[2].plot(alpha_deg, P_sum / 1e6, label="PΣ")
    axs[2].plot(alpha_deg, Pj / 1e6, label="Pj")
    axs[2].plot(alpha_deg, Pg / 1e6, label="Pg")
    axs[2].set_xlabel("α, °")
    axs[2].set_ylabel("P, МПа")
    axs[2].set_title("Газовые и инерционные давления")
    axs[2].legend()
    axs[2].grid()

    # 3. силы N, K
    axs[3].plot(alpha_deg, N, label="N")
    axs[3].plot(alpha_deg, K, label="K")
    axs[3].set_xlabel("α, °")
    axs[3].set_ylabel("Сила, Н")
    axs[3].set_title("Силы N и K")
    axs[3].legend()
    axs[3].grid()

    # 4. силы Z, T
    axs[4].plot(alpha_deg, Z, label="Z")
    axs[4].plot(alpha_deg, T, label="T")
    axs[4].set_xlabel("α, °")
    axs[4].set_ylabel("Сила, Н")
    axs[4].set_title("Силы Z и T")
    axs[4].legend()
    axs[4].grid()

    # 5. Пустой (как в оригинале)
    axs[5].axis("off")

    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "full_graphs.png"))
    plt.close(fig)
