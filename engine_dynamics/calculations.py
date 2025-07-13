
import numpy as np
from scipy.optimize import fsolve

DEG = np.pi / 180


def calculate_engine_dynamics(params):
    D = params['D']
    S = params['S']
    eps = params['eps']
    n_rpm = params['n_rpm']
    Pr = params['Pr']
    Pa = params['Pa']
    n1 = params['n1']
    n2 = params['n2']
    lam = params['lam']
    lam_z = params['lam_z']
    rho = params['rho']
    m_pd = params['m_pd']
    m_sh = params['m_sh']
    m2 = 2 / 3 * m_sh

    F_p = np.pi * D**2 / 4
    Vh = S * F_p
    Vc = Vh / (eps - 1)
    Va = Vh + Vc

    Pc = Pa * eps**n1
    Pz = Pc * lam_z
    Vz = Vc
    Vz_ = Vz * rho
    Pz_ = Pz
    Pb = Pz_ * (Vz_ / Va)**n2

    R = S / 2
    L = R / lam

    alpha_deg = np.arange(0, 720.0 + 0.5, 0.5)
    alpha = alpha_deg * DEG
    beta = np.arcsin(lam * np.sin(alpha))
    S_p = R * (1 - np.cos(alpha)) + L * (1 - np.cos(beta))
    V_alpha = Vc + F_p * S_p

    def volume_eq(phi):
        beta_ = np.arcsin(lam * np.sin(phi))
        S_ = R * (1 - np.cos(phi)) + L * (1 - np.cos(beta_))
        return Vc + F_p * S_ - rho * Vc

    phi = fsolve(volume_eq, 15.0 * DEG)[0]
    phi_deg = phi / DEG

    Pg = np.empty_like(alpha)
    Pg[(alpha_deg >= 0) & (alpha_deg < 180)] = Pa
    mask = (alpha_deg >= 180) & (alpha_deg < 360)
    Pg[mask] = Pa * (Va / V_alpha[mask])**n1
    Pg[np.isclose(alpha_deg, 360)] = Pz
    mask = (alpha_deg > 360) & (alpha_deg <= 360 + phi_deg)
    Pg[mask] = Pz
    mask = (alpha_deg > 360 + phi_deg) & (alpha_deg < 540)
    Pg[mask] = Pz_ * (Vz_ / V_alpha[mask])**n2
    Pg[np.isclose(alpha_deg, 540)] = Pr
    mask = (alpha_deg > 540) & (alpha_deg <= 720)
    Pg[mask] = Pr

    omega = np.pi * n_rpm / 30

    def piston_accel(a):
        sin_a = np.sin(a)
        cos_a = np.cos(a)
        beta = np.arcsin(lam * sin_a)
        cos_b = np.cos(beta)
        sin_b = np.sin(beta)
        d_beta = lam * cos_a / cos_b
        d2_beta = (-lam * sin_a / cos_b) - lam**2 * cos_a**2 * sin_b / cos_b**3
        d2S = R * cos_a + L * (sin_b * d2_beta + cos_b * d_beta**2)
        return omega**2 * d2S

    a_p = piston_accel(alpha)
    Pj = -m_pd * a_p
    P_sum = Pg + Pj

    N = P_sum * np.tan(beta)
    K = P_sum / np.cos(beta)
    Z = K * np.cos(alpha + beta)
    T = K * np.sin(alpha + beta)

    V_comp = np.linspace(Vc, Va, 1001)
    P_comp = Pa * (Va / V_comp)**n1

    V_exp = np.linspace(Va, Vz_, 1001)
    P_exp = Pz_ * (Vz_ / V_exp)**n2

    V_iso_add = np.array([Vc, Vc])
    P_iso_add = np.array([Pc, Pz])
    V_iso_bar_V = np.array([Vz, Vz_])
    P_iso_bar_P = np.array([Pz, Pz])
    V_iso_rej = np.array([Va, Va])
    P_iso_rej = np.array([Pb, Pr])
    Pr_prime = Pr + 0.11e6
    V_rr = np.array([Va, Vc])
    P_rr = np.array([Pr, Pr_prime])

    # Результаты (пример: работа, КПД и пр.)
    A_cycle = np.trapz(P_sum, x=V_alpha)
    Q_in = (Pz - Pc) * Vc + Pz * (Vz_ - Vz)
    eta = A_cycle / Q_in if Q_in else 0

    results = {
        "Работа за цикл (Дж)": round(A_cycle, 3),
        "Подвод тепла Qвх (Дж)": round(Q_in, 3),
        "КПД (η)": round(eta * 100, 2)
    }

    data = {
        "alpha_deg": alpha_deg,
        "Pg": Pg,
        "Pj": Pj,
        "P_sum": P_sum,
        "N": N,
        "K": K,
        "Z": Z,
        "T": T,
        "V_alpha": V_alpha,
        "V_comp": V_comp,
        "P_comp": P_comp,
        "V_exp": V_exp,
        "P_exp": P_exp,
        "V_iso_add": V_iso_add,
        "P_iso_add": P_iso_add,
        "V_iso_bar_V": V_iso_bar_V,
        "P_iso_bar_P": P_iso_bar_P,
        "V_iso_rej": V_iso_rej,
        "P_iso_rej": P_iso_rej,
        "V_rr": V_rr,
        "P_rr": P_rr,
        "Pr": Pr
    }

    return results, data
