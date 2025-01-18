FROM python:3.12-slim

# Set the working directory
WORKDIR /app/project_0

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Poetry
RUN pip install poetry

# Copy only the necessary files for dependencies installation
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-root

COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY . /app

ENTRYPOINT ["/app/entrypoint.sh"]
