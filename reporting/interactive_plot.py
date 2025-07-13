
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import os

def plot_interactive(data: dict, output_dir="output"):
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            "P-V диаграмма", "Pg(α)",
            "Pg, Pj, PΣ", "Силы N и K",
            "Силы Z и T", "Резерв"
        )
    )

    # (0) P-V диаграмма
    fig.add_trace(go.Scatter(x=data["V_comp"]*1e6, y=data["P_comp"]/1e6, name="Сжатие"), row=1, col=1)
    fig.add_trace(go.Scatter(x=data["V_iso_add"]*1e6, y=data["P_iso_add"]/1e6, name="Изохора +Q"), row=1, col=1)
    fig.add_trace(go.Scatter(x=data["V_iso_bar_V"]*1e6, y=data["P_iso_bar_P"]/1e6, name="Изобара +Q"), row=1, col=1)
    fig.add_trace(go.Scatter(x=data["V_exp"]*1e6, y=data["P_exp"]/1e6, name="Расширение"), row=1, col=1)
    fig.add_trace(go.Scatter(x=data["V_iso_rej"]*1e6, y=data["P_iso_rej"]/1e6, name="Изохора –Q"), row=1, col=1)
    fig.add_trace(go.Scatter(x=data["V_rr"]*1e6, y=data["P_rr"]/1e6, name="Выпуск P_rr"), row=1, col=1)
    fig.add_trace(go.Scatter(x=data["V_rr"]*1e6, y=[data["Pr"]/1e6]*2, name="Полка Pr"), row=1, col=1)

    # (1) Pg(α)
    fig.add_trace(go.Scatter(x=data["alpha_deg"], y=data["Pg"]/1e6, name="Pg(α)"), row=1, col=2)

    # (2) Pg, Pj, PΣ
    fig.add_trace(go.Scatter(x=data["alpha_deg"], y=data["P_sum"]/1e6, name="PΣ"), row=2, col=1)
    fig.add_trace(go.Scatter(x=data["alpha_deg"], y=data["Pj"]/1e6, name="Pj"), row=2, col=1)
    fig.add_trace(go.Scatter(x=data["alpha_deg"], y=data["Pg"]/1e6, name="Pg"), row=2, col=1)

    # (3) Силы N, K
    fig.add_trace(go.Scatter(x=data["alpha_deg"], y=data["N"], name="N"), row=2, col=2)
    fig.add_trace(go.Scatter(x=data["alpha_deg"], y=data["K"], name="K"), row=2, col=2)

    # (4) Силы Z, T
    fig.add_trace(go.Scatter(x=data["alpha_deg"], y=data["Z"], name="Z"), row=3, col=1)
    fig.add_trace(go.Scatter(x=data["alpha_deg"], y=data["T"], name="T"), row=3, col=1)

    fig.update_layout(height=900, width=1200, title_text="Интерактивные графики двигателя")

    os.makedirs(output_dir, exist_ok=True)
    html_path = os.path.join(output_dir, "interactive_graphs.html")
    fig.write_html(html_path, auto_open=True)
