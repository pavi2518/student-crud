# ---------- Stage 1: Base Image ----------
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files to container
COPY . .

# Set environment variables (optional defaults)
ENV FIREBASE_DB_URL="https://student-crud-36bc3-default-rtdb.firebaseio.com/"
# NOTE: Do NOT hardcode FIREBASE_SERVICE_ACCOUNT — pass it securely at runtime

# Expose port 5000
EXPOSE 5000

# Command to start Flask app
CMD ["python", "app.py"]
