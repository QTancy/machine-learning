# Gunakan image Python yang ringan
FROM python:3.10-slim

# Buat direktori kerja
WORKDIR /app

# Salin semua file ke dalam container
COPY . .

# Install dependency
RUN pip install --upgrade pip && pip install -r requirements.txt

# Port default FastAPI
EXPOSE 8000

# Jalankan aplikasi
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
