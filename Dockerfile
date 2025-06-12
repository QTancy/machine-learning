# ----- Tahap Build (Multi-stage Build untuk instalasi dependensi) -----
FROM python:3.11-slim-buster AS build 

WORKDIR /app

COPY requirements.txt ./

RUN python -m venv /app/.venv && \
    /app/.venv/bin/pip install --no-cache-dir -r requirements.txt

# ----- Tahap Produksi (Menggunakan image yang lebih kecil untuk runtime) -----
FROM python:3.11-slim-buster


WORKDIR /app

COPY --from=build /app/.venv /app/.venv


COPY . .

ENV PATH="/app/.venv/bin:$PATH"

ENV PORT 8080

EXPOSE 8080


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]
