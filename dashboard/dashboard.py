import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ==============================================================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Capital Bikeshare Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tema visual global untuk semua chart Seaborn/Matplotlib
sns.set_theme(style="whitegrid")

# Custom CSS untuk styling modern dan konsisten
st.markdown("""
    <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 800;
            color: #1e3a8a;
            margin-bottom: 0.2rem;
            letter-spacing: -0.02em;
        }
        .sub-header {
            font-size: 1.05rem;
            color: #4b5563;
            margin-bottom: 1.5rem;
        }
        
        /* Badge Persentase Delta (Tag Kapsul Biru Bersih Tanpa Panah) */
        div[data-testid="stMetricDelta"] {
            background-color: rgba(37, 99, 235, 0.12) !important;
            border: 1px solid rgba(37, 99, 235, 0.25) !important;
            border-radius: 9999px !important;
            padding: 0.15rem 0.55rem !important;
            width: fit-content !important;
            font-weight: 600 !important;
        }
        div[data-testid="stMetricDelta"] svg {
            display: none !important;
        }
        div[data-testid="stMetricDelta"],
        div[data-testid="stMetricDelta"] *,
        div[data-testid="stMetricDelta"] > div {
            color: #1d4ed8 !important;
        }

        /* Tag Filter Musim */
        span[data-baseweb="tag"] {
            background-color: #dbeafe !important;
            color: #1e40af !important;
            border: 1px solid #bfdbfe !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
        }
        span[data-baseweb="tag"] svg {
            fill: #1e40af !important;
        }

        /* Navigasi Tab */
        button[data-baseweb="tab"]:hover, 
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #2563eb !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] p {
            color: #2563eb !important;
            font-weight: 600;
        }
        div[data-baseweb="tab-highlight"] {
            background-color: #2563eb !important;
        }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. PEMUATAN DATASET
# ==============================================================================
@st.cache_data
def load_datasets():
    base_dir = Path(__file__).resolve().parent
    
    def resolve_path(filename):
        search_paths = [
            base_dir / filename,
            base_dir / "dashboard" / filename,
            base_dir.parent / "dashboard" / filename,
            Path("dashboard") / filename,
            Path(filename)
        ]
        for p in search_paths:
            if p.exists():
                return p
        return None

    day_file = resolve_path("main_data.csv")
    hour_file = resolve_path("hour_data.csv")

    if not day_file or not hour_file:
        st.error("Gagal memuat dataset bersih. Pastikan berkas 'main_data.csv' dan 'hour_data.csv' tersedia.")
        st.stop()
        
    day_df = pd.read_csv(day_file, parse_dates=['dteday'])
    hour_df = pd.read_csv(hour_file, parse_dates=['dteday'])
    return day_df, hour_df

day_df, hour_df = load_datasets()


# ==============================================================================
# 3. HELPER FUNCTIONS (AGREGASI DATA UNTUK VISUALISASI)
# ==============================================================================
def create_season_rentals_df(df):
    season_order = ['Spring', 'Summer', 'Fall', 'Winter']
    season_df = df.groupby('season')['cnt'].mean().reindex(season_order).reset_index()
    return season_df

def create_weather_rentals_df(df):
    weather_df = df.groupby('weathersit')['cnt'].mean().sort_values(ascending=False).reset_index()
    return weather_df

def create_hourly_pattern_df(df_hour):
    hourly_df = df_hour.groupby(['workingday', 'hr'])[['casual', 'registered', 'cnt']].mean().reset_index()
    return hourly_df

def create_monthly_trends_df(df):
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_pivot = df.pivot_table(index='mnth', columns='yr', values='cnt', aggfunc='sum')
    monthly_pivot.index = [month_names[i-1] for i in monthly_pivot.index]
    return monthly_pivot

def create_temp_cluster_df(df):
    temp_bins = [-float('inf'), 12, 22, 30, float('inf')]
    temp_labels = ['Cold (< 12°C)', 'Mild (12°C - 22°C)', 'Warm (22°C - 30°C)', 'Hot (> 30°C)']
    df_copy = df.copy()
    df_copy['temp_cluster'] = pd.cut(df_copy['temp_celsius'], bins=temp_bins, labels=temp_labels)
    cluster_df = df_copy.groupby('temp_cluster', observed=True)['cnt'].mean().reset_index()
    return cluster_df


# ==============================================================================
# 4. SIDEBAR (FILTER RENTANG WAKTU & MUSIM)
# ==============================================================================
min_date = day_df['dteday'].min().date()
max_date = day_df['dteday'].max().date()

with st.sidebar:
    st.image("https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=500&auto=format&fit=crop&q=80", use_container_width=True)
    st.markdown("## Capital Bikeshare")
    st.markdown("Filter data analisis berdasarkan preferensi Anda:")
    
    # 1. Filter Rentang Waktu
    date_range = st.date_input(
        label="Pilih Rentang Tanggal",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date
        
    # 2. Filter Musim
    all_seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    selected_seasons = st.multiselect(
        label="Pilih Musim",
        options=all_seasons,
        default=all_seasons
    )
    
    st.markdown("---")
    st.markdown("### Informasi Pembuat")
    st.markdown("**Nama:** Ezra Abhinaya Pasaribu")
    st.markdown("**Kelas:** Belajar Fundamental Analisis Data")
    st.markdown("**Program:** Dicoding Academy")


# ==============================================================================
# 5. MENERAPKAN FILTER DATA
# ==============================================================================
filtered_day_df = day_df[
    (day_df['dteday'].dt.date >= start_date) &
    (day_df['dteday'].dt.date <= end_date) &
    (day_df['season'].isin(selected_seasons))
]

filtered_hour_df = hour_df[
    (hour_df['dteday'].dt.date >= start_date) &
    (hour_df['dteday'].dt.date <= end_date) &
    (hour_df['season'].isin(selected_seasons))
]

if filtered_day_df.empty:
    st.warning("Tidak ada data pada kombinasi filter rentang tanggal dan musim yang dipilih. Silakan atur kembali filter di sidebar.")
    st.stop()


# ==============================================================================
# 6. HEADER & METRIC CARDS
# ==============================================================================
st.markdown('<div class="main-header">Capital Bikeshare Performance Dashboard</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">Menampilkan ringkasan data operasional dari <b>{start_date.strftime("%d %b %Y")}</b> hingga <b>{end_date.strftime("%d %b %Y")}</b></div>', unsafe_allow_html=True)

# Menghitung Metrik Utama
total_rentals = filtered_day_df['cnt'].sum()
total_registered = filtered_day_df['registered'].sum()
total_casual = filtered_day_df['casual'].sum()
total_days = filtered_day_df['dteday'].nunique()
avg_daily = total_rentals / total_days if total_days > 0 else 0

reg_pct = (total_registered / total_rentals * 100) if total_rentals > 0 else 0
cas_pct = (total_casual / total_rentals * 100) if total_rentals > 0 else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Penyewaan Sepeda", value=f"{total_rentals:,} unit")
with col2:
    st.metric(label="Pengguna Terdaftar (Member)", value=f"{total_registered:,} unit", delta=f"{reg_pct:.1f}% dari total")
with col3:
    st.metric(label="Pengguna Kasual (Non-Member)", value=f"{total_casual:,} unit", delta=f"{cas_pct:.1f}% dari total")
with col4:
    st.metric(label="Rata-rata Sewa Harian", value=f"{avg_daily:,.0f} unit/hari", delta=f"{total_days} hari aktif")


# ==============================================================================
# 7. TAB KONTEN ANALISIS INTERAKTIF
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "Pengaruh Musim & Cuaca",
    "Pola Jam Sibuk & Pengguna",
    "Tren Bulanan & Segmentasi Suhu",
    "Rekomendasi Action Items"
])

# ------------------------------------------------------------------------------
# TAB 1: PENGARUH MUSIM & KONDISI CUACA (PERTANYAAN 1)
# ------------------------------------------------------------------------------
with tab1:
    st.subheader("Dampak Faktor Lingkungan terhadap Volume Sewa Harian")
    st.markdown("Bagian ini mengevaluasi bagaimana pergantian musim dan kondisi atmosfer memengaruhi minat bersepeda harian.")
    
    col_chart1, col_chart2 = st.columns(2)
    
    season_summary = create_season_rentals_df(filtered_day_df)
    weather_summary = create_weather_rentals_df(filtered_day_df)
    
    with col_chart1:
        fig1, ax1 = plt.subplots(figsize=(7, 4.8))
        bars1 = sns.barplot(
            data=season_summary,
            x='season',
            y='cnt',
            hue='season',
            legend=False,
            palette=['#94a3b8', '#64748b', '#1e40af', '#3b82f6'],
            ax=ax1
        )
        ax1.set_title("Rata-rata Sewa Harian per Musim", fontsize=12, fontweight='bold', pad=12)
        ax1.set_xlabel("Musim", fontsize=10)
        ax1.set_ylabel("Rata-rata Sewa (Unit)", fontsize=10)
        ax1.set_ylim(0, 6500)
        
        for p in bars1.patches:
            val = p.get_height()
            if not np.isnan(val) and val > 0:
                ax1.annotate(f"{val:,.0f}", (p.get_x() + p.get_width() / 2., val),
                             ha='center', va='bottom', fontsize=9, fontweight='bold',
                             xytext=(0, 4), textcoords='offset points')
        st.pyplot(fig1)
        
    with col_chart2:
        fig2, ax2 = plt.subplots(figsize=(7, 4.8))
        bars2 = sns.barplot(
            data=weather_summary,
            x='weathersit',
            y='cnt',
            hue='weathersit',
            legend=False,
            palette=['#1e40af', '#60a5fa', '#94a3b8'],
            ax=ax2
        )
        ax2.set_title("Rata-rata Sewa Harian per Kondisi Cuaca", fontsize=12, fontweight='bold', pad=12)
        ax2.set_xlabel("Kondisi Cuaca", fontsize=10)
        ax2.set_ylabel("Rata-rata Sewa (Unit)", fontsize=10)
        ax2.set_ylim(0, 6500)
        
        for p in bars2.patches:
            val = p.get_height()
            if not np.isnan(val) and val > 0:
                ax2.annotate(f"{val:,.0f}", (p.get_x() + p.get_width() / 2., val),
                             ha='center', va='bottom', fontsize=9, fontweight='bold',
                             xytext=(0, 4), textcoords='offset points')
        st.pyplot(fig2)
        
    st.info("""
        **Key Insights Lingkungan:**
        - **Musim Gugur (Fall)** menjadi periode emas operasional dengan rata-rata tertinggi **5.644 unit/hari**, sedangkan **Musim Semi (Spring)** mengalami titik terendah (**2.604 unit/hari**).
        - **Cuaca Hujan/Salju Ringan (Light Snow/Rain)** menyebabkan penurunan dramatis sebesar **63,03%** dibanding cuaca cerah (anjlok dari 4.877 unit menjadi 1.803 unit/hari).
    """)


# ------------------------------------------------------------------------------
# TAB 2: POLA JAM SIBUK & SEGMENTASI PENGGUNA (PERTANYAAN 2)
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("Diferensiasi Jam Sibuk: Komuter Harian vs. Rekreasi Akhir Pekan")
    st.markdown("Perbandingan pola peminjaman per jam (0–23) antara anggota terdaftar (*registered*) dan penyewa kasual (*casual*).")
    
    hourly_df = create_hourly_pattern_df(filtered_hour_df)
    
    fig3, ax3 = plt.subplots(nrows=1, ncols=2, figsize=(15, 5), sharey=True)
    
    # Subplot 1: Hari Kerja
    wd_data = hourly_df[hourly_df['workingday'] == 'Working Day']
    ax3[0].plot(wd_data['hr'], wd_data['registered'], color='#1e40af', linewidth=2.5, marker='o', label='Registered (Member)')
    ax3[0].plot(wd_data['hr'], wd_data['casual'], color='#f59e0b', linewidth=2, linestyle='--', marker='s', label='Casual (Non-Member)')
    ax3[0].axvspan(7, 9, color='#bfdbfe', alpha=0.3, label='Rush Hour Pagi (07.00 - 09.00)')
    ax3[0].axvspan(16, 19, color='#fed7aa', alpha=0.3, label='Rush Hour Sore (16.00 - 19.00)')
    ax3[0].set_title("Hari Kerja (Working Day)\nLonjakan Tajam Jam Masuk & Pulang Kantor", fontsize=11, fontweight='bold')
    ax3[0].set_xlabel("Jam (0 - 23)", fontsize=10)
    ax3[0].set_ylabel("Rata-rata Sewa per Jam (Unit)", fontsize=10)
    ax3[0].set_xticks(range(0, 24, 2))
    ax3[0].legend(loc='upper right', fontsize=8)
    
    # Subplot 2: Akhir Pekan & Hari Libur
    nwd_data = hourly_df[hourly_df['workingday'] == 'Weekend/Holiday']
    ax3[1].plot(nwd_data['registered'], color='#1e40af', linewidth=2.5, marker='o', label='Registered (Member)')
    ax3[1].plot(nwd_data['casual'], color='#f59e0b', linewidth=2, linestyle='--', marker='s', label='Casual (Non-Member)')
    ax3[1].axvspan(12, 16, color='#fef08a', alpha=0.3, label='Jam Rekreasi Santai (12.00 - 16.00)')
    ax3[1].set_title("Akhir Pekan & Libur (Weekend/Holiday)\nKurva Santai Unimodal Puncak Siang-Sore", fontsize=11, fontweight='bold')
    ax3[1].set_xlabel("Jam (0 - 23)", fontsize=10)
    ax3[1].set_xticks(range(0, 24, 2))
    ax3[1].legend(loc='upper right', fontsize=8)
    
    plt.tight_layout()
    st.pyplot(fig3)
    
    st.info("""
        **Key Insights Jam Sibuk:**
        - **Hari Kerja (Pola Bimodal):** Anggota terdaftar mendominasi jam berangkat kerja pukul **08.00 (455 unit/jam)** dan jam pulang kerja pukul **17.00–18.00 (442–468 unit/jam)**. Pengguna kasual sangat pasif.
        - **Akhir Pekan (Pola Unimodal):** Pengguna kasual melonjak signifikan pada siang hingga sore hari (pukul **12.00–16.00**, puncak di **14.00 rata-rata 140 unit/jam**) untuk keperluan rekreasi.
    """)


# ------------------------------------------------------------------------------
# TAB 3: TREN TAHUNAN & ANALISIS LANJUTAN SUHU (PERTANYAAN 3 & CLUSTERING)
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("Tren Pertumbuhan Bulanan dan Analisis Lanjutan Klaster Suhu")
    st.markdown("Membandingkan performa Year-over-Year (2011 vs 2012) serta identifikasi zona kenyamanan suhu (*Temperature Clustering*).")
    
    col_t1, col_t2 = st.columns([1.3, 1])
    
    with col_t1:
        monthly_trends = create_monthly_trends_df(filtered_day_df)
        fig4, ax4 = plt.subplots(figsize=(7.5, 4.8))
        
        if 2011 in monthly_trends.columns:
            ax4.plot(monthly_trends.index, monthly_trends[2011], marker='o', linewidth=2.2, color='#94a3b8', label='2011 (Total: 1.24 jt)')
        if 2012 in monthly_trends.columns:
            ax4.plot(monthly_trends.index, monthly_trends[2012], marker='s', linewidth=2.8, color='#1e40af', label='2012 (+64.88% YoY)')
            
        ax4.set_title("Pertumbuhan Sewa Bulanan (2011 vs 2012)", fontsize=11, fontweight='bold')
        ax4.set_xlabel("Bulan", fontsize=10)
        ax4.set_ylabel("Total Sewa (Unit)", fontsize=10)
        ax4.legend(loc='upper left', fontsize=8)
        st.pyplot(fig4)
        
    with col_t2:
        temp_cluster_df = create_temp_cluster_df(filtered_day_df)
        fig5, ax5 = plt.subplots(figsize=(6, 4.8))
        bars5 = sns.barplot(
            data=temp_cluster_df,
            x='temp_cluster',
            y='cnt',
            hue='temp_cluster',
            dodge=False,
            legend=False,
            palette=['#94a3b8', '#60a5fa', '#1e40af', '#f97316'],
            ax=ax5
        )
        ax5.set_title("Temperature Comfort Clustering\n(Sweet Spot: 22°C - 30°C)", fontsize=11, fontweight='bold')
        ax5.set_xlabel("Cluster Suhu", fontsize=9)
        ax5.set_ylabel("Rata-rata Sewa Harian (Unit)", fontsize=10)
        ax5.tick_params(axis='x', rotation=15, labelsize=8)
        ax5.set_ylim(0, 6500)
        
        for p in bars5.patches:
            val = p.get_height()
            if not np.isnan(val) and val > 0:
                ax5.annotate(f"{val:,.0f}", (p.get_x() + p.get_width() / 2., val),
                             ha='center', va='bottom', fontsize=8, fontweight='bold',
                             xytext=(0, 3), textcoords='offset points')
        st.pyplot(fig5)
        
    st.info("""
        **Key Insights Pertumbuhan & Suhu:**
        - **Pertumbuhan YoY Melesat +64,88%:** Dari 1,24 juta unit (2011) ke 2,05 juta unit (2012). Bulan puncak bergeser dari Juni 2011 (143 rb) ke September 2012 (218 rb).
        - **Sweet Spot Suhu Hangat:** Rentang **Warm (22°C - 30°C)** mencatatkan utilisasi tertinggi (**5.719 unit/hari**), sedangkan suhu dingin **Cold (< 12°C)** anjlok 61% ke 2.228 unit/hari.
    """)


# ------------------------------------------------------------------------------
# TAB 4: REKOMENDASI ACTION ITEMS BISNIS
# ------------------------------------------------------------------------------
with tab4:
    st.subheader("Rekomendasi Strategis bagi Manajemen Capital Bikeshare")
    st.markdown("Langkah operasional dan monetisasi konkret berdasarkan temuan analitik data:")
    
    rec_col1, rec_col2 = st.columns(2)
    
    with rec_col1:
        st.markdown("""
            #### 1. Smart Bike Rebalancing
            - **Hari Kerja:** Alokasikan truk logistik untuk mengisi unit di stasiun perumahan pada pukul **06.00–07.30 pagi**, dan siapkan dock kosong di stasiun perkantoran pada pukul **15.30–16.30 sore** sebelum jam pulang kantor.
            - **Akhir Pekan:** Geser fokus distribusi unit ke stasiun area taman kota, objek wisata, dan tepian sungai mulai pukul **10.30 pagi**.
            
            #### 2. Seasonal Maintenance Scheduling
            - Manfaatkan periode permintaan sepi pada **Januari–Maret (suhu < 12°C)** untuk menarik 30%–40% armada ke bengkel guna *overhaul* dan servis preventif.
            - Pastikan **100% armada prima** sebelum bulan Mei–Oktober saat permintaan memasuki *sweet spot* (suhu 22°C–30°C).
        """)
        
    with rec_col2:
        st.markdown("""
            #### 3. Program Konversi Pengguna Kasual (18,83%)
            - Pengguna kasual menyumbang lebih dari 620 ribu peminjaman. Luncurkan paket langganan komuter akhir pekan (*Weekend Pass*) atau promo diskon membership bagi pengguna kasual yang menyewa lebih dari 3 kali sebulan.
            
            #### 4. Weather Contingency Alert & Rain Check
            - Integrasikan aplikasi seluler dengan ramalan cuaca lokal. Saat terdeteksi hujan/salju, kirim notifikasi keselamatan jalan licin dan bagikan voucher diskon (*Rain Check Voucher*) untuk dipakai pada hari cerah berikutnya guna menjaga retensi pengguna.
        """)

# ==============================================================================
# 8. FOOTER
# ==============================================================================
st.markdown("---")
st.caption("Capital Bikeshare Performance Dashboard • Dibuat oleh Ezra Abhinaya Pasaribu untuk Submission Dicoding 'Belajar Fundamental Analisis Data'")
