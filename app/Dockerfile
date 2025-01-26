# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy script and requirements
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/bitcoin_fetcher.py .

# Run the script
CMD ["python", "bitcoin_fetcher.py"]
