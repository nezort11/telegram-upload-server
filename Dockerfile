FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r ./src/requirements.txt

# For running image without docker compose
# CMD yarn handler
