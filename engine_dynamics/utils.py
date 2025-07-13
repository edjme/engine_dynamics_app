
import os
from fpdf import FPDF

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("DejaVu", "", os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf"), uni=True)
        self.set_font("DejaVu", "", 12)

def save_input_data(params: dict, output_dir: str = "output"):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "input.txt")
    with open(path, "w", encoding="utf-8") as f:
        for k, v in params.items():
            f.write(f"{k} = {v}\n")

def save_results(results: dict, output_dir: str = "output"):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "result_.txt")
    with open(path, "w", encoding="utf-8") as f:
        for k, v in results.items():
            f.write(f"{k} = {v}\n")

def generate_pdf_report(params: dict, results: dict, output_dir: str = "output"):
    pdf = PDF()
    pdf.add_page()

    pdf.set_font("DejaVu", "", 14)
    pdf.cell(0, 10, "Отчёт по расчёту динамики двигателя", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 10, "Входные параметры:", ln=True)
    for k, v in params.items():
        pdf.cell(0, 8, f"{k} = {v}", ln=True)

    pdf.ln(5)
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 10, "Результаты расчёта:", ln=True)
    for k, v in results.items():
        if isinstance(v, float):
            pdf.cell(0, 8, f"{k} = {v:.4g}", ln=True)
        else:
            pdf.cell(0, 8, f"{k} = {v}", ln=True)

    for img_name in ["full_graphs.png"]:
        img_path = os.path.join(output_dir, img_name)
        if os.path.exists(img_path):
            pdf.add_page()
            pdf.cell(0, 10, f"Графики ({img_name}):", ln=True)
            pdf.image(img_path, x=10, y=30, w=190)

    os.makedirs(output_dir, exist_ok=True)
    pdf.output(os.path.join(output_dir, "report.pdf"))
