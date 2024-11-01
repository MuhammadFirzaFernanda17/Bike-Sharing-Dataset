# -*- coding: utf-8 -*-
"""Bike_Sharing_Dataset.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/144bpe0zyi6ewMmqt27EFqwtixFQYTZE2

# Proyek Analisis Data: Bike Sharing Dataset
- **Nama:** Muhammad Firza Fernanda
- **Email:** firzafernanda17@gmail.com
- **ID Dicoding:** benarinifirza17

## Menentukan Pertanyaan Bisnis

- Pertanyaan 1 : Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda?
- Pertanyaan 2 : Pada jam berapa sewa sepeda paling banyak terjadi?

## Import Semua Packages/Library yang Digunakan
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv

"""## Data Wrangling

Pada tahap ini, **hour.csv** dan **day.csv** digabungkan menjadi **mergered_dataset.csv** untuk memudahkan analisis data secara keseluruhan
"""

file_names = ['data/hour.csv', 'data/day.csv']
output_file = 'mergered_dataset.csv'

with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)

    for file_name in file_names:
        with open(file_name, 'r') as infile:
            reader = csv.reader(infile)
            for row in reader:
                writer.writerow(row)

print("Dataset berhasil digabungkan!")

"""### Gathering Data

Pada tahap ini, **mergered_dataset.csv** dibaca menggunakan Pandas dan ditampilkan beberapa baris pertama untuk memastikan data telah dimuat dengan benar. Langkah ini juga mencakup pengecekan struktur dan kelengkapan data untuk memastikan dataset siap digunakan dalam analisis selanjutnya.
"""

df = pd.read_csv("mergered_dataset.csv")
print(df.head())

"""**Insight:**
- Pada dataset yang didapatkan, kita bisa mendapatkan insight untuk dapat menjawab pertanyaan bisnis yang dibuat
1. Pertanyaan pertama, akan digunakan kolom cuaca (weathersit) dan kolom total sepeda yang dirental (cnt) sebagai penganalisisan pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda. (weathersit) menggunakan kategorik, dimana angka
1 menunjukkan cuaca yang cerah atau berawan,
2 kabut dan/atau berawan,
3 hujan ringan,
4 hujan lebat.

2. Pertanyaan kedua, akan digunakan kolom jam (hr) dan kolom total sepeda yang dirental (cnt) sebagai penganalisisan pada jam berapa sewa sepeda paling banyak terjadi

### Assessing Data

Memeriksa jumlah nilai kosong di setiap kolom untuk memastikan data siap digunakan.
"""

print(df.isnull().sum())

"""Menampilkan baris-baris dalam data yang memiliki nilai kosong pada kolom **cnt** untuk mengidentifikasi data yang mungkin perlu diperbaiki atau dihapus."""

df_null_cnt = df.loc[df['cnt'].isnull()]
print(df_null_cnt)

"""Memeriksa jumlah baris duplikat dalam dataset untuk memastikan tidak ada data yang tercatat lebih dari sekali"""

print(df.duplicated().sum())

"""**Insight:**
- Ada nilai NaN/Null pada kolom cnt, dimana cnt adalah erupakan jumlah total sepeda yang disewa, termasuk pengguna kasual (casual) dan pengguna terdaftar (registered)
- Tidak ada nilai duplikat dimana pembersihan pada nilai duplikat tidak diperlukan

### Cleaning Data

Baris dengan nilai **cnt** yang kosong telah dihapus untuk memastikan semua data siap digunakan dalam analisis jumlah penyewaan.
"""

df.dropna(subset=['cnt'], inplace=True)
print(df.isnull().sum())

"""Memeriksa apakah ada nilai **cnt** yang masih kosong setelah proses penghapusan"""

df_null_cnt = df.loc[df['cnt'].isnull()]
print(df_null_cnt)

"""**Insight:**
- Baris dengan kolom cnt yang bernilai NaN/Null dihapus

## Exploratory Data Analysis (EDA)

