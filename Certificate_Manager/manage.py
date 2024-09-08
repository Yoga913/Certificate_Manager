#!/usr/bin/python3
"""manage.py"""

from sys import argv
from sys import exit as sys_exit
from typing import Any, Optional
import subprocess
import datetime
import sqlite3
import pathlib

# Mendapatkan direktori kerja saat ini
PATH = pathlib.Path.cwd()

# Teks bantuan yang akan muncul ketika pengguna meminta bantuan
HELP_TEXT = """
Penggunaan: manage.py [-h] database

-h, --help          Munculkan pesan bantuan ini
database            Nama database sertifikat
"""

# Teks menu yang menampilkan opsi yang tersedia
MENU_TEXT = """
###########################
# [1] DAFTAR SERTIFIKAT   #
# [2] LIHAT YANG AKTIF    #
# [3] LIHAT SERTIFIKAT    #
# [4] PERBARUI SERTIFIKAT #
# [5] EKSTRAK SERTIFIKAT  #
# [6] KELUAR              #
###########################
"""

# Teks menu pembaruan sertifikat
UPDATE_TEXT = """
###########################
# [1] TANGGAL DITAMBAHKAN #
# [2] DIPAKAI             #
# [3] TANGGAL DIGUNAKAN   #
# [4] DIBANNED            #
# [5] TANGGAL DIBANNED    #
# [6] BUTUH AKTIVASI      #
# [7] SEDANG DIGUNAKAN    #
###########################
"""

# Fungsi untuk menampilkan daftar sertifikat di database
def list_certs(cursor_obj: sqlite3.Cursor) -> None:
    """Menampilkan semua sertifikat yang ada di DATABASE."""
    cursor_obj.execute('select * from certs')
    rows = cursor_obj.fetchall()
    for row in rows:
        cursor_obj.execute(f'select banned from certs where id = "{row[0]}"')
        is_banned = cursor_obj.fetchall()[0][0]
        if is_banned == 1:
            print(f"TERBANNED\t{row[0]}")
        else:
            print(f"\t{row[0]}")

# Fungsi untuk menampilkan data sertifikat
def print_cert(name: str, cursor_obj: sqlite3.Cursor) -> None:
    """Menampilkan data sertifikat berdasarkan nama."""
    try:
        cursor_obj.execute(f'select * from certs where id is "{name}"')
        cert_data = cursor_obj.fetchall()
        bools = {0: "Tidak", 1: "Ya"}
        print(f"""
                             Nama:  {cert_data[0][0]}
              Tanggal Ditambahkan:  {cert_data[0][1]}
                          Dipakai:  {bools[cert_data[0][2]]}
                Tanggal Digunakan:  {cert_data[0][3]}
                         Dibanned:  {bools[cert_data[0][4]]}
                 Tanggal Dibanned:  {cert_data[0][5]}
             Membutuhkan Aktivasi:  {bools[cert_data[0][6]]}
                 Sedang Digunakan:  {bools[cert_data[0][7]]}\n""")
    except IndexError:
        print("\n[!] Nama Sertifikat Tidak Valid [!]")

# Fungsi untuk meminta pengguna memasukkan nama sertifikat dan menampilkan data sertifikat tersebut
def view_cert(cursor_obj: sqlite3.Cursor) -> None:
    """Melihat data sertifikat berdasarkan nama."""
    name = input("[*] Nama Sertifikat: ")
    print_cert(name, cursor_obj)

