# Use the official Python image from the Docker Hub
FROM python:3.12-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . /app/

# Run the Django server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "AFSPADE_BACKEND.wsgi:application"]
