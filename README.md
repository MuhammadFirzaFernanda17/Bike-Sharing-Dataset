# Proyek Analisis Data Sewa Sepeda

## Struktur Berkas
- 'data/': Berisi Dataset yang digunakan dalam analisis
- 'dashboard/': Berisi berkas untuk dashboard Streamlit.
  - 'bike_sharing_dataset.py': Berkas utama untuk menjalankan dashboard.
  - 'mergered_dataset.csv' : Dataset yang digunakan dalam dashboard.
- 'Bike_Sharing_Dataset.ipynb': Berkas Jupyter Notebook yang berisi analisis data.
- `requirements.txt`: Daftar library yang diperlukan untuk menjalankan proyek.
- `README.md`: Dokumen ini.
- `url.txt`: Berisi informasi tambahan

## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run dashboard.py
```
