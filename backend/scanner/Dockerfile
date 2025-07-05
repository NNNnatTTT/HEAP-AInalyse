# Use an official Python runtime as base image
FROM python:3.9-slim

# First install system dependencies
RUN apt-get update && \
    apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    libtesseract-dev

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port 5000 for Flask
EXPOSE 5004

# Run the app
CMD ["python", "app.py"]
