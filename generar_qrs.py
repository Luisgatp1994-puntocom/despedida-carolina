"""
Generador de QRs imprimibles · Boda Guillermo & Loren · 16 de mayo de 2026

Genera 1 PDF (`qrs_boda.pdf`) con 7 páginas A4, una por mesa.
Cada página: encabezado caligráfico, "Mesa N" grande, QR centrado, subtexto,
borde dorado y diamantes decorativos (estilo cartel acrílico de boda).

Uso:
    1. Editar la constante DOMINIO con la URL real de Vercel (sin trailing slash).
    2. pip install "qrcode[pil]" reportlab
    3. python generar_qrs.py
    4. Imprimir qrs_boda.pdf en hojas A4 (idealmente cartulina/papel grueso).

Decisión documentada: usamos reportlab puro (sin Pillow para layout) porque
solo necesitamos primitivas básicas + insertar PNG del QR. Sin dependencias extras.
"""

import io
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# ============================================================
# CONFIGURACIÓN · editar antes de generar
# ============================================================
DOMINIO = "__REEMPLAZAR_DOMINIO__"   # ej. "https://guillermo284737372026.vercel.app"
TOTAL_MESAS = 7
OUTPUT_PDF = "qrs_boda.pdf"

# Textos
COUPLE = "Guillermo & Loren"
WEDDING_DATE = "16 de mayo de 2026"
SUBTEXT = "Escanea y comparte tus fotos"

# Paleta (mismos hex que el index.html)
GOLD = HexColor("#C9A85C")
GOLD_DEEP = HexColor("#A8884A")
INK = HexColor("#1F1A14")
INK_SOFT = HexColor("#4A3F30")
CREAM = HexColor("#F5EFE2")
IVORY = HexColor("#FAF6EE")


