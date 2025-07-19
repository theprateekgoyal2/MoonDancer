# Use Python 3.9
FROM python:3.9

# Set working directory
WORKDIR /app

# Create a non-root user and group with UID and GID in the required range
RUN groupadd -g 10014 appgroup && \
    useradd -m -u 10014 -g appgroup appuser

COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Change ownership of working directory to the non-root user
RUN chown -R appuser:appgroup /app

RUN chmod a+x entrypoint.sh

# Switch to non-root user
USER 10014

# Expose necessary ports
EXPOSE 8080 8501

# Run the entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
