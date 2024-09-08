#!/usr/bin/python3
"""add.py"""

from sys import argv  # Mengimpor modul sys untuk menangani argumen dari baris perintah
from sys import exit as sys_exit  # Mengimpor fungsi exit dan mengganti nama menjadi sys_exit
import datetime  # Mengimpor modul datetime untuk menangani waktu dan tanggal
import sqlite3  # Mengimpor modul sqlite3 untuk menangani database SQLite
import pathlib  # Mengimpor modul pathlib untuk memanipulasi jalur file

# Mengambil path saat ini di mana skrip dijalankan
PATH = pathlib.Path.cwd()

# Teks bantuan yang akan ditampilkan jika pengguna meminta bantuan
HELP_TEXT = """
Penggunaan: add.py [-h] directory

-h, --help          tampilkan pesan bantuan ini
directory           direktori dengan sertifikat yang akan ditambahkan
"""

# Fungsi untuk menambahkan sertifikat baru ke database
def add_certs(cert_dir: str) -> None:
    """Menambahkan sertifikat baru ke database. Inisialisasi database jika belum ada."""

    # Jika database belum ada, inisialisasi database baru
    d_b = cert_dir + ".db"
    if (PATH / d_b).is_file() is False:
        con = sqlite3.connect(d_b)  # Membuat atau menghubungkan ke database
        cursor_obj = con.cursor()  # Membuat cursor untuk menjalankan perintah SQL
        # Membuat tabel 'certs' dengan berbagai kolom untuk menyimpan informasi sertifikat
        cursor_obj.execute('CREATE TABLE certs(id text PRIMARY KEY, '
                           'date_added text, applied integer, '
                           'date_applied text, banned integer, '
                           'banned_date text, required_activation integer, '
                           'currently_used integer)')

    # Membuka koneksi ke database yang ada atau baru
    con = sqlite3.connect(d_b)
    cursor_obj = con.cursor()
    added_certs = []  # Menyimpan sertifikat yang berhasil ditambahkan
    skipped_certs = []  # Menyimpan sertifikat yang dilewati (sudah ada di database)
    add_path = PATH / cert_dir  # Mengatur path direktori sertifikat

    # Iterasi setiap file dalam direktori yang diberikan
    for cert_file in add_path.iterdir():

        # Memeriksa apakah file di direktori benar-benar file sertifikat (ekstensi .txt)
        if (cert_file.is_file()
                and cert_file.suffix == ".txt"):  # TODO: Temukan tanda tangan file
            cert_name = cert_file.name  # Mengambil nama file sertifikat
            added = datetime.datetime.now()  # Menyimpan waktu saat sertifikat ditambahkan
            entities = (cert_name, added, 0, 0, 0, 0)  # Mengatur nilai untuk ditambahkan ke database

            # Mencoba menambahkan sertifikat yang unik ke dalam database
            try:
                cursor_obj.execute(
                    'INSERT INTO certs(id, date_added, '
                    'applied, banned, required_activation, currently_used) '
                    'VALUES(?, ?, ?, ?, ?, ?)', entities)
                con.commit()  # Menyimpan perubahan ke database
                added_certs.append(cert_name)  # Menambahkan sertifikat ke daftar yang berhasil

            # Jika sertifikat sudah ada di database, lewati
            except sqlite3.IntegrityError:
                skipped_certs.append(cert_name)  # Menambahkan sertifikat ke daftar yang dilewati

    # Menutup koneksi ke database setelah selesai
    con.close()

    # Menampilkan hasil kepada pengguna
    if skipped_certs:
        print("\n[*] Sudah ada di DATABASE, dilewati:\n")
        for _x in skipped_certs:
            print("\t" + _x)
    if added_certs:
        print("\n\n[*] Ditambahkan ke DATABASE:\n")
        for _x in added_certs:
            print("\t" + _x)
    print(f"\n\n[*] Ditambahkan: {len(added_certs)}")
    print(f"[*] Dilewati {len(skipped_certs)}\n")


# Jika program dijalankan langsung (bukan diimpor sebagai modul)
if __name__ == "__main__":

    # Memeriksa apakah pengguna meminta bantuan
    if len(argv) < 2 or argv[1] == "--help" or argv[1] == "-h":
        print(HELP_TEXT)  # Menampilkan teks bantuan
        sys_exit()  # Keluar dari program

    # Memeriksa apakah direktori yang diberikan valid, jika ya, jalankan proses penambahan sertifikat
    if (PATH / argv[1]).is_dir():
        CERT_DIR = argv[1]
        if CERT_DIR[-1] == "/":  # Menghapus karakter "/" terakhir dari nama direktori jika ada
            CERT_DIR = CERT_DIR[:-1]
        try:
            add_certs(CERT_DIR)  # Memanggil fungsi untuk menambahkan sertifikat
        except KeyboardInterrupt:  # Menangkap interupsi dari keyboard (Ctrl+C)
            sys_exit()  # Keluar dari program
    else:
        # Jika direktori tidak valid, tampilkan pesan kesalahan
        print(f"\n[*] {argv[1]} bukan direktori yang valid\n")

### Penjelasan Alur Program:
# 1. **Impor Modul:**
#   - `sys`: untuk mengambil argumen command-line dan keluar dari program.
#   - `datetime`: untuk mengambil waktu saat sertifikat ditambahkan.
#   - `sqlite3`: untuk berinteraksi dengan database SQLite.
#   - `pathlib`: untuk menangani operasi path secara lebih mudah.

# 2. **Variabel Global:**
#   - `PATH`: menyimpan direktori kerja saat ini.
#   - `HELP_TEXT`: berisi pesan bantuan yang ditampilkan saat opsi `-h` atau `--help` digunakan.

# 3. **Fungsi `add_certs`:**
#   - Inisialisasi database jika belum ada, dan buat tabel `certs`.
#   - Iterasi melalui file di direktori sertifikat. Jika file adalah sertifikat `.txt`, tambahkan ke database.
#   - Jika sertifikat sudah ada di database, sertifikat tersebut dilewati.

# 4. **Bagian `if __name__ == "__main__":`**
#   - Memeriksa apakah argumen yang diberikan pengguna valid.
#   - Jika direktori valid, fungsi `add_certs` dipanggil untuk menambahkan sertifikat ke database.

# Program ini dapat digunakan di sistem mana pun yang memiliki Python 3 dan SQLite terpasang.
