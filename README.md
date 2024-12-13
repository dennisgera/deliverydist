# Distance Calculator

A web application that calculates the distance between two addresses. The application consists of a FastAPI backend and a Next.js frontend.

## Features

- Calculate distance between two addresses
- View history of previous calculations
- Data persistence for search history
- Error handling and loading states

## Prerequisites

Before running this application, make sure you have Docker installed on your machine:
- [Docker Installation Guide](https://docs.docker.com/get-docker/)

## Running the Application

1. Clone the repository:
```bash
git clone dennisgera/deliverydist
cd deliverydist
```

2. Start the application using Docker Compose:
```bash
docker compose up
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

To rebuild the containers after making changes:
```bash
docker compose up --build
```

To stop the application:
```bash
docker compose down
```

## Tech Stack

### Backend
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- Poetry (Dependency management)
- Nominatim API (Geocoding)

### Frontend
- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui components

## API Endpoints

- `GET /api/v1/queries` - Get history of distance calculations
- `POST /api/v1/queries` - Calculate distance between two addresses

## Development

If you want to run the services separately for development:

1. Backend:
```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

2. Frontend:
```bash
cd frontend
npm install
npm run dev
```