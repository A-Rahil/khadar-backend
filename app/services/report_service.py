from fpdf import FPDF

class HealthReport(FPDF):
    def header(self):
        self.image()
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Khadar - Plant Health Report')
        self.ln(10)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page' + str(self.page_no()) + '{nb}', 0, 0, 'C')
def generatePDFReport(farm)