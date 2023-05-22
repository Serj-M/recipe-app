# Installing base image
FROM python:3.10

# Installing dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Setting the working directory inside the container
RUN mkdir /app
WORKDIR /app

# Copying project dependencies
COPY requirements.txt .

# Installing project dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copying project files into the container
COPY . .

# Defining the command to start the FastAPI server
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000