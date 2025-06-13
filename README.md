# QTancy Machine-learning

## Deskripsi Proyek
Repositori ini berisi *machine-learning* untuk aplikasi **QTancy**. Pada repository ini akan digunakan sebagai API yang bertanggung jawab untuk menyediakan *endpoint* RESTful untuk fitur **QCap** dan **Qrep**.

## Fitur Utama
* **QCap:** Model akan memproses foto struk yang diberikan pengguna untuk bisa diolah melalui proses OCR+NER serta langsung mengklasifikasikan kategori-kategori setiap barang yang ada di dalam struk, kemudian akan menyimpan kedalam database.
* **QRep:** Akan melakukan query terhadap semua struk yang pernah diekstrasi melalui fitur QCap oleh pengguna dan menampilkan laporannya. 

---

## Teknologi yang Digunakan

* **Bahasa Pemrograman:** Python yang digunakan versi 3.11.7
* **Framework:** Fast API
* **Autentikasi:** JWT (JSON WEB TOKEN)
* **Database:** PostgreSQL (Di deploy melalui Neon tech)
* **Lain-lain:** Docker ( Sebagai Container Builder, Penerapan CI/CD di Google Cloud Service)

---

## Memulai Proyek

Ikuti langkah-langkah di bawah ini untuk menjalankan proyek ini di lingkungan lokal Anda.

### Instalasi  
1. Buat .venv terlebih dahulu
  ```
  python -m venv .venv 
  ```

2. Aktifkan .venv (untuk windows)
  ```
  \.venv/Scripts/activate
  ```

3. Bisa jalankan line berikut untuk install library
  ```
  pip install -r requirements.txt
  ```

4. Buat file .env untuk menyimpan SECRET_KEY (JWT) dan DATABASE_URL (Neon Tech)
  ```
  DATABASE_URL='LINK DATABASE ANDA'
  SECRET_KEY = 'KUNCI RAHASIA ANDA'
  ```

### Menjalankan Aplikasi

1. Bisa jalankan local server dengan perintah berikut ini
  ```
  uvicorn app.main:app --reload
  ```

2. Matikan/keluar .venv
  ```
  deactivate
  ```

