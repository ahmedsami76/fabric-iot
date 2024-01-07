# Use the official Python 3.8-slim image as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Define environment variables (optional defaults can be provided)
ENV IOT_HUB_NAME=your-iot-hub-name
ENV DEVICE_ID=your-device-id
ENV SHARED_ACCESS_KEY=your-shared-access-key

# Command to run the application
CMD ["python", "iot-sensor.py"]
