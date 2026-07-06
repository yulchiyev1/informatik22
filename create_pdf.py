from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Informatik22 - O\'qituvchilar uchun Qo\'llanma', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Sahifa {self.page_no()}', 0, 0, 'C')

def create():
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    with open('Qollanma.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        # Strip emojis and unsupported characters
        clean_line = line.encode('latin-1', 'ignore').decode('latin-1').strip()
        
        # very basic markdown parsing
        if clean_line.startswith('# '):
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, clean_line[2:], 0, 1)
            pdf.set_font("Arial", size=11)
        elif clean_line.startswith('## '):
            pdf.ln(4)
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 8, clean_line[3:], 0, 1)
            pdf.set_font("Arial", size=11)
        elif clean_line.startswith('### '):
            pdf.ln(2)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 6, clean_line[4:], 0, 1)
            pdf.set_font("Arial", size=11)
        elif clean_line.startswith('- '):
            pdf.multi_cell(0, 6, '    * ' + clean_line[2:])
        elif clean_line == '---':
            pdf.ln(4)
            pdf.cell(0, 0, '', 'T')
            pdf.ln(4)
        elif clean_line == '':
            pdf.ln(3)
        else:
            # Replace basic markdown bold
            clean_line = clean_line.replace('**', '')
            pdf.multi_cell(0, 6, clean_line)

    pdf.output("Qollanma.pdf")

if __name__ == "__main__":
    create()
