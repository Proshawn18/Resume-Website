# Use an official Python runtime as a parent image
# Using a slim version to keep the image size small
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir ensures that pip doesn't store cache, reducing image size
# --trusted-host pypi.python.org can help avoid SSL issues in some environments
RUN pip install --no-cache-dir -r requirements.txt --trusted-host pypi.python.org

# Copy the rest of your application's code into the container
# This includes main.py and the templates directory
COPY . .

# Make port 8080 available to the world outside this container
# Google Cloud Run will use this port
EXPOSE 8080

# Define environment variable
# Cloud Run will set this variable, and we'll use it to run the app on the correct port
ENV PORT 8080

# Run main.py when the container launches
# The command is split into a list of strings
CMD ["python", "main.py"]