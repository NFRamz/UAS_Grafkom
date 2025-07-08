import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Shape:

    def __init__(self, tipe_bentuk, warna, ketebalan):
        self.tipe_bentuk = tipe_bentuk
        self.warna = warna
        self.ketebalan = ketebalan
        self.terpilih = False
        self.simpul = []

    def gambar(self, timpa_warna=None, mode_gambar=GL_LINE_LOOP):

        glColor3fv(timpa_warna or self.warna)
        glLineWidth(self.ketebalan)
        glBegin(mode_gambar)


        for simpul_tunggal in self.simpul:
            glVertex2f(simpul_tunggal[0], simpul_tunggal[1])
        glEnd()

    def get_titikPusat(self):

        if not self.simpul: return 0, 0

        # Hitung rata-rata dari semua koordinat x dan y.
        koordinat_x = [s[0] for s in self.simpul]
        koordinat_y = [s[1] for s in self.simpul]

        return sum(koordinat_x) / len(koordinat_x), sum(koordinat_y) / len(koordinat_y)

    def transformasi(self, matriks):

        simpul_baru = []
        for x, y in self.simpul:
            vektor = np.array([x, y, 1])
            vektor_hasil = matriks @ vektor # perkalian matriks.
            simpul_baru.append((vektor_hasil[0], vektor_hasil[1]))# Kembalikan ke koordinat 2D dan simpan.

        self.simpul = simpul_baru

# ============================================ ====================================================
class Titik(Shape):

    def __init__(self, p1, warna, ketebalan):
        super().__init__("titik", warna, ketebalan)
        self.simpul.append(p1)

    def gambar(self, timpa_warna=None):
        glColor3fv(timpa_warna or self.warna)
        glPointSize(self.ketebalan * 2)
        glBegin(GL_POINTS)
        glVertex2f(self.simpul[0][0], self.simpul[0][1])
        glEnd()

class Garis(Shape):

    def __init__(self, p1, p2, warna, ketebalan):
        super().__init__("garis", warna, ketebalan)
        self.simpul.extend([p1, p2])

    def gambar(self, timpa_warna=None):
        # Memanggil metode gambar dari parent class dengan mode GL_LINES.
        super().gambar(timpa_warna, GL_LINES)

class Persegi(Shape):

    def __init__(self, p1, p2, warna, ketebalan):
        super().__init__("persegi", warna, ketebalan)
        min_x, max_x = min(p1[0], p2[0]), max(p1[0], p2[0])
        min_y, max_y = min(p1[1], p2[1]), max(p1[1], p2[1])
        # Buat 4 simpul dari dua titik diagonal.
        self.simpul.extend([(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)])

class Elips(Shape):

    def __init__(self, pusat, radius_x, radius_y, warna, ketebalan):
        super().__init__("elips", warna, ketebalan)
        self.pusat = pusat  # Titik pusat elips.
        self.radius_x = radius_x  # Radius horizontal.
        self.radius_y = radius_y  # Radius vertikal.
        self.sudut = 0.0  # Sudut rotasi dalam derajat.
        self._buat_simpul()

    def _buat_simpul(self):

        self.simpul = []
        jumlah_segmen = 72  # Jumlah segmen yang cukup untuk membuat elips terlihat halus.
        for i in range(jumlah_segmen):
            sudut_segmen = 2 * math.pi * i / jumlah_segmen
            x = self.radius_x * math.cos(sudut_segmen)
            y = self.radius_y * math.sin(sudut_segmen)
            self.simpul.append((x, y))

    def gambar(self, timpa_warna=None):
        """
        Menggambar elips dengan mempertimbangkan translasi dan rotasi menggunakan
        stack matriks OpenGL untuk mengisolasi transformasi.
        """
        glColor3fv(timpa_warna or self.warna)
        glLineWidth(self.ketebalan)

        glPushMatrix()  # 1. Simpan kondisi matriks saat ini agar tidak mempengaruhi objek lain.

        # 2. Pindahkan sistem koordinat ke pusat elips.
        glTranslatef(self.pusat[0], self.pusat[1], 0)
        # 3. Putar sistem koordinat pada sumbu Z.
        glRotatef(self.sudut, 0, 0, 1)

        # 4. Gambar simpul-simpul elips (yang berpusat di 0,0) pada sistem koordinat
        #    yang sudah ditransformasi.
        glBegin(GL_LINE_LOOP)
        for simpul_tunggal in self.simpul:
            glVertex2f(simpul_tunggal[0], simpul_tunggal[1])
        glEnd()

        glPopMatrix()  # 5. Kembalikan matriks ke kondisi semula.

    def get_titikPusat(self):
        return self.pusat

    def dapatkan_simpul_hasil_transformasi(self):
        hasil_transformasi = []
        sudut_rad = math.radians(self.sudut)
        cos_s, sin_s = math.cos(sudut_rad), math.sin(sudut_rad)
        for x_local, y_local in self.simpul:

            rotate_x = x_local * cos_s - y_local * sin_s
            rotate_y = x_local * sin_s + y_local * cos_s

            # meambahkan translasi untuk mendapatkan koordinat global.
            x_global = rotate_x + self.pusat[0]
            y_global = rotate_y + self.pusat[1]
            hasil_transformasi.append((x_global, y_global))
        return hasil_transformasi

    def transformasi(self, matriks):
        """Override metode transformasi khusus untuk Elips."""
        # Terapkan translasi pada pusat elips.
        x_center, y_center = self.pusat
        vektor = np.array([x_center, y_center, 1])
        vektor_hasil = matriks @ vektor
        self.pusat = (vektor_hasil[0], vektor_hasil[1])

        # Cek apakah matriks mengandung rotasi.
        if matriks[0, 0] == matriks[1, 1] and matriks[0, 1] == -matriks[1, 0]:
            # Ekstrak sudut rotasi dari matriks.
            perubahan_sudut_rad = math.atan2(matriks[1, 0], matriks[0, 0])
            self.sudut += math.degrees(perubahan_sudut_rad)

        # Penskalaan dihandle di `terapkan_transformasi` dengan mengubah radius.
        self._buat_simpul()


