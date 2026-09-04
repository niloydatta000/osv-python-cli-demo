FROM python:3.13-slim


# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set the entry point for the container
ENTRYPOINT ["python3", "main.py"]
