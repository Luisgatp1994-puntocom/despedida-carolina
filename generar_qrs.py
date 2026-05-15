"""
Generador de QRs por mesa para la boda Guillermo & Loren · 16 de mayo de 2026.

Genera un PDF imprimible con 7 páginas (una por mesa). Cada página contiene:
  - Encabezado: "Guillermo & Loren · 16 de mayo de 2026"
  - "Mesa N" en grande
  - QR centrado, mínimo ~10 cm de lado
  - Subtexto: "Escanea y comparte tus fotos"
  - Borde dorado y ornamento decorativo simple

Dependencias:
    pip install "qrcode[pil]" reportlab

Uso:
    1) Editar la constante DOMINIO con el dominio real (Vercel).
    2) python generar_qrs.py
    3) Se genera el archivo qrs_boda.pdf en el mismo directorio.
"""

import io
import os
import qrcode
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# =============================================================================
# CONFIG
# =============================================================================

# REEMPLAZAR por el dominio real una vez Vercel termine el deploy.
# Ejemplo: "https://fotos-guillermoyloren.vercel.app"
DOMINIO = "__REEMPLAZAR_DOMINIO__"

TOTAL_MESAS = 7
OUTPUT_PDF = "qrs_boda.pdf"

# Texto
COUPLE_NAME = "Guillermo & Loren"
WEDDING_DATE = "16 de mayo de 2026"
CTA_TEXT = "Escanea y comparte tus fotos"

# Paleta (alineada con la del frontend)
GOLD = HexColor("#C9A85C")
GOLD_DEEP = HexColor("#A8884A")
INK = HexColor("#1F1A14")
INK_SOFT = HexColor("#4A3F30")
CREAM = HexColor("#FAF6EE")

# Tamaño página: A5 vertical (148 x 210 mm). Se imprime cómodo en A4 cortando.
PAGE_W, PAGE_H = A5


# =============================================================================
# QR
# =============================================================================

