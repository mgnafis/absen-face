# Aplikasi Realtime Face Recognition dengan Streamlit

Aplikasi ini memungkinkan Anda untuk melakukan pendaftaran wajah dan deteksi wajah secara *realtime* menggunakan kamera perangkat Anda.

## Persyaratan

Pastikan Anda telah menginstal Python (disarankan versi 3.8+) dan dependensi yang diperlukan.

## Instalasi

1.  **Instal Dependensi:**
    ```bash
    pip install -r requirements.txt
    ```
    **Catatan Penting:** Pemasangan `face-recognition` dan `dlib` mungkin memerlukan beberapa *library* sistem seperti `cmake` dan *compiler* C++. Jika Anda mengalami masalah instalasi, pastikan Anda telah menginstal dependensi sistem tersebut.

2.  **Jalankan Aplikasi:**
    ```bash
    streamlit run app.py
    ```

## Cara Penggunaan

1.  **Pendaftaran Wajah:**
    *   Akses aplikasi melalui *browser* Anda (biasanya di `http://localhost:8501`).
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
*   `face_data.pkl`: File tempat data wajah (encoding dan nama) disimpan secara persisten. (Akan dibuat secara otomatis saat pendaftaran pertama).
*   `README.md`: Dokumentasi ini.
