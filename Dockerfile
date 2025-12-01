# Use an official lightweight Python image
FROM python:3.9-slim

# Forces Python to print to the console immediately
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy dependency definition
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src

# Run the application
CMD ["python", "src/main.py"]