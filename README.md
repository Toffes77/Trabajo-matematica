# La paradoja de Banach–Tarski — presentación animada

Presentación de matemática hecha con [Manim Community](https://www.manim.community/) y
[manim-slides](https://github.com/jeertmans/manim-slides), al estilo de 3Blue1Brown
(fondo negro, fuente Computer Modern, 1080p a 60 FPS).

**Autores:** Maletti, De Lauro y Moyano.

Toda la presentación es **una sola escena** (`BanachTarski` en `presentacion.py`). Cada
`self.next_slide()` marca un "paso": al presentar se avanza con → y se retrocede con ←.
Algunos pasos son *loops* (se repiten solos hasta que apretás →).

---

## Contenido

| Bloque | Qué pasa |
|---|---|
| Portada | Título "BANACH-TARSKI" y autores |
| La paradoja | Una esfera → fragmentos → dos esferas iguales |
| La discusión (slides 3–7) | Monigotes que se insultan, zoom a "AXIOMA DE ELECCIÓN...", "No tiene sentido", "BANACH-TARSKI" |
| Conjuntos (8–9) | Cajas con elementos (incluye fotos de `caras/`), se elige uno de cada caja |
| Hotel de Hilbert (9.5–17) | Hotel, puertas, huéspedes que se mudan, fila infinita, regla N = 2n |
| Traslaciones (18–25) | Vector que se traslada en 2D y 3D; "la traslación se anota a través de un vector" |
| Rotaciones | Bloque "?" en 3D (modelo en `modelo3d/`) que rota en 2D y en 3D; matriz de rotación |
| El teorema (26) | Enunciado formal; a un monigote le explota la cabeza |
| Esfera de puntos (27–31) | Se le sacan capas hasta que queda un punto: "Por acá" |
| Movimientos (32–38) | Brújula N/S/E/W, arccos(1/3) ≈ 70,53°, el desfase, palabras de movimientos, la esfera estalla |

Las imágenes de `IMAGENES_REFERENCIA/` son los bocetos originales de cada slide.

---

## Instalación (Windows)

1. **Python 3.12** y **FFmpeg** en el PATH.
2. **LaTeX**: [MiKTeX](https://miktex.org/) (se usa para fórmulas `MathTex`/`Tex`).
   Activar la instalación automática de paquetes:
   ```bash
   initexmf --set-config-value="[MPM]AutoInstall=1"
   ```
3. Entorno virtual y dependencias:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
4. **Placa de video**: las slides de rotaciones renderizan el modelo 3D con OpenGL (`moderngl`).
   Para *presentar* no hace falta (se usa el video ya generado), pero sí para *generar* el video.

Las fuentes **CMU Serif** (Computer Modern, la de 3Blue1Brown) vienen en `fuentes/` y se
cargan solas desde el código; no hace falta instalarlas.

---

## Generar y presentar

Prueba rápida (480p):
```bash
.\.venv\Scripts\manim.exe -ql presentacion.py BanachTarski
```

Versión final (1080p, 60 FPS):
```bash
.\.venv\Scripts\manim.exe -qh presentacion.py BanachTarski
```

Presentar (→ avanza, ← retrocede, F pantalla completa):
```bash
.\.venv\Scripts\manim-slides.exe BanachTarski
```

El video completo queda en `media/videos/presentacion/<calidad>/BanachTarski.mp4` y los
pasos de la presentación en `slides/` (ambas carpetas están en `.gitignore`).

---

## Estructura

```
presentacion.py        Toda la presentación (helpers arriba, la escena BanachTarski abajo)
render3d.py            Render GPU (moderngl) de un .obj para usarlo como imagen en Manim
caras/                 Fotos de caras con fondo transparente (PNG RGBA)
fuentes/               CMU Serif (.otf), cargadas con manimpango
modelo3d/Cube_obj.obj  Bloque "?" usado en Rotaciones
IMAGENES_REFERENCIA/   Bocetos de cada slide
prueba*.py             Escenas de prueba de la instalación (no forman parte de la presentación)
AGENTS.md              Cómo trabajar en este proyecto (para personas y asistentes de IA)
```

Si vas a modificar la presentación (o a pedírselo a una IA), leé **[AGENTS.md](AGENTS.md)**.
