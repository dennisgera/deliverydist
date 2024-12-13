# Stage 1: Backend Build
FROM python:3.11-slim as backend-build

# Install poetry
RUN pip install poetry

# Set working directory
WORKDIR /app

# Copy backend requirements
COPY backend/pyproject.toml backend/poetry.lock ./backend/

# Configure poetry to not create virtual environment
RUN cd backend && poetry config virtualenvs.create false && poetry install --no-dev

# Copy backend code
COPY backend ./backend

# Expose backend port
EXPOSE 8000

# Command to run backend
CMD ["sh", "-c", "cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000"]

# Stage 2: Frontend Build
FROM node:20-slim as frontend-build

# Set working directory
WORKDIR /app

# Copy frontend dependencies
COPY frontend/package*.json ./frontend/

# Install dependencies
RUN cd frontend && npm install

# Copy frontend code
COPY frontend ./frontend

# Build frontend
RUN cd frontend && npm run build

# Expose frontend port
EXPOSE 3000

# Command to run frontend
CMD ["sh", "-c", "cd frontend && npm run start"]