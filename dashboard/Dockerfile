FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# This line assumes requirements.txt is in the same folder as the Dockerfile
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8501
ENTRYPOINT ["python", "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]