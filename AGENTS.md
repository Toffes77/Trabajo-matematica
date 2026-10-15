# AGENTS.md — cómo trabajar en esta presentación

Guía para asistentes de IA (Claude, Codex, Copilot, Cursor, etc.) y para personas que
modifiquen el proyecto. Leela entera antes de tocar `presentacion.py`.

## El flujo de trabajo

1. El autor dibuja un boceto de la slide y lo guarda en `IMAGENES_REFERENCIA/SLIDE<n>.png`,
   y describe en el chat qué se anima. **Mirá siempre la imagen de referencia** antes de programar.
   Ojo: a veces el número del archivo no coincide con el orden real; si algo no cierra, preguntá.
2. Se agrega el código al final de `BanachTarski.construct()` (justo antes de `def loop_discusion`),
   continuando desde el estado en que quedó la slide anterior.
3. Se renderiza en **480p** (`-ql`) y se **verifican cuadros** del video (ver abajo).
4. La versión **1080p60** (`-qh`) se genera **solo cuando el autor la pide** (tarda mucho).
   Nunca usar 720p (`-qm`).

## Comandos

```bash
# Antes de renderizar en una terminal nueva, MiKTeX tiene que estar en el PATH:
#   $env:PATH = "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64;$env:PATH"
.\.venv\Scripts\manim.exe -ql presentacion.py BanachTarski   # prueba
.\.venv\Scripts\manim.exe -qh presentacion.py BanachTarski   # final (solo si lo piden)
.\.venv\Scripts\manim-slides.exe BanachTarski                # presentar
```

Verificar cuadros (no confíes en que "renderizó sin error"; mirá el resultado):
```bash
# último cuadro
ffmpeg -v error -y -sseof -0.1 -i media/videos/presentacion/480p60/BanachTarski.mp4 -update 1 fin.png
# hoja de contacto de los últimos 20 s
ffmpeg -v error -y -ss <duracion-20> -i <video> -vf "fps=1/2,scale=480:-1,tile=3x4" -frames:v 1 hoja.png
```
Calculá los tiempos sumando los `run_time` desde el final del video.

## Estilo (no negociable)

- **Fondo negro**, **60 FPS** (`config.frame_rate = 60` arriba del archivo).
- **Fuente**: `FUENTE = "CMU Serif"` (Computer Modern, estilo 3Blue1Brown), **sin negrita**.
  Fórmulas con `MathTex`/`Tex` (LaTeX, misma familia tipográfica).
- **Sin ángulos vivos** en monigotes, globos, cajas, puertas: usar `round_corners`, `RoundedRectangle`,
  `LineJointType.ROUND`, `CapStyleType.ROUND` (evita la "costura" donde cierra el trazo).
- Colores: verde de las esferas `VERDE*` (helper `esfera()`), vector amarillo `YELLOW`,
  verde 3b1b `#83C167`, rojo `#FC6255`, celeste del punto de inicio `#9CDCEB`.
- Textos en **castellano correcto** (tildes, "Banach", "Hilbert", "traslación", "a través").
  Si el boceto tiene un error de ortografía o de nombre, corregilo y avisá al autor.
- Cuando el boceto contradice la matemática (p. ej. un ángulo), hacé lo correcto y avisá.

## Helpers que ya existen (reutilizalos)

| Helper | Para qué |
|---|---|
| `esfera(radio, capas)` | Esfera verde sombreada (círculos concéntricos). Más `capas` = degradé más suave (útil al hacer zoom). |
| `fragmento(...)` | Trozo roto de esfera (Intersection con las capas de la esfera). |
| `persona()`, `persona_con_cara(nombre, escala)`, `persona_feliz(escala)`, `botones_mob()` | Monigotes. `p[0]` es la cabeza y `p[1]` el cuerpo en todos. |
| `cara(nombre, alto)` | Foto de `caras/<nombre>.png` recortada a su contorno. |
| `globo_dialogo(centro, a, b, colas)` | Globo de historieta como **una sola curva suave** (no usar `Union`, deja líneas). |
| `nube(...)` | Nube de pensamiento sin picos. |
| `saltar`, `saltar_a`, `entrar` | Caminar a los saltitos / entrar por una puerta. |
| `habitacion`, `mover_puerta` | Puertas del hotel; `mover_puerta` abre/cierra girando sobre la bisagra izquierda. |
| `simbolo_enojo`, `corazon_mob`, `reloj_mob` | Íconos. |
| `pos_zoom(m, p, zoom, destino)` | Para hacer "zoom" moviendo/escalando objetos alrededor de un punto. |
| `proj(p)` / `proyectar(...)` | Cámara 3D hecha a mano (trackers `a_t`, `b_t`, `ox`, `oy`, `s_t`). Con a=b=0 es 2D. |
| `Modelo3D` (`render3d.py`) | Render GPU de un `.obj`; devuelve una imagen RGBA. |

## Trampas conocidas (ya nos pasaron)

- **`Union` de Manim no fusiona bien los contornos** con trazo: se ven líneas cruzadas. Construir el contorno a mano.
- **Imágenes que cambian cada cuadro**: actualizar *la misma* `ImageMobject` (`m.pixel_array = ...`).
  Reemplazar submobjects en un updater deja "fantasmas" congelados de cuadros anteriores.
- **Escalar con `.animate.scale` escala las puntas de flecha**: para zoom de diagramas con flechas,
  redibujar con `always_redraw` y una cámara (trackers de zoom/centro) en vez de escalar.
- `play(run_time=..., rate_func=...)` pisa el ritmo de todas las animaciones; para ritmos distintos
  dentro del mismo `play`, usar `mob.animate(rate_func=...)` y **no** pasar `rate_func` al `play`.
- Antes de escalar/rotar objetos con `always_redraw`, hacer `clear_updaters()`.
- `Group` (no `VGroup`) cuando hay `ImageMobject` adentro.
- Loops de manim-slides (`self.next_slide(loop=True)`): la animación tiene que **terminar exactamente
  igual que empieza** (usar funciones periódicas con frecuencias enteras).
- Los "zoom hasta negro" apuntan a una **zona negra** de la pantalla, así no queda una figura tapando todo.
- Personas en movimiento: ubicarlas por el **cuerpo** (`p[1]`), porque las fotos cambian la caja del grupo.

## Git

- No subir `.venv/`, `media/` ni `slides/` (están en `.gitignore`; se regeneran).
- Mensajes de commit en castellano, cortos y descriptivos ("Agrega slides 35–38: palabras de movimientos").
