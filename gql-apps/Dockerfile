# Use the official Python base image
FROM python:3.13-slim
# Set the working directory inside the container
WORKDIR /usr/gql-apps/app

# Copy the requirements file to the working directory
COPY requirements.txt /usr/gql-apps/app/

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY . /usr/gql-apps/app/

# Expose the port on which the application will run
EXPOSE 8080

# Run the FastAPI application using uvicorn server
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
# CMD ["fastapi", "run", "gql-apps/main.py", "--port", "80"]
