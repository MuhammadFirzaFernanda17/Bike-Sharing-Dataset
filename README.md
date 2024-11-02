# Proyek Analisis Data Sewa Sepeda

Proyek ini melakukan analisis data mengenai penyewaan sepeda menggunakan dataset yang telah disediakan. Analisis ini mencakup pemrosesan data, visualisasi, dan pembuatan dashboard menggunakan Streamlit.

## Struktur Berkas

- `data/`: Berisi Dataset yang digunakan dalam analisis
- `dashboard/`: Berisi berkas untuk dashboard Streamlit.
  - `bike_sharing_dataset.py`: Berkas utama untuk menjalankan dashboard.
  - `mergered_dataset.csv` : Dataset yang digunakan dalam dashboard.
- `Bike_Sharing_Dataset.ipynb`: Berkas Jupyter Notebook yang berisi analisis data.
- `requirements.txt`: Daftar library yang diperlukan untuk menjalankan proyek.
- `README.md`: Dokumen ini.
- `url.txt`: Berisi informasi tambahan

## Membuat Virtual Environment

```
python -m venv env
source env/bin/activate       # Untuk MacOS/Linux
env\Scripts\activate          # Untuk Windows
```

## Instalasi Library

```
pip install -r requirements.txt
```

## Menjalankan Dashboard Streamlit

```
streamlit run dashboard/bike_sharing_dataset.py
```
