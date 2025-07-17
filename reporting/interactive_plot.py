from plotly.subplots import make_subplots
import plotly.graph_objs as go
from plotly.offline import plot


def plot_interactive(data, output_path=None):
    alpha = data.get("alpha_deg")
    Pg = data.get("Pg")
    Pj = data.get("Pj")
    P_sum = data.get("P_sum")
    N = data.get("N")
    K = data.get("K")
    Z = data.get("Z")
    T = data.get("T")

    fig = make_subplots(rows=3, cols=2, subplot_titles=[
        "Pg(α)", "Pj(α)", "P_sum(α)", "N & K", "Z & T", ""])

    if alpha is not None and Pg is not None:
        fig.add_trace(go.Scatter(x=alpha, y=Pg, name="Pg"), row=1, col=1)
    if alpha is not None and Pj is not None:
        fig.add_trace(go.Scatter(x=alpha, y=Pj, name="Pj"), row=1, col=2)
    if alpha is not None and P_sum is not None:
        fig.add_trace(go.Scatter(x=alpha, y=P_sum, name="P_sum"), row=2, col=1)
    if alpha is not None and N is not None and K is not None:
        fig.add_trace(go.Scatter(x=alpha, y=N, name="N"), row=2, col=2)
        fig.add_trace(go.Scatter(x=alpha, y=K, name="K"), row=2, col=2)
    if alpha is not None and Z is not None and T is not None:
        fig.add_trace(go.Scatter(x=alpha, y=Z, name="Z"), row=3, col=1)
        fig.add_trace(go.Scatter(x=alpha, y=T, name="T"), row=3, col=1)

    fig.update_layout(height=800, width=1000,
                      title_text="Интерактивные графики")

    # если путь указан — сохраняем
    if output_path:
        plot(fig, filename=str(output_path), auto_open=False)
    else:
        fig.show()
