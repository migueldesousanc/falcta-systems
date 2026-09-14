"""
Generates the Falcata Systems capability brief (PDF).

Print-friendly (white background) by design, even though the website uses a
dark theme: this is meant to be printed or forwarded internally by
procurement contacts, and a full black page prints poorly on office
laser/inkjet printers.

Originally a strict one-pager; with the Compliance and Founders sections
added for content parity with the site, it now runs one full page plus a
few trailing footer lines onto a short second page. If that's worth fixing
properly, the honest options are trimming a section's copy or accepting
two pages outright -- not further shrinking type/leading to force page 1.

Typography/color intentionally mirror the website's current (post-redesign)
identity: Archivo for headings/labels (the site's --font-heading), a plain
sans for body copy, no bracket wordmark, no "// " prefixes, and both site
accent colors (orange as primary, teal as secondary) rather than orange
doing all the work.

Run: python3 generate_brief.py
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
pdf.cell(0, 6, "UAS & Geospatial Intelligence -- Built for the field, not the brochure.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.set_draw_color(*ACCENT)
pdf.set_line_width(0.8)
y = pdf.get_y() + 3
pdf.line(pdf.l_margin, y, PAGE_W - pdf.r_margin, y)
pdf.ln(5)

# Who we're building for
section_title(pdf, "Who We're Building For")
pdf.set_x(pdf.l_margin)
pdf.set_font("Archivo", "B", 10)
pdf.set_text_color(*DARK)
pdf.cell(0, 6, "Portuguese Army   |   Portuguese Air Force   |   Civil Protection", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_x(pdf.l_margin)
pdf.ln(1)
body_text(
    pdf,
    "We're designing Vanguard around the real operational demands of tactical "
    "reconnaissance, airborne systems integration, and emergency terrain survey -- "
    "the environments our target users actually operate in.",
    size=9.5,
)

# Current stage
section_title(pdf, "Current Stage")
body_text(
    pdf,
    "We're currently building our first Vanguard prototype -- sourcing core hardware, "
    "including LiDAR, radar, and flight control components, now, with a first field "
    "test targeted for this December. Our focus is hostile-environment performance "
    "and mission-critical reliability from day one."
)

# Technology focus
section_title(pdf, "Technology Focus")
tag_row(pdf, ["GPS-DENIED NAVIGATION", "LIDAR INTEGRATION", "RESILIENT COMMS", "AUTONOMOUS FLIGHT", "GEOAI"])

# Platform capabilities
section_title(pdf, "Platform Capabilities")
bullets = [
    "GPS-denied navigation: radar-based ground-reflection sensing corrects inertial drift, "
    "maintaining accurate speed and altitude data without a satellite link.",
    "Clean value chain: electronics sourced exclusively from allied nations (NATO, Taiwan, "
    "Japan), avoiding espionage risk and vetoed hardware.",
    "Modular sensor payloads: interchangeable sensor bay supporting multiple ranging "
    "technologies for topography and obstacle detection.",
    "Lean manufacturing: in-house PCB prototyping and 3D-printed aero-grade chassis, cutting "
    "unit costs well below traditional defense-contractor pricing.",
]
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(*DARK)
for b in bullets:
    pdf.set_x(pdf.l_margin)
    pdf.cell(4, 5.0, chr(149))
    pdf.set_x(pdf.l_margin + 5)
    pdf.multi_cell(PAGE_W - pdf.l_margin - pdf.r_margin - 5, 5.0, b)
    pdf.ln(0.2)

# Future pipeline (teal: the site's second accent, used here to visually set
# roadmap/future work apart from the current-capability sections above)
section_title(pdf, "Future Pipeline", color=TEAL)
pdf.set_x(pdf.l_margin)
pdf.set_font("Archivo", "B", 10)
pdf.set_text_color(*DARK)
pdf.cell(0, 5.2, "Geospatial Intelligence Platform", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
body_text(
    pdf,
    "Drone-based airborne surveys -- magnetometry, LiDAR, gamma-ray spectrometry -- "
    "processed with machine learning for terrain analysis and threat assessment.",
    size=9.5,
)
pdf.set_x(pdf.l_margin)
pdf.set_font("Archivo", "B", 10)
pdf.set_text_color(*DARK)
pdf.cell(0, 5.2, "Managed Survey Services", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
body_text(
    pdf,
    "Full-cycle airborne data collection and reporting for defence and civil protection "
    "organizations, from flight planning through delivered analysis.",
    size=9.5,
)

# Compliance & trust posture
section_title(pdf, "Compliance & Trust Posture")
body_text(
    pdf,
    "Regulatory & Certification: we are not yet certified under ANAC/EASA drone "
    "regulations. Pursuing the appropriate certification pathway is part of our "
    "roadmap as we move toward operational testing.",
    size=9.5,
)
body_text(
    pdf,
    "Export Control & Procurement: we have not yet established formal export-control "
    "or NATO STANAG compliance status. We intend to build this posture in step with "
    "our first operational partnerships.",
    size=9.5,
)

# Founders
section_title(pdf, "Founders")
pdf.set_x(pdf.l_margin)
pdf.set_font("Archivo", "B", 10)
pdf.set_text_color(*DARK)
pdf.cell(0, 5.2, "Mike -- Founder, Sensor Integration & Software Architecture", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
body_text(
    pdf,
    "Convinced a radar chip and a LiDAR module to stop arguing and cooperate -- "
    "basically diplomacy. When the platform doesn't need GPS to know where it is, "
    "that's Mike.",
    size=9.5,
)
pdf.set_x(pdf.l_margin)
pdf.set_font("Archivo", "B", 10)
pdf.set_text_color(*DARK)
pdf.cell(0, 5.2, "Nuno -- Founder, Hardware, PCB & Manufacturing", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
body_text(
    pdf,
    "Builds the part that has to survive being dropped, shaken, rained on, and "
    "occasionally yelled at -- chassis, CAD models, and PCB design included.",
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
pdf.cell(0, 4.3, "Prepared by Falcata Systems. For recipient use in evaluating Falcata Systems as a supplier.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.output("../falcata-systems-capability-brief.pdf")
print("done")
