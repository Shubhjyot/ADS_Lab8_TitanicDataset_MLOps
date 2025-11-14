# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY src/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy source
COPY src /app/src
COPY data/ /app/data/  

WORKDIR /app/src

# Train model at build time if data is present (makes image self-contained)
ENV DATA_PATH=/app/data/train.csv
ENV MODEL_OUT=/app/src/model.joblib
RUN if [ -f "$DATA_PATH" ]; then python train.py; else echo "Skipping training: data/train.csv not present"; fi

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]