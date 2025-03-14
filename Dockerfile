# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install Java
RUN apt-get update && apt-get install -y openjdk-11-jdk

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]