from fpdf import FPDF
import os

pdf = FPDF()
pdf.add_page()

base_path = os.path.dirname(os.path.abspath(__file__))

pdf.add_font("DejaVu", "", os.path.join(base_path, "DejaVuSans.ttf"))
pdf.add_font("DejaVu", "B", os.path.join(base_path, "DejaVuSans-Bold.ttf"))

pdf.set_font("DejaVu", "B", 16)
pdf.cell(0, 10, "Test DejaVu Bold", ln=True)

pdf.set_font("DejaVu", "", 14)
pdf.cell(0, 10, "Test DejaVu Regular", ln=True)

pdf.output("test_fonts.pdf")
print("PDF generated.")
