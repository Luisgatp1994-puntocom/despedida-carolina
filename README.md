# Boda Guillermo & Loren · QR Photo Drop

Sistema web para que los invitados de la boda suban fotos escaneando un QR por mesa.
Stack: HTML + JS vanilla + Cloudinary (storage gratis 25 GB) + Vercel + script Python para QRs.

**Boda:** 16 de mayo de 2026
**Mesas:** 7
**Invitados esperados:** ~70

---

## 1. Cuenta Cloudinary (gratis, sin tarjeta)

1. https://cloudinary.com/users/register_free → sign up (con Google o email)
2. En el dashboard → engranaje ⚙️ → **Settings** → pestaña **"Upload"**
3. Scroll a **"Upload presets"** → **"Add upload preset"**
4. Configurar:
   - **Preset name:** `boda_guillermo_loren`
   - **Signing Mode:** **Unsigned** ⚠️ (clave)
   - **Folder:** `boda-guillermo-loren`
   - Save
5. Copiar:
   - **Cloud Name** (aparece arriba en el dashboard)
   - **Preset name** (el que acabaste de crear)
6. Pegarlos en `cloudinary-config.js` reemplazando los `__REEMPLAZAR_*__`

## 2. Deploy en Vercel (proyecto NUEVO)

1. https://vercel.com/new
2. Importar el repo de GitHub
3. Framework preset: **Other** (HTML estático)
4. Build command: **vacío**
5. Output directory: **`.`** (raíz)
6. Deploy

URL resultante: `https://<nombre-proyecto>.vercel.app`

## 3. Generar los QRs imprimibles

1. Editar `generar_qrs.py`: cambiar la constante `DOMINIO` por la URL de Vercel
2. Instalar dependencias:
   ```bash
   pip install "qrcode[pil]" reportlab
   ```
3. Ejecutar:
   ```bash
   python generar_qrs.py
   ```
4. Salida: `qrs_boda.pdf` con 7 páginas (una por mesa)

## 4. Imprimir el PDF

- A4, idealmente cartulina o papel mate grueso
- QR mínimo **10×10 cm** impreso
- Recortar y poner en cada mesa

## 5. Test end-to-end (CRÍTICO antes del evento)

1. **iPhone** (Safari): escanear QR mesa 1 → subir 3 fotos → ver pantalla de éxito
2. **Android** (Chrome): repetir con mesa 2
3. Cloudinary dashboard → **Media Library** → folder `boda-guillermo-loren/mesa-1/` → confirmar archivos
4. Verificar tags y context: cada foto tiene `mesa-N`, `boda-guillermo-loren` y contexto con nombre/device
5. Probar sin internet: debe aparecer el banner "Sin conexión"

## 6. Descargar fotos después del evento

**Opción A — Bulk por mesa (recomendado):**
- Cloudinary dashboard → **Media Library** → filtrar por tag `mesa-N` → seleccionar todo → "Download as ZIP"

**Opción B — Todo de una:**
- Filtrar por tag `boda-guillermo-loren` → seleccionar todo → "Download as ZIP"

---

## Estructura del repo

```
.
├── index.html              # SPA completa (3 pantallas)
├── cloudinary-config.js    # Config Cloudinary (rellenar)
├── generar_qrs.py          # Script generador del PDF de QRs
├── README.md
└── .gitignore
```

## Notas técnicas

- **Compresión cliente:** cada foto se reduce a max 1920px lado mayor, calidad 0.85 (JPG) antes de subir → ahorra ~70% del tamaño.
- **Retry:** 2 reintentos por foto con backoff (800ms, 1600ms).
- **Offline-aware:** detecta `navigator.onLine` y muestra banner.
- **Persistencia mesa:** `localStorage["boda_mesa"]` sobrevive a refrescos.
- **Free tier Cloudinary:** 25 GB storage + 25 GB bandwidth/mes. Tu uso esperado: ~280 MB después de compresión. Estás usando <2% del free tier.
- **Costo total esperado:** **$0 USD**.
- **Sin tarjeta de crédito requerida.**

## Seguridad

- El `upload_preset` es de tipo **unsigned** → el browser puede subir directo sin API key
- Limitado a imágenes (configurable en el preset desde Cloudinary)
- Las fotos NO son públicamente listables — solo los novios con cuenta Cloudinary acceden al Media Library
- Folder structure por mesa permite filtrado y bulk download
