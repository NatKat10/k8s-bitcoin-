# Base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy the files from the current directory to the container
COPY requirements.txt requirements.txt
COPY bitcoin_fetcher.py bitcoin_fetcher.py

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install curl
RUN apt-get update && apt-get install -y curl && apt-get clean

# Expose port 80
EXPOSE 80

# Run the bitcoin_fetcher script and redirect HTTP server logs to a separate file
CMD ["sh", "-c", "python bitcoin_fetcher.py & python -m http.server 80 --bind 0.0.0.0 --directory /app --cgi"]

