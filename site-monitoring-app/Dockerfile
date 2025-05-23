FROM python:3.11-slim

# Installe ping (iputils-ping) et nettoie le cache APT
RUN apt-get update \
 && apt-get install -y iputils-ping \
 && rm -rf /var/lib/apt/lists/*

# Ton reste du Dockerfile
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
