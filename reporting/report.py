from fpdf import FPDF
from pathlib import Path
# import matplotlib 
# matplotlib.use("Agg")   # рендер в файл, Без GUI
import matplotlib.pyplot as plt
import numpy as np

class PDF(FPDF):
    def header(self):
        font_path = Path(__file__).parent / "DejaVuSans.ttf"
        if "DejaVu" not in self.fonts:
            self.add_font("DejaVu", "", str(font_path), uni=True)
            self.add_font("DejaVu", "B", str(font_path), uni=True)
        self.set_font("DejaVu", "B", 14)
        self.cell(0, 10, "Отчёт по расчёту динамики двигателя", border=False, ln=1, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.cell(0, 10, f"Страница {self.page_no()}", 0, 0, "C")


def create_pdf_report(results: dict, output_path: Path):
    # --- Стр.1: параметры и результаты ---
    pdf = PDF()
    pdf.set_auto_page_break(True, margin=15)
    pdf.add_page()

    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 10, "Входные параметры:", ln=True)
    params_keys = ["D","S","eps","n_rpm","Pr","Pa","n1","n2","lam","lam_z","rho","m_pd","m_sh"]
    for k in params_keys:
        if k in results:
            v = results[k]
            pdf.cell(0, 8, f"{k} = {v}", ln=True)

    pdf.ln(4)
    pdf.cell(0, 10, "Результаты расчёта:", ln=True)
    res_keys = ["phi_deg","Pb","Pz","Pg_avg","V_alpha_avg","A_cycle","Q_in","eta"]
    for k in res_keys:
        if k in results:
            v = results[k]
            if isinstance(v, float):
                pdf.cell(0, 8, f"{k} = {v:.4g}", ln=True)
            else:
                pdf.cell(0, 8, f"{k} = {v}", ln=True)

    # --- Сбор данных для графиков ---
    alpha    = np.array(results.get("alpha_deg", []))
    Pg       = np.array(results.get("Pg", []))
    Pj       = np.array(results.get("Pj", []))
    P_sum    = np.array(results.get("P_sum", []))
    N        = np.array(results.get("N", []))
    K        = np.array(results.get("K", []))
    Z        = np.array(results.get("Z", []))
    T        = np.array(results.get("T", []))
    V_comp   = np.array(results.get("V_comp", []))
    P_comp   = np.array(results.get("P_comp", []))
    V_exp    = np.array(results.get("V_exp", []))
    P_exp    = np.array(results.get("P_exp", []))
    V_iso_add= results.get("V_iso_add", [])
    P_iso_add= results.get("P_iso_add", [])
    V_iso_bar= results.get("V_iso_bar_V", [])
    P_iso_bar= results.get("P_iso_bar_P", [])
    V_iso_rej= results.get("V_iso_rej", [])
    P_iso_rej= results.get("P_iso_rej", [])
    V_rr     = results.get("V_rr", [])
    P_rr     = results.get("P_rr", [])

    # --- Стр.3: пять графиков вместе на одном холсте ---
    fig, axs = plt.subplots(3, 2, figsize=(10, 8))
    axs = axs.flatten()

    # 0: P–V диаграмма
    # if V_comp.size and P_comp.size:
        # axs[0].plot(V_comp * 1e6, P_comp/1e6, label="Сжатие")
        # axs[0].plot(V_iso_add, P_iso_add, "r--", label="Изохора +Q")
        # axs[0].plot(V_exp * 1e6, P_exp/1e6, label="Расширение")
        # axs[0].plot(V_iso_bar, P_iso_bar, "k-", label="Изобара")
        # axs[0].plot(V_iso_rej, P_iso_rej, "r-", label="Изохора -Q")
        # axs[0].plot(V_rr, P_rr, "g--", label="Полка Pr")
        # axs[0].set_title("P–V диаграмма")
        # axs[0].set_xlabel("V, см³")
        # axs[0].set_ylabel("P, МПа")
        # axs[0].legend(fontsize=6)

    # 0: P–V диаграмма
    if V_comp.size and P_comp.size:
        Vc6  = V_comp * 1e6        # м³→см³
        Vadd = np.array(V_iso_add) * 1e6
        Vexp = V_exp * 1e6
        Vbar = np.array(V_iso_bar) * 1e6
        Vrej = np.array(V_iso_rej) * 1e6
        Vrr6 = np.array(V_rr) * 1e6
        axs[0].plot(Vc6,      P_comp/1e6, label="Сжатие")
        axs[0].plot(Vadd,     P_iso_add/1e6, "r--", label="Изохора +Q")
        axs[0].plot(Vexp,     P_exp/1e6, label="Расширение")
        axs[0].plot(Vbar,     P_iso_bar/1e6, "k-", label="Изобара")
        axs[0].plot(Vrej,     P_iso_rej/1e6, "r-", label="Изохора -Q")
        axs[0].plot(Vrr6,     P_rr/1e6, "g--", label="Полка Pr")

    # 1: Pg(α)
    if alpha.size and Pg.size:
        axs[1].plot(alpha, Pg/1e6)
        axs[1].set_title("Давление газов Pg(α)")
        axs[1].set_xlabel("α, °")
        axs[1].set_ylabel("Pг, МПа")

    # 2: Pg, Pj, P_sum
    if alpha.size and Pg.size and Pj.size and P_sum.size:
        axs[2].plot(alpha, Pg/1e6, label="Pg")
        axs[2].plot(alpha, Pj/1e6, label="Pj")
        axs[2].plot(alpha, P_sum/1e6, label="P_sum")
        axs[2].set_title("Газовые и инерционные давления")
        axs[2].set_xlabel("α, °")
        axs[2].set_ylabel("P, МПа")
        axs[2].legend(fontsize=6)

    # 3: Силы N и K
    if alpha.size and N.size and K.size:
        axs[3].plot(alpha, N, label="N")
        axs[3].plot(alpha, K, label="K")
        axs[3].set_title("Силы N и K")
        axs[3].set_xlabel("α, °")
        axs[3].set_ylabel("Сила, Н")
        axs[3].legend(fontsize=6)

    # 4: Силы Z и T
    if alpha.size and Z.size and T.size:
        axs[4].plot(alpha, Z, label="Z")
        axs[4].plot(alpha, T, label="T")
        axs[4].set_title("Силы Z и T")
        axs[4].set_xlabel("α, °")
        axs[4].set_ylabel("Сила, Н")
        axs[4].legend(fontsize=6)

    # 5: пустой
    axs[5].axis("off")

    plt.tight_layout()
    img = output_path.parent / "full_graphs.png"
    fig.savefig(img, dpi=150)
    plt.close(fig)

    # Вставляем весь холст на новую страницу
    pdf.add_page()
    pdf.image(str(img), w=180)
    # img.unlink(missing_ok=True)
    try:
        img.unlink()
    except FileNotFoundError:
        pass

    # --- Сохраняем PDF ---
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(output_path))
