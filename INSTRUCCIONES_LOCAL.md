# Cómo correr local · Boda Guillermo & Loren

## ⚠️ Antes de empezar — lee esto

**Correr local NO basta para la boda.** Tu teléfono y los de los invitados necesitan una URL pública (HTTPS) para escanear el QR. `localhost` solo funciona desde tu propia computadora.

**Opciones para tener URL pública:**
1. **Vercel** (lo que veníamos hablando — 3 clics)
2. **ngrok** o **cloudflared** — túnel temporal desde tu computadora a internet (gratis)
3. **Netlify drop** (subir el ZIP a netlify.com/drop, 1 paso)

Pero primero, vamos a verificar que funciona local:

---

## 1. Requisitos (lo que necesitas instalado)

- **Python 3** (viene por defecto en Mac/Linux). Si no, `brew install python3`
- **Un navegador** (Safari/Chrome)
- **Conexión a internet** (porque sube a Cloudinary)

## 2. Correrlo local

Abre Terminal, navega a la carpeta del proyecto y ejecuta:

```bash
cd ruta/a/Guillermo284737372026
python3 -m http.server 8000
```

Verás:
```
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

## 3. Abrirlo en el browser

En Safari/Chrome ve a:
```
http://localhost:8000/?mesa=1
```

Deberías ver la pantalla con "Guillermo & Loren", Mesa 1, etc.

## 4. Probar el flujo completo

1. Clic en **"Tomar foto / Elegir de galería"**
2. Elige 1-2 fotos de tu disco
3. Verifica que se ven los thumbnails
4. Clic **"Enviar"**
5. Espera la progress bar
6. Pantalla de éxito ✅
7. Abre tu dashboard de Cloudinary → Media Library → folder `boda-guillermo-loren/mesa-1/` → confirma que las fotos están ahí

## 5. Si las fotos NO suben

Posibles causas:

### A. Preset Cloudinary sigue en "Signed"
Esto es el #1 más probable. Verifica:
- Cloudinary dashboard → ⚙️ Settings → Upload → Upload Presets
- En la columna "Mode" para `boda_guillermo_loren` debe decir **"Unsigned"**
- Si dice "Signed": clic en el preset → cambiar a Unsigned → Save

### B. Console del browser muestra error CORS
Cloudinary acepta unsigned uploads desde cualquier origen, así que NO debería pasar. Si pasa: revisa que el cloud name `du9nzknuq` esté bien escrito en `cloudinary-config.js`.

### C. "Upload preset must be whitelisted for unsigned uploads"
Es el mismo problema A. Cambia el preset a Unsigned.

### D. Pantalla en blanco al abrir
Abre la consola del browser (Cmd+Opt+I en Mac, F12 en Windows) y mira si hay errores rojos. Pásamelos por el chat.

---

## 6. Para que funcione con celulares (no solo tu Mac)

### Opción rápida: cloudflared tunnel (gratis, sin cuenta)

```bash
# Instalar (una vez)
brew install cloudflared

# Correr (después de tener python3 -m http.server 8000 corriendo)
cloudflared tunnel --url http://localhost:8000
```

Te dará una URL temporal tipo `https://abc-xyz.trycloudflare.com` que dura mientras tengas el comando corriendo. Esa URL funciona en cualquier celular del mundo.

### Opción más durable: Vercel (lo que ya te describí)
Es 3 clics en vercel.com/new y funciona para siempre. Recomendado para el evento.

---

## 7. Generar los QRs

Una vez que tengas la URL final (vercel.app, cloudflared, lo que sea):

```bash
# Instalar dependencias (una vez)
pip3 install "qrcode[pil]" reportlab

# Editar generar_qrs.py: cambiar DOMINIO = "__REEMPLAZAR_DOMINIO__"
# por la URL real, ej: DOMINIO = "https://guillermo284737372026.vercel.app"

# Ejecutar
python3 generar_qrs.py
```

Saldrá `qrs_boda.pdf` con 7 páginas. Imprime y listo.

---

## Estructura del proyecto

```
.
├── index.html              # App principal (SPA 3 pantallas)
├── cloudinary-config.js    # Config Cloudinary (ya está completa)
├── generar_qrs.py          # Genera el PDF de los QRs
├── README.md               # Documentación general
├── INSTRUCCIONES_LOCAL.md  # Este archivo
└── .gitignore
```

¿Problemas? Vuelve al chat y cuéntame qué ves.
