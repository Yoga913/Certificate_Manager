# **Certificate Manager**

Proyek sederhana untuk menganalisis dan mengelola sertifikat digital menggunakan Python dan bash script. 
Program ini memungkinkan Anda untuk melihat, memperbarui, dan mengekstrak sertifikat dari database SQLite, serta menganalisis dan mengelola status sertifikat (banned, aktif, dll.).

## **Fitur Utama**

- **DAFTAR SERTIFIKAT**: Menampilkan daftar semua sertifikat dalam database, termasuk status banned.
- **LIHAT SERTIFIKAT YANG AKTIF Cert**: Melihat sertifikat yang sedang aktif digunakan.
- **LIHAT SERTIFIKAT**: Menampilkan detail dari sertifikat tertentu berdasarkan ID.
- **PERABRUI SERTIFIKAT**: Memperbarui informasi terkait sertifikat, seperti status penggunaan, tanggal banned, dll.
- **EKSTRAK SERTIFIKAT**: Mengekstrak sertifikat baru dari folder dan memperbarui database secara otomatis.

## **Instalasi**

1. Clone repositori ini:
   ```bash
   git clone https://github.com/Yoga913/certificate-manager.git
   cd Certificate_Manager
   ```

2. Pastikan **Python 3.x** dan **SQLite3** sudah terinstal di sistem Anda.

3. Inisialisasi database:
   ```bash
   python3 init_db.py
   ```
   `init_db.py` Bisa Anda Tambahkan Sendiri!
## **Penggunaan**

1. **Menjalankan Program**:
   Jalankan skrip utama untuk mengakses menu manajemen sertifikat:
   ```bash
   python3 manage.py certs.db
   ```

2. **Menu Utama**:
   Setelah program dijalankan, pilih salah satu opsi berikut:
   - `[1] DAFTAR SERTIFIKAT`: Melihat daftar semua sertifikat.
   - `[2] LIHAT SERTIFIKAT YANG AKTIF`: Melihat sertifikat yang sedang digunakan.
   - `[3] LIHAT SERTIFIKAT`: Menampilkan detail sertifikat tertentu.
   - `[4] PERABRUI SERTIFIKAT`: Memperbarui informasi sertifikat.
   - `[5] EKSTRAK SERTIFIKAT`: Mengekstrak sertifikat baru dan memperbarui database.
   - `[6] KELUAR`: Keluar dari program.

3. **Mengekstrak Sertifikat**:
   Untuk menambahkan sertifikat baru dari folder tertentu, jalankan skrip bash berikut:
   ```bash
   ./bpi-extract.sh /path/to/certs/folder
   ```

## **Contoh Penggunaan**

- **Melihat sertifikat yang aktif**:
   Jalankan `manage.py`, pilih opsi `[2] LIHAT SERTIFIKAT YANG AKTIF` untuk melihat sertifikat yang sedang digunakan.
  
- **Memperbarui status sertifikat**:
   Pilih opsi `[4] PERABRUI SERTIFIKAT` dan masukkan ID sertifikat untuk memperbarui statusnya, seperti banned atau diterapkan.

- **Mengekstrak sertifikat baru**:
   Jalankan `bpi-extract.sh` untuk menambahkan sertifikat baru dari folder yang ditentukan.
  
**Untuk Penggunaan Lebih Lanjut:**
[Klik]()

## **Lisensi**

Proyek ini dilisensikan di bawah MIT License. Lihat file `LICENSE` untuk informasi lebih lanjut.
