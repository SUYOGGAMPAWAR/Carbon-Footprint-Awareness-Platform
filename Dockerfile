# Use an official, lightweight Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install Flask directly (skipping requirements.txt for speed)
RUN pip install --no-cache-dir flask

# Copy the current directory contents into the container at /app
COPY app.py /app/

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]