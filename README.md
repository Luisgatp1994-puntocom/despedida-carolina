# Boda Guillermo & Loren · QR Photo Drop

Sistema web para que los invitados de la boda suban fotos escaneando un QR por mesa.
Stack: HTML + JS vanilla + Firebase (Storage + Firestore) + Vercel + script Python para QRs.

**Boda:** 16 de mayo de 2026
**Mesas:** 7
**Invitados esperados:** ~70

---

## 1. Crear proyecto Firebase NUEVO

> ⚠️ NO usar los proyectos existentes (Salud & Sabor, LucAi). Este es un proyecto separado.

1. https://console.firebase.google.com → "Agregar proyecto"
2. Nombre: `boda-guillermo-loren` (o el que prefieras)
3. **Desactivar Google Analytics** (no lo necesitamos)
4. Crear

## 2. Activar Storage y Firestore

**Storage:**
- Build → Storage → "Comenzar"
- Modo: **Producción** (NO modo de prueba)
- Región: `southamerica-east1` (São Paulo) o `us-east1`

**Firestore:**
- Build → Firestore Database → "Crear base de datos"
- Modo: **Producción**
- Región: **misma que Storage**

## 3. Pegar reglas de seguridad

**Storage rules** (Storage → Reglas):
copiar el contenido de `storage.rules` y pegar → Publicar.

**Firestore rules** (Firestore → Reglas):
copiar el contenido de `firestore.rules` y pegar → Publicar.

## 4. Configurar la app Web en Firebase

1. Configuración del proyecto (engranaje) → "Tus apps" → ícono `</> Web`
2. Apodo: `boda-web` · NO marcar Firebase Hosting
3. Copiar el objeto `firebaseConfig` que aparece.
4. Pegar los valores reales en `firebase-config.js` reemplazando los `__REEMPLAZAR_*__`.

## 5. Deploy en Vercel (proyecto NUEVO)

1. https://vercel.com/new
2. Importar el repo de GitHub
3. Framework preset: **Other** (es HTML estático)
4. Build command: **vacío**
5. Output directory: **`.`** (raíz)
6. Deploy

URL resultante: `https://<nombre-proyecto>.vercel.app`

## 6. Dominio

No es necesario un dominio custom para una boda de un día. El `*.vercel.app`
funciona perfecto y trae HTTPS gratis.

## 7. Generar los QRs imprimibles

1. Editar `generar_qrs.py`: cambiar la constante `DOMINIO` por la URL de Vercel.
2. Instalar dependencias:
   ```bash
   pip install "qrcode[pil]" reportlab
   ```
3. Ejecutar:
   ```bash
   python generar_qrs.py
   ```
4. Salida: `qrs_boda.pdf` con 7 páginas (una por mesa).

## 8. Imprimir el PDF

- A4, idealmente cartulina o papel mate grueso.
- Verificar que el QR mide al menos **10×10 cm** impreso.
- Recortar y poner en cada mesa (soporte acrílico o base de madera).

## 9. Test end-to-end (CRÍTICO antes del evento)

1. Desde un **iPhone** (Safari): escanear QR de mesa 1 → subir 3 fotos → verificar pantalla de éxito.
2. Desde un **Android** (Chrome): repetir con mesa 2.
3. Abrir Firebase Console → Storage → carpeta `boda-guillermo-loren/mesa-1/` → confirmar que están los archivos.
4. Firebase Console → Firestore → colección `fotos` → confirmar 3 documentos con metadata correcta.
5. Probar sin internet: el banner naranja "Sin conexión" debería aparecer.

---

## Estructura del repo

```
.
├── index.html           # SPA completa (3 pantallas)
├── firebase-config.js   # Config Firebase (rellenar credenciales)
├── storage.rules        # Reglas Storage
├── firestore.rules      # Reglas Firestore
├── generar_qrs.py       # Script generador del PDF de QRs
└── README.md
```

## Después de la boda

- Descargar todas las fotos desde Firebase Console → Storage → seleccionar carpetas → descargar.
- (Opcional) Pausar facturación en Firebase si excede free tier (improbable: estimado 2-4 GB de uso).
- (Opcional) Eliminar el proyecto Vercel una vez bajadas las fotos.

## Notas técnicas

- **Compresión cliente:** cada foto se reduce a max 1920px lado mayor, calidad 0.85 (JPG) antes de subir → ahorra ~70% del tamaño.
- **Retry:** 2 reintentos por foto con backoff (800ms, 1600ms). Si falla 3 veces, se marca como error pero NO bloquea las demás.
- **Offline-aware:** detecta `navigator.onLine` y muestra banner.
- **Persistencia mesa:** `localStorage["boda_mesa"]` para sobrevivir refrescos.
- **Free tier Firebase Spark:** 5 GB Storage, 1 GiB transfer/día, Firestore 50k lecturas/día. Suficiente para una boda de 70 personas.
- **Costo total esperado:** **$0 USD**.
