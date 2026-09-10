"""
Generates the Falcta Systems one-page capability brief (PDF).

Print-friendly (white background) by design, even though the website uses a
dark theme: this is meant to be printed or forwarded internally by
procurement contacts, and a full black page prints poorly on office
laser/inkjet printers.

Run: python3 generate_brief.py
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
pdf.cell(0, 6, "UAS & Geospatial Intelligence -- Built for the field, not the brochure.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.set_draw_color(*ACCENT)
pdf.set_line_width(0.8)
y = pdf.get_y() + 3
pdf.line(pdf.l_margin, y, PAGE_W - pdf.r_margin, y)
pdf.ln(8)

# Who we serve
section_title(pdf, "Who We Serve")
pdf.set_x(pdf.l_margin)
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(*DARK)
pdf.cell(0, 6, "Portuguese Army   |   Portuguese Air Force   |   Civil Protection", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_x(pdf.l_margin)
pdf.ln(2)

# Current service
section_title(pdf, "Current Service -- Custom Drone Development")
body_text(
    pdf,
    "End-to-end design and build of UAS platforms tailored to operational requirements. "
    "Focus on hostile-environment performance and mission-critical reliability -- systems "
    "that keep working when GPS, comms, or field conditions do not cooperate."
)

# Technology focus
section_title(pdf, "Technology Focus")
tag_row(pdf, ["GPS-DENIED NAVIGATION", "LIDAR INTEGRATION", "RESILIENT COMMS", "AUTONOMOUS FLIGHT", "GEOAI"])

# Platform capabilities
section_title(pdf, "Platform Capabilities")
bullets = [
    "GPS-denied navigation: 60GHz FMCW radar coupled with an STM32 MCU, correcting IMU "
    "drift from ground-reflection speed and altitude data.",
    "Clean value chain: electronics sourced exclusively from allied nations (NATO, Taiwan, "
    "Japan), avoiding espionage risk and vetoed hardware.",
    "Modular sensor payloads: interchangeable Doppler radar and LiDAR slots for topography "
    "and obstacle detection.",
    "Lean manufacturing: in-house PCB prototyping and 3D-printed aero-grade chassis, cutting "
    "unit costs well below traditional defense-contractor pricing.",
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
section_title(pdf, "Future Pipeline")
pdf.set_x(pdf.l_margin)
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(*DARK)
pdf.cell(0, 5.5, "Geospatial Intelligence Platform", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
body_text(
    pdf,
    "Drone-based airborne surveys -- magnetometry, LiDAR, gamma-ray spectrometry -- "
    "processed with machine learning for terrain analysis and threat assessment.",
    size=9.5,
)
pdf.set_x(pdf.l_margin)
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(*DARK)
pdf.cell(0, 5.5, "Managed Survey Services", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
body_text(
    pdf,
    "Full-cycle airborne data collection and reporting for defence and civil protection "
    "clients, from flight planning through delivered analysis.",
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
pdf.cell(0, 5, "Prepared by Falcta Systems. For recipient use in evaluating Falcta Systems as a supplier.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.output("/tmp/claude-1000/-home-mikescorreia/dfd06df4-1b54-4d0c-be61-11503a912948/scratchpad/falcta-systems-capability-brief.pdf")
print("done")
