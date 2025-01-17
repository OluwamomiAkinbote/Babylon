# Start from an official Python image
FROM python:3.10

# Install system dependencies required for mysqlclient
RUN apt-get update \
    && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    python3-dev

# Set the working directory
WORKDIR /app

# Copy your project files
COPY . /app/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the application port (if applicable)
EXPOSE 8000

# Command to run the app
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:$PORT"]

