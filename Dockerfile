# Base image; python alpine for barebones functionality
FROM python:3.13-alpine

# Create working app directory
WORKDIR /app

# Copy just requirements first to prevent pip install rebuild from image layer shenanigans
COPY requirements.txt .

# Install requirements
RUN \
apk add --no-cache libpq-dev gcc && \
pip install --no-cache-dir -r requirements.txt

# Print output from Python commands to Docker container console for feedback
ENV PYTHONUNBUFFERED 1

# Copy that code folder over into /app directory
COPY . .

# Make the app available
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
