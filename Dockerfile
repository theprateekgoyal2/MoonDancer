# Use Python 3.9
FROM python:3.9

# Create a non-root user and group
RUN groupadd -g 10014 appgroup && \
    useradd -m -u 10014 -g appgroup appuser

# Set working directory
WORKDIR /app

# Change ownership of the working directory
RUN chown -R appuser:appgroup /app

# Copy project files
COPY --chown=appuser:appgroup . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose necessary ports
EXPOSE 5000 8501

# Copy entrypoint script & make it executable
COPY --chown=appuser:appgroup entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch to non-root user
USER appuser

# Run the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
