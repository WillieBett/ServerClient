# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org grpcio-tools grpcio

# Generate the gRPC files
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto

# Make port XXXX available to the world outside this container
EXPOSE 8888

# Run run_test_1.py when the container launches
CMD ["python", "run_test_1.py"]