# Use Python image
FROM python:3.9

# Set working directory
WORKDIR /

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for Flask & Streamlit
EXPOSE 5000 8501

# Start Flask, Celery, and Streamlit
CMD bash -c "
    python backend/main.py &
    python frontend/app.py &
    celery -A backend.working-application.celery_config.celery_worker worker --loglevel=info &
    celery -A backend.working-application.celery_config.celery_worker beat --loglevel=info
    wait