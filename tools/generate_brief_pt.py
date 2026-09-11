"""
Generates the Portuguese version of the Falcta Systems one-page capability
brief (PDF). Mirrors generate_brief.py's layout and styling exactly; only
the copy is translated.

Run: python3 generate_brief_pt.py
Requires: fpdf2 (pip install fpdf2)
"""
from fpdf import FPDF, XPos, YPos

DARK = (18, 22, 26)
MUTED = (90, 100, 110)
ACCENT = (204, 122, 0)      # slightly deepened orange for print contrast
GREEN = (30, 110, 55)       # deepened green for print contrast
LINE = (225, 228, 232)

PAGE_W = 210  # A4 mm


class Brief(FPDF):
    def header(self):
        pass

    def footer(self):
        pass


def section_title(pdf, text):
    pdf.set_x(pdf.l_margin)
    pdf.ln(4)
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Courier", "B", 11)
    pdf.set_text_color(*ACCENT)
    pdf.cell(0, 6, f"// {text.upper()}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_draw_color(*LINE)
    pdf.set_line_width(0.2)
    y = pdf.get_y() + 1
    pdf.line(pdf.l_margin, y, PAGE_W - pdf.r_margin, y)
    pdf.set_x(pdf.l_margin)
    pdf.ln(4)


def body_text(pdf, text, size=10, leading=5.2):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "", size)
    pdf.set_text_color(*DARK)
    pdf.multi_cell(0, leading, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(pdf.l_margin)


def tag_row(pdf, tags):
    pdf.set_font("Courier", "", 9)
    x = pdf.l_margin
    y = pdf.get_y()
    pdf.set_draw_color(*GREEN)
    for t in tags:
        w = pdf.get_string_width(t) + 6
        if x + w > PAGE_W - pdf.r_margin:
            x = pdf.l_margin
            y += 8
        pdf.set_xy(x, y)
        pdf.set_text_color(*GREEN)
        pdf.cell(w, 6.5, t, border=1, align="C")
        x += w + 3
    pdf.set_xy(pdf.l_margin, y + 10)


pdf = Brief(format="A4", unit="mm")
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_margins(20, 18, 20)
pdf.add_page()

# Header
pdf.set_x(pdf.l_margin)
pdf.set_font("Courier", "B", 22)
pdf.set_text_color(*DARK)
pdf.cell(0, 10, "[ FALCTA SYSTEMS ]", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.set_x(pdf.l_margin)
pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(*MUTED)
pdf.cell(0, 6, "UAS e Inteligência Geoespacial -- Feito para o terreno, não para o folheto.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.set_draw_color(*ACCENT)
pdf.set_line_width(0.8)
y = pdf.get_y() + 3
pdf.line(pdf.l_margin, y, PAGE_W - pdf.r_margin, y)
pdf.ln(8)

# Who we serve
section_title(pdf, "A Quem Servimos")
pdf.set_x(pdf.l_margin)
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(*DARK)
pdf.cell(0, 6, "Exército Português   |   Força Aérea Portuguesa   |   Proteção Civil", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_x(pdf.l_margin)
pdf.ln(2)

# Current service
section_title(pdf, "Serviço Atual -- Desenvolvimento de Drones Personalizados")
body_text(
    pdf,
    "Conceção e construção integral de plataformas UAS adaptadas a requisitos operacionais. "
    "Foco no desempenho em ambientes hostis e na fiabilidade crítica da missão -- sistemas "
    "que continuam a funcionar quando o GPS, as comunicações ou as condições no terreno não "
    "colaboram."
)

# Technology focus
section_title(pdf, "Foco Tecnológico")
tag_row(pdf, ["NAVEGAÇÃO SEM GPS", "INTEGRAÇÃO LIDAR", "COMUNICAÇÕES RESILIENTES", "VOO AUTÓNOMO", "GEOIA"])

# Platform capabilities
section_title(pdf, "Capacidades da Plataforma")
bullets = [
    "Navegação sem GPS: radar FMCW de 60GHz combinado com um MCU STM32, corrigindo o desvio "
    "do IMU a partir de dados de velocidade e altitude por reflexão do solo.",
    "Cadeia de valor limpa: eletrónica adquirida exclusivamente junto de nações aliadas "
    "(NATO, Taiwan, Japão), evitando riscos de espionagem e hardware vetado.",
    "Cargas úteis modulares: slots intercambiáveis de radar Doppler e LiDAR para topografia "
    "e deteção de obstáculos.",
    "Fabrico lean: prototipagem de PCBs internamente e chassis impresso em 3D de grau "
    "aeronáutico, reduzindo os custos unitários muito abaixo dos preços tradicionais da "
    "indústria de defesa.",
]
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(*DARK)
for b in bullets:
    pdf.set_x(pdf.l_margin)
    pdf.cell(4, 5.2, chr(149))
    pdf.set_x(pdf.l_margin + 5)
    pdf.multi_cell(PAGE_W - pdf.l_margin - pdf.r_margin - 5, 5.2, b)
    pdf.ln(0.5)

# Future pipeline
section_title(pdf, "Próximos Desenvolvimentos")
pdf.set_x(pdf.l_margin)
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(*DARK)
pdf.cell(0, 5.5, "Plataforma de Inteligência Geoespacial", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
body_text(
    pdf,
    "Levantamentos aéreos com drones -- magnetometria, LiDAR, espectrometria de raios gama -- "
    "processados com aprendizagem automática para análise de terreno e avaliação de ameaças.",
    size=9.5,
)
pdf.set_x(pdf.l_margin)
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(*DARK)
pdf.cell(0, 5.5, "Serviços de Levantamento Geridos", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
body_text(
    pdf,
    "Recolha de dados aéreos e elaboração de relatórios de ciclo completo para clientes de "
    "defesa e proteção civil, desde o planeamento de voo até à entrega da análise.",
    size=9.5,
)

# Footer block
pdf.set_y(-38)
pdf.set_x(pdf.l_margin)
pdf.set_draw_color(*LINE)
pdf.set_line_width(0.2)
pdf.line(pdf.l_margin, pdf.get_y(), PAGE_W - pdf.r_margin, pdf.get_y())
pdf.ln(3)
pdf.set_x(pdf.l_margin)
pdf.set_font("Courier", "", 9)
pdf.set_text_color(*MUTED)
pdf.cell(0, 5, "comms@falctasystems.com   |   R. Padre Francisco Branco, 3050-238 Luso, Portugal", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_x(pdf.l_margin)
pdf.cell(0, 5, "falctasystems.com", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_x(pdf.l_margin)
pdf.set_font("Helvetica", "I", 8)
pdf.cell(0, 5, "Preparado pela Falcta Systems. Para uso do destinatário na avaliação da Falcta Systems como fornecedor.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.output("../falcta-systems-capability-brief-pt.pdf")
print("done")
