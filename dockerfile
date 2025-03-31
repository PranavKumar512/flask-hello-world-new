# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Expose the port if you're running a FastAPI app
EXPOSE 8000

# Command to run your FastAPI app
# Replace `api/index.py` with the entry point of your app
CMD ["uvicorn", "api.index:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
