Python yang digunakan versi 3.11.7

## Buat .venv terlebih dahulu
```
python -m venv .venv 
```

## Aktifkan .venv (untuk windows)
```
\.venv/Scripts/activate
```

## Bisa jalankan line berikut untuk install library
```
pip install -r requirements.txt
```

## Ini semua library yang aku install secara manual
```
pip install python-multipart
pip install scikit-learn
pip install joblib
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install tensorflow sentencepiece
pip install protobuf
```

## Bisa jalankan local server dengan perintah berikut ini
```
uvicorn app.main:app --reload
```

## Matikan/keluar .venv
```
deactivate
```

