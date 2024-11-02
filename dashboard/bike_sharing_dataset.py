# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import streamlit as st
from datetime import datetime, timedelta

# Streamlit dashboard layout
st.title("Proyek Analisis Data: Bike Sharing Dataset")
st.write("**Nama:** Muhammad Firza Fernanda")
st.write("**Email:** firzafernanda17@gmail.com")
st.write("**ID Dicoding:** benarinifirza17")

st.header("Menentukan Pertanyaan Bisnis")
st.write("""
1. Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda?
2. Pada jam berapa sewa sepeda paling banyak terjadi?
""")

# Tahap Data Wrangling
st.header("Data Wrangling")

# Merge dataset dari file hour.csv dan day.csv menjadi mergered_dataset.csv
file_names = ['data/hour.csv', 'data/day.csv']
output_file = 'mergered_dataset.csv'

with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    for file_name in file_names:
        with open(file_name, 'r') as infile:
            reader = csv.reader(infile)
            for row in reader:
                writer.writerow(row)

st.success("Dataset berhasil digabungkan menjadi mergered_dataset.csv")

# Load merged dataset
df = pd.read_csv("mergered_dataset.csv")
st.write("Data yang dimuat:")
st.write(df.head())

# Cleaning data
st.header("Cleaning Data")
st.write("Menghapus baris dengan nilai kosong pada kolom **cnt**")

df.dropna(subset=['cnt'], inplace=True)
st.write("Jumlah nilai kosong per kolom setelah pembersihan:")
st.write(df.isnull().sum())

# Exploratory Data Analysis (EDA)
st.header("Exploratory Data Analysis (EDA)")

# Pertanyaan 1: Pengaruh kondisi cuaca terhadap jumlah penyewaan
st.subheader("Pertanyaan 1: Pengaruh Kondisi Cuaca terhadap Jumlah Penyewaan Sepeda")

# Hitung rata-rata jumlah penyewaan berdasarkan kondisi cuaca
mean_cnt_by_weather = df.groupby('weathersit')['cnt'].mean().sort_values(ascending=False)
norm = plt.Normalize(mean_cnt_by_weather.min(), mean_cnt_by_weather.max())
colors = plt.cm.viridis(norm(mean_cnt_by_weather.values))

fig1, ax1 = plt.subplots()
sns.barplot(x=mean_cnt_by_weather.index, y=mean_cnt_by_weather.values, palette=colors, ax=ax1)
ax1.set_title('Rata-rata Jumlah Penyewaan Sepeda berdasarkan Kondisi Cuaca')
ax1.set_xlabel('Kondisi Cuaca (1: Cerah, 2: Berkabut, 3: Salju, 4: Hujan)')
ax1.set_ylabel('Rata-rata Jumlah Penyewaan')
ax1.set_xticks(range(4))
ax1.set_xticklabels(['Cerah', 'Berkabut', 'Salju', 'Hujan'], rotation=45)
ax1.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig1)

# Pertanyaan 2: Jam tertinggi penyewaan sepeda
st.subheader("Pertanyaan 2: Pada Jam Berapa Sewa Sepeda Paling Banyak Terjadi?")

# Hitung total penyewaan berdasarkan jam
total_cnt_by_hour = df.groupby('hr')['cnt'].sum()

fig2, ax2 = plt.subplots()
sns.lineplot(x=total_cnt_by_hour.index.astype(int), y=total_cnt_by_hour.values, marker='o', color='blue', ax=ax2)
ax2.set_title('Total Jumlah Penyewaan Sepeda berdasarkan Jam')
ax2.set_xlabel('Jam')
ax2.set_ylabel('Total Jumlah Penyewaan')
ax2.set_xticks(range(24))
ax2.set_xticklabels(range(24), rotation=45)
ax2.grid(True, linestyle='--', alpha=0.7)
st.pyplot(fig2)

# RFM Analysis
st.header("Analisis Lanjutan: RFM Score")

# Pastikan kolom dteday dalam format datetime
df['dteday'] = pd.to_datetime(df['dteday'])
snapshot_date = df['dteday'].max() + timedelta(days=1)

# Menghitung total penyewaan untuk pengguna kasual dan terdaftar
df['total_rentals'] = df['casual'] + df['registered']

# Menghitung RFM untuk pengguna kasual dan terdaftar
rfm_df = df.groupby(['season', 'holiday', 'workingday']).agg({
    'dteday': lambda x: (snapshot_date - x.max()).days,  # Recency
    'total_rentals': ['count', 'sum']  # Frequency dan Monetary
}).reset_index()

# Mengubah nama kolom
rfm_df.columns = ['season', 'holiday', 'workingday', 'recency', 'frequency', 'monetary']

# Segmentasi berdasarkan kuartil
rfm_df['r_quartile'] = pd.qcut(rfm_df['recency'], 4, labels=[4, 3, 2, 1])
rfm_df['f_quartile'] = pd.qcut(rfm_df['frequency'], 4, labels=[1, 2, 3, 4])
rfm_df['m_quartile'] = pd.qcut(rfm_df['monetary'], 4, labels=[1, 2, 3, 4])

# Menghitung RFM Score
rfm_df['RFMScore'] = rfm_df['r_quartile'].astype(str) + rfm_df['f_quartile'].astype(str) + rfm_df['m_quartile'].astype(str)
st.write("RFM Score:")
st.write(rfm_df[['season', 'holiday', 'workingday', 'recency', 'frequency', 'monetary', 'RFMScore']].head())

# Visualisasi Distribusi Monetary
st.subheader("Distribusi Pengeluaran berdasarkan Musim dan Hari Kerja")
fig3, ax3 = plt.subplots()
sns.histplot(rfm_df['monetary'], bins=30, kde=True, ax=ax3)
ax3.set_title('Distribusi Pengeluaran')
ax3.set_xlabel('Total Pengeluaran')
ax3.set_ylabel('Frekuensi')
ax3.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig3)

# Visualisasi Distribusi RFM Score
st.subheader("Distribusi RFM Score")
fig4, ax4 = plt.subplots()
sns.countplot(x='RFMScore', data=rfm_df, ax=ax4)
ax4.set_title('Distribusi RFM Score')
ax4.set_xlabel('RFM Score')
ax4.set_ylabel('Jumlah Pelanggan')
ax4.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig4)

st.write("**Insight:**
- Pelanggan dengan skor RFM tinggi (432) adalah yang paling berharga, dengan frekuensi pembelian yang baik dan pengeluaran tinggi. Strategi retensi perlu difokuskan pada mereka.
- Penyewaan sepeda lebih tinggi pada cuaca cerah dan pada jam sibuk.")