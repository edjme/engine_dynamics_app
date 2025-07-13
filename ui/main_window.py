from PySide6.QtWidgets import QApplication, QMainWindow
from ui.input_form import InputForm

def run_app():
    app = QApplication([])
    window = QMainWindow()
    window.setWindowTitle("Engine Dynamics App")

    form = InputForm()
    window.setCentralWidget(form)

    window.resize(800, 600)
    window.show()
    app.exec()
