# Use an official Python runtime as a base image
FROM python:3.11.4

# Set the working directory in the container
WORKDIR /groupsapi

# Copy the requirements file into the container at /app
COPY requirements.txt /groupsapi/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /groupsapi/

# Specify the port number the container should expose
EXPOSE 8000

# Run the command to start the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "groupsapi:app"]