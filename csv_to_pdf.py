import pandas as pd
from fpdf import FPDF
import textwrap

class PDF(FPDF):
    def header(self):
        self.set_fill_color(30, 144, 255)  # Azul encabezado
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 14)
        self.cell(0, 12, 'Resultados SUEMZIT', ln=True, align='C', fill=True)
        self.ln(4)
        self.set_font('Arial', 'B', 11)
        self.set_fill_color(100, 149, 237)
        self.set_text_color(255, 255, 255)
        col_widths = [70, 20, 70]
        titulos = ['Sección', 'Año', 'Periodo']
        for i, titulo in enumerate(titulos):
            self.cell(col_widths[i], 10, titulo, border=1, align='C', fill=True)
        self.ln()
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', '', 10)

    def row(self, data, col_widths, fill):
        # Calcula el número de líneas necesarias para cada celda
        line_counts = []
        for i, datum in enumerate(data):
            lines = self.multi_cell_lines(str(datum), col_widths[i])
            line_counts.append(lines)
        max_lines = max(line_counts)
        row_height = 6 * max_lines
        # Salto de página si no cabe la fila
        if self.get_y() + row_height > self.page_break_trigger:
            self.add_page()
        y_before = self.get_y()
        for i, datum in enumerate(data):
            x_before = self.get_x()
            self.multi_cell(col_widths[i], 6, str(datum), border=1, align='L', fill=fill)
            self.set_xy(x_before + col_widths[i], y_before)
        self.ln(row_height)

    def multi_cell_lines(self, text, width):
        # Calcula cuántas líneas ocupará el texto en una multicell
        if not text:
            return 1
        # Aproximación: divide el texto en líneas de longitud máxima
        wrapped = textwrap.wrap(text, width=int(width/2.5))
        return max(1, len(wrapped))

# Lee el archivo CSV generado
csv_file = 'suemzit_resultados.csv'
df = pd.read_csv(csv_file)

pdf = PDF()
pdf.add_page()

col_widths = [70, 20, 70]

# Alternar color de fondo para filas
fill_colors = [(245, 245, 245), (255, 255, 255)]
for idx, (_, row) in enumerate(df.iterrows()):
    fill = idx % 2 == 0
    pdf.set_fill_color(*fill_colors[idx % 2])
    pdf.row([
        str(row['seccion']),
        str(row['año']),
        str(row['periodo'])
    ], col_widths, fill=fill)

pdf.output('suemzit_resultados.pdf')
print('Archivo suemzit_resultados.pdf generado correctamente.')
