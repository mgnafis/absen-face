# Aplikasi Realtime Face Recognition dengan Streamlit

Aplikasi ini memungkinkan Anda untuk melakukan pendaftaran wajah dan deteksi wajah secara *realtime* menggunakan kamera perangkat Anda.

## Persyaratan

Pastikan Anda telah menginstal Python (disarankan versi 3.8+) dan dependensi yang diperlukan.

## Instalasi Lokal

1.  **Instal Dependensi:**
    ```bash
    pip install -r requirements.txt
    ```
    **Catatan Penting:** Pemasangan `face-recognition` dan `dlib` memerlukan *compiler* C++ dan pustaka sistem seperti `cmake` dan `libboost-all-dev`. Jika Anda mengalami masalah instalasi, pastikan Anda telah menginstal dependensi sistem tersebut.

2.  **Jalankan Aplikasi:**
    ```bash
    streamlit run app.py
    ```

## Deployment di Streamlit Cloud

Untuk *deployment* di Streamlit Cloud, Anda perlu menambahkan file `packages.txt` untuk menginstal dependensi sistem yang diperlukan oleh `dlib` dan `face-recognition`.

1.  Pastikan file-file berikut ada di repositori Anda:
    *   `app.py`
    *   `requirements.txt`
    *   `packages.txt` (Berisi `cmake`, `libsm-dev`, `libxext-dev`, `libboost-all-dev`)
2.  *Deploy* aplikasi Anda seperti biasa. Streamlit Cloud akan secara otomatis membaca `packages.txt` dan menginstal dependensi sistem sebelum menginstal dependensi Python.

## Cara Penggunaan

1.  **Pendaftaran Wajah:**
    *   Akses aplikasi melalui *browser* Anda.
    *   Di **Sidebar** sebelah kiri, masukkan nama orang yang akan didaftarkan.
    *   Gunakan tombol **Ambil Foto** untuk mengambil gambar wajah. Pastikan wajah terlihat jelas.
    *   Setelah wajah terdeteksi, data wajah (encoding) akan disimpan, dan Anda akan melihat pesan sukses.

2.  **Deteksi Realtime:**
    *   Di bagian utama aplikasi, klik tombol **START** pada komponen *WebRTC Streamer*.
    *   Aplikasi akan mulai mengakses kamera Anda dan mencoba mengenali wajah yang muncul di *frame* video.
    *   Wajah yang sudah terdaftar akan ditandai dengan kotak hijau dan namanya. Wajah yang tidak dikenal akan ditandai sebagai "Unknown".

3.  **Menghapus Data:**
    *   Gunakan tombol **Hapus Semua Data Wajah** di sidebar untuk menghapus semua data wajah yang telah didaftarkan. Data akan disimpan dalam file `face_data.pkl`.

## Struktur File

*   `app.py`: Kode utama aplikasi Streamlit.
*   `requirements.txt`: Daftar pustaka Python yang diperlukan.
*   `packages.txt`: Daftar dependensi sistem Linux untuk Streamlit Cloud.
*   `face_data.pkl`: File tempat data wajah (encoding dan nama) disimpan secara persisten. (Akan dibuat secara otomatis saat pendaftaran pertama).
*   `README.md`: Dokumentasi ini.
