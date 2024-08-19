# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables to avoid Python buffering
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask application
EXPOSE 5000

# Define the command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