def make_qr_image(url: str):
    """Genera un PNG en memoria con el QR para la URL dada.

    Usamos corrección de error H (~30%) para que el QR siga siendo escaneable
    aunque tenga marcas de impresión, dobleces o reflejos del acrílico.
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1F1A14", back_color="#FAF6EE")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)


# =============================================================================
# Decoración
# =============================================================================

def draw_border(c: canvas.Canvas):
    """Marco dorado doble en la página."""
    margin = 10 * mm
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.rect(margin, margin, PAGE_W - 2 * margin, PAGE_H - 2 * margin)
    inner = margin + 3 * mm
    c.setLineWidth(0.4)
    c.rect(inner, inner, PAGE_W - 2 * inner, PAGE_H - 2 * inner)


def draw_diamond_divider(c: canvas.Canvas, y: float, half_width: float = 35 * mm):
    """Línea fina con un diamantito al centro (estilo cartel)."""
    cx = PAGE_W / 2
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.line(cx - half_width, y, cx - 4 * mm, y)
    c.line(cx + 4 * mm, y, cx + half_width, y)
    # Diamante (rotated square)
    c.saveState()
    c.translate(cx, y)
    c.rotate(45)
    c.setFillColor(GOLD)
    c.rect(-1.6 * mm, -1.6 * mm, 3.2 * mm, 3.2 * mm, stroke=0, fill=1)
    c.restoreState()


def draw_corner_ornament(c: canvas.Canvas, x: float, y: float, flip_x=False, flip_y=False):
    """Dibuja un ornamento floral minimalista en una esquina."""
    c.saveState()
    c.translate(x, y)
    if flip_x:
        c.scale(-1, 1)
    if flip_y:
        c.scale(1, -1)
    c.setStrokeColor(GOLD)
    c.setFillColor(GOLD)
    c.setLineWidth(0.6)
    # Tallo curvo
    p = c.beginPath()
    p.moveTo(0, 0)
    p.curveTo(10 * mm, 4 * mm, 16 * mm, 12 * mm, 22 * mm, 22 * mm)
    c.drawPath(p, stroke=1, fill=0)
    # Hojitas
    for (cx, cy, r) in [(8 * mm, 4 * mm, 2.2 * mm),
                        (14 * mm, 10 * mm, 1.8 * mm),
                        (20 * mm, 18 * mm, 1.6 * mm)]:
        c.circle(cx, cy, r, stroke=1, fill=0)
    # Florcita al final
    c.circle(22 * mm, 22 * mm, 2.4 * mm, stroke=1, fill=1)
    c.restoreState()


# =============================================================================
# Página por mesa
# =============================================================================

def draw_page(c: canvas.Canvas, mesa: int, url: str):
    # Fondo crema
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    # Marco
    draw_border(c)

    # Ornamentos en las 4 esquinas (dentro del marco)
    margin = 14 * mm
    draw_corner_ornament(c, margin, PAGE_H - margin - 0 * mm, flip_y=True)
    draw_corner_ornament(c, PAGE_W - margin, PAGE_H - margin, flip_x=True, flip_y=True)
    draw_corner_ornament(c, margin, margin + 22 * mm)  # ya cae cerca del piso del marco
    draw_corner_ornament(c, PAGE_W - margin, margin + 22 * mm, flip_x=True)

    # Encabezado: nombre pareja (usamos Helvetica-Oblique como sustituto del script;
    # ReportLab no incluye Great Vibes por defecto y registrar fuentes externas
    # añade complejidad innecesaria para un MVP).
    c.setFillColor(GOLD_DEEP)
    c.setFont("Helvetica-Oblique", 30)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 30 * mm, COUPLE_NAME)

    # Fecha
    c.setFont("Helvetica", 9)
    c.setFillColor(GOLD_DEEP)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 38 * mm, WEDDING_DATE.upper())

    # Divider
    draw_diamond_divider(c, PAGE_H - 44 * mm)

    # "Mesa N"
    c.setFillColor(INK)
    c.setFont("Helvetica", 11)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 56 * mm, "MESA")
    c.setFont("Helvetica-Bold", 48)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 75 * mm, str(mesa))

    # QR (al menos 10 cm de lado)
    qr_size = 95 * mm
    qr_x = (PAGE_W - qr_size) / 2
    qr_y = (PAGE_H - qr_size) / 2 - 18 * mm
    # Fondo blanco crujiente atrás del QR para máximo contraste al escanear
    c.setFillColor(HexColor("#FFFFFF"))
    c.rect(qr_x - 3 * mm, qr_y - 3 * mm, qr_size + 6 * mm, qr_size + 6 * mm,
           stroke=0, fill=1)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.rect(qr_x - 3 * mm, qr_y - 3 * mm, qr_size + 6 * mm, qr_size + 6 * mm,
           stroke=1, fill=0)

    qr_img = make_qr_image(url)
    c.drawImage(qr_img, qr_x, qr_y, width=qr_size, height=qr_size,
                preserveAspectRatio=True, mask='auto')

    # CTA debajo del QR
    c.setFillColor(INK_SOFT)
    c.setFont("Helvetica-Oblique", 13)
    c.drawCentredString(PAGE_W / 2, qr_y - 14 * mm, CTA_TEXT)

    # Divider inferior
    draw_diamond_divider(c, 22 * mm, half_width=30 * mm)

    # Pie
    c.setFillColor(GOLD_DEEP)
    c.setFont("Helvetica", 7)
    c.drawCentredString(PAGE_W / 2, 16 * mm, "Con cariño · 16.05.2026")


# =============================================================================
# Main
# =============================================================================

def main():
    if "__REEMPLAZAR" in DOMINIO:
        print("⚠️  ATENCIÓN: edita la constante DOMINIO al inicio del script "
              "con la URL real de Vercel antes de imprimir.\n")
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), OUTPUT_PDF)
    c = canvas.Canvas(out_path, pagesize=A5)
    c.setTitle("QRs Boda Guillermo & Loren")
    c.setAuthor("Guillermo & Loren")
    for mesa in range(1, TOTAL_MESAS + 1):
        url = f"{DOMINIO.rstrip('/')}/?mesa={mesa}"
        draw_page(c, mesa, url)
        c.showPage()
    c.save()
    print(f"✅ Generado: {out_path}")
    print(f"   {TOTAL_MESAS} páginas · una por mesa")
    print("   Imprime en A4 escalando al 100% o directamente en A5.")


if __name__ == "__main__":
    main()
