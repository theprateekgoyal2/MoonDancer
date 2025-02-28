# Use Python 3.9
FROM python:3.9

# Set working directory
WORKDIR /app

# Create a non-root user and group with UID and GID in the required range
RUN groupadd -g 10014 appgroup && \
    useradd -m -u 10014 -g appgroup appuser

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Change ownership of working directory to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER 10014

# Expose necessary ports
EXPOSE 5000 8501

# Copy entrypoint script & make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
