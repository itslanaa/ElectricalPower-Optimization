## Live Deployment Demo (Streamlit) : https://electricalpower-optimization.streamlit.app/

# ⚡ ElectricalPower Optimization

Proyek ini bertujuan untuk mengoptimasi konsumsi daya listrik rumah tangga menggunakan **algoritma Greedy**. Pengguna dapat mengunggah dataset konsumsi listrik, melakukan simulasi optimasi, melihat visualisasi pola konsumsi, dan mengekspor hasil analisis ke dalam format CSV dan PDF melalui antarmuka.

## ✨ Fitur Utama

- **Optimasi Konsumsi Daya (Efficient Power Allocation):**  
  Menggunakan algoritma Greedy untuk mengidentifikasi jam-jam tidak efisien dalam konsumsi daya, mengurangi konsumsi pada jam tersebut, serta menggeser sebagian beban ke jam-jam yang lebih efisien.

- **Visualisasi Interaktif:**  
  Menyediakan grafik konsumsi sebelum dan sesudah optimasi, pola konsumsi rata-rata per jam, serta persentase penghematan harian yang mudah dibaca dan diinterpretasikan.

- **Ekspor Hasil:**  
  Hasil analisis dapat diunduh dalam bentuk:
  - **CSV** untuk ringkasan konsumsi dan IKE
  - **PDF** yang berisi grafik visualisasi dan tabel ringkasan

## 💻 Teknologi yang Digunakan

- **Bahasa Pemrograman:** Python  
- **Framework UI:** Streamlit  
- **Library Analisis & Visualisasi:**
  - pandas
  - numpy
  - matplotlib
  - seaborn


## 📂 Struktur Proyek
```
/
├── app.py # Antarmuka utama
├── helper/
│   └── analysis.py # Modul analisis utama berbasis algoritma Greedy
├── requirements.txt # python dependencies
├── LICENSE # MIT License
└── README.md
```

## 🛠️ Cara Menjalankan Secara Lokal

1. **Buat environment virtual (opsional tapi disarankan):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Untuk Windows: .venv\Scripts\activate

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan Aplikasi:**
   ```bash
   python app.py 
   ```
## 📄 Lisensi

Repositori ini dilisensikan di bawah **MIT License** — yang berarti kamu bebas menggunakan, menyalin, memodifikasi, maupun mendistribusikan proyek ini, baik untuk tujuan pribadi maupun komersial, selama mencantumkan atribusi kepada pembuat asli.

Silakan lihat file [LICENSE](LICENSE) untuk informasi selengkapnya.

