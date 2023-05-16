# Installing base image
FROM python:3.10

# Installing dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Setting the working directory inside the container
WORKDIR /app

# Copying project dependencies
COPY requirements.txt .

# Installing project dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copying project files into the container
COPY . .

# Setting environment variables for FastAPI
ENV PYTHONPATH=/app

# Defining the command to start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]