### Explore ...
"""

print(df.describe(include='all'))

df.groupby('weathersit')['cnt'].mean().sort_values(ascending=False)

df.groupby('hr')['cnt'].mean().sort_values(ascending=False)

"""**Insight:**
- Jumlah penyewaan sepeda tertinggi pada kategori cuaca yang lebih baik (kategori 1 dan 2) dan sebaliknya untuk kategori cuaca yang lebih buruk (kategori 3 dan 4)
- Biasanya penyewaan sepeda paling tinggi terjadi pada jam-jam tertentu, seperti jam sibuk di pagi (07:00 - 09:00) dan sore (17:00 - 19:00)

## Visualization & Explanatory Analysis

### Pertanyaan 1:

Menghitung rata-rata jumlah penyewaan sepeda berdasarkan kondisi cuaca, mengatur warna batang grafik berdasarkan intensitas penyewaan dari gelap untuk nilai rendah hingga terang untuk nilai tinggi
"""

# Hitung rata-rata jumlah penyewaan berdasarkan kondisi cuaca
mean_cnt_by_weather = df.groupby('weathersit')['cnt'].mean().sort_values(ascending=False)

# Normalisasi nilai untuk palet warna
norm = plt.Normalize(mean_cnt_by_weather.min(), mean_cnt_by_weather.max())
colors = plt.cm.viridis(norm(mean_cnt_by_weather.values))

# Visualisasi
plt.figure(figsize=(10, 6))
sns.barplot(x=mean_cnt_by_weather.index, y=mean_cnt_by_weather.values, palette=colors)
plt.title('Rata-rata Jumlah Penyewaan Sepeda berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca (1: Cerah, 2: Berkabut, 3: Salju, 4: Hujan)')
plt.ylabel('Rata-rata Jumlah Penyewaan')
plt.xticks(ticks=range(4), labels=['Cerah', 'Berkabut', 'Salju', 'Hujan'], rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

"""### Pertanyaan 2:

Menghitung dan memvisualisasikan total penyewaan sepeda per jam dalam grafik garis.
"""

# Hitung total penyewaan berdasarkan jam
total_cnt_by_hour = df.groupby('hr')['cnt'].sum()

# Visualisasi
plt.figure(figsize=(10, 6))
sns.lineplot(x=total_cnt_by_hour.index.astype(int), y=total_cnt_by_hour.values, marker='o', color='blue')
plt.title('Total Jumlah Penyewaan Sepeda berdasarkan Jam')
plt.xlabel('Jam')
plt.ylabel('Total Jumlah Penyewaan')
plt.xticks(ticks=range(24), rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

"""**Insight:**
- Jumlah penyewaan sepeda tertinggi pada kategori cuaca yang lebih baik (kategori 1 dan 2) dan sebaliknya untuk kategori cuaca yang lebih buruk (kategori 3 dan 4)
- Biasanya penyewaan sepeda paling tinggi terjadi pada jam-jam tertentu, seperti jam sibuk di pagi (07:00 - 09:00) dan sore (17:00 - 19:00)

## Analisis Lanjutan (Opsional)

