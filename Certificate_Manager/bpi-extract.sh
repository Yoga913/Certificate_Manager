#!/bin/sh

##############################################################
# Porting Bash/Bash port dari alat ekstraksi sertifikat RAW BPI BTC untuk 
#   mengekstrak sertifikat dan kunci dari blob biner BPI 
#   menggunakan binwalk dan openssl
##############################################################

#===================#
# Memeriksa argumen #
#===================#
dt=$(date '+%Y/%m/%d %R:%S');  # Mendapatkan tanggal dan waktu saat ini
if [ -z "$*" ]; then  # Jika tidak ada argumen yang diberikan
    echo "Penggunaan: ./bpi-extract.sh FILE";  # Menampilkan pesan penggunaan
    exit 0;  # Keluar dari skrip
fi;
if ! test -f $1; then  # Memeriksa apakah file yang diberikan ada
    echo "$dt File tidak ditemukan";  # Menampilkan pesan kesalahan jika file tidak ada
    exit 0;  # Keluar dari skrip
fi;

#=================================================#
# Memastikan semua alat yang dibutuhkan terpasang #
#=================================================#
ps="binwalk openssl mktemp basename dirname awk cut test date grep dd stat mkdir cat rm echo mv tr"  # Daftar perintah yang diperlukan
for i in $ps; do
    if ! command -v $i 1>/dev/null; then  # Memeriksa apakah perintah ada di sistem
        echo "Perintah $i tidak terpasang";  # Menampilkan pesan jika perintah tidak ada
        exit 0;  # Keluar dari skrip
    fi;
done;

#=========================#
# Mengurai file dari blob #
#=========================#
tf=$(mktemp /dev/shm/tmp.XXXXXXXXX);  # Membuat file sementara di memori
ed=$(dirname $1);  # Mendapatkan direktori file yang diberikan
fn=$(basename $1);  # Mendapatkan nama file yang diberikan
echo "Alat ekstraksi sertifikat BPI Plastik BCM Versi 1.0";  # Menampilkan informasi alat
echo "$dt Mengekstrak $ed/$fn";  # Menampilkan informasi file yang sedang diekstrak
binwalk -e $1 -C $ed 1>$tf;  # Mengekstrak konten file menggunakan binwalk
ko=$(cat $tf | awk '(NR==4){ print $2 }' | cut -c 3-);  # Mendapatkan nama file kunci utama
kt=$(cat $tf | awk '(NR==5){ print $2 }' | cut -c 3-);  # Mendapatkan nama file kunci tambahan
co=$(cat $tf | awk '(NR==6){ print $2 }' | cut -c 3-);  # Mendapatkan nama file sertifikat utama
ct=$(cat $tf | awk '(NR==7){ print $2 }' | cut -c 3-);  # Mendapatkan nama file sertifikat tambahan

#===================================================================#
# Memeriksa apakah blob valid dan menghasilkan file yang diharapkan #
#===================================================================#
cs="${ko}.key ${kt}.key ${co}.crt ${ct}.crt";  # Daftar file yang harus ada
for i in $cs; do
    if ! test -f $ed/_$fn.extracted/$i; then  # Jika file yang diharapkan tidak ditemukan
        rm $tf; rm -r _$1.extracted 2>/dev/null;  # Hapus file sementara dan direktori ekstraksi
        echo "$dt File rusak";  # Menampilkan pesan kesalahan
        exit 0;  # Keluar dari skrip
    fi;
done;

#=======================================================#
# Output yang tidak diperlukan (sesuai dengan versi BTC) #
#========================================================#
echo "$dt Baca versi: 1";
echo "$dt";

#==========================================================================#
# Ekstrak MAC dan buat direktori baru, hapus yang sudah ada jika ditemukan #
#==========================================================================#
ma=$(openssl x509 -inform der -in $ed/_$fn.extracted/$co.crt -noout -text | grep "CN = " | awk '(NR==2){ print $NF }' | tr -d :);  # Ekstrak MAC dari sertifikat
if test -d $ed/$ma; then  # Jika direktori sudah ada
    rm -r $ed/$ma;  # Hapus direktori lama
fi;
mkdir $ed/$ma;  # Buat direktori baru
echo "$dt $ed/$ma/";

#======================#
# Ekstrak kunci publik #
#======================#
openssl rsa -inform der -in $ed/_$fn.extracted/$ko.key -RSAPublicKey_out -outform der -out pub.key 2>/dev/null;  # Ekstrak kunci publik
echo "$dt Menulis pub.key, ukuran: $(stat --format='%s' pub.key)";

#=====================#
# Ekstrak kunci privat #
#=====================#
openssl rsa -inform der -in $ed/_$fn.extracted/$ko.key -outform der -out private.key 2>/dev/null;  # Ekstrak kunci privat
echo "$dt Menulis private.key, ukuran: $(stat --format='%s' private.key)";

#====================#
# Ekstrak kunci root #
#====================#
rs=$(($(stat --format='%s' private.key) + 28));  # Menghitung offset untuk mengekstrak kunci root
dd if=$ed/_$fn.extracted/$ko.key of=root.key bs=1 skip=$rs count=270 2>/dev/null;  # Ekstrak kunci root
echo "$dt Menulis root.key, ukuran: $(stat --format='%s' root.key)";

#========================#
# Ekstrak sertifikat CM #
#=======================#
openssl x509 -inform der -in $ed/_$fn.extracted/$co.crt -outform der -out cm.cer;  # Ekstrak sertifikat CM
echo "$dt Menulis cm.cer, ukuran: $(stat --format='%s' cm.cer)";

#=======================#
# Ekstrak sertifikat CA #
#=======================#
openssl x509 -inform der -in $ed/_$fn.extracted/$ct.crt -outform der -out ca.cer;  # Ekstrak sertifikat CA
echo "$dt Menulis ca.cer, ukuran: $(stat --format='%s' ca.cer)";

#==========================#
# Bersihkan file sementara #
#==========================#
mv *.key $ed/$ma; mv *cer $ed/$ma;  # Pindahkan file ke direktori yang baru dibuat
rm -r $ed/_$fn.extracted; rm $tf;  # Hapus file sementara dan direktori ekstraksi

#====================================#
# Dapatkan ukuran gabungan dari file #
#====================================#
sf=0;
for i in $ed/$ma/*; do sf=$(($sf + $(stat --format='%s' $i))); done;  # Hitung total ukuran file
echo "$dt Total ukuran: $sf"

# Program ini seharusnya dapat berjalan di sistem mana pun yang memiliki alat yang diperlukan seperti `binwalk`, `openssl`, dan lainnya.