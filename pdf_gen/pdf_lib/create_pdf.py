from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_pdf(file_name):
    c = canvas.Canvas(file_name, pagesize=letter)
    c.drawString(100, 750, "Hello, this is a PDF created with Python!")
    c.save()
