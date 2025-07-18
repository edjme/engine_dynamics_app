
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QFileDialog, QHBoxLayout, QComboBox
)
from engine_dynamics import calculations
from reporting import plotting, interactive_plot, save_io as utils


class InputForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Engine Dynamics Calculator")

        self.inputs = {}
        self.layout = QVBoxLayout(self)

        self.default_params = {
            'D': '0.16', 'S': '0.14', 'eps': '17',
            'n_rpm': '1700', 'Pr': '110000', 'Pa': '90000',
            'n1': '1.38', 'n2': '1.22', 'lam': '0.333',
            'lam_z': '2', 'rho': '1.4', 'm_pd': '330', 'm_sh': '330'
        }

        for key, value in self.default_params.items():
            label = QLabel(f"{key}:")
            input_field = QLineEdit(value)
            self.inputs[key] = input_field
            self.layout.addWidget(label)
            self.layout.addWidget(input_field)

        button_layout = QHBoxLayout()

        calc_btn = QPushButton("Рассчитать")
        calc_btn.clicked.connect(self.calculate)
        button_layout.addWidget(calc_btn)

        graph_btn = QPushButton("Графики")
        graph_btn.clicked.connect(self.show_graph)
        button_layout.addWidget(graph_btn)

        report_btn = QPushButton("Сохранить отчёт (PDF)")
        report_btn.clicked.connect(self.save_report)
        button_layout.addWidget(report_btn)

        self.layout.addLayout(button_layout)

        # Preset combobox (на будущее)
        self.preset_combo = QComboBox()
        self.layout.addWidget(QLabel("Выбор шаблона:"))
        self.layout.addWidget(self.preset_combo)

        self.results = None
        self.data = None

    def get_params(self):
        try:
            return {k: float(field.text()) for k, field in self.inputs.items()}
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Проверьте ввод чисел.")
            return None

    def calculate(self):
        import datetime
        from pathlib import Path

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_dir = Path("output") / timestamp
        output_dir.mkdir(parents=True, exist_ok=True)

        params = self.get_params()
        if params is None:
            return

        self.results, self.data = calculations.calculate_engine_dynamics(
            params)

        utils.save_input_data(params, output_dir)
        utils.save_results(self.results, output_dir)
        interactive_plot.plot_interactive(self.data, output_dir=output_dir)
        self.output_dir = output_dir

        QMessageBox.information(self, "Готово", "Расчёт завершён.")

    def show_graph(self):
        if not hasattr(self, "data") or not self.data:
            QMessageBox.warning(self, "Ошибка", "Сначала выполните расчёт.")
            return

        if "Pa" not in self.data:
            QMessageBox.warning(
                self, "Ошибка", "Отсутствуют данные для построения графика.")
            return

        plotting.plot_graph(self.data)

    def save_report(self):
        if self.results and self.data:
            params = self.get_params()
            utils.generate_pdf_report(params, self.results)
            QMessageBox.information(self, "Сохранено", "PDF отчёт создан.")
        else:
            QMessageBox.warning(self, "Ошибка", "Сначала выполните расчёт.")
