from fpdf import FPDF

class HealthReport(FPDF):
    def header(self):
        self.image()
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Khadar - Plant Health Report')