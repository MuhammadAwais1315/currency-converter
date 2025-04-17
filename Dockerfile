FROM python:3.9-slim


# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        python3-tk \
        tk-dev \
        libssl-dev \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Install virtual display dependencies
RUN apt-get update && \
    apt-get install -y \
        xvfb \
        xauth && \
    rm -rf /var/lib/apt/lists/*

# Add wrapper script
RUN echo '#!/bin/sh\nXvfb :99 -screen 0 1024x768x24 &\nexport DISPLAY=:99\npython /app/app.py' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt


# Copy certificates instead of symlinking
RUN cp /usr/local/lib/python3.9/site-packages/certifi/cacert.pem /etc/ssl/certs/ca-certificates.crt

CMD ["python", "app.py"]