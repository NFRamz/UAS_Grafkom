import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

titik_sudut = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

sisi = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

normals = (
    (0, 0, -1),     # Belakang
    (-1, 0, 0),     # Kiri
    (0, 0, 1),      # Depan
    (1, 0, 0),      # Kanan
    (0, 1, 0),      # Atas
    (0, -1, 0)  # Bawah
)


def draw_cube():
    """Menggambar kubus berdasarkan vertices, surfaces, dan normals."""
    glBegin(GL_QUADS)
    for i, surface in enumerate(sisi):
        glNormal3fv(normals[i])  # Terapkan normal untuk sisi saat ini
        for vertex_index in surface:
            glVertex3fv(titik_sudut[vertex_index])
    glEnd()


def setup_lighting():
    """
    3. Shading & Pencahayaan
    """
    glEnable(GL_LIGHTING)  # Mengaktifkan perhitungan pencahayaan
    glEnable(GL_LIGHT0)  # Mengaktifkan sumber cahaya 0
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    # jenis-jenis cahaya
    ambient_light = [0.2, 0.2, 0.2, 1.0]
    diffuse_light = [0.8, 0.8, 0.8, 1.0]
    specular_light = [1.0, 1.0, 1.0, 1.0]
    light_position = [5.0, 5.0, 5.0, 1.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    material_specular = [1.0, 1.0, 1.0, 1.0]
    material_shininess = [128.0]
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, material_shininess)

    # OpenGL fixed-function pipeline secara default menggunakan Gouraud shading
    # untuk mengaplikasikan model pencahayaan Phong per-vertex.
    glShadeModel(GL_SMOOTH)


def main():
    pygame.init()
    display = (1024, 768)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Modul B: Objek 3D  Kubus")

    glEnable(GL_DEPTH_TEST)  # Memastikan objek yang lebih dekat menutupi objek yang lebih jauh
    setup_lighting()

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    # Variabel untuk transformasi
    translate_x, translate_y, translate_z = 0.0, 0.0, -10.0
    rotate_x, rotate_y = 0, 0

    # Variabel untuk rotasi dengan mouse drag
    mouse_down = False
    last_mouse_pos = (0, 0)

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # --- 2. Transformasi Objek 3D ---
            # Translasi dengan Keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    translate_x -= 0.5
                if event.key == pygame.K_RIGHT:
                    translate_x += 0.5
                if event.key == pygame.K_UP:
                    translate_y += 0.5
                if event.key == pygame.K_DOWN:
                    translate_y -= 0.5
                if event.key == pygame.K_w:  # Maju
                    translate_z += 0.5
                if event.key == pygame.K_s:  # Mundur
                    translate_z -= 0.5

            # Rotasi Mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Tombol kiri mouse ditekan
                    mouse_down = True
                    last_mouse_pos = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Tombol kiri mouse dilepas
                    mouse_down = False

            if event.type == pygame.MOUSEMOTION:
                if mouse_down:
                    dx, dy = event.pos[0] - last_mouse_pos[0], event.pos[1] - last_mouse_pos[1]
                    rotate_y += dx * 0.4
                    rotate_x += dy * 0.4
                    last_mouse_pos = event.pos

        # Membersihkan buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()  # Mereset matriks transformasi ke posisi awal setiap frame

        # --- 4. Kamera dan Perspektif ---
        glTranslatef(translate_x, translate_y, translate_z)
        glRotatef(rotate_x, 1, 0, 0)
        glRotatef(rotate_y, 0, 1, 0)

        glColor3f(0.8, 0.4, 0.2)  #warna kubus
        draw_cube()

        # Update display
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()