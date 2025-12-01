import streamlit as st
import cv2
import numpy as np
import face_recognition
import pickle
import os
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, VideoTransformerBase, RTCConfiguration

# --- Konfigurasi ---
DATA_PATH = "face_data.pkl"
st.set_page_config(page_title="Realtime Face Recognition", layout="wide")

# --- Fungsi Utilitas ---

def load_face_data():
    """Memuat data wajah (encoding dan nama) dari file pickle."""
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'rb') as f:
            return pickle.load(f)
    return {"known_face_encodings": [], "known_face_names": []}

def save_face_data(data):
    """Menyimpan data wajah ke file pickle."""
    with open(DATA_PATH, 'wb') as f:
        pickle.dump(data, f)

# --- Kelas Pemroses Video Realtime ---

class FaceRecognitionProcessor(VideoProcessorBase):
    """
    Memproses frame video secara realtime untuk mendeteksi dan mengenali wajah.
    """
    def __init__(self):
        self.face_data = load_face_data()
        self.known_face_encodings = self.face_data["known_face_encodings"]
        self.known_face_names = self.face_data["known_face_names"]

    def recv(self, frame):
        # Mengubah frame menjadi array numpy
        img = frame.to_ndarray(format="bgr")
        
        # Mengubah dari BGR (OpenCV) ke RGB (face_recognition)
        rgb_frame = img[:, :, ::-1]

        # Mencari semua wajah dan encoding wajah di frame saat ini
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            
            # Mencocokkan wajah dengan wajah yang sudah dikenal
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            
            # Menggunakan wajah yang paling cocok
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            # Menggambar kotak di sekitar wajah
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)

            # Menggambar label dengan nama di bawah wajah
            cv2.rectangle(img, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        return img

# --- Streamlit App ---

def main():
    st.title("Aplikasi Realtime Face Recognition")
    st.markdown("---")

    # Sidebar untuk pendaftaran wajah
    st.sidebar.header("Pendaftaran Wajah Baru")
    
    # Input nama
    new_face_name = st.sidebar.text_input("Masukkan Nama:", key="new_face_name")
    
    # Input gambar dari kamera
    st.sidebar.markdown("Ambil gambar wajah Anda:")
    camera_image = st.sidebar.camera_input("Ambil Foto", key="camera_input")

    if camera_image is not None and new_face_name:
        # Memproses gambar yang diambil
        try:
            # Mengubah BytesIO menjadi array numpy
            file_bytes = np.asarray(bytearray(camera_image.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            
            # Mengubah dari BGR ke RGB
            rgb_img = img[:, :, ::-1]
            
            # Mencari encoding wajah
            face_encodings = face_recognition.face_encodings(rgb_img)
            
            if len(face_encodings) > 0:
                new_encoding = face_encodings[0]
                
                # Memuat data yang sudah ada
                face_data = load_face_data()
                
                # Menambahkan data wajah baru
                face_data["known_face_encodings"].append(new_encoding)
                face_data["known_face_names"].append(new_face_name.strip().title())
                
                # Menyimpan data
                save_face_data(face_data)
                
                st.sidebar.success(f"Wajah **{new_face_name.strip().title()}** berhasil didaftarkan!")
                
                # Membersihkan input kamera setelah pendaftaran berhasil
                st.session_state["camera_input"] = None
                st.session_state["new_face_name"] = ""
                
            else:
                st.sidebar.error("Wajah tidak terdeteksi di gambar. Pastikan wajah terlihat jelas.")
                
        except Exception as e:
            st.sidebar.error(f"Terjadi kesalahan saat memproses gambar: {e}")

    # Tombol untuk menghapus semua data wajah
    if st.sidebar.button("Hapus Semua Data Wajah"):
        if os.path.exists(DATA_PATH):
            os.remove(DATA_PATH)
        st.sidebar.warning("Semua data wajah telah dihapus.")
        # Memuat ulang data di session state agar realtime
        st.experimental_rerun()


    # Bagian utama untuk deteksi realtime
    st.header("Deteksi Wajah Realtime")
    st.info("Pastikan Anda sudah mendaftarkan wajah di sidebar sebelum memulai deteksi.")

    # Menampilkan daftar wajah yang sudah terdaftar
    current_data = load_face_data()
    if current_data["known_face_names"]:
        st.subheader("Wajah yang Sudah Terdaftar:")
        st.write(", ".join(current_data["known_face_names"]))
    else:
        st.warning("Belum ada wajah yang terdaftar. Silakan daftarkan wajah Anda di sidebar.")

    # Konfigurasi WebRTC
    rtc_configuration = RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )

    # Memulai stream WebRTC
    webrtc_streamer(
        key="realtime_face_recognition",
        video_processor_factory=FaceRecognitionProcessor,
        rtc_configuration=rtc_configuration,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

if __name__ == "__main__":
    main()