Menghitung skor RFM (Recency, Frequency, Monetary) untuk pengguna sepeda berdasarkan data sewa dengan mengelompokkan data berdasarkan musim, hari libur, dan hari kerja, serta menghitung total penyewaan, recency, frequency, dan monetary untuk setiap segmen
"""

# Pastikan kolom dteday dalam format datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# Menentukan tanggal akhir untuk analisis
snapshot_date = df['dteday'].max() + pd.Timedelta(days=1)

# Menghitung total penyewaan untuk pengguna kasual dan terdaftar
df['total_rentals'] = df['casual'] + df['registered']

# Pastikan total_rentals adalah tipe data numerik
df['total_rentals'] = pd.to_numeric(df['total_rentals'], errors='coerce')

# Menghitung RFM untuk pengguna kasual dan terdaftar
rfm_df = df.groupby(['season', 'holiday', 'workingday']).agg({
    'dteday': lambda x: (snapshot_date - x.max()).days,  # Recency
    'total_rentals': ['count', 'sum']  # Frequency dan Monetary
}).reset_index()

# Mengubah nama kolom
rfm_df.columns = ['season', 'holiday', 'workingday', 'recency', 'frequency', 'monetary']

# Pastikan kolom monetary adalah tipe data numerik
rfm_df['monetary'] = pd.to_numeric(rfm_df['monetary'], errors='coerce')

# Segmentasi berdasarkan kuartil
rfm_df['r_quartile'] = pd.qcut(rfm_df['recency'], 4, labels=[4, 3, 2, 1])  # 1 = paling baru
rfm_df['f_quartile'] = pd.qcut(rfm_df['frequency'], 4, labels=[1, 2, 3, 4])  # 4 = paling sering
rfm_df['m_quartile'] = pd.qcut(rfm_df['monetary'], 4, labels=[1, 2, 3, 4])  # 4 = paling banyak

# Menghitung RFM Score
rfm_df['RFMScore'] = rfm_df['r_quartile'].astype(str) + rfm_df['f_quartile'].astype(str) + rfm_df['m_quartile'].astype(str)

# Menampilkan hasil akhir
print(rfm_df[['season', 'holiday', 'workingday', 'recency', 'frequency', 'monetary', 'RFMScore']].head())

"""Visualisasi ini menunjukkan distribusi total pengeluaran pengguna berdasarkan analisis RFM, dengan histogram yang menampilkan frekuensi pengeluaran serta kurva estimasi kepadatan untuk memberikan gambaran lebih jelas tentang sebaran data.

"""

# Visualisasi distribusi monetary
plt.figure(figsize=(10, 6))
sns.histplot(rfm_df['monetary'], bins=30, kde=True)
plt.title('Distribusi Pengeluaran berdasarkan Musim dan Hari Kerja')
plt.xlabel('Total Pengeluaran')
plt.ylabel('Frekuensi')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

"""Visualisasi ini menggambarkan distribusi RFM Score di antara pelanggan, menunjukkan jumlah pelanggan dalam setiap segmen RFM untuk membantu memahami perilaku dan nilai masing-masing segmen dalam basis pelanggan.

"""

# Visualisasi segmen RFM
plt.figure(figsize=(10, 6))
sns.countplot(x='RFMScore', data=rfm_df, hue=None)
plt.title('Distribusi RFM Score')
plt.xlabel('RFM Score')
plt.ylabel('Jumlah Pelanggan')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

"""**Insight:**
- Terdapat variasi dalam nilai RFM, menunjukkan adanya segmen pelanggan dengan tingkat loyalitas dan pengeluaran yang berbeda-beda.
- Pelanggan dengan skor RFM tinggi (432) adalah yang paling berharga, dengan frekuensi pembelian yang baik dan pengeluaran tinggi. Strategi retensi perlu difokuskan pada mereka.

## Conclusion

**Conclution pertanyaan 1**
-  Rata-rata jumlah penyewaan sepeda paling tinggi terjadi pada kondisi cuaca cerah menunjukkan bahwa cuaca yang baik mendorong lebih banyak orang untuk menyewa sepeda.
- Kondisi cuaca seperti hujan dan salju menunjukkan rata-rata penyewaan yang lebih rendah, menandakan bahwa cuaca ekstrem mengurangi minat masyarakat untuk menggunakan layanan penyewaan sepeda.

**Conclution pertanyaan 2**
-  Data menunjukkan bahwa penyewaan sepeda mencapai puncaknya pada jam-jam tertentu, biasanya di pagi hari (sekitar pukul 8-9) dan sore hari (sekitar pukul 17-18). Ini mencerminkan pola penggunaan sepeda oleh orang-orang yang berangkat ke tempat kerja atau pulang dari aktivitas sehari-hari.
"""