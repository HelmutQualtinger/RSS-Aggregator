# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt using pip
# Also install gunicorn for a production-ready web server and lxml for XML parsing
RUN pip install --no-cache-dir -r requirements.txt gunicorn lxml

# Copy the current directory contents into the container at /app
COPY . .

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME World

# Run app.py when the container launches using Gunicorn
# The Flask app object is named 'app' in app.py
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]