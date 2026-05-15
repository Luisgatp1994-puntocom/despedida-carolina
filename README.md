# QR Photo Drop · Boda Guillermo & Loren

> Sistema web mobile-first para que los invitados de la boda **Guillermo & Loren** (16 de mayo de 2026) escaneen un QR en su mesa y suban fotos directo a Firebase.

**Stack:** HTML + JS vanilla + Firebase (Storage + Firestore) + Vercel.
**Sin builds, sin frameworks, sin backend propio.**

---

## Estructura del repo

```
.
├── index.html            # SPA con las 3 pantallas (welcome / preview / success)
├── firebase-config.js    # Config Firebase + lista de invitados por mesa
├── storage.rules         # Reglas de Firebase Storage
├── firestore.rules       # Reglas de Firestore
├── generar_qrs.py        # Script Python para generar el PDF con los 7 QRs
└── README.md             # Este archivo
```

---

## Pasos para deploy

### 1. Crear un proyecto Firebase **NUEVO**

> ⚠️ No usar proyectos existentes (Salud & Sabor, LucAi, etc.). Este sistema vive en su propio proyecto para no mezclar facturación ni reglas.

1. Ir a https://console.firebase.google.com → **Add project**.
2. Nombre sugerido: `boda-guillermo-loren`. Desactivar Google Analytics (no se necesita).
3. Una vez creado, ir a **Build → Storage** → **Get started** → elegir región (recomendado `us-central1` o la más cercana) → modo producción.
4. Ir a **Build → Firestore Database** → **Create database** → modo producción → misma región que Storage.

### 2. Aplicar las reglas

En la consola:

- **Storage → Rules** → pegar el contenido de `storage.rules` → **Publish**.
- **Firestore → Rules** → pegar el contenido de `firestore.rules` → **Publish**.

### 3. Copiar la config a `firebase-config.js`

1. En Firebase Console: **⚙️ Settings → Project settings → General → Your apps → `</>` (Web)**.
2. Registrar la app (nombre cualquiera, no marcar Hosting).
3. Copiar el objeto `firebaseConfig` que aparece.
4. Reemplazar los placeholders `__REEMPLAZAR_*__` en `firebase-config.js`.

### 4. Deploy en Vercel **(proyecto NUEVO)**

> ⚠️ No reutilizar proyectos existentes en Vercel.

1. Push del repo a GitHub (rama `claude/wedding-qr-photo-upload-RqRWj` o `main`).
2. https://vercel.com/new → importar el repo.
3. **Framework Preset:** `Other` (es HTML estático, sin build).
4. Deploy. Vercel asigna un dominio `*.vercel.app`.

### 5. (Opcional) Dominio custom

Si querés un subdominio (ej. `fotos.tudominio.com`):

- Vercel → Project → Settings → Domains → agregar.
- Configurar el CNAME en el proveedor del dominio.

### 6. Generar los QRs

Editar `generar_qrs.py`:

```python
DOMINIO = "https://tu-dominio.vercel.app"   # o el dominio custom
```

Ejecutar:

```bash
pip install "qrcode[pil]" reportlab
python generar_qrs.py
```

Sale `qrs_boda.pdf` con **7 páginas (una por mesa)**. Imprimir.

- Tamaño página: A5. Se puede imprimir directamente en A5, o en A4 al 100% y recortar.
- El QR queda ~9.5 cm de lado, suficiente para escaneo a 0.5–1 m del cartel.
- Pegar cada hoja en su mesa (recomendado: enmarcar o plastificar).

### 7. Test end-to-end **antes del evento**

Desde un celular (idealmente dos: iOS + Android):

- [ ] Escanear el QR de Mesa 5 (por ejemplo) y verificar que abre la app con `?mesa=5`.
- [ ] Tocar **Tomar foto** → seleccionar 3 fotos de galería.
- [ ] Ver previews → tocar **Enviar 3 fotos** → ver progreso → llegar a pantalla de éxito.
- [ ] En Firebase Console → **Storage** → `boda-guillermo-loren/mesa-5/` → deben aparecer 3 archivos.
- [ ] En Firebase Console → **Firestore** → colección `fotos` → deben aparecer 3 documentos con `mesa: 5`.
- [ ] Probar con conexión apagada: debe mostrar aviso de "Sin conexión" y no romper.
- [ ] Probar sin parámetro `?mesa=` (entrar directo al dominio) → debe aparecer dropdown manual.

---

## Después del evento: descargar el bulk

Los novios (admins del proyecto Firebase) pueden:

### Opción A — Firebase Console (manual)

- **Storage → `boda-guillermo-loren/`** → cada carpeta `mesa-N/` se descarga foto por foto desde la UI.

### Opción B — `gsutil` (todas las fotos de una)

Requiere instalar [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).

```bash
gcloud auth login
gsutil -m cp -r gs://<TU_STORAGE_BUCKET>/boda-guillermo-loren ./descarga-fotos
```

`<TU_STORAGE_BUCKET>` es el valor de `storageBucket` en `firebase-config.js` (sin el `.appspot.com` extra si tu config lo trae completo, copiarlo tal cual).

---

## Checklist pre-evento

- [ ] Proyecto Firebase nuevo creado
- [ ] Storage + Firestore activos
- [ ] Reglas aplicadas (Storage + Firestore)
- [ ] `firebase-config.js` con credenciales reales
- [ ] Deploy en Vercel exitoso
- [ ] Dominio funcionando con HTTPS
- [ ] `generar_qrs.py` actualizado con el dominio real
- [ ] PDF impreso (QRs de al menos 10×10 cm)
- [ ] Test desde iPhone + Android
- [ ] Subidas de 5 fotos seguidas sin problemas
- [ ] Verificado en Firebase Console que llegan las fotos
- [ ] Plan B listo (servicio comercial standby, por si falla algo el día)

---

## Decisiones técnicas (resumen)

| Decisión | Por qué |
|---|---|
| Sin framework | MVP de 48 h, cero overhead |
| Firebase Storage + Firestore | Free tier cubre el evento; admin desde Console |
| Compresión cliente (1920px, q=0.85) | Reduce subida de 4 MB a ~400-700 KB → más rápido en redes móviles de salón |
| Reintentos 3x con backoff | Resiliencia ante caídas momentáneas del Wi-Fi |
| Reglas `read: false` en Storage | Las fotos NO son públicas, solo los novios |
| `localStorage` para mesa | Si el invitado refresca, no pierde la mesa |
| Sin auth de invitados | El QR físico ya actúa como "permiso" + reglas validan rangos |
| QR con corrección de error H | Sobrevive a reflejos, dobleces, fotos del cartel desde lejos |

---

## Soporte

Si algo falla durante el evento, plan de emergencia:

1. Verificar que el dominio responde (abrir desde un celular).
2. Verificar consola Firebase: ¿se están creando documentos?
3. Si Storage está al límite (5 GB free), upgrade momentáneo al plan Blaze.
4. Como último recurso: pedir a invitados que envíen las fotos a un número de WhatsApp/Telegram acordado.