#==========================================================================================
class Main:
    def __init__(self):
        self.lebar, self.tinggi = 1280, 720
        self.header_primaryWindow = b"Modul_A"

        self.daftar_bentuk, self.titik_sementara, self.bentuk_terpilih = [], [], None
        self.mode_sekarang = 'PILIH'
        self.pilihan_mode = {
            '1': 'GAMBAR_TITIK', 'd': 'GAMBAR_TITIK', '2': 'GAMBAR_GARIS', 'l': 'GAMBAR_GARIS',
            '3': 'GAMBAR_PERSEGI', 'r': 'GAMBAR_PERSEGI', '4': 'GAMBAR_ELIPS', 'e': 'GAMBAR_ELIPS',
            's': 'PILIH', 'w': 'TENTUKAN_JENDELA_AWAL'
        }
        self.daftar_warna=[
            (1, 0, 0),  # Red
            (0, 1, 0),  # Green
            (0, 0, 1),  # Blue
            (1, 1, 0),  # Yellow
            (1, 0.5, 0),  # Orange
            (0, 1, 1),  # Cyan
            (1, 0, 1),  # Magenta
            (0.5, 0, 0.5),  # Purple
            (0.5, 0.25, 0),  # Brown
            (0, 0, 0),  # Black
            (0.5, 0.5, 0.5),  # Gray
            (0.8, 0.8, 0.2),  # Light Yellow
            (0.2, 0.8, 0.8),  # Light Cyan
            (0.8, 0.2, 0.8),  # Light Magenta
            (0.2, 0.2, 0.8),  # Indigo
            (0.8, 0.4, 0.2),  # Light Brown
            (0.4, 0.8, 0.2),  # Olive
            (0.2, 0.8, 0.4),  # Mint
            (0.8, 0.2, 0.4),  # Pink
            (0.4, 0.2, 0.8),  # Violet
            (0.2, 0.4, 0.8),  # Sky Blue
            (0.8, 0.8, 0.8),  # Very Light Gray
            (0.3, 0.3, 0.3),  # Dark Gray
            (0.9, 0.6, 0.7),  # Pastel Pink
            (0.6, 0.9, 0.7),  # Pastel Green
            (0.7, 0.6, 0.9),  # Pastel Purple
            (0.9, 0.9, 0.6),  # Pastel Yellow
            (0.6, 0.9, 0.9),  # Pastel Cyan
            (0.9, 0.6, 0.9),  # Pastel Magenta
        ]
        self.indeks_warna = 2
        self.warna_sekarang = self.daftar_warna[self.indeks_warna]
        self.ketebalan_sekarang = 2.0
        self.window_clipping = None
        self.warna_potong = (0.2, 0.8, 0.2)
        self.drag_window = False
        self.posisi_awal_geser = None
        self.DI_DALAM, self.KIRI, self.KANAN, self.BAWAH, self.ATAS = 0, 1, 2, 4, 8


    def inisialisasi_gl(self):

        glClearColor(1.0, 1.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.lebar, self.tinggi, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def display_infoMenu(self):

        baris_bantuan = [
            "--- MODE --- ",
            f"Mode Saat Ini: {self.mode_sekarang.replace('_', ' ')}",
            " [1] Titik | [2] Garis | [3] Persegi | [4] Elips",
            " [s] Pilih Objek",
            " [w] Tentukan/Reset Jendela Pemotongan",

            " ",

            "--- KONTROL ---",
            f"[c] untuk ganti Warna: {self.warna_sekarang}",
            f"[+/-] untuk ubah Tebal: {self.ketebalan_sekarang:.1f}",
            "[x] Hapus Semua | [ESC] Batal Pilih Mode",

            " ",

            "--- TRANSFORMASI---",
            "*Pencet tombol s dulu",
            " ",
            "Translasi: Panah",
            "Rotasi: []/{}",
            "Skala: PgUp/PgDn"
        ]

        if self.window_clipping:
            baris_bantuan.append("\nJendela Pemotongan Aktif. Klik & seret untuk geser.")
        return baris_bantuan

    def gambar_teks(self, x, y, teks, font=GLUT_BITMAP_9_BY_15):

        glColor3f(0.1, 0.1, 0.1)
        glRasterPos2f(x, y)
        for karakter in teks:
            glutBitmapCharacter(font, ord(karakter))

    def tampilkan(self):

        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        for bentuk in self.daftar_bentuk:
            if self.window_clipping:
                self.gambar_terpotong(bentuk)
            else:
                bentuk.gambar()

            if bentuk.terpilih:
                self.gambar_kotak_seleksi(bentuk)

        if self.window_clipping:
            self.draw_window_clipping()

        offset_y = 20
        for baris in self.display_infoMenu():
            for bagian in baris.split('\n'):
                self.gambar_teks(10, offset_y, bagian)
                offset_y += 17

        glutSwapBuffers()

    def gambar_terpotong(self, bentuk):

        if bentuk.tipe_bentuk == 'titik':
            if self.check_titik_di_dalam_jendela(bentuk.simpul[0]):
                bentuk.gambar(timpa_warna=self.warna_potong)
            return

        if bentuk.tipe_bentuk == 'garis':
            accept, p1, p2 = self.algoritma_cohen_sutherland(bentuk.simpul[0], bentuk.simpul[1])

            if accept:
                Garis(p1, p2, self.warna_potong, bentuk.ketebalan).gambar()
            return

        if bentuk.tipe_bentuk in ['persegi', 'elips']:
            poligon_subjek = bentuk.dapatkan_simpul_hasil_transformasi() if bentuk.tipe_bentuk == 'elips' else bentuk.simpul
            poligon_hasil_potong = self.algoritma_sutherland_hodgman(poligon_subjek)

            if poligon_hasil_potong:
                glBegin(GL_POLYGON)
                glColor4f(self.warna_potong[0], self.warna_potong[1], self.warna_potong[2], 0.3)
                for v in poligon_hasil_potong:
                    glVertex2f(v[0], v[1])
                glEnd()
                bentuk_temporer = Shape('poligon', self.warna_potong, bentuk.ketebalan)
                bentuk_temporer.simpul = poligon_hasil_potong
                bentuk_temporer.gambar()

    def gambar_kotak_seleksi(self, bentuk):

        daftar_simpul = bentuk.dapatkan_simpul_hasil_transformasi() if bentuk.tipe_bentuk == 'elips' else bentuk.simpul

        if not daftar_simpul:
            return

        koordinat_x = [s[0] for s in daftar_simpul]
        koordinat_y = [s[1] for s in daftar_simpul]
        min_x, max_x, min_y, max_y = min(koordinat_x), max(koordinat_x), min(koordinat_y), max(koordinat_y)

        glColor4f(0.3, 0.5, 0.8, 0.5);
        glLineWidth(2.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(min_x - 5, min_y - 5);
        glVertex2f(max_x + 5, min_y - 5)
        glVertex2f(max_x + 5, max_y + 5);
        glVertex2f(min_x - 5, max_y + 5)
        glEnd()

    def draw_window_clipping(self):
        x_min, y_min, x_max, y_max = self.window_clipping
        glColor4f(0.8, 0.2, 0.2, 0.7);
        glLineWidth(3.0)
        glLineStipple(1, 0xAAAA);
        glEnable(GL_LINE_STIPPLE)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x_min, y_min);
        glVertex2f(x_max, y_min)
        glVertex2f(x_max, y_max);
        glVertex2f(x_min, y_max)
        glEnd()
        glDisable(GL_LINE_STIPPLE)

    def ubah_ukuran(self, l, t):
        self.lebar, self.tinggi = l, t
        glViewport(0, 0, l, t)
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity()
        gluOrtho2D(0, l, t, 0)
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity()

    def shortcut_keyboard(self, tombol, x, y):
        teks_tombol = tombol.decode("utf-8").lower()

        if teks_tombol in self.pilihan_mode:
            self.mode_sekarang = self.pilihan_mode[teks_tombol]
            if self.mode_sekarang == 'TENTUKAN_JENDELA_AWAL': self.window_clipping = None
            self.titik_sementara = []

        elif teks_tombol == 'c':
            self.indeks_warna = (self.indeks_warna + 1) % len(self.daftar_warna)
            self.warna_sekarang = self.daftar_warna[self.indeks_warna]
            if self.bentuk_terpilih: self.bentuk_terpilih.warna = self.warna_sekarang

        elif tombol == b'+' or tombol == b'=':
            self.ketebalan_sekarang = min(20.0, self.ketebalan_sekarang + 0.5)
            if self.bentuk_terpilih: self.bentuk_terpilih.ketebalan = self.ketebalan_sekarang

        elif tombol == b'-' or tombol == b'_':
            self.ketebalan_sekarang = max(1.0, self.ketebalan_sekarang - 0.5)
            if self.bentuk_terpilih: self.bentuk_terpilih.ketebalan = self.ketebalan_sekarang

        elif teks_tombol == 'x':
            self.daftar_bentuk.clear();
            self.bentuk_terpilih = None;
            self.window_clipping = None

        elif ord(tombol) == 27:
            if self.bentuk_terpilih: self.bentuk_terpilih.terpilih = False; self.bentuk_terpilih = None
            self.titik_sementara = []

            if 'GAMBAR' in self.mode_sekarang or 'TENTUKAN' in self.mode_sekarang: self.mode_sekarang = 'PILIH'

        if self.bentuk_terpilih:
            if tombol == b'[' or tombol == b'{':
                self.terapkan_transformasi(self.bentuk_terpilih, 'rotasi', -5)

            elif tombol == b']' or tombol == b'}':
                self.terapkan_transformasi(self.bentuk_terpilih, 'rotasi', 5)

        glutPostRedisplay()

    def shortcut_keyboard2(self, tombol, x, y):
        if self.bentuk_terpilih:
            if tombol == GLUT_KEY_UP:
                self.terapkan_transformasi(self.bentuk_terpilih, 'translasi', (0, -5))

            elif tombol == GLUT_KEY_DOWN:
                self.terapkan_transformasi(self.bentuk_terpilih, 'translasi', (0, 5))

            elif tombol == GLUT_KEY_LEFT:
                self.terapkan_transformasi(self.bentuk_terpilih, 'translasi', (-5, 0))

            elif tombol == GLUT_KEY_RIGHT:
                self.terapkan_transformasi(self.bentuk_terpilih, 'translasi', (5, 0))

            elif tombol == GLUT_KEY_PAGE_UP:
                self.terapkan_transformasi(self.bentuk_terpilih, 'skala', 1.05)

            elif tombol == GLUT_KEY_PAGE_DOWN:
                self.terapkan_transformasi(self.bentuk_terpilih, 'skala', 0.95)

        glutPostRedisplay()

    def mouse(self, tombol, status, x, y):

        if tombol == GLUT_LEFT_BUTTON:
            if status == GLUT_DOWN:
                if self.window_clipping and self.check_titik_di_dalam_jendela((x, y)):
                    self.drag_window = True;
                    self.posisi_awal_geser = (x, y);
                    glutPostRedisplay();
                    return

                if self.mode_sekarang == 'PILIH':
                    if self.bentuk_terpilih: self.bentuk_terpilih.terpilih = False
                    self.bentuk_terpilih = None

                    for bentuk in reversed(self.daftar_bentuk):
                        simpul = bentuk.dapatkan_simpul_hasil_transformasi() if bentuk.tipe_bentuk == 'elips' else bentuk.simpul
                        koordinat_x = [s[0] for s in simpul];
                        koordinat_y = [s[1] for s in simpul]

                        if not (min(koordinat_x) < x < max(koordinat_x) and min(koordinat_y) < y < max(
                            koordinat_y)): continue
                        self.bentuk_terpilih = bentuk;
                        bentuk.terpilih = True;
                        break

                elif self.mode_sekarang == 'GAMBAR_TITIK':
                    self.daftar_bentuk.append(Titik((x, y), self.warna_sekarang, self.ketebalan_sekarang))

                elif 'GAMBAR' in self.mode_sekarang:
                    self.titik_sementara.append((x, y))

                    if len(self.titik_sementara) == 2:
                        p1, p2 = self.titik_sementara[0], self.titik_sementara[1]

                        if self.mode_sekarang == 'GAMBAR_GARIS':
                            self.daftar_bentuk.append(Garis(p1, p2, self.warna_sekarang, self.ketebalan_sekarang))

                        elif self.mode_sekarang == 'GAMBAR_PERSEGI':
                            self.daftar_bentuk.append(Persegi(p1, p2, self.warna_sekarang, self.ketebalan_sekarang))

                        elif self.mode_sekarang == 'GAMBAR_ELIPS':
                            rx = abs(p2[0] - p1[0]);
                            ry = abs(p2[1] - p1[1])
                            self.daftar_bentuk.append(Elips(p1, rx, ry, self.warna_sekarang, self.ketebalan_sekarang))
                        self.titik_sementara = []

                elif self.mode_sekarang == 'TENTUKAN_JENDELA_AWAL':
                    self.titik_sementara.append((x, y)); self.mode_sekarang = 'TENTUKAN_JENDELA_AKHIR'

                elif self.mode_sekarang == 'TENTUKAN_JENDELA_AKHIR':
                    self.titik_sementara.append((x, y));
                    p1, p2 = self.titik_sementara
                    self.window_clipping = (
                    min(p1[0], p2[0]), min(p1[1], p2[1]), max(p1[0], p2[0]), max(p1[1], p2[1]))
                    self.titik_sementara = [];
                    self.mode_sekarang = 'PILIH'

            elif status == GLUT_UP:
                if self.drag_window: self.drag_window = False; self.posisi_awal_geser = None

        glutPostRedisplay()

    def geser_mouse(self, x, y):

        if self.drag_window and self.window_clipping:
            dx, dy = x - self.posisi_awal_geser[0], y - self.posisi_awal_geser[1]
            x_min, y_min, x_max, y_max = self.window_clipping
            self.window_clipping = (x_min + dx, y_min + dy, x_max + dx, y_max + dy)
            self.posisi_awal_geser = (x, y)

            glutPostRedisplay()

    def terapkan_transformasi(self, bentuk, tipe_transformasi, nilai):
        pusat_x, pusat_y = bentuk.get_titikPusat()

        ke_asal = np.array([[1, 0, -pusat_x], [0, 1, -pusat_y], [0, 0, 1]])
        dari_asal = np.array([[1, 0, pusat_x], [0, 1, pusat_y], [0, 0, 1]])

        matriks_total = np.identity(3)

        if tipe_transformasi == 'translasi':
            dx, dy = nilai
            matriks_total = np.array([[1, 0, dx], [0, 1, dy], [0, 0, 1]])

        elif tipe_transformasi == 'rotasi':
            sudut = np.deg2rad(nilai)
            cos_s, sin_s = np.cos(sudut), np.sin(sudut)
            rotasi = np.array([[cos_s, -sin_s, 0], [sin_s, cos_s, 0], [0, 0, 1]])

            matriks_total = dari_asal @ rotasi @ ke_asal

        elif tipe_transformasi == 'skala':
            skala_x = skala_y = nilai

            penskalaan = np.array([[skala_x, 0, 0], [0, skala_y, 0], [0, 0, 1]])
            matriks_total = dari_asal @ penskalaan @ ke_asal

            if bentuk.tipe_bentuk == 'elips':
                bentuk.radius_x *= skala_x;
                bentuk.radius_y *= skala_y

        bentuk.transformasi(matriks_total)

    def hitung_outCode(self, p):
        x, y = p
        x_min, y_min, x_max, y_max = self.window_clipping
        regionCode = self.DI_DALAM

        if x < x_min:
            regionCode |= self.KIRI

        elif x > x_max:
            regionCode |= self.KANAN

        if y < y_min:
            regionCode |= self.BAWAH

        elif y > y_max:
            regionCode |= self.ATAS

        return regionCode

    def check_titik_di_dalam_jendela(self, titik):
        if not self.window_clipping:
            return True

        x_min, y_min, x_max, y_max = self.window_clipping
        return x_min <= titik[0] <= x_max and y_min <= titik[1] <= y_max

    def algoritma_cohen_sutherland(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        outCode1, outCode2 = self.hitung_outCode(p1), self.hitung_outCode(p2)
        x_min, y_min, x_max, y_max = self.window_clipping

        while True:

            if outCode1 == 0 and outCode2 == 0:
                return True, (x1, y1), (x2, y2)

            if (outCode1 & outCode2) != 0:
                return False, None, None

            #outCode_pilihan=outCode1 if outCode1 else outCode2
            if outCode1:
                outCode_pilihan=outCode1
            else:
                outCode_pilihan=outCode2

            if outCode_pilihan & self.ATAS:
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1);
                y = y_max

            elif outCode_pilihan & self.BAWAH:
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1);
                y = y_min

            elif outCode_pilihan & self.KANAN:
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1);
                x = x_max

            elif outCode_pilihan & self.KIRI:
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1);
                x = x_min

            if outCode_pilihan == outCode1:
                x1, y1 = x, y;
                outCode1 = self.hitung_outCode((x1, y1))

            else:
                x2, y2 = x, y;
                outCode2 = self.hitung_outCode((x2, y2))

    def algoritma_sutherland_hodgman(self, poligon_subjek):
        list_titikHasil = poligon_subjek

        for batasJendela in range(4):
            list_titikInput = list_titikHasil
            list_titikHasil = []

            if not list_titikInput: return []

            titik_awal = list_titikInput[-1]

            for i in list_titikInput:
                titikAwal_diDalam = self._apakah_diDalam_batas(titik_awal, batasJendela)
                titikAkhir_diDalam = self._apakah_diDalam_batas(i, batasJendela)

                if titikAkhir_diDalam:
                    if not titikAwal_diDalam:
                        list_titikHasil.append(self._cari_perpotonganBatas(titik_awal, i, batasJendela))
                    list_titikHasil.append(i)
                elif titikAwal_diDalam:
                    list_titikHasil.append(self._cari_perpotonganBatas(titik_awal, i, batasJendela))
                titik_awal = i

        return list_titikHasil

    def _apakah_diDalam_batas(self, p, sisi):
        """Helper untuk Sutherland-Hodgman: ."""
        x_min, y_min, x_max, y_max = self.window_clipping
        if sisi == 0:
            return p[0] >= x_min

        if sisi == 1:
            return p[0] <= x_max

        if sisi == 2:
            return p[1] >= y_min

        if sisi == 3:
            return p[1] <= y_max

        return False

    def _cari_perpotonganBatas(self, p1, p2, sisi):
        """untuk Sutherland-Hodgman: cari titik potong."""
        x_min, y_min, x_max, y_max = self.window_clipping
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]

        if sisi == 0:  # KIRI
            return (x_min, p1[1] + dy * (x_min - p1[0]) / dx if dx != 0 else p1[1])

        if sisi == 1:  # KANAN
            return (x_max, p1[1] + dy * (x_max - p1[0]) / dx if dx != 0 else p1[1])

        if sisi == 2:  # BAWAH
            return (p1[0] + dx * (y_min - p1[1]) / dy if dy != 0 else p1[0], y_min)

        if sisi == 3:  # ATAS
            return (p1[0] + dx * (y_max - p1[1]) / dy if dy != 0 else p1[0], y_max)

        return None

    def run(self):

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
        glutInitWindowSize(self.lebar, self.tinggi)
        glutInitWindowPosition(100, 100)
        glutCreateWindow(self.header_primaryWindow)
        self.inisialisasi_gl()

        glutDisplayFunc(self.tampilkan)
        glutReshapeFunc(self.ubah_ukuran)
        glutKeyboardFunc(self.shortcut_keyboard)
        glutSpecialFunc(self.shortcut_keyboard2)
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.geser_mouse)

        glutMainLoop()


if __name__ == "__main__":
    app = Main()
    app.run()