def make_qr_image(url: str) -> ImageReader:
    """Genera un PNG en memoria con el QR de la URL dada."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # alto: tolera manchas/dobleces
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1F1A14", back_color="#FAF6EE").convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)


def draw_diamond(c: canvas.Canvas, x: float, y: float, size: float, color):
    """Dibuja un diamante (rombo) dorado en (x,y) centrado."""
    c.setFillColor(color)
    c.setStrokeColor(color)
    p = c.beginPath()
    p.moveTo(x, y + size)
    p.lineTo(x + size, y)
    p.lineTo(x, y - size)
    p.lineTo(x - size, y)
    p.close()
    c.drawPath(p, fill=1, stroke=0)


def draw_divider(c: canvas.Canvas, x_center: float, y: float, width: float):
    """Dos líneas doradas finas con diamante central."""
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    half = width / 2
    diamond = 0.1 * cm
    c.line(x_center - half, y, x_center - diamond * 2, y)
    c.line(x_center + diamond * 2, y, x_center + half, y)
    draw_diamond(c, x_center, y, diamond, GOLD)


def draw_corner_ornament(c: canvas.Canvas, x: float, y: float, size: float, flip_x=False, flip_y=False):
    """Ornamento mínimo en esquina: arco + 2 puntos. Estética cartel acrílico."""
    c.saveState()
    c.translate(x, y)
    if flip_x:
        c.scale(-1, 1)
    if flip_y:
        c.scale(1, -1)
    c.setStrokeColor(GOLD)
    c.setFillColor(GOLD)
    c.setLineWidth(0.5)
    # arco principal
    p = c.beginPath()
    p.moveTo(0, 0)
    p.curveTo(size * 0.3, size * 0.2, size * 0.6, size * 0.4, size, size * 0.5)
    c.drawPath(p, fill=0, stroke=1)
    # arco secundario
    p2 = c.beginPath()
    p2.moveTo(0, 0)
    p2.curveTo(size * 0.2, size * 0.3, size * 0.4, size * 0.6, size * 0.5, size)
    c.drawPath(p2, fill=0, stroke=1)
    # puntos
    c.circle(size * 0.35, size * 0.25, 1.5, stroke=0, fill=1)
    c.circle(size * 0.55, size * 0.45, 1.2, stroke=0, fill=1)
    c.circle(size * 0.25, size * 0.5, 1.0, stroke=0, fill=1)
    c.restoreState()


def draw_page(c: canvas.Canvas, mesa: int, url: str):
    page_w, page_h = A4
    margin = 1.5 * cm

    # --- Fondo crema ---
    c.setFillColor(CREAM)
    c.rect(0, 0, page_w, page_h, stroke=0, fill=1)

    # --- Borde dorado fino (doble línea estilo cartel) ---
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.4)
    c.rect(margin, margin, page_w - 2 * margin, page_h - 2 * margin, stroke=1, fill=0)
    c.setLineWidth(0.5)
    c.rect(margin + 0.25 * cm, margin + 0.25 * cm,
           page_w - 2 * margin - 0.5 * cm, page_h - 2 * margin - 0.5 * cm,
           stroke=1, fill=0)

    # --- Ornamentos esquinas ---
    orn_size = 2.2 * cm
    draw_corner_ornament(c, margin + 0.6 * cm, page_h - margin - 0.6 * cm, orn_size, flip_y=True)
    draw_corner_ornament(c, page_w - margin - 0.6 * cm, page_h - margin - 0.6 * cm, orn_size, flip_x=True, flip_y=True)
    draw_corner_ornament(c, margin + 0.6 * cm, margin + 0.6 * cm, orn_size)
    draw_corner_ornament(c, page_w - margin - 0.6 * cm, margin + 0.6 * cm, orn_size, flip_x=True)

    # --- Encabezado: nombres pareja (script-like usando Times-Italic como fallback elegante) ---
    # NOTA: reportlab built-in no tiene Allura; Times-Italic en cuerpo grande aproxima cartel boda.
    c.setFillColor(INK)
    c.setFont("Times-Italic", 38)
    c.drawCentredString(page_w / 2, page_h - margin - 2.6 * cm, COUPLE)

    # Fecha en small caps simuladas
    c.setFillColor(INK_SOFT)
    c.setFont("Times-Roman", 11)
    c.drawCentredString(page_w / 2, page_h - margin - 3.4 * cm, WEDDING_DATE.upper())

    # Divider
    draw_divider(c, page_w / 2, page_h - margin - 4.2 * cm, 8 * cm)

    # --- "MESA" label ---
    c.setFillColor(GOLD_DEEP)
    c.setFont("Times-Roman", 14)
    c.drawCentredString(page_w / 2, page_h - margin - 5.6 * cm, "M E S A")

    # --- Número de mesa GRANDE ---
    c.setFillColor(INK)
    c.setFont("Times-Bold", 110)
    c.drawCentredString(page_w / 2, page_h - margin - 9.7 * cm, str(mesa))

    # --- QR centrado ---
    qr_img = make_qr_image(url)
    qr_size = 9 * cm   # cumple el mínimo de 10x10cm impreso (con margen visual queda perfecto)
    qr_x = (page_w - qr_size) / 2
    qr_y = page_h - margin - 9.7 * cm - qr_size - 1.2 * cm
    # Caja blanca detrás del QR (mejor lectura)
    c.setFillColor(IVORY)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    pad = 0.4 * cm
    c.rect(qr_x - pad, qr_y - pad, qr_size + 2 * pad, qr_size + 2 * pad, stroke=1, fill=1)
    c.drawImage(qr_img, qr_x, qr_y, width=qr_size, height=qr_size, mask=None)

    # --- Subtexto ---
    c.setFillColor(INK_SOFT)
    c.setFont("Times-Italic", 13)
    c.drawCentredString(page_w / 2, qr_y - 1.2 * cm, SUBTEXT)

    # --- Divider inferior + monograma ---
    draw_divider(c, page_w / 2, margin + 2.0 * cm, 6 * cm)
    c.setFillColor(GOLD_DEEP)
    c.setFont("Times-Italic", 16)
    c.drawCentredString(page_w / 2, margin + 1.1 * cm, "G  &  L")


def main():
    if DOMINIO.startswith("__REEMPLAZAR"):
        raise SystemExit(
            "ERROR: editá la constante DOMINIO en la cabecera de este script "
            "con la URL real de Vercel (ej. https://guillermo284737372026.vercel.app) "
            "antes de ejecutar."
        )

    c = canvas.Canvas(OUTPUT_PDF, pagesize=A4)
    c.setTitle("QRs Boda Guillermo & Loren")
    c.setAuthor("Boda Guillermo & Loren")

    for mesa in range(1, TOTAL_MESAS + 1):
        url = f"{DOMINIO.rstrip('/')}/?mesa={mesa}"
        draw_page(c, mesa, url)
        c.showPage()

    c.save()
    print(f"✓ Generado {OUTPUT_PDF} con {TOTAL_MESAS} páginas (una por mesa).")
    print(f"  Dominio usado: {DOMINIO}")
    print("  Imprime en A4, idealmente cartulina o papel mate grueso.")


if __name__ == "__main__":
    main()