# Fungsi untuk memperbarui nilai tertentu dari sertifikat
def update_cert(con: sqlite3.Connection, cursor_obj: sqlite3.Cursor) -> None:
    """Memperbarui nilai dari sertifikat tertentu."""
    cases = ["1", "2", "3", "4", "5", "6", "7"]
    bools = {"tidak": "0", "ya": "1"}
    bool_items = ["applied", "banned", "required_activation", "currently_used"]
    name = input("[*] Nama sertifikat: ")
    print_cert(name, cursor_obj)
    print(UPDATE_TEXT)
    update_choice = input("\n[*] Pilih Nilai Yang Akan Diperbarui: ")
    if update_choice in cases:
        item = update_switch(update_choice)
        value = input("[*] Nilai Terbaru: ")
        if item in bool_items:
            if value.lower() == "tidak" or value.lower() == "ya":
                value = bools[value.lower()]
                cursor_obj.execute(f'UPDATE certs SET {item} = "{value}" '
                                   f'where id is "{name}"')
                con.commit()
            else:
                print('\n[!] Diharapkan Nilai YA atau TIDAK [!]')
        else:
            none_safe_value: Optional[str] = None if value == "" else value
            cursor_obj.execute(
                f'UPDATE certs SET {item} = "{none_safe_value}" '
                'where id is "{name}"')
            con.commit()
        print_cert(name, cursor_obj)
    else:
        print("\n[!] Pilihan Tidak Valid [!]")

# Fungsi yang menangani logika dari menu utama
def menu_switch(case: str, cert_dir: str, con: sqlite3.Connection,
                cursor_obj: sqlite3.Cursor) -> None:
    """Pengalih menu utama."""
    switch = {
        "1": list_certs,
        "2": view_current,
        "3": view_cert,
        "4": update_cert,
        "5": extract_cert,
        "6": leave
    }
    function_call: Any = switch[case]
    if case in ["1", "2", "3"]:
        function_call(cursor_obj)
    elif case == "5":
        function_call(cert_dir, con, cursor_obj)
    elif case == "6":
        function_call()
    else:
        function_call(con, cursor_obj)

# Fungsi yang menghubungkan pilihan pembaruan dengan kolom di database
def update_switch(case: str) -> str:
    """Pengalih pembaruan sertifikat."""
    switch = {
        "1": "date_added",
        "2": "applied",
        "3": "date_applied",
        "4": "banned",
        "5": "banned_date",
        "6": "required_activation",
        "7": "currently_used"
    }
    return switch[case]

# Fungsi untuk keluar dari program
def leave() -> None:
    """Keluar dari program."""
    print()
    sys_exit()

# Fungsi untuk melihat sertifikat yang sedang digunakan
def view_current(cursor_obj: sqlite3.Cursor) -> None:
    """Tampilkan sertifikat yang sedang digunakan."""
    cursor_obj.execute('select id from certs where currently_used is "1"')
    rows = cursor_obj.fetchall()
    try:
        name = rows[0][0]
        print()
        print_cert(name, cursor_obj)
    except IndexError:
        print("\n[!] Tidak Ada Sertifikat Yang Sedang Digunakan [!]")

# Fungsi untuk menampilkan menu utama dan menangani pilihan pengguna
def menu(cert_dir: str, con: sqlite3.Connection,
         cursor_obj: sqlite3.Cursor) -> None:
    """Menu utama."""
    cases = ["1", "2", "3", "4", "5", "6"]
    while True:
        print(MENU_TEXT)
        choice = input("[*] Pilihan: ")
        if choice not in cases:
            continue
        menu_switch(choice, cert_dir, con, cursor_obj)

# Bagian utama program
if __name__ == "__main__":

    # Cek jika pengguna meminta bantuan
    if len(argv) < 2 or argv[1] == "--help" or argv[1] == "-h":
        print(HELP_TEXT)
        sys_exit()

    # Cek apakah file yang diberikan adalah file database yang valid
    if (PATH / argv[1]).suffix == ".db":
        CON = sqlite3.connect(argv[1])
        CURSOR_OBJ = CON.cursor()
        print(type(CON), type(CURSOR_OBJ))
        try:
            CURSOR_OBJ.execute("select * from certs")
        except sqlite3.DatabaseError:
            print(f"\n[*] {argv[1]} bukan file database sertifikat yang valid\n")
            sys_exit()
        try:
            menu(argv[1], CON, CURSOR_OBJ)
        except KeyboardInterrupt:
            sys_exit()
    else:
        print(f"\n[*] {argv[1]} bukan file database yang valid\n")
