import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Fixture untuk menyiapkan database sebelum pengujian dan membersihkannya setelah selesai."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Fixture untuk mendapatkan koneksi database dan menutupnya setelah pengujian."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Menguji pembuatan database dan tabel pengguna."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Tabel 'users' harus ada dalam database."

def test_add_new_user(setup_database, connection):
    """Menguji penambahan pengguna baru."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Pengguna harus ditambahkan ke database."

# Berikut adalah pengujian yang bisa ditulis:
def test_add_existing_user(setup_database, connection):
    """Menguji penambahan pengguna dengan nama pengguna yang sudah ada."""
    add_user('testuser', 'testuser@example.com', 'password123')
    assert not add_user('testuser','testuser@example.com', 'password123'), "Menambahkan pengguna dengan nama pengguna yang sudah ada harus gagal." 

def test_check_authentication(setup_database, connection):
    """Menguji keberhasilan autentikasi pengguna."""
    add_user('testuser', 'testuser@example.com', 'password123')
    assert authenticate_user('testuser', 'password123'), "Autentikasi pengguna harus berhasil."

def test_check_authentication_user_not_exist(setup_database, connection):
    """Menguji autentikasi pengguna yang tidak ada."""
    assert not authenticate_user('nonexistentuser', 'password123'), "Autentikasi pengguna yang tidak ada harus gagal."

def test_check_authentication_wrong_password(setup_database, connection):
    """Menguji autentikasi dengan kata sandi yang salah."""
    add_user('testuser', 'testuser@example.com', 'password123')
    assert not authenticate_user('testuser', 'wrongpw'), "Autentikasi dengan kata sandi yang salah harus gagal."

def test_display_user(setup_database, connection):
    """Menguji tampilan yang benar dari daftar pengguna."""
    add_user('testuser', 'testuser@example.com', 'password123')
    result = display_users()
    assert ('testuser', 'testuser@example.com') in result, "Daftar pengguna harus menampilkan pengguna yang telah ditambahkan."






"""""
Menguji percobaan menambahkan pengguna dengan nama pengguna yang sudah ada.
Menguji keberhasilan autentikasi pengguna.
Menguji autentikasi pengguna yang tidak ada.
Menguji autentikasi dengan kata sandi yang salah.
Menguji tampilan yang benar dari daftar pengguna.
"""