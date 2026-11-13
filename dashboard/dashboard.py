import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur tata letak halaman Streamlit
st.set_page_config(
    page_title="Bike Sharing Analytics Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Membaca data bersih yang sudah ada di folder dashboard
@st.cache_data
def load_data():
    df = pd.read_csv("../data/main_data.csv")
    df["dteday"] = pd.to_datetime(df["dteday"])
    return df

df_day = load_data()

# Sidebar: Filter Rentang Tanggal
min_date = df_day["dteday"].min()
max_date = df_day["dteday"].max()

with st.sidebar:
    st.title("🚲 Bike Sharing")
    st.markdown("Filter Data Berdasarkan Rentang Waktu:")
    
    start_date, end_date = st.date_input(
        label="Rentang Tanggal",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter dataframe berdasarkan tanggal di sidebar
main_df = df_day[(df_day["dteday"] >= str(start_date)) & 
                 (df_day["dteday"] <= str(end_date))]

# Header Utama Dashboard
st.header("📊 Dashboard Analisis Penyewaan Sepeda")
st.markdown("Dashboard interaktif ini menyajikan eksplorasi data peminjaman sepeda berdasarkan kondisi cuaca, musim, dan suhu.")

# Metrik / KPI Ringkasan
col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = main_df["cnt"].sum()
    st.metric("Total Peminjaman", value=f"{total_rentals:,}")
with col2:
    total_registered = main_df["registered"].sum()
    st.metric("Penyewa Terdaftar", value=f"{total_registered:,}")
with col3:
    total_casual = main_df["casual"].sum()
    st.metric("Penyewa Biasa (Casual)", value=f"{total_casual:,}")

st.divider()

# Visualisasi Pertanyaan 1: Pengaruh Kondisi Cuaca & Hari Kerja
st.subheader("1. Pengaruh Kondisi Cuaca terhadap Rata-rata Peminjaman")
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(
    x="weathersit",
    y="cnt",
    hue="workingday",
    data=main_df,
    palette="Set2",
    errorbar=None,
    ax=ax1
)
ax1.set_title("Rata-rata Peminjaman Sepeda Berdasarkan Cuaca dan Status Hari", fontsize=12, fontweight="bold")
ax1.set_xlabel("Kondisi Cuaca (1: Cerah, 2: Berawan/Mendung, 3: Hujan/Salju Ringan)")
ax1.set_ylabel("Rata-rata Jumlah Peminjaman")
ax1.set_xticks([0, 1, 2])
ax1.set_xticklabels(["Cerah (Clear)", "Berawan (Mist)", "Hujan (Light Snow)"])
ax1.legend(title="Status Hari", labels=["Libur / Weekend (0)", "Hari Kerja (1)"])
st.pyplot(fig1)

st.divider()

# Visualisasi Pertanyaan 2: Analisis Musim dan Suhu
st.subheader("2. Tren Peminjaman Berdasarkan Musim dan Suhu Udara")

col_left, col_right = st.columns(2)

with col_left:
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    sns.barplot(
        x="season",
        y="cnt",
        data=main_df,
        estimator=sum,
        palette="viridis",
        errorbar=None,
        ax=ax2
    )
    ax2.set_title("Total Peminjaman Berdasarkan Musim", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Musim")
    ax2.set_ylabel("Total Akumulasi Peminjaman")
    ax2.set_xticks([0, 1, 2, 3])
    ax2.set_xticklabels(["Spring", "Summer", "Fall", "Winter"])
    st.pyplot(fig2)

with col_right:
    fig3, ax3 = plt.subplots(figsize=(7, 5))
    sns.scatterplot(
        x="temp",
        y="registered",
        data=main_df,
        alpha=0.6,
        color="steelblue",
        ax=ax3
    )
    sns.regplot(
        x="temp",
        y="registered",
        data=main_df,
        scatter=False,
        color="crimson",
        ax=ax3
    )
    ax3.set_title("Korelasi Suhu (Temp) vs Penyewa Terdaftar", fontsize=11, fontweight="bold")
    ax3.set_xlabel("Suhu Dinormalisasi (Temp)")
    ax3.set_ylabel("Penyewa Terdaftar (Registered)")
    st.pyplot(fig3)

st.caption("Copyright © 2026 - Bike Sharing Dashboard Project")