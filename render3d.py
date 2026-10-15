"""Render de un modelo .obj con la GPU (moderngl, offscreen) para usarlo dentro de Manim.

Proyección ortográfica: el punto m (coordenadas del modelo, centrado y normalizado a tamaño ~1)
se ve en pantalla en (R @ m)[:2]. R ya incluye la rotación de la cámara y la del objeto.
Devuelve una imagen RGBA cuadrada que cubre [-medio, medio] x [-medio, medio] en esas coordenadas.
"""

import numpy as np
import moderngl

VERT = """
#version 330
uniform mat3 R;
uniform float medio;
uniform float zmax;
in vec3 pos;
in vec3 normal;
in vec3 color;
out vec3 v_normal;
out vec3 v_color;
void main() {
    vec3 p = R * pos;
    v_normal = R * normal;
    v_color = color;
    // x, y a [-1, 1]; z hacia el espectador (más z = más cerca)
    gl_Position = vec4(p.x / medio, p.y / medio, -p.z / zmax, 1.0);
}
"""

FRAG = """
#version 330
uniform vec3 luz;
in vec3 v_normal;
in vec3 v_color;
out vec4 f_color;
void main() {
    vec3 n = normalize(v_normal);
    if (!gl_FrontFacing) n = -n;
    float difusa = max(dot(n, luz), 0.0);
    vec3 h = normalize(luz + vec3(0.0, 0.0, 1.0));
    float brillo = pow(max(dot(n, h), 0.0), 40.0) * 0.25;
    vec3 c = v_color * (0.38 + 0.62 * difusa) + brillo;
    f_color = vec4(c, 1.0);
}
"""


def cargar_obj(ruta):
    """Lee vértices, caras (n-gonos) y el material de cada cara."""
    V, F, M = [], [], []
    mat = None
    with open(ruta) as f:
        for linea in f:
            if linea.startswith("v "):
                V.append([float(x) for x in linea.split()[1:4]])
            elif linea.startswith("usemtl"):
                mat = linea.split()[1]
            elif linea.startswith("f "):
                F.append([int(t.split("/")[0]) - 1 for t in linea.split()[1:]])
                M.append(mat)
    return np.array(V, dtype="f4"), F, M


class Modelo3D:
    def __init__(self, ruta, colores, resolucion=640, muestras=4):
        """colores: dict material -> (r, g, b) en 0..1."""
        V, F, M = cargar_obj(ruta)
        # Centrar y normalizar: la arista más larga de la caja pasa a medir 1
        lo, hi = V.min(0), V.max(0)
        V = (V - (lo + hi) / 2) / (hi - lo).max()

        # Triangular y duplicar vértices para sombreado plano (normal por cara)
        pos, nor, col = [], [], []
        for cara, mat in zip(F, M):
            c = colores.get(mat, (0.8, 0.8, 0.8))
            for k in range(1, len(cara) - 1):
                tri = V[[cara[0], cara[k], cara[k + 1]]]
                n = np.cross(tri[1] - tri[0], tri[2] - tri[0])
                largo = np.linalg.norm(n)
                if largo < 1e-12:
                    continue
                n = n / largo
                pos.extend(tri)
                nor.extend([n, n, n])
                col.extend([c, c, c])
        datos = np.hstack([np.array(pos), np.array(nor), np.array(col)]).astype("f4")

        self.ctx = moderngl.create_standalone_context()
        self.prog = self.ctx.program(vertex_shader=VERT, fragment_shader=FRAG)
        vbo = self.ctx.buffer(datos.tobytes())
        self.vao = self.ctx.vertex_array(self.prog, [(vbo, "3f 3f 3f", "pos", "normal", "color")])
        self.res = resolucion
        self.fbo_ms = self.ctx.framebuffer(
            color_attachments=[self.ctx.renderbuffer((resolucion, resolucion), 4, samples=muestras)],
            depth_attachment=self.ctx.depth_renderbuffer((resolucion, resolucion), samples=muestras),
        )
        self.fbo = self.ctx.framebuffer(color_attachments=[self.ctx.renderbuffer((resolucion, resolucion), 4)])
        self.prog["luz"].value = tuple(np.array([-0.45, 0.6, 0.66]) / np.linalg.norm([-0.45, 0.6, 0.66]))

    def render(self, R, medio=0.9):
        """Imagen RGBA (uint8, res x res) del modelo visto con la matriz R (3x3)."""
        self.fbo_ms.use()
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.clear(0.0, 0.0, 0.0, 0.0)
        self.prog["R"].write(np.asarray(R, dtype="f4").T.copy().tobytes())  # GLSL es column-major
        self.prog["medio"].value = float(medio)
        self.prog["zmax"].value = 2.0
        self.vao.render(moderngl.TRIANGLES)
        self.ctx.copy_framebuffer(self.fbo, self.fbo_ms)
        img = np.frombuffer(self.fbo.read(components=4), dtype=np.uint8).reshape(self.res, self.res, 4)
        return np.flipud(img).copy()  # OpenGL tiene el origen abajo a la izquierda
