"""
Generates the Portuguese version of the Falcata Systems capability brief
(PDF). Mirrors generate_brief.py's layout and styling exactly; only the
copy is translated. See generate_brief.py for design notes (typography,
color, and the one-page-plus-a-bit page count).

Run: python3 generate_brief_pt.py
Requires: fpdf2 (pip install fpdf2)
Fonts: tools/fonts/Archivo-{Regular,Bold,ExtraBold}.ttf (SIL OFL, vendored
       alongside this script so the build doesn't depend on network access).
"""
from fpdf import FPDF, XPos, YPos

DARK = (18, 22, 26)
MUTED = (90, 100, 110)
ACCENT = (204, 122, 0)      # deepened orange (--accent-primary) for print contrast
TEAL = (35, 100, 115)       # deepened teal (--accent-teal) for print contrast
GREEN = (30, 110, 55)       # deepened green (--accent-secondary / --hud-green)
LINE = (225, 228, 232)

PAGE_W = 210  # A4 mm


class Brief(FPDF):
    def header(self):
        pass

    def footer(self):
        pass


def section_title(pdf, text, color=ACCENT):
    pdf.set_x(pdf.l_margin)
    pdf.ln(2.5)
    y = pdf.get_y()
    pdf.set_fill_color(*color)
    pdf.rect(pdf.l_margin, y, 1.2, 5.5, style="F")
    pdf.set_xy(pdf.l_margin + 4, y)
    pdf.set_font("Archivo", "B", 11.5)
    pdf.set_text_color(*DARK)
    pdf.cell(0, 5.5, text.upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_draw_color(*LINE)
    pdf.set_line_width(0.2)
    y = pdf.get_y() + 0.8
    pdf.line(pdf.l_margin, y, PAGE_W - pdf.r_margin, y)
    pdf.set_x(pdf.l_margin)
    pdf.ln(2.5)


def body_text(pdf, text, size=10, leading=4.6):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", "", size)
    pdf.set_text_color(*DARK)
    pdf.multi_cell(0, leading, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(pdf.l_margin)


def tag_row(pdf, tags):
    pdf.set_font("Archivo", "B", 9)
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
        pdf.cell(w, 6.0, t, border=1, align="C")
        x += w + 3
    pdf.set_xy(pdf.l_margin, y + 7)


pdf = Brief(format="A4", unit="mm")
pdf.set_auto_page_break(auto=True, margin=12)
pdf.set_margins(20, 15, 20)
pdf.add_font("Archivo", "", "fonts/Archivo-Regular.ttf")
pdf.add_font("Archivo", "B", "fonts/Archivo-Bold.ttf")
pdf.add_font("ArchivoXB", "", "fonts/Archivo-ExtraBold.ttf")
pdf.add_page()

# Header
pdf.set_x(pdf.l_margin)
pdf.set_font("ArchivoXB", "", 24)
pdf.set_text_color(*DARK)
pdf.cell(0, 10, "FALCATA SYSTEMS", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.set_x(pdf.l_margin)
pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(*MUTED)
pdf.cell(0, 6, "UAS e Inteligência Geoespacial -- Feito para o terreno, não para o folheto.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.set_draw_color(*ACCENT)
pdf.set_line_width(0.8)
y = pdf.get_y() + 3
pdf.line(pdf.l_margin, y, PAGE_W - pdf.r_margin, y)
pdf.ln(5)

# Para quem estamos a construir
section_title(pdf, "Para Quem Estamos a Construir")
pdf.set_x(pdf.l_margin)
pdf.set_font("Archivo", "B", 10)
pdf.set_text_color(*DARK)
pdf.cell(0, 6, "Exército Português   |   Força Aérea Portuguesa   |   Proteção Civil", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_x(pdf.l_margin)
pdf.ln(1)
body_text(
    pdf,
    "Estamos a conceber a Vanguard em torno das exigências operacionais reais do "
    "reconhecimento tático, da integração de sistemas aerotransportados e do "
    "levantamento de terreno em emergência -- os ambientes onde os nossos "
    "utilizadores-alvo realmente operam.",
    size=9.5,
)

# Fase atual
section_title(pdf, "Fase Atual")
body_text(
    pdf,
    "Estamos atualmente a construir o nosso primeiro protótipo Vanguard -- a "
    "adquirir hardware essencial, incluindo LiDAR, radar e componentes de "
    "controlo de voo, com um primeiro teste de campo previsto para dezembro. "
    "O nosso foco é o desempenho em ambientes hostis e a fiabilidade crítica "
    "da missão desde o primeiro dia."
)

# Foco tecnológico
section_title(pdf, "Foco Tecnológico")
tag_row(pdf, ["NAVEGAÇÃO SEM GPS", "INTEGRAÇÃO LIDAR", "COMUNICAÇÕES RESILIENTES", "VOO AUTÓNOMO", "GEOIA"])

# Capacidades da plataforma
section_title(pdf, "Capacidades da Plataforma")
bullets = [
    "Navegação sem GPS: deteção por radar através de reflexões do solo corrige o desvio "
    "inercial, mantendo dados precisos de velocidade e altitude sem ligação por satélite.",
    "Cadeia de valor limpa: eletrónica adquirida exclusivamente junto de nações aliadas "
    "(NATO, Taiwan, Japão), evitando riscos de espionagem e hardware vetado.",
    "Cargas úteis modulares: módulo de sensores intercambiável que suporta múltiplas "
    "tecnologias de deteção para topografia e deteção de obstáculos.",
    "Fabrico lean: prototipagem de PCBs internamente e chassis impresso em 3D de grau "
    "aeronáutico, reduzindo os custos unitários muito abaixo dos preços tradicionais da "
    "indústria de defesa.",
]
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(*DARK)
for b in bullets:
    pdf.set_x(pdf.l_margin)
    pdf.cell(4, 5.0, chr(149))
    pdf.set_x(pdf.l_margin + 5)
    pdf.multi_cell(PAGE_W - pdf.l_margin - pdf.r_margin - 5, 5.0, b)
    pdf.ln(0.2)

# Próximos desenvolvimentos (teal: o segundo accent do site, usado aqui para
# distinguir visualmente o roteiro futuro das secções de capacidade atual)
section_title(pdf, "Próximos Desenvolvimentos", color=TEAL)
pdf.set_x(pdf.l_margin)
pdf.set_font("Archivo", "B", 10)
pdf.set_text_color(*DARK)
pdf.cell(0, 5.2, "Plataforma de Inteligência Geoespacial", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
body_text(
    pdf,
    "Levantamentos aéreos com drones -- magnetometria, LiDAR, espectrometria de raios gama -- "
    "processados com aprendizagem automática para análise de terreno e avaliação de ameaças.",
    size=9.5,
)
pdf.set_x(pdf.l_margin)
pdf.set_font("Archivo", "B", 10)
pdf.set_text_color(*DARK)
pdf.cell(0, 5.2, "Serviços de Levantamento Geridos", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
body_text(
    pdf,
    "Recolha de dados aéreos e elaboração de relatórios de ciclo completo para organizações "
    "de defesa e proteção civil, desde o planeamento de voo até à entrega da análise.",
    size=9.5,
)

# Conformidade e postura de confiança
section_title(pdf, "Conformidade e Postura de Confiança")
body_text(
    pdf,
    "Regulamentação e Certificação: ainda não estamos certificados ao abrigo da "
    "regulamentação de drones ANAC/EASA. Avançar pela via de certificação adequada "
    "faz parte do nosso roteiro à medida que avançamos para os testes operacionais.",
    size=9.5,
)
body_text(
    pdf,
    "Controlo de Exportação e Aquisição: ainda não estabelecemos um estatuto formal "
    "de conformidade em controlo de exportação ou NATO STANAG. Pretendemos construir "
    "esta postura a par das nossas primeiras parcerias operacionais.",
    size=9.5,
)

# Fundadores
section_title(pdf, "Fundadores")
pdf.set_x(pdf.l_margin)
pdf.set_font("Archivo", "B", 10)
pdf.set_text_color(*DARK)
pdf.cell(0, 5.2, "Mike -- Fundador, Integração de Sensores e Arquitetura de Software", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
body_text(
    pdf,
    "Convenceu um chip de radar e um módulo LiDAR a deixarem de discutir e a "
    "cooperar -- basicamente diplomacia. Quando a plataforma não precisa de GPS "
    "para saber onde está, é o Mike.",
    size=9.5,
)
pdf.set_x(pdf.l_margin)
pdf.set_font("Archivo", "B", 10)
pdf.set_text_color(*DARK)
pdf.cell(0, 5.2, "Nuno -- Fundador, Hardware, PCB e Fabrico", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
body_text(
    pdf,
    "Constrói a peça que tem de sobreviver a ser deixada cair, abanada, encharcada "
    "pela chuva e, de vez em quando, repreendida aos gritos -- chassis, modelos CAD "
    "e design de PCBs incluídos.",
    size=9.5,
)

# Footer block -- flows after content rather than pinned to the bottom of
# page 1, since this brief now runs close to a full page with the added
# Compliance and Founders sections.
pdf.ln(0.5)
pdf.set_x(pdf.l_margin)
pdf.set_draw_color(*LINE)
pdf.set_line_width(0.2)
pdf.line(pdf.l_margin, pdf.get_y(), PAGE_W - pdf.r_margin, pdf.get_y())
pdf.ln(3)
pdf.set_x(pdf.l_margin)
pdf.set_font("Archivo", "", 9)
pdf.set_text_color(*MUTED)
pdf.cell(0, 4.3, "comms@falcatasystems.site   |   Luso, Portugal", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_x(pdf.l_margin)
pdf.cell(0, 4.3, "falcatasystems.site", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_x(pdf.l_margin)
pdf.set_font("Helvetica", "I", 8)
pdf.cell(0, 4.3, "Preparado pela Falcata Systems. Para uso do destinatário na avaliação da Falcata Systems como fornecedor.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.output("../falcata-systems-capability-brief-pt.pdf")
print("done")
