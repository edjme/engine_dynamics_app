from .calculations import calculate_engine_dynamics
from .utils import save_input_data, save_results
from .plotting import plot_graph

def run_engine_calculations(params: dict, output_dir: str = "output"):
    # Сохраняем входные параметры
    save_input_data(params, output_dir)

    # Выполняем расчёты
    x, y = calculate_engine_dynamics(params)

    # Сохраняем ключевые метрики
    results = {
        "Max Y": max(y),
        "Min Y": min(y),
        "Points": len(x)
    }
    save_results(results, output_dir)

    # Строим график
    plot_graph(x, y, title="График динамики двигателя", output_dir=output_dir)

    return results
