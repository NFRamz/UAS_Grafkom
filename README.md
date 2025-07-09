### <h1 align="center"> Hello Welcome to my Github<img src="https://media.giphy.com/media/hvRJCLFzcasrR4ia7z/giphy.gif" width="40"></h1>
<p align="center">
•●•
<p align="center">
  <a href="https://github.com/NFRamz"><img src="https://readme-typing-svg.herokuapp.com?lines=Naufal+Ramzi+;NIM+202310370311026;Grafika+Komputer+4H+- Informatika;&center=true&width=500&height=50"></a>
</p>
<br>

# 🎨 Modul A

Aplikasi ini adalah visualisasi objek 2D menggunakan Python dan OpenGL, mendukung pemodelan titik, garis, persegi, dan elips, lengkap dengan transformasi serta algoritma pemotongan (clipping) Cohen-Sutherland dan Sutherland-Hodgman.

---

## 🕹️ Controls

| Kategori         | Tombol | Fungsi                                                                 |
|------------------|------|------------------------------------------------------------------------|
| **Mode Gambar**  | `1`  | Gambar Titik                                                           |
|                  | `2`  | Gambar Garis                                                           |
|                  | `3`  | Gambar Persegi                                                         |
|                  | `4`  | Gambar Elips                                                           |
| **Mode Pilih**   | `s`  | Pilih objek                                                            |
| **Clipping**     | `w`  | Tentukan jendela pemotongan (klik dua titik)                           |
|                  | (klik & seret) | Geser jendela pemotongan                                               |
| **Warna & Ukuran**| `c`  | Ganti warna objek                                                      |
|                  | `+` / `=` | Perbesar ketebalan                                                     |
|                  | `-` / `_` | Perkecil ketebalan                                                     |
| **Transformasi** | Panah (↑ ↓ ← →) | Translasi objek terpilih                                               |
|                  | `[` / `{` | Rotasi kiri (−5°)                                                      |
|                  | `]` / `}` | Rotasi kanan (+5°)                                                     |
|                  | `Page Up` / `Page Down` | Perbesar / Perkecil skala                                              |
| **Lainnya**      | `x`  | Hapus semua objek                                                      |
|                  | `Esc` | Batalkan mode, reset seleksi                                           |

---

## 🧠 Algoritma Clipping

### ✂️ Cohen-Sutherland (untuk Garis)
- Menggunakan region code (bitwise) untuk mengevaluasi posisi titik terhadap window.
- Efisien untuk 1 garis lurus.

### ✂️ Sutherland-Hodgman (untuk Poligon)
- Memotong poligon terhadap tiap sisi window satu per satu.
- Menghasilkan poligon baru dari hasil potongan.

---

<br>
<br>
<br>

# 🧊 Modul B – Visualisasi Objek 3D Kubus

Aplikasi ini adalah visualisasi interaktif objek 3D berupa **kubus**, dibuat dengan Python menggunakan **PyOpenGL** dan **Pygame**. Program ini mendukung **transformasi 3D** (translasi dan rotasi) serta simulasi pencahayaan menggunakan **shading dan lighting model** realistis (ambient, diffuse, specular).

---

## 🕹️ Controls

| Kategori                       | Tombol / Aksi                             | Fungsi                                   |
|--------------------------------|-------------------------------------------|-------------------------------------------|
| **Translasi (Gerak)**          | ← (kiri)/ (kanan)→ / (atas) ↑ / (bawah) ↓ | Geser kubus ke kiri / kanan / atas / bawah |
|                                | `W` / `S`                                 | Geser kubus ke depan / belakang (zoom)   |
| **Rotasi (Menggunakan Mouse)** | Klik kiri + drag                          | Rotasi kubus secara interaktif            |
| **Keluar**                     | Klik tombol close (X)                     | Menutup aplikasi                         |

---

## 💡 Fitur Utama

- 🎲 Visualisasi **kubus 3D** yang dapat diputar dan digeser.
- 💡 Efek pencahayaan Phong: **Ambient**, **Diffuse**, dan **Specular**.
- 🌓 **Shading model Gouraud (GL_SMOOTH)** untuk pencahayaan per-vertex.
- 🖱️ **Kontrol rotasi dengan mouse drag**, sangat responsif.
- 🎮 **Kontrol keyboard** untuk translasi (gerak bebas dalam ruang 3D).

---
