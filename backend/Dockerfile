FROM python:3.11-slim

# Install poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

# Copy backend requirements
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create virtual environment
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy backend code
COPY . .

# Expose backend port
EXPOSE 8000

# Command to run backend
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]