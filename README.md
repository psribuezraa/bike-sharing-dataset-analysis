# Proyek Analisis Data: Bike Sharing Dataset

Proyek akhir untuk kelas **Belajar Fundamental Analisis Data** pada platform **Dicoding Academy**. Proyek ini mencakup alur lengkap analisis data (*Data Wrangling, Exploratory Data Analysis, Data Visualization*) hingga pengembangan dashboard interaktif berbasis **Streamlit**.

- **Nama:** Ezra Abhinaya Pasaribu
- **Email:** psribuezraa@gmail.com
- **ID Dicoding:** ezra_psribu

---

## Pertanyaan Bisnis (SMART Questions)
1. Bagaimana kondisi cuaca (*weathersit*) dan pergantian musim (*season*) memengaruhi rata-rata jumlah penyewaan sepeda harian (*cnt*) sepanjang tahun 2011–2012, dan pada kondisi seperti apa terjadi penurunan sewa paling signifikan?
2. Bagaimana perbedaan karakteristik pola peminjaman sepeda per jam (*hourly trend*) antara pengguna kasual (*casual*) dan pengguna terdaftar (*registered*) pada hari kerja (*workingday*) dibandingkan hari libur/akhir pekan (*weekend/holiday*) selama periode 2011–2012?
3. Berapa persentase pertumbuhan total penyewaan sepeda (*Year-over-Year*) dari tahun 2011 ke tahun 2012, dan pada bulan apa terjadi performa penyewaan tertinggi (*peak month*) di masing-masing tahun?

---

## Struktur Direktori Proyek

```text
proyek_akhir/
├── dashboard/
│   ├── main_data.csv          # Dataset harian bersih yang telah diproses
│   ├── hour_data.csv          # Dataset per jam bersih untuk pola jam sibuk
│   └── dashboard.py           # Script utama aplikasi Streamlit
├── data/                      # Dataset mentah (raw data)
│   ├── day.csv
│   └── hour.csv
├── dataset/                   # Dataset mentah asli
│   ├── day.csv
│   ├── hour.csv
│   └── Readme.txt
├── Proyek_Analisis_Data.ipynb # Notebook Jupyter yang sudah tereksekusi penuh
├── README.md                  # Dokumentasi proyek dan panduan menjalankan
├── requirements.txt           # Daftar pustaka Python yang dibutuhkan
└── url.txt                    # Tautan aplikasi setelah dideploy ke Streamlit Cloud
```

---

## Panduan Menjalankan Proyek Secara Lokal

### 1. Clone Repository atau Unduh Berkas
Pastikan Anda berada di direktori proyek `proyek_akhir`:
```bash
cd "D:\Asah 2026 Journey\Belajar Fundamental Analisis Data\proyek_akhir"
```

### 2. Membuat dan Mengaktifkan Virtual Environment (Opsional tapi Direkomendasikan)
Menggunakan terminal / PowerShell:
```bash
python -m venv venv
# Mengaktifkan di Windows:
.\venv\Scripts\activate
```

### 3. Menginstal Dependensi
Instal semua pustaka yang dibutuhkan menggunakan file `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Menjalankan Dashboard Streamlit
Anda dapat menjalankan dashboard langsung dari folder root atau dari dalam folder `dashboard`:

```bash
# Dari root proyek_akhir:
streamlit run dashboard/dashboard.py

# Atau masuk ke dalam folder dashboard:
cd dashboard
streamlit run dashboard.py
```
Aplikasi dashboard akan otomatis terbuka di browser lokal Anda pada alamat: `http://localhost:8501`.

---

## Panduan Deployment ke Streamlit Community Cloud

1. Buat repositori publik di **GitHub** (misalnya bernama `bike-sharing-analysis`).
2. Unggah seluruh isi folder `proyek_akhir` ke repositori GitHub tersebut.
3. Masuk ke [Streamlit Community Cloud](https://share.streamlit.io/) dan hubungkan dengan akun GitHub Anda.
4. Klik tombol **"New app"**, lalu atur:
   - **Repository:** Pilih repositori yang baru Anda buat.
   - **Branch:** `main`
   - **Main file path:** `dashboard/dashboard.py`
5. Klik **"Deploy!"**.
6. Salin URL publik aplikasi yang dihasilkan dan masukkan ke dalam berkas `url.txt`.

---

## Ringkasan Temuan & Rekomendasi Utama

1. **Pengaruh Lingkungan**: Musim Gugur (*Fall*) adalah musim tersibuk (**5.644 unit/hari**), sedangkan cuaca presipitasi hujan/salju (*Light Snow/Rain*) menurunkan minat sewa sebesar **63,03%**.
2. **Jam Sibuk Komuter**: Pada hari kerja, anggota terdaftar membentuk lonjakan tajam pada pukul **08.00 pagi (455 unit/jam)** dan **17.00–18.00 sore (442–468 unit/jam)**. Sebaliknya pada akhir pekan, pengguna kasual mendominasi siang hari pukul **12.00–16.00 (puncak 140 unit/jam)** untuk rekreasi.
3. **Pertumbuhan Kuat**: Bisnis tumbuh **+64,88% YoY** dari tahun 2011 ke 2012 dengan zona kenyamanan suhu optimal (*Sweet Spot*) berada di rentang **22°C–30°C**.
