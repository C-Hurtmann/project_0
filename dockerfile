# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies using Poetry
RUN poetry install --no-root

# Expose port 6379 for Redis
EXPOSE 6379

# Command to run Celery worker with Poetry
CMD ["poetry", "run", "celery", "-A", "app.tasks", "worker", "--loglevel=info"]