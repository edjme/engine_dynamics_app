from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QFormLayout, QMessageBox
)
from engine_dynamics import calculations
# from reporting import report
from pathlib import Path
from datetime import datetime
from reporting.interactive_plot import plot_interactive
from reporting.report import create_pdf_report




class InputForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Расчёт динамики двигателя")

        # --- Параметры формы с дефолтами ---
        self.layout = QVBoxLayout()
        form = QFormLayout()
        self.inputs = {}

        defaults = {
            "D": "0.16",
            "S": "0.14",
            "eps": "17",
            "n_rpm": "1700",
            "Pr": "110000",
            "Pa": "90000",
            "n1": "1.38",
            "n2": "1.22",
            "lam": "0.333",
            "lam_z": "2",
            "rho": "1.4",
            "m_pd": "330",
            "m_sh": "330"
        }
        labels = {
            "D": "Диаметр цилиндра (D), м",
            "S": "Ход поршня (S), м",
            "eps": "Степень сжатия (ε)",
            "n_rpm": "Частота вращения (n), об/мин",
            "Pr": "Давление в конце расширения (Pr), Па",
            "Pa": "Начальное давление (Pa), Па",
            "n1": "Показатель политропы сжатия (n1)",
            "n2": "Показатель политропы расширения (n2)",
            "lam": "λ = R/L",
            "lam_z": "λ_z",
            "rho": "ρ = Vz/Vz_",
            "m_pd": "Масса поршня (кг)",
            "m_sh": "Масса шатуна (кг)",
        }

        for key in labels:
            w = QLineEdit()
            w.setText(defaults[key])
            self.inputs[key] = w
            form.addRow(QLabel(labels[key]), w)

        self.layout.addLayout(form)

        # --- Кнопки ---
        btn_calc = QPushButton("Рассчитать")
        btn_calc.clicked.connect(self.calculate)
        self.layout.addWidget(btn_calc)

        btn_graph = QPushButton("Графики")
        btn_graph.clicked.connect(self.show_graph)
        self.layout.addWidget(btn_graph)

        self.setLayout(self.layout)
        self.results = None
        self.data = None
        self.output_dir = None

    def get_params(self):
        params = {}
        try:
            for k, w in self.inputs.items():
                params[k] = float(w.text())
        except ValueError:
            QMessageBox.warning(
                self, "Ошибка", "Введите все параметры корректно.")
            return None
        return params

    def calculate(self):
        params = self.get_params()
        if params is None:
            return

        # --- расчёт ---
        self.results, self.data = calculations.calculate_engine_dynamics(
            params)

        # --- создаём папку с меткой ---
        stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.output_dir = Path("output") / stamp
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # --- генерируем PDF автоматически ---
        # передаём в отчёт и входные, и выходные данные
        create_pdf_report({**params, **self.results, **self.data},
                                 self.output_dir / "report.pdf")

        QMessageBox.information(
            self, "Готово",
            f"Расчёт завершён и PDF сохранён в:\n{self.output_dir}"
        )

    def show_graph(self):
        if self.data is None:
            QMessageBox.warning(self, "Ошибка", "Сначала выполните расчёт.")
            return
        try:
            from reporting import interactive_plot
            interactive_plot.plot_interactive(self.data)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка графиков", str(e))
