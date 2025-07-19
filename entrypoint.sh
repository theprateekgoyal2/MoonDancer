#!/bin/sh

# Set PYTHONPATH so imports work correctly
# ENV PYTHONPATH="/app"

# Start Flask Backend
python backend/main.py --server.port=8080 --server.address=0.0.0.0 &

# Start Streamlit Frontend
streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0 &

# Start Celery Worker
celery -A backend.celery_config.celery_worker worker --loglevel=info &

# Start Celery Beat
celery -A backend.celery_config.celery_worker beat --loglevel=info &

# Wait to keep container running
wait
