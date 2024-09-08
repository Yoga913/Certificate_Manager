#!/bin/sh

################################################################
# Menuliskan daftar semua sertifikat yang ada di database ke file 
# 'certlist.txt', hanya itu yang dilakukan
################################################################

# Memeriksa apakah argumen yang diberikan kosong (tidak ada argumen)
if [ -z "$*" ]; then
    echo "Penggunaan: ./get-certs.sh DATABASE_FILE"  # Menampilkan cara penggunaan jika tidak ada argumen
    exit 0  # Keluar dari skrip
fi

# Menggunakan 'expect' untuk menjalankan perintah manage.py secara interaktif
RESULT=$(expect - << EOF
spawn $(pwd)/manage.py $1
sleep 1
expect "Choice: "
sleep 1
send "1\n"
sleep 1
expect "\n" 
EOF
)

# Menyimpan hasil keluaran dari perintah ke dalam file certlist.txt
# Mengambil baris dari hasil keluaran mulai dari baris ke-13 hingga 11 baris sebelum akhir
echo "$RESULT" | tail -n +13 | head -n -11 > certlist.txt

#####################################################################################################################################################
### Penjelasan alur kode:
# 1. **Pemeriksaan Argumen:**
#    - Jika tidak ada argumen yang diberikan (file database tidak disediakan), program akan menampilkan pesan penggunaan (`./get-certs.sh DATABASE_FILE`) dan keluar.

# 2. **Menggunakan `expect`:**
#    - `expect` digunakan untuk mengotomatisasi interaksi dengan skrip `manage.py`. Program ini menunggu respons dari skrip dan mengirim input secara otomatis.
#    - Program menunggu prompt dengan teks "Choice: ", lalu mengirim input `1` yang mungkin adalah opsi untuk mendapatkan daftar sertifikat dari database.
#    - `expect` akan menunggu keluaran dari perintah dan menyimpannya ke dalam variabel `RESULT`.

# 3. **Menyimpan hasil ke file:**
#    - Output yang diperoleh dari `expect` kemudian disaring:
#      - Mengambil baris mulai dari baris ke-13 hingga menghilangkan 11 baris dari akhir keluaran.
#    - Hasil akhirnya ditulis ke file `certlist.txt`.

# Kode ini seharusnya dapat berjalan di sistem mana pun yang mendukung `expect` dan `bash`.