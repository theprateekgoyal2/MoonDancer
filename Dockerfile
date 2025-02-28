# Use Python 3.9
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose necessary ports
EXPOSE 5000 8501

# Start all services
CMD bash -c "
    python backend/main.py &
    streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0 &
    celery -A backend.celery_config.celery_worker worker --loglevel=info &
    celery -A backend.celery_config.celery_worker beat --loglevel=info
    wait
"