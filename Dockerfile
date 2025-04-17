# Dockerfile
FROM python:3.9-slim-bullseye

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    python3-tk \
    tk-dev \
    libssl-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Install Python packages
RUN pip install --no-cache-dir certifi requests

# Set up SSL certificates
RUN ln -s /usr/local/lib/python3.9/site-packages/certifi/cacert.pem /etc/ssl/certs/ca-certificates.crt

CMD ["python", "app.py"